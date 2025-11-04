# HateX
# Twitter Hate Speech Detector

Simple Flask app that loads a trained model from `model.pkl` and exposes a small web UI for single-text predictions.

Setup
1. Place your trained model file as `model.pkl` in the project root. The model should be a scikit-learn estimator or a pipeline that accepts raw text (a typical pipeline: [vectorizer, classifier]). It should be serialised with `joblib.dump` or `pickle`.
2. Create a virtualenv and install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run

```
python app.py
```

Open http://localhost:5000 and paste a tweet to analyze.

Notes
- If your model expects preprocessed input, wrap that preprocessing in a pipeline before saving so the server can pass raw text.
- This app uses Flask's dev server. For production use, put it behind Gunicorn or another WSGI server.
