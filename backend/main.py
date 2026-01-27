"""
FastAPI Backend for Sentence Segmentation Tool

This module implements a REST API for sentence segmentation using:
1. Baseline: Rule-based regex sentence splitter
2. Proposed: spaCy-based NLP sentence segmentation

Supports English (mandatory) and multilingual extension (French, German, Spanish).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.baseline_splitter import BaselineSentenceSplitter
from backend.spacy_splitter import SpacySentenceSplitter

app = FastAPI(
    title="Sentence Segmentation API",
    description="A web-based sentence segmentation tool using NLP",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'frontend/' directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize splitters
baseline_splitter = BaselineSentenceSplitter()
spacy_splitter = SpacySentenceSplitter()


class SegmentationRequest(BaseModel):
    """Request model for sentence segmentation"""
    text: str
    language: str = "en"
    method: str = "spacy"  # "baseline" or "spacy"


class SegmentationResponse(BaseModel):
    """Response model containing segmented sentences"""
    sentences: List[str]
    method: str
    language: str
    count: int


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend HTML"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Frontend not found. Please ensure frontend/index.html exists.</h1>"


@app.post("/segment", response_model=SegmentationResponse)
async def segment_sentences(request: SegmentationRequest):
    """
    Segment input text into sentences using either baseline or spaCy method.
    
    Args:
        request: SegmentationRequest containing text, language, and method
        
    Returns:
        SegmentationResponse with segmented sentences and metadata
        
    Raises:
        HTTPException: If language is not supported or segmentation fails
    """
    try:
        # Validate language
        supported_languages = ["en", "fr", "de", "es"]
        if request.language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' not supported. Supported: {supported_languages}"
            )
        
        # Select segmentation method
        if request.method == "baseline":
            # Baseline only supports English
            if request.language != "en":
                raise HTTPException(
                    status_code=400,
                    detail="Baseline method only supports English. Use 'spacy' for multilingual support."
                )
            sentences = baseline_splitter.split(request.text)
        elif request.method == "spacy":
            sentences = spacy_splitter.split(request.text, request.language)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Method '{request.method}' not supported. Use 'baseline' or 'spacy'"
            )
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return SegmentationResponse(
            sentences=sentences,
            method=request.method,
            language=request.language,
            count=len(sentences)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Sentence Segmentation API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
