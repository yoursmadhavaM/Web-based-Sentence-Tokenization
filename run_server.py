#!/usr/bin/env python3
"""
Convenience script to run the FastAPI server.

Usage:
    python run_server.py
"""

import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("="*70)
    print("Starting Sentence Segmentation API Server")
    print("="*70)
    print("\nServer will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server.\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
