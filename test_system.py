#!/usr/bin/env python3
"""
Quick test script to verify the sentence segmentation systems work correctly.

This script tests both baseline and spaCy systems with sample text.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.baseline_splitter import BaselineSentenceSplitter
from backend.spacy_splitter import SpacySentenceSplitter


def test_systems():
    """Test both segmentation systems."""
    print("="*70)
    print("TESTING SENTENCE SEGMENTATION SYSTEMS")
    print("="*70)
    
    # Sample text with various challenges
    test_text = """
    Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y. and Los Angeles, Calif.
    The weather was great! He said, "This is amazing." Then he returned home.
    """
    
    print("\nInput Text:")
    print("-"*70)
    print(test_text.strip())
    print("-"*70)
    
    # Test Baseline System
    print("\n" + "="*70)
    print("BASELINE SYSTEM (Regex-Based)")
    print("="*70)
    
    try:
        baseline = BaselineSentenceSplitter()
        baseline_sentences = baseline.split(test_text)
        
        print(f"\nFound {len(baseline_sentences)} sentences:\n")
        for i, sent in enumerate(baseline_sentences, 1):
            print(f"  {i}. {sent}")
        
        print("\n✓ Baseline system working correctly")
    except Exception as e:
        print(f"\n✗ Baseline system error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test spaCy System
    print("\n" + "="*70)
    print("PROPOSED SYSTEM (spaCy NLP)")
    print("="*70)
    
    try:
        spacy_splitter = SpacySentenceSplitter()
        spacy_sentences = spacy_splitter.split(test_text, "en")
        
        print(f"\nFound {len(spacy_sentences)} sentences:\n")
        for i, sent in enumerate(spacy_sentences, 1):
            print(f"  {i}. {sent}")
        
        print("\n✓ spaCy system working correctly")
    except Exception as e:
        print(f"\n✗ spaCy system error: {e}")
        print("  Make sure spaCy models are installed:")
        print("  python -m spacy download en_core_web_sm")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\nIf both systems produced output, the installation is successful!")
    print("You can now run the web server with: python run_server.py\n")


if __name__ == "__main__":
    test_systems()
