#!/usr/bin/env python3
"""
Simple script to start the Python FastAPI server.
"""

import os
import sys
import uvicorn

# Set environment for development
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("PORT", "9091")

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=9091,
                reload=True,
                log_level="info")
