from fastapi import APIRouter, HTTPException
from loguru import logger

from app.models.input import ContentRequest, InputSource
from app.services.input_service.input_layer import InputService
from app.services.llm_service.llm_service import LLMService, RawThreadData
from app.core.config import settings

router = APIRouter()
input_service = InputService()
# Initialize LLM Service with API key from settings
llm_service = LLMService(api_key=settings.gemini_api_key)

@router.post(
    "/generate-script",
    summary="Generate script from Reddit URL",
    description="Scrape a Reddit thread and generate a video script"
)
async def generate_script(request: ContentRequest):
    """
    Generate a script from a Reddit URL.
    
    Args:
        request: ContentRequest containing the URL
        
    Returns:
        JSON object with the generated script
    """
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    try:
        logger.info(f"Generating script for URL: {request.url}")
        
        # 1. Scrape Content
        scraped_content = await input_service.scrape_content(InputSource.REDDIT, str(request.url))
        
        # 2. Convert to RawThreadData
        raw_thread = RawThreadData(
            title=scraped_content.title,
            content=scraped_content.content,
            author=scraped_content.author or "Anonymous",
            subreddit=scraped_content.metadata.get("subreddit", "reddit"),
            upvotes=scraped_content.metadata.get("upvotes", 0),
            comments=[
                {
                    "author": c.author,
                    "content": c.content,
                    "upvotes": c.upvotes
                }
                for c in scraped_content.comments
            ]
        )
        
        # 3. Generate Script
        script = await llm_service.generate_structured_script(raw_thread)
        
        return {
            "success": True,
            "data": {
                "background": script.background,
                "lines": [
                    {
                        "speaker": line.speaker,
                        "text": line.text,
                        "audio_file_path": line.audio_file_path,
                        "start_time": line.start_time,
                        "duration": line.duration
                    }
                    for line in script.lines
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the input layer service is running"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "input-layer",
        "version": "0.1.0"
    }
