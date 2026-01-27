"""
Evaluation Script for Sentence Segmentation

This module implements evaluation metrics (Precision, Recall, F1-score) to compare
the baseline regex-based system with the proposed spaCy-based system.

The evaluation uses manually annotated gold standard data where sentence boundaries
are marked for comparison.

ERROR ANALYSIS:
---------------
Common error types identified in sentence segmentation:

1. Abbreviation Errors:
   - Baseline: Often splits on abbreviations (e.g., "Dr.", "U.S.A.", "N.Y.")
   - Proposed: Better handling through trained models
   - Example: "Dr. Smith went..." → Baseline may split incorrectly

2. Decimal Number Errors:
   - Baseline: May split on decimal points (e.g., "3.14" → "3." and "14")
   - Proposed: Recognizes numeric patterns correctly

3. Quotation Mark Handling:
   - Baseline: May split before closing quotes
   - Proposed: Understands quote boundaries better
   - Example: 'He said, "This is amazing."' → Should be one sentence

4. Ellipsis and Multiple Punctuation:
   - Baseline: May create multiple splits on "..." or "?!"
   - Proposed: Handles complex punctuation patterns

5. Capitalization Ambiguity:
   - Baseline: Relies heavily on capital letters after punctuation
   - Proposed: Uses linguistic context beyond capitalization

6. Edge Cases:
   - URLs, email addresses, dates
   - Acronyms vs. abbreviations
   - Titles and honorifics
"""

import sys
import os
import json
from typing import List, Set, Tuple, Dict
from collections import defaultdict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.baseline_splitter import BaselineSentenceSplitter
from backend.spacy_splitter import SpacySentenceSplitter


class SegmentationEvaluator:
    """
    Evaluator for comparing sentence segmentation systems.
    
    Computes Precision, Recall, and F1-score by comparing predicted
    sentence boundaries with gold standard annotations.
    """
    
    def __init__(self):
        """Initialize evaluator with baseline and proposed systems."""
        self.baseline_splitter = BaselineSentenceSplitter()
        self.spacy_splitter = SpacySentenceSplitter()
    
    def _get_sentence_boundaries(self, text: str, sentences: List[str]) -> Set[int]:
        """
        Extract sentence boundary positions from segmented sentences.
        
        Args:
            text: Original text
            sentences: List of segmented sentences
            
        Returns:
            Set of character positions where sentences end
        """
        boundaries = set()
        current_pos = 0
        
        for i, sentence in enumerate(sentences):
            # Find sentence in original text
            sentence_start = text.find(sentence.strip(), current_pos)
            if sentence_start == -1:
                # If exact match not found, approximate
                sentence_start = current_pos
            
            sentence_end = sentence_start + len(sentence.strip())
            if i < len(sentences) - 1:  # Not the last sentence
                boundaries.add(sentence_end)
            
            current_pos = sentence_end
        
        return boundaries
    
    def evaluate(self, text: str, gold_sentences: List[str], 
                 language: str = "en") -> dict:
        """
        Evaluate both baseline and proposed systems against gold standard.
        
        Args:
            text: Original input text
            gold_sentences: Gold standard sentence segmentation
            language: Language code for spaCy model
            
        Returns:
            Dictionary containing evaluation metrics for both systems
        """
        # Get predictions from both systems
        baseline_sentences = self.baseline_splitter.split(text)
        spacy_sentences = self.spacy_splitter.split(text, language)
        
        # Get gold standard boundaries
        gold_boundaries = self._get_sentence_boundaries(text, gold_sentences)
        
        # Get predicted boundaries
        baseline_boundaries = self._get_sentence_boundaries(text, baseline_sentences)
        spacy_boundaries = self._get_sentence_boundaries(text, spacy_sentences)
        
        # Calculate metrics for baseline
        baseline_metrics = self._calculate_metrics(
            gold_boundaries, baseline_boundaries, len(gold_sentences), len(baseline_sentences)
        )
        
        # Calculate metrics for proposed system
        spacy_metrics = self._calculate_metrics(
            gold_boundaries, spacy_boundaries, len(gold_sentences), len(spacy_sentences)
        )
        
        # Perform error analysis
        baseline_errors = self._analyze_errors(text, gold_sentences, baseline_sentences, "baseline")
        spacy_errors = self._analyze_errors(text, gold_sentences, spacy_sentences, "proposed")
        
        return {
            "baseline": {
                "sentences": baseline_sentences,
                "count": len(baseline_sentences),
                "errors": baseline_errors,
                **baseline_metrics
            },
            "proposed": {
                "sentences": spacy_sentences,
                "count": len(spacy_sentences),
                "errors": spacy_errors,
                **spacy_metrics
            },
            "gold_standard": {
                "sentences": gold_sentences,
                "count": len(gold_sentences)
            },
            "text": text
        }
    
    def _calculate_metrics(self, gold_boundaries: Set[int], 
                          predicted_boundaries: Set[int],
                          gold_count: int, predicted_count: int) -> dict:
        """
        Calculate Precision, Recall, and F1-score.
        
        Args:
            gold_boundaries: Set of gold standard boundary positions
            predicted_boundaries: Set of predicted boundary positions
            gold_count: Number of gold standard sentences
            predicted_count: Number of predicted sentences
            
        Returns:
            Dictionary with precision, recall, f1_score
        """
        # True Positives: boundaries that match exactly
        # We allow small tolerance (±5 characters) for boundary matching
        tp = 0
        matched_gold = set()
        matched_pred = set()
        
        for gold_pos in gold_boundaries:
            for pred_pos in predicted_boundaries:
                if abs(gold_pos - pred_pos) <= 5:  # Tolerance window
                    tp += 1
                    matched_gold.add(gold_pos)
                    matched_pred.add(pred_pos)
                    break
        
        # False Positives: predicted boundaries not in gold
        fp = len(predicted_boundaries) - len(matched_pred)
        
        # False Negatives: gold boundaries not in predictions
        fn = len(gold_boundaries) - len(matched_gold)
        
        # Calculate metrics
        precision = tp / predicted_count if predicted_count > 0 else 0.0
        recall = tp / gold_count if gold_count > 0 else 0.0
        
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0
        
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn
        }
    
    def evaluate_file(self, input_file: str, gold_file: str, 
                     language: str = "en") -> dict:
        """
        Evaluate systems using text files.
        
        Args:
            input_file: Path to input text file
            gold_file: Path to gold standard JSON file (list of sentences)
            language: Language code
            
        Returns:
            Evaluation results dictionary
        """
        # Read input text
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Read gold standard
        with open(gold_file, 'r', encoding='utf-8') as f:
            gold_data = json.load(f)
            gold_sentences = gold_data.get('sentences', gold_data) if isinstance(gold_data, dict) else gold_data
        
        return self.evaluate(text, gold_sentences, language)
    
    def _analyze_errors(self, text: str, gold_sentences: List[str], 
                        predicted_sentences: List[str], system_name: str) -> Dict:
        """
        Analyze common error types in sentence segmentation.
        
        Args:
            text: Original text
            gold_sentences: Gold standard sentences
            predicted_sentences: Predicted sentences
            system_name: Name of the system being analyzed
            
        Returns:
            Dictionary with error analysis
        """
        errors = {
            "abbreviation_errors": [],
            "quotation_errors": [],
            "decimal_errors": [],
            "over_segmentation": [],
            "under_segmentation": [],
            "total_errors": 0
        }
        
        # Check for abbreviation-related errors
        abbreviation_patterns = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'U.S.A.', 'N.Y.', 'etc.']
        for pattern in abbreviation_patterns:
            if pattern in text:
                # Check if predicted segmentation incorrectly splits on abbreviation
                for pred_sent in predicted_sentences:
                    if pattern in pred_sent:
                        # Check if this sentence matches gold standard
                        matches_gold = any(pattern in gold_sent for gold_sent in gold_sentences)
                        if not matches_gold:
                            errors["abbreviation_errors"].append({
                                "pattern": pattern,
                                "sentence": pred_sent[:50] + "..." if len(pred_sent) > 50 else pred_sent
                            })
        
        # Check for quotation mark errors
        if '"' in text or "'" in text:
            for pred_sent in predicted_sentences:
                quote_count = pred_sent.count('"') + pred_sent.count("'")
                if quote_count % 2 != 0:  # Odd number of quotes suggests error
                    errors["quotation_errors"].append(pred_sent[:50] + "..." if len(pred_sent) > 50 else pred_sent)
        
        # Check for decimal number errors
        import re
        decimal_pattern = r'\d+\.\d+'
        decimals = re.findall(decimal_pattern, text)
        for decimal in decimals:
            for pred_sent in predicted_sentences:
                if decimal in pred_sent:
                    # Check if decimal is split incorrectly
                    if pred_sent.strip().endswith('.' + decimal.split('.')[1][0]):
                        errors["decimal_errors"].append({
                            "decimal": decimal,
                            "sentence": pred_sent[:50] + "..." if len(pred_sent) > 50 else pred_sent
                        })
        
        # Over-segmentation: more sentences than gold standard
        if len(predicted_sentences) > len(gold_sentences):
            errors["over_segmentation"] = {
                "count": len(predicted_sentences) - len(gold_sentences),
                "ratio": len(predicted_sentences) / len(gold_sentences) if len(gold_sentences) > 0 else 0
            }
        
        # Under-segmentation: fewer sentences than gold standard
        if len(predicted_sentences) < len(gold_sentences):
            errors["under_segmentation"] = {
                "count": len(gold_sentences) - len(predicted_sentences),
                "ratio": len(predicted_sentences) / len(gold_sentences) if len(gold_sentences) > 0 else 0
            }
        
        errors["total_errors"] = (
            len(errors["abbreviation_errors"]) +
            len(errors["quotation_errors"]) +
            len(errors["decimal_errors"])
        )
        
        return errors


def print_evaluation_results(results: dict, format_type: str = "table"):
    """
    Print evaluation results in a readable format.
    
    Args:
        results: Results dictionary from evaluate() method
        format_type: "table" for academic table format, "detailed" for verbose output
    """
    if format_type == "table":
        print_table_format(results)
    else:
        print_detailed_format(results)


def print_table_format(results: dict):
    """
    Print evaluation results in academic table format suitable for reports.
    
    Args:
        results: Results dictionary from evaluate() method
    """
    baseline = results['baseline']
    proposed = results['proposed']
    gold_count = results['gold_standard']['count']

    # Ensure baseline_errors and proposed_errors are dictionaries
    baseline_errors = baseline.get('errors', {})
    proposed_errors = proposed.get('errors', {})

    # Debugging the structure of errors
    print("Debugging baseline_errors structure:", baseline_errors)
    print("Debugging proposed_errors structure:", proposed_errors)

    if isinstance(baseline_errors, list):
        baseline_errors = {str(index): error for index, error in enumerate(baseline_errors) if isinstance(error, dict)}
    if isinstance(proposed_errors, list):
        proposed_errors = {str(index): error for index, error in enumerate(proposed_errors) if isinstance(error, dict)}

    print("\n" + "="*80)
    print("EVALUATION RESULTS - SENTENCE SEGMENTATION SYSTEMS")
    print("="*80)

    # Main metrics table
    print("\nTable 1: Performance Metrics Comparison")
    print("-" * 80)
    print(f"{'Metric':<20} {'Baseline System':<25} {'Proposed System (spaCy)':<25} {'Improvement':<15}")
    print("-" * 80)

    precision_imp = proposed['precision'] - baseline['precision']
    recall_imp = proposed['recall'] - baseline['recall']
    f1_imp = proposed['f1_score'] - baseline['f1_score']

    print(f"{'Precision':<20} {baseline['precision']:<25.4f} {proposed['precision']:<25.4f} {precision_imp:+.4f} ({precision_imp*100:+.2f}%)")
    print(f"{'Recall':<20} {baseline['recall']:<25.4f} {proposed['recall']:<25.4f} {recall_imp:+.4f} ({recall_imp*100:+.2f}%)")
    print(f"{'F1-Score':<20} {baseline['f1_score']:<25.4f} {proposed['f1_score']:<25.4f} {f1_imp:+.4f} ({f1_imp*100:+.2f}%)")
    print("-" * 80)

    # Detailed metrics table
    print("\nTable 2: Detailed Evaluation Metrics")
    print("-" * 80)
    print(f"{'System':<20} {'Sentences':<15} {'TP':<10} {'FP':<10} {'FN':<10} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 80)
    print(f"{'Gold Standard':<20} {gold_count:<15} {'-':<10} {'-':<10} {'-':<10} {'-':<12} {'-':<12} {'-':<12}")
    print(f"{'Baseline (Regex)':<20} {baseline['count']:<15} {baseline['true_positives']:<10} "
          f"{baseline['false_positives']:<10} {baseline['false_negatives']:<10} "
          f"{baseline['precision']:<12.4f} {baseline['recall']:<12.4f} {baseline['f1_score']:<12.4f}")
    print(f"{'Proposed (spaCy)':<20} {proposed['count']:<15} {proposed['true_positives']:<10} "
          f"{proposed['false_positives']:<10} {proposed['false_negatives']:<10} "
          f"{proposed['precision']:<12.4f} {proposed['recall']:<12.4f} {proposed['f1_score']:<12.4f}")
    print("-" * 80)

    # Error analysis table
    print("\nTable 3: Error Analysis")
    print("-" * 80)
    print(f"{'Error Type':<30} {'Baseline':<25} {'Proposed (spaCy)':<25}")
    print("-" * 80)

    print(f"{'Abbreviation Errors':<30} {len(baseline_errors.get('abbreviation_errors', [])):<25} "
          f"{len(proposed_errors.get('abbreviation_errors', [])):<25}")
    print(f"{'Quotation Errors':<30} {len(baseline_errors.get('quotation_errors', [])):<25} "
          f"{len(proposed_errors.get('quotation_errors', [])):<25}")
    print(f"{'Decimal Number Errors':<30} {len(baseline_errors.get('decimal_errors', [])):<25} "
          f"{len(proposed_errors.get('decimal_errors', [])):<25}")

    baseline_over = baseline_errors.get('over_segmentation', {}).get('count', 0)
    proposed_over = proposed_errors.get('over_segmentation', {}).get('count', 0)
    print(f"{'Over-segmentation (count)':<30} {baseline_over:<25} {proposed_over:<25}")

    baseline_under = baseline_errors.get('under_segmentation', {}).get('count', 0)
    proposed_under = proposed_errors.get('under_segmentation', {}).get('count', 0)
    print(f"{'Under-segmentation (count)':<30} {baseline_under:<25} {proposed_under:<25}")

    print(f"{'Total Errors':<30} {baseline_errors.get('total_errors', 0):<25} "
          f"{proposed_errors.get('total_errors', 0):<25}")
    print("-" * 80)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    if f1_imp > 0:
        print(f"✓ The proposed spaCy-based system outperforms the baseline by {f1_imp*100:.2f}% in F1-score.")
        print(f"  - Precision improvement: {precision_imp*100:+.2f}%")
        print(f"  - Recall improvement: {recall_imp*100:+.2f}%")
    else:
        print(f"⚠ The baseline system performs better. Consider model improvements.")
    print("="*80 + "\n")


def print_detailed_format(results: dict):
    """
    Print detailed evaluation results with verbose output.
    
    Args:
        results: Results dictionary from evaluate() method
    """
    print("\n" + "="*70)
    print("SENTENCE SEGMENTATION EVALUATION RESULTS")
    print("="*70)
    
    print(f"\nGold Standard: {results['gold_standard']['count']} sentences")
    
    print("\n" + "-"*70)
    print("BASELINE SYSTEM (Rule-Based Regex)")
    print("-"*70)
    baseline = results['baseline']
    print(f"Sentences Found: {baseline['count']}")
    print(f"Precision: {baseline['precision']:.4f}")
    print(f"Recall:    {baseline['recall']:.4f}")
    print(f"F1-Score:  {baseline['f1_score']:.4f}")
    print(f"True Positives:  {baseline['true_positives']}")
    print(f"False Positives: {baseline['false_positives']}")
    print(f"False Negatives: {baseline['false_negatives']}")
    
    # Error details for baseline
    if 'errors' in baseline:
        errors = baseline['errors']
        if errors.get('total_errors', 0) > 0:
            print("\nError Analysis:")
            if errors.get('abbreviation_errors'):
                print(f"  Abbreviation errors: {len(errors['abbreviation_errors'])}")
            if errors.get('quotation_errors'):
                print(f"  Quotation errors: {len(errors['quotation_errors'])}")
            if errors.get('decimal_errors'):
                print(f"  Decimal errors: {len(errors['decimal_errors'])}")
    
    print("\n" + "-"*70)
    print("PROPOSED SYSTEM (spaCy NLP)")
    print("-"*70)
    proposed = results['proposed']
    print(f"Sentences Found: {proposed['count']}")
    print(f"Precision: {proposed['precision']:.4f}")
    print(f"Recall:    {proposed['recall']:.4f}")
    print(f"F1-Score:  {proposed['f1_score']:.4f}")
    print(f"True Positives:  {proposed['true_positives']}")
    print(f"False Positives: {proposed['false_positives']}")
    print(f"False Negatives: {proposed['false_negatives']}")
    
    # Error details for proposed
    if 'errors' in proposed:
        errors = proposed['errors']
        if errors.get('total_errors', 0) > 0:
            print("\nError Analysis:")
            if errors.get('abbreviation_errors'):
                print(f"  Abbreviation errors: {len(errors['abbreviation_errors'])}")
            if errors.get('quotation_errors'):
                print(f"  Quotation errors: {len(errors['quotation_errors'])}")
            if errors.get('decimal_errors'):
                print(f"  Decimal errors: {len(errors['decimal_errors'])}")
    
    print("\n" + "-"*70)
    print("IMPROVEMENT ANALYSIS")
    print("-"*70)
    precision_improvement = proposed['precision'] - baseline['precision']
    recall_improvement = proposed['recall'] - baseline['recall']
    f1_improvement = proposed['f1_score'] - baseline['f1_score']
    
    print(f"Precision Improvement: {precision_improvement:+.4f} ({precision_improvement*100:+.2f}%)")
    print(f"Recall Improvement:    {recall_improvement:+.4f} ({recall_improvement*100:+.2f}%)")
    print(f"F1-Score Improvement:  {f1_improvement:+.4f} ({f1_improvement*100:+.2f}%)")
    
    if f1_improvement > 0:
        print(f"\n✓ Proposed system outperforms baseline by {f1_improvement*100:.2f}% in F1-score")
    else:
        print(f"\n⚠ Baseline system performs better. Consider model improvements.")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    # Example usage
    evaluator = SegmentationEvaluator()
    
    # Sample evaluation
    sample_text = """
    Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y. and Los Angeles, Calif.
    The weather was great! He said, "This is amazing." Then he returned home.
    """
    
    gold_sentences = [
        "Dr. Smith went to the U.S.A. in 2020.",
        "He visited New York, N.Y. and Los Angeles, Calif.",
        "The weather was great!",
        'He said, "This is amazing."',
        "Then he returned home."
    ]
    
    results = evaluator.evaluate(sample_text, gold_sentences)
    print_evaluation_results(results)
