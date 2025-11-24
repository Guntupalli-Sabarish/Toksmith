import sys
import os
from sqlalchemy import text

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.db.session import engine

def fix_enum():
    print("Attempting to add 'AUDIO_GENERATED' to projectstatus enum...")
    with engine.connect() as connection:
        try:
            # PostgreSQL specific command to add value to enum
            # We use a transaction to ensure safety, though ALTER TYPE cannot run inside a transaction block 
            # in some older postgres versions, but usually it's fine in autocommit mode or specific blocks.
            # However, SQLAlchemy connection might be in a transaction.
            # For ALTER TYPE ADD VALUE, it cannot run inside a transaction block.
            # We need to set isolation level to AUTOCOMMIT.
            
            connection.execution_options(isolation_level="AUTOCOMMIT")
            
            connection.execute(text("ALTER TYPE projectstatus ADD VALUE 'AUDIO_GENERATED';"))
            print("Successfully added 'AUDIO_GENERATED' to projectstatus enum.")
        except Exception as e:
            if "already exists" in str(e):
                print("Value 'AUDIO_GENERATED' already exists in enum.")
            else:
                print(f"Error: {e}")
                # Try checking if it exists first or just print error
                print("If the error is 'duplicate value', it is safe to ignore.")

if __name__ == "__main__":
    fix_enum()
