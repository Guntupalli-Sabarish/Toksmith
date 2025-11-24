import sys
import os
from sqlalchemy import text

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.db.session import engine
from app.db.base import Base
# Import all models to ensure they are registered with Base
from app.models import VideoProject, Script, DialogueLine, Character, Asset, ProjectAsset

def update_schema():
    print("Updating database schema...")
    try:
        # Create all tables defined in Base.metadata
        # This will only create tables that don't exist.
        # For existing tables with changes (like VideoProject), it won't automatically alter them.
        # We might need manual ALTER statements for VideoProject if we want to add columns without dropping.
        
        Base.metadata.create_all(bind=engine)
        print("Created missing tables.")

        # Manually add new columns to VideoProject if they don't exist
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            
            # Add title column
            try:
                connection.execute(text("ALTER TABLE video_projects ADD COLUMN IF NOT EXISTS title VARCHAR;"))
                print("Added 'title' column to video_projects.")
            except Exception as e:
                print(f"Error adding title: {e}")

            # Add resolution column
            try:
                connection.execute(text("ALTER TABLE video_projects ADD COLUMN IF NOT EXISTS resolution VARCHAR DEFAULT '1080x1920';"))
                print("Added 'resolution' column to video_projects.")
            except Exception as e:
                print(f"Error adding resolution: {e}")
                
            # Update Enum type for status
            # Adding new values to the enum
            new_statuses = ["VIDEO_RENDERING", "COMPLETED"]
            for status in new_statuses:
                try:
                    connection.execute(text(f"ALTER TYPE projectstatus ADD VALUE '{status}';"))
                    print(f"Added '{status}' to projectstatus enum.")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"Value '{status}' already exists in enum.")
                    else:
                        print(f"Error adding {status}: {e}")

    except Exception as e:
        print(f"Schema update failed: {e}")

if __name__ == "__main__":
    update_schema()
