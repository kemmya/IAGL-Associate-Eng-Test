#!/usr/bin/env python3
"""
Production-ready TODO application server.
Entry point for running the FastAPI application.
"""

import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()