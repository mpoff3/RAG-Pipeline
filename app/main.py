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
  # Mount the exported Next.js static front-end
  # (static files copied into app/static during build)
  app.mount(
      "/",
      StaticFiles(directory=os.path.join(os.getcwd(), "app/static"), html=True),
      name="static_frontend",
  )