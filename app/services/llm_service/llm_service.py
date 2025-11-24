import json
from typing import Dict, List, Optional, Any
from app.models.script import Script, DialogueLine
from .providers.base import LLMProvider
from .providers.gemini_provider import GeminiLLMProvider

class RawThreadData:
    """Represents raw thread data from Reddit or other sources."""
    
    def __init__(
        self,
        title: str,
        content: str,
        author: str,
        subreddit: str,
        upvotes: int,
        comments: List[Dict[str, Any]]
    ):
        self.title = title
        self.content = content
        self.author = author
        self.subreddit = subreddit
        self.upvotes = upvotes
        self.comments = comments

class LLMService:
    """Service for generating structured video scripts using LLM."""

    def __init__(self, provider: Optional[LLMProvider] = None):
        """
        Initialize LLM Service with a provider.

        Args:
            provider: LLMProvider instance (defaults to GeminiLLMProvider)
        """
        self.provider = provider or GeminiLLMProvider()

    async def generate_structured_script(self, raw_thread: RawThreadData) -> Script:
        """
        Generate a structured video script from raw thread data.
        """
        print(f"Generating structured script for thread: {raw_thread.title}")
        
        try:
            # Build the prompt
            prompt = self._build_prompt(raw_thread)

            # Call LLM API via provider
            llm_response = await self.provider.generate_content(prompt)

            # Parse the response
            content_str = self.provider.parse_response(llm_response)
            script_data = self._parse_script_json(content_str)

            # Create and return the script entity
            return Script.create(
                lines=script_data["lines"],
                background=script_data.get("background", "minecraft-parkour"),
                characters=script_data.get("characters", [])
            )

        except Exception as error:
            print(f"Error generating script: {error}")
            raise Exception(f"Failed to generate script: {str(error)}")

    def _build_prompt(self, raw_thread: RawThreadData) -> str:
        """Build the LLM prompt for script generation."""
        # Format top comments
        comments_text = "\n".join([
            f"{i+1}. {comment.get('author', 'Anonymous')} "
            f"({comment.get('upvotes', 0)} upvotes): {comment.get('content', '')}"
            for i, comment in enumerate(raw_thread.comments[:3])
        ])

        prompt = f"""You are an expert content creator who specializes in turning Reddit posts into engaging TikTok/Reel video scripts.

Convert the following Reddit thread into a conversational video script format. The script should be engaging, natural, and perfect for a short-form video.

**Reddit Thread:**
- Subreddit: r/{raw_thread.subreddit}
- Title: {raw_thread.title}
- Author: {raw_thread.author}
- Upvotes: {raw_thread.upvotes}

**Post Content:**
{raw_thread.content}

**Top Comments:**
{comments_text}

**Instructions:**
1. Create a script with clear speaker roles: "Narrator", "OP", "Commenter1", "Commenter2", etc.
2. Start with an engaging hook that introduces the situation
3. Present the original post content in a conversational way
4. Include 2-3 of the most interesting/relevant comments
5. End with a call-to-action asking viewers what they think
6. Keep each dialogue line under 50 words for better pacing
7. Make it sound natural and engaging, not robotic

**Output Format (JSON):**
{{
  "lines": [
    {{
      "speaker": "Narrator",
      "text": "dialogue text here",
      "audio_file_path": "",
      "start_time": 0,
      "duration": 0
    }}
  ],
  "background": "minecraft-parkour",
  "characters": ["narrator", "op", "commenter1", "commenter2"]
}}

Respond ONLY with valid JSON, no additional text or formatting."""

        return prompt

    def _parse_script_json(self, content: str) -> Dict[str, Any]:
        """Parse JSON content string into script data."""
        try:
            # Clean the response content
            cleaned_content = content.strip()

            # Remove any markdown code blocks if present
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content.replace("```json", "", 1)
                cleaned_content = cleaned_content.rsplit("```", 1)[0]
            elif cleaned_content.startswith("```"):
                cleaned_content = cleaned_content.replace("```", "", 1)
                cleaned_content = cleaned_content.rsplit("```", 1)[0]

            cleaned_content = cleaned_content.strip()

            # Parse JSON
            parsed = json.loads(cleaned_content)

            # Validate the parsed response
            if not self._validate_response(parsed):
                raise ValueError("Invalid script format from LLM")

            # Convert to DialogueLine objects
            lines = [
                DialogueLine(
                    speaker=line.get("speaker", "Narrator"),
                    text=line.get("text", ""),
                    audio_file_path=line.get("audio_file_path", line.get("audioFilePath", "")),
                    start_time=line.get("start_time", line.get("startTime", 0)),
                    duration=line.get("duration", 0)
                )
                for line in parsed.get("lines", [])
            ]

            return {
                "lines": lines,
                "background": parsed.get("background", "minecraft-parkour"),
                "characters": parsed.get("characters", ["narrator", "op", "commenter1", "commenter2"])
            }

        except json.JSONDecodeError as error:
            print(f"Failed to parse LLM response as JSON: {error}")
            print(f"Raw response: {content}")
            raise Exception("Failed to parse script from LLM response")
        except Exception as error:
            print(f"Error parsing script response: {error}")
            raise

    def _validate_response(self, response: Any) -> bool:
        """Validate that the parsed response has the correct structure."""
        if not isinstance(response, dict):
            return False
        if "lines" not in response or not isinstance(response["lines"], list):
            return False
        for line in response["lines"]:
            if not isinstance(line, dict):
                return False
            if "speaker" not in line or "text" not in line:
                return False
        return True
