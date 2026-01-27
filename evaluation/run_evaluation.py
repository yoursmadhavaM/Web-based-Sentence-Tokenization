#!/usr/bin/env python3
"""
Run evaluation script for sentence segmentation systems.

This script evaluates both baseline and proposed systems using sample data
and prints comprehensive evaluation results in academic table format.

The evaluation uses manually annotated English sentences as gold standard data
and computes Precision, Recall, and F1-score for both systems.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.evaluate import SegmentationEvaluator, print_evaluation_results


def evaluate_all_datasets():
    """Evaluate on all gold standard datasets."""
    evaluator = SegmentationEvaluator()
    
    # Load comprehensive gold standard data
    gold_data_path = os.path.join(os.path.dirname(__file__), "gold_standard_data.json")
    
    all_results = []
    
    try:
        with open(gold_data_path, 'r', encoding='utf-8') as f:
            gold_data = json.load(f)
        
        datasets = gold_data.get('datasets', [])
        
        print("="*80)
        print("COMPREHENSIVE EVALUATION - MULTIPLE DATASETS")
        print("="*80)
        print(f"\nEvaluating {len(datasets)} datasets...\n")
        
        # Evaluate each dataset
        for dataset in datasets:
            dataset_id = dataset.get('id', 'unknown')
            description = dataset.get('description', '')
            text = dataset.get('text', '')
            gold_sentences = dataset.get('sentences', [])
            
            print(f"\n{'='*80}")
            print(f"Dataset: {dataset_id}")
            print(f"Description: {description}")
            print(f"{'='*80}")
            
            results = evaluator.evaluate(text, gold_sentences, language="en")
            all_results.append({
                'dataset_id': dataset_id,
                'results': results
            })
            
            # Print table format results
            print_evaluation_results(results, format_type="table")
        
        # Aggregate results
        print("\n" + "="*80)
        print("AGGREGATED RESULTS ACROSS ALL DATASETS")
        print("="*80)
        
        total_gold = sum(len(r['results']['gold_standard']['sentences']) for r in all_results)
        total_baseline_tp = sum(r['results']['baseline']['true_positives'] for r in all_results)
        total_baseline_fp = sum(r['results']['baseline']['false_positives'] for r in all_results)
        total_baseline_fn = sum(r['results']['baseline']['false_negatives'] for r in all_results)
        total_baseline_count = sum(r['results']['baseline']['count'] for r in all_results)
        
        total_proposed_tp = sum(r['results']['proposed']['true_positives'] for r in all_results)
        total_proposed_fp = sum(r['results']['proposed']['false_positives'] for r in all_results)
        total_proposed_fn = sum(r['results']['proposed']['false_negatives'] for r in all_results)
        total_proposed_count = sum(r['results']['proposed']['count'] for r in all_results)
        
        # Calculate aggregated metrics
        baseline_precision = total_baseline_tp / total_baseline_count if total_baseline_count > 0 else 0
        baseline_recall = total_baseline_tp / total_gold if total_gold > 0 else 0
        baseline_f1 = 2 * (baseline_precision * baseline_recall) / (baseline_precision + baseline_recall) if (baseline_precision + baseline_recall) > 0 else 0
        
        proposed_precision = total_proposed_tp / total_proposed_count if total_proposed_count > 0 else 0
        proposed_recall = total_proposed_tp / total_gold if total_gold > 0 else 0
        proposed_f1 = 2 * (proposed_precision * proposed_recall) / (proposed_precision + proposed_recall) if (proposed_precision + proposed_recall) > 0 else 0
        
        print("\nTable: Aggregated Performance Metrics")
        print("-" * 80)
        print(f"{'Metric':<20} {'Baseline System':<25} {'Proposed System (spaCy)':<25} {'Improvement':<15}")
        print("-" * 80)
        
        precision_imp = proposed_precision - baseline_precision
        recall_imp = proposed_recall - baseline_recall
        f1_imp = proposed_f1 - baseline_f1
        
        print(f"{'Precision':<20} {baseline_precision:<25.4f} {proposed_precision:<25.4f} {precision_imp:+.4f} ({precision_imp*100:+.2f}%)")
        print(f"{'Recall':<20} {baseline_recall:<25.4f} {proposed_recall:<25.4f} {recall_imp:+.4f} ({recall_imp*100:+.2f}%)")
        print(f"{'F1-Score':<20} {baseline_f1:<25.4f} {proposed_f1:<25.4f} {f1_imp:+.4f} ({f1_imp*100:+.2f}%)")
        print("-" * 80)
        
        print(f"\nTotal Gold Standard Sentences: {total_gold}")
        print(f"Baseline: {total_baseline_count} sentences (TP: {total_baseline_tp}, FP: {total_baseline_fp}, FN: {total_baseline_fn})")
        print(f"Proposed: {total_proposed_count} sentences (TP: {total_proposed_tp}, FP: {total_proposed_fp}, FN: {total_proposed_fn})")
        
        print("\n" + "="*80)
        print("Evaluation complete!")
        print("="*80 + "\n")
        
    except FileNotFoundError:
        print(f"Warning: Gold standard data file not found at {gold_data_path}")
        print("Falling back to single dataset evaluation...\n")
        evaluate_single_dataset()


def evaluate_single_dataset():
    """Evaluate on single sample dataset."""
    evaluator = SegmentationEvaluator()
    
    # Load sample data
    sample_data_path = os.path.join(os.path.dirname(__file__), "sample_data.json")
    
    try:
        with open(sample_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        text = data['text']
        gold_sentences = data['sentences']
        
        print("="*80)
        print("SENTENCE SEGMENTATION EVALUATION")
        print("="*80)
        print(f"\nInput text: {text[:100]}...")
        print(f"Gold standard sentences: {len(gold_sentences)}")
        print("\nRunning evaluation...\n")
        
        # Run evaluation
        results = evaluator.evaluate(text, gold_sentences, language="en")
        
        # Print results in table format
        print_evaluation_results(results, format_type="table")
        
        # Additional detailed output
        print("\n" + "-"*80)
        print("DETAILED SENTENCE COMPARISON")
        print("-"*80)
        
        print("\nGold Standard Sentences:")
        for i, sent in enumerate(results['gold_standard']['sentences'], 1):
            print(f"  {i}. {sent}")
        
        print("\nBaseline Sentences:")
        for i, sent in enumerate(results['baseline']['sentences'], 1):
            print(f"  {i}. {sent}")
        
        print("\nProposed (spaCy) Sentences:")
        for i, sent in enumerate(results['proposed']['sentences'], 1):
            print(f"  {i}. {sent}")
        
        print("\n" + "="*80)
        print("Evaluation complete!")
        print("="*80 + "\n")
        
    except FileNotFoundError:
        print(f"Error: Sample data file not found at {sample_data_path}")
        print("Using inline sample data...\n")
        
        # Fallback to inline data
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
        print_evaluation_results(results, format_type="table")


def main():
    """Main function to run evaluation."""
    # Try to evaluate all datasets first, fall back to single if file not found
    try:
        evaluate_all_datasets()
    except Exception as e:
        print(f"Error in comprehensive evaluation: {e}")
        print("Falling back to single dataset evaluation...\n")
        evaluate_single_dataset()


if __name__ == "__main__":
    main()
