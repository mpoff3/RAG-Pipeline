from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .core.config import settings
from .api.endpoints import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix=settings.API_V1_STR)

# Mount the Next.js static files
app.mount("/_next", StaticFiles(directory="frontend/.next"), name="next_static")

@app.get("/")
async def root():
    return FileResponse("frontend/.next/server/pages/index.html")

@app.get("/{catch_all:path}")
async def catch_all(catch_all: str):
    # Try to serve the static file
    static_path = f"frontend/.next/server/pages/{catch_all}.html"
    if os.path.exists(static_path):
        return FileResponse(static_path)
    # Fall back to index.html for client-side routing
    return FileResponse("frontend/.next/server/pages/index.html") 