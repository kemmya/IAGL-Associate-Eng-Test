
"""
Main FastAPI application entry point.
Sets up the FastAPI app with middleware, routers, and configuration.
"""

import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .config import settings
from .routes import router
from .exceptions import TodoAppException


# Configure logging
def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A production-ready TODO application API built with FastAPI",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)


# Global exception handler for TodoAppException
@app.exception_handler(TodoAppException)
async def todo_exception_handler(request: Request, exc: TodoAppException):
    """Handle custom TodoApp exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.message,
            "error_code": exc.error_code
        }
    )


# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions."""
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


# Include API routes
app.include_router(router)


# Serve static files (React app) - only in production
if not settings.debug:
# Serve static files (React app) - only in production when dist exists
 import os
if not settings.debug and os.path.exists("dist/public"):
    app.mount("/", StaticFiles(directory="dist/public", html=True), name="static")


def main():
    """Main entry point for running the application."""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()