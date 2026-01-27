# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download spaCy Models
```bash
# English (required)
python -m spacy download en_core_web_sm

# Optional: Multilingual support
python -m spacy download fr_core_news_sm  # French
python -m spacy download de_core_news_sm  # German
python -m spacy download es_core_news_sm  # Spanish
```

**Or use the automated setup script:**
```bash
python setup.py
```

### Step 3: Test Installation
```bash
python test_system.py
```

## Running the Application

### Start the Server
```bash
python run_server.py
```

### Access the Web Interface
Open your browser and go to: **http://localhost:8000**

### API Endpoint
The API is available at: **http://localhost:8000/docs** (Swagger UI)

## Running Evaluation

```bash
python evaluation/run_evaluation.py
```

This will compare baseline vs. proposed system and show Precision, Recall, and F1-score.

## Docker Deployment

### Build and Run
```bash
docker build -t sentence-segmentation .
docker run -p 8000:8000 sentence-segmentation
```

### Or use Docker Compose
```bash
docker-compose up
```

## Example Usage

### Web Interface
1. Enter text: `"Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y. The weather was great!"`
2. Select language: English
3. Select method: spaCy (or Baseline)
4. Click "Segment Sentences"

### API Call
```bash
curl -X POST "http://localhost:8000/segment" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Dr. Smith went to the U.S.A. in 2020. He visited New York, N.Y.",
    "language": "en",
    "method": "spacy"
  }'
```

## Troubleshooting

**Problem:** spaCy models not found
- **Solution:** Run `python -m spacy download en_core_web_sm`

**Problem:** Port 8000 already in use
- **Solution:** Change port in `run_server.py` or use: `uvicorn backend.main:app --port 8001`

**Problem:** Import errors
- **Solution:** Ensure you're in the project root directory and dependencies are installed

## Project Structure

```
NLP/
├── backend/          # FastAPI backend
├── frontend/         # Web interface
├── evaluation/       # Evaluation scripts
├── requirements.txt  # Dependencies
└── README.md        # Full documentation
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Run evaluation to see baseline vs. proposed comparison
3. Try different languages (if models installed)
4. Experiment with your own text samples
