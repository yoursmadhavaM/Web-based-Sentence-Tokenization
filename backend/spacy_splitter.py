"""
spaCy-Based Sentence Splitter - Proposed NLP System

This module implements sentence segmentation using spaCy, a state-of-the-art
NLP library. This is the proposed system that leverages linguistic knowledge
and trained models to accurately identify sentence boundaries.

Supports English (mandatory) and multilingual extension (French, German, Spanish).
"""

import spacy
import os
from typing import List


class SpacySentenceSplitter:
    """
    Sentence splitter using spaCy NLP models.
    
    This class loads appropriate spaCy models for different languages and
    uses spaCy's built-in sentence segmentation capabilities, which are
    based on trained models that understand linguistic patterns.
    """
    
    def __init__(self):
        """Initialize the spaCy splitter and load models."""
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """
        Load spaCy models for supported languages.
        
        Models are loaded lazily - only when first needed for a language.
        Falls back to English if a model fails to load.
        """
        # Language to model mapping
        language_models = {
            "en": "en_core_web_sm",
            "fr": "fr_core_news_sm",
            "de": "de_core_news_sm",
            "es": "es_core_news_sm"
        }
        
        # Try to load English model first (mandatory)
        try:
            self.models["en"] = spacy.load("en_core_web_sm")
            print("✓ Loaded English model (en_core_web_sm)")
        except OSError:
            print("⚠ Warning: English model not found. Please install with:")
            print("  python -m spacy download en_core_web_sm")
            print("  Falling back to basic tokenization...")
            self.models["en"] = None
        
        # Try to load multilingual models (optional)
        for lang_code, model_name in language_models.items():
            if lang_code == "en":
                continue  # Already loaded
            
            try:
                self.models[lang_code] = spacy.load(model_name)
                print(f"✓ Loaded {lang_code} model ({model_name})")
            except OSError:
                print(f"⚠ Warning: {model_name} not found. Install with:")
                print(f"  python -m spacy download {model_name}")
                print(f"  Falling back to English model for {lang_code}...")
                # Fallback to English model if available
                self.models[lang_code] = self.models.get("en")
    
    def split(self, text: str, language: str = "en") -> List[str]:
        """
        Split text into sentences using spaCy.
        
        Args:
            text: Input text to segment
            language: Language code (en, fr, de, es)
            
        Returns:
            List of sentences (strings)
        """
        if not text or not text.strip():
            return []
        
        # Get appropriate model (fallback to English if language model unavailable)
        model = self.models.get(language) or self.models.get("en")
        
        if model is None:
            # Fallback: basic sentence splitting if no model available
            print("⚠ No spaCy model available. Using basic fallback.")
            return self._fallback_split(text)
        
        try:
            # Process text with spaCy
            doc = model(text)
            
            # Extract sentences using spaCy's sentence segmentation
            sentences = [sent.text.strip() for sent in doc.sents]
            
            # Filter out empty sentences
            sentences = [s for s in sentences if s]
            
            return sentences
        
        except Exception as e:
            print(f"⚠ Error in spaCy processing: {e}")
            # Fallback to basic splitting
            return self._fallback_split(text)
    
    def _fallback_split(self, text: str) -> List[str]:
        """
        Fallback sentence splitting when spaCy models are unavailable.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        import re
        # Simple regex-based fallback
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
