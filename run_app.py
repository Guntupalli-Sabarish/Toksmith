import uvicorn
from app.main import app

if __name__ == "__main__":
    print("="*60)
    print("Starting ToksMith Video Project App...")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
