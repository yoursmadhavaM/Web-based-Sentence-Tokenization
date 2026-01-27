#!/usr/bin/env python3
"""
Setup script for Sentence Segmentation Tool.

This script helps set up the project by:
1. Installing dependencies
2. Downloading spaCy models
3. Verifying installation
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False
        )
        print(f"✓ {description} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description} failed")
        print(f"  Return code: {e.returncode}\n")
        return False


def main():
    """Main setup function."""
    print("\n" + "="*70)
    print("SENTENCE SEGMENTATION TOOL - SETUP")
    print("="*70)
    
    # Step 1: Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("⚠ Warning: Some dependencies may not have installed correctly.")
        print("  You can try manually: pip install -r requirements.txt\n")
    
    # Step 2: Download English model (mandatory)
    print("\n" + "="*70)
    print("DOWNLOADING SPACY MODELS")
    print("="*70)
    print("\nDownloading English model (mandatory)...")
    
    if not run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading English spaCy model"
    ):
        print("⚠ Warning: English model download failed.")
        print("  The application may not work correctly.")
        print("  Try manually: python -m spacy download en_core_web_sm\n")
    
    # Step 3: Optional multilingual models
    print("\nOptional: Download multilingual models?")
    print("These are optional but enable French, German, and Spanish support.")
    response = input("Download multilingual models? (y/n): ").strip().lower()
    
    if response == 'y':
        models = [
            ("fr_core_news_sm", "French"),
            ("de_core_news_sm", "German"),
            ("es_core_news_sm", "Spanish")
        ]
        
        for model_name, lang_name in models:
            print(f"\nDownloading {lang_name} model...")
            run_command(
                f"{sys.executable} -m spacy download {model_name}",
                f"Downloading {lang_name} spaCy model"
            )
    
    # Step 4: Verify installation
    print("\n" + "="*70)
    print("VERIFYING INSTALLATION")
    print("="*70)
    
    try:
        import spacy
        import fastapi
        print("✓ spaCy imported successfully")
        print("✓ FastAPI imported successfully")
        
        # Try loading English model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✓ English model loaded successfully")
        except OSError:
            print("✗ English model not found")
            print("  Run: python -m spacy download en_core_web_sm")
        
        print("\n" + "="*70)
        print("SETUP COMPLETE!")
        print("="*70)
        print("\nTo start the server, run:")
        print("  python run_server.py")
        print("\nOr:")
        print("  python -m uvicorn backend.main:app --reload")
        print("\nThen open http://localhost:8000 in your browser.\n")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Please ensure all dependencies are installed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
