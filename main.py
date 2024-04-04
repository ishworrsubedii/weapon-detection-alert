"""
Created By: ishwor subedi
Date: 2024-01-02
"""
import uvicorn

from src.api.fast_api import app

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
