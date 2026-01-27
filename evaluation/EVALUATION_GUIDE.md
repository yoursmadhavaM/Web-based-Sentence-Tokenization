# Evaluation Module Guide

## Overview

The evaluation module provides comprehensive evaluation of sentence segmentation systems using manually annotated English sentences as gold standard data. It computes Precision, Recall, and F1-score metrics and compares the baseline (regex-based) system with the proposed (spaCy-based) system.

## Features

### ✅ Gold Standard Data
- **Manually annotated English sentences** stored in JSON format
- Multiple test datasets covering various edge cases:
  - Abbreviations (Dr., U.S.A., N.Y., etc.)
  - Decimal numbers (98.6, 3.14159, etc.)
  - Quotations and dialogue
  - Titles and honorifics
  - Complex punctuation

### ✅ Evaluation Metrics
- **Precision**: Proportion of predicted sentence boundaries that are correct
- **Recall**: Proportion of gold standard boundaries that were found
- **F1-Score**: Harmonic mean of Precision and Recall
- **True Positives (TP)**: Correctly identified sentence boundaries
- **False Positives (FP)**: Incorrectly predicted boundaries
- **False Negatives (FN)**: Missed gold standard boundaries

### ✅ Error Analysis
The module includes comprehensive error analysis identifying:
1. **Abbreviation Errors**: Incorrect splitting on abbreviations
2. **Quotation Errors**: Issues with quote boundary detection
3. **Decimal Number Errors**: Splitting on decimal points
4. **Over-segmentation**: Creating too many sentences
5. **Under-segmentation**: Creating too few sentences

### ✅ Academic Report Format
Results are output in table format suitable for academic reports:
- **Table 1**: Performance Metrics Comparison
- **Table 2**: Detailed Evaluation Metrics
- **Table 3**: Error Analysis

## Usage

### Basic Evaluation

```python
from evaluation.evaluate import SegmentationEvaluator, print_evaluation_results

evaluator = SegmentationEvaluator()

# Evaluate with gold standard data
text = "Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y."
gold_sentences = [
    "Dr. Smith went to the U.S.A. in 2020.",
    "He visited New York, N.Y."
]

results = evaluator.evaluate(text, gold_sentences, language="en")
print_evaluation_results(results, format_type="table")
```

### Running Full Evaluation

```bash
python evaluation/run_evaluation.py
```

This will:
1. Load all gold standard datasets from `gold_standard_data.json`
2. Evaluate each dataset separately
3. Compute aggregated metrics across all datasets
4. Output results in academic table format

## Output Format

### Table Format (Academic Report Ready)

```
================================================================================
EVALUATION RESULTS - SENTENCE SEGMENTATION SYSTEMS
================================================================================

Table 1: Performance Metrics Comparison
--------------------------------------------------------------------------------
Metric               Baseline System          Proposed System (spaCy)    Improvement
--------------------------------------------------------------------------------
Precision            0.8500                   0.9500                    +0.1000 (+10.00%)
Recall               0.8000                   0.9000                    +0.1000 (+10.00%)
F1-Score             0.8242                   0.9242                    +0.1000 (+10.00%)
--------------------------------------------------------------------------------

Table 2: Detailed Evaluation Metrics
--------------------------------------------------------------------------------
System               Sentences      TP         FP         FN         Precision    Recall       F1-Score
--------------------------------------------------------------------------------
Gold Standard        5              -          -          -          -            -            -
Baseline (Regex)     6              4          2          1          0.6667       0.8000       0.7273
Proposed (spaCy)     5              4          1          1          0.8000       0.8000       0.8000
--------------------------------------------------------------------------------

Table 3: Error Analysis
--------------------------------------------------------------------------------
Error Type                        Baseline                  Proposed (spaCy)
--------------------------------------------------------------------------------
Abbreviation Errors              2                         0
Quotation Errors                1                         0
Decimal Number Errors           0                         0
Over-segmentation (count)       1                         0
Under-segmentation (count)       0                         0
Total Errors                    3                         0
--------------------------------------------------------------------------------
```

## Gold Standard Data Structure

The gold standard data is stored in `gold_standard_data.json`:

```json
{
  "datasets": [
    {
      "id": "dataset_1",
      "description": "Text with abbreviations and complex punctuation",
      "text": "Full text here...",
      "sentences": ["Sentence 1.", "Sentence 2."]
    }
  ],
  "metadata": {
    "total_sentences": 22,
    "total_datasets": 5,
    "language": "en"
  }
}
```

## Error Analysis Details

### Abbreviation Errors
- **Baseline**: Often splits incorrectly on abbreviations like "Dr.", "U.S.A.", "N.Y."
- **Proposed**: Better handling through trained linguistic models
- **Example**: "Dr. Smith went..." → Baseline may split after "Dr."

### Quotation Errors
- **Baseline**: May split before closing quotes
- **Proposed**: Understands quote boundaries better
- **Example**: 'He said, "This is amazing."' → Should be one sentence

### Decimal Number Errors
- **Baseline**: May split on decimal points (e.g., "3.14" → "3." and "14")
- **Proposed**: Recognizes numeric patterns correctly

### Over-segmentation
- Creating more sentences than the gold standard
- Indicates system is too aggressive in splitting

### Under-segmentation
- Creating fewer sentences than the gold standard
- Indicates system is too conservative in splitting

## Academic Use

The evaluation module is designed for academic reporting:

1. **Reproducible**: Uses standardized gold standard data
2. **Comprehensive**: Covers multiple error types and edge cases
3. **Formatted**: Output in table format suitable for papers
4. **Documented**: Includes error analysis comments explaining common issues

## Customization

### Adding New Gold Standard Data

Edit `gold_standard_data.json` to add new test cases:

```json
{
  "id": "dataset_6",
  "description": "Your test case description",
  "text": "Your test text here...",
  "sentences": ["Sentence 1.", "Sentence 2."]
}
```

### Modifying Error Analysis

Edit the `_analyze_errors` method in `evaluate.py` to add custom error detection patterns.

## References

- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

Where:
- TP = True Positives (correct boundaries)
- FP = False Positives (incorrect boundaries)
- FN = False Negatives (missed boundaries)
