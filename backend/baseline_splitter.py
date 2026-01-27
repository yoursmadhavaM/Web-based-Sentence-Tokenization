"""
Baseline Sentence Splitter - Rule-Based Approach

This module implements a simple regex-based sentence segmentation method
as a baseline for comparison with the proposed spaCy-based system.

The baseline uses regular expressions to identify sentence boundaries based on:
- Periods, exclamation marks, question marks
- Handling of abbreviations and decimal numbers
- Basic whitespace normalization
"""

import re
from typing import List


class BaselineSentenceSplitter:
    """
    Rule-based sentence splitter using regular expressions.
    
    This is a simple baseline implementation that splits sentences based on
    punctuation marks (., !, ?) followed by whitespace or end of string.
    It attempts to handle common abbreviations and decimal numbers.
    """
    
    def __init__(self):
        """Initialize the baseline splitter with compiled regex patterns."""
        # Common abbreviations that should not end sentences
        self.abbreviations = {
            'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr', 'vs', 'etc',
            'e.g', 'i.e', 'a.m', 'p.m', 'am', 'pm', 'inc', 'ltd', 'corp',
            'st', 'ave', 'blvd', 'rd', 'no', 'vol', 'pp', 'fig', 'ed'
        }
        
        # Pattern to match sentence endings
        # Matches: . ! ? followed by space or end of string
        # Excludes: decimal numbers, abbreviations, URLs
        self.sentence_end_pattern = re.compile(
            r'(?<!\d)(?<!\.)(?<![A-Za-z]\.)([.!?]+)(?:\s+|$)',
            re.MULTILINE
        )
    
    def split(self, text: str) -> List[str]:
        """
        Split text into sentences using rule-based approach.
        
        Args:
            text: Input text to segment
            
        Returns:
            List of sentences (strings)
        """
        if not text or not text.strip():
            return []
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Simple approach: split on sentence-ending punctuation
        # Look for . ! ? followed by space and capital letter, or end of string
        sentences = []
        current_sentence = ""
        
        i = 0
        while i < len(text):
            char = text[i]
            current_sentence += char
            
            # Check for sentence-ending punctuation
            if char in '.!?':
                # Look ahead to see what comes next
                if i + 1 >= len(text):
                    # End of text - this is definitely a sentence end
                    sentences.append(current_sentence.strip())
                    break
                elif text[i + 1] == ' ':
                    # Space after punctuation - check what follows
                    # Look for capital letter (likely new sentence start)
                    j = i + 2
                    while j < len(text) and text[j] == ' ':
                        j += 1
                    
                    if j < len(text) and text[j].isupper():
                        # Capital letter follows - likely sentence boundary
                        # But check if it's an abbreviation
                        words = current_sentence.strip().split()
                        if words:
                            last_word = words[-1].rstrip('.!?').lower()
                            # If not an abbreviation, split here
                            if last_word not in self.abbreviations or len(last_word) > 3:
                                sentences.append(current_sentence.strip())
                                current_sentence = ""
                                i = j - 1  # Continue from the capital letter
                                continue
            
            i += 1
        
        # Add remaining text as last sentence
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        # Fallback: if no sentences found, use simple regex split
        if not sentences:
            # Simple split on punctuation followed by space
            parts = re.split(r'([.!?]+)\s+', text)
            sentences = []
            for i in range(0, len(parts), 2):
                if i < len(parts):
                    sentence = parts[i]
                    if i + 1 < len(parts):
                        sentence += parts[i + 1]
                    sentence = sentence.strip()
                    if sentence:
                        sentences.append(sentence)
            if not sentences:
                sentences = [text]
        
        # Final cleanup
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _is_abbreviation(self, word: str) -> bool:
        """
        Check if a word is a common abbreviation.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is an abbreviation
        """
        return word.lower().rstrip('.') in self.abbreviations
