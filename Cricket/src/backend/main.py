import os
import sys

# Add root dir to sys path to resolve src modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from src.backend.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cricket AI Analyst API",
    description="Backend for the Multi-Agent Cricket Assistant",
    version="1.0.0"
)

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cricket AI Analyst API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
