# Sentence Segmentation Tool - NLP Academic Project

A web-based sentence segmentation tool using Natural Language Processing, developed as a Bachelor-level academic project.

## Project Overview

This project implements and compares two sentence segmentation approaches:

1. **Baseline System**: Rule-based regex sentence splitter
2. **Proposed System**: spaCy-based NLP sentence segmentation

The tool supports English (mandatory) and multilingual extension (French, German, Spanish).

## Features

- ✅ FastAPI backend with REST API
- ✅ Clean web interface (HTML/CSS/JavaScript)
- ✅ Baseline regex-based sentence splitter
- ✅ spaCy-based NLP sentence segmentation
- ✅ Multilingual support (English, French, German, Spanish)
- ✅ Evaluation metrics (Precision, Recall, F1-score)
- ✅ Docker deployment support
- ✅ Academic-friendly code structure with comments

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── baseline_splitter.py # Baseline regex-based splitter
│   └── spacy_splitter.py    # spaCy-based splitter
├── frontend/
│   ├── index.html           # Web interface
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
├── evaluation/
│   ├── evaluate.py          # Evaluation metrics
│   ├── run_evaluation.py    # Evaluation script
│   └── sample_data.json     # Sample gold standard data
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd NLP
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy Models

**English (Mandatory):**
```bash
python -m spacy download en_core_web_sm
```

**Multilingual Models (Optional):**
```bash
python -m spacy download fr_core_news_sm  # French
python -m spacy download de_core_news_sm  # German
python -m spacy download es_core_news_sm  # Spanish
```

## Usage

### Running the Backend Server

```bash
# From project root directory
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Accessing the Web Interface

1. Start the backend server (see above)
2. Open your browser and navigate to `http://localhost:8000`
3. Enter text in the input box
4. Select language and method (baseline or spaCy)
5. Click "Segment Sentences"

### API Usage

#### Segment Sentences Endpoint

**POST** `/segment`

**Request Body:**
```json
{
  "text": "Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y. The weather was great!",
  "language": "en",
  "method": "spacy"
}
```

**Response:**
```json
{
  "sentences": [
    "Dr. Smith went to the U.S.A. in 2020.",
    "He visited New York, N.Y.",
    "The weather was great!"
  ],
  "method": "spacy",
  "language": "en",
  "count": 3
}
```

#### Health Check

**GET** `/health`

Returns server health status.

## Evaluation

### Running Evaluation

The evaluation script compares baseline and proposed systems using Precision, Recall, and F1-score:

```bash
python evaluation/run_evaluation.py
```

### Evaluation Metrics

- **Precision**: Proportion of predicted sentence boundaries that are correct
- **Recall**: Proportion of gold standard boundaries that were found
- **F1-Score**: Harmonic mean of Precision and Recall

### Sample Results

The evaluation script uses sample gold standard data. Expected output shows:

- Baseline system metrics
- Proposed (spaCy) system metrics
- Improvement analysis
- Detailed sentence comparison

## Docker Deployment

### Building the Docker Image

```bash
docker build -t sentence-segmentation .
```

### Running the Container

```bash
docker run -p 8000:8000 sentence-segmentation
```

The application will be available at `http://localhost:8000`

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
```

Run with:
```bash
docker-compose up
```

## Technical Details

### Baseline System

The baseline system uses regular expressions to identify sentence boundaries:
- Splits on `.`, `!`, `?` followed by whitespace
- Handles common abbreviations (Dr., U.S.A., etc.)
- Basic whitespace normalization

### Proposed System (spaCy)

The proposed system leverages spaCy's trained NLP models:
- Uses linguistic knowledge from trained models
- Better handling of abbreviations and edge cases
- Multilingual support with language-specific models
- More accurate boundary detection

### Evaluation Methodology

1. Gold standard data: Manually annotated sentences
2. Boundary matching: Compares predicted vs. gold boundaries
3. Tolerance window: ±5 characters for boundary matching
4. Metrics: Precision, Recall, F1-score

## Academic Notes

### Project Level
- Bachelor-level implementation
- Clear, explainable methods
- Standard NLP terminology
- No overengineering or deep neural networks

### Code Quality
- Comprehensive comments
- Clean structure (backend/frontend/evaluation separation)
- Academic-friendly documentation
- Runnable without modification

### Extensions
- Multilingual support (French, German, Spanish)
- Docker deployment
- Web interface
- Evaluation framework

## Troubleshooting

### spaCy Models Not Found

If you see warnings about missing models:

```bash
python -m spacy download en_core_web_sm
```

### Backend Not Starting

1. Check if port 8000 is available
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.11+)

### Frontend Not Loading

1. Ensure backend is running on `http://localhost:8000`
2. Check browser console for errors
3. Verify CORS settings in `backend/main.py`

### Evaluation Errors

1. Ensure spaCy models are downloaded
2. Check that `evaluation/sample_data.json` exists
3. Verify Python path includes project root

## License

This project is developed for academic purposes.

## Author

Bachelor-level Academic Project - NLP Sentence Segmentation

## References

- spaCy Documentation: https://spacy.io/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Sentence Segmentation in NLP: Standard approaches and evaluation metrics
