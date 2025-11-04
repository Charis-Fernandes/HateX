from flask import Flask, render_template, request, jsonify
import os
import traceback
import random
import re

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
app = Flask(__name__, template_folder="templates")


def fake_predict(text: str):
    """Simple heuristic-based fake detector.

    Returns a tuple (label, confidence) where confidence is between 0.94 and 0.99.
    This intentionally ignores any saved model and uses lightweight patterns.
    """
    t = text.lower()
    # obvious hate indicators (avoid hard-coded slurs; use general patterns)
    patterns = [
        r"\bhate\b",
        r"\bkill\b",
        r"should die",
        r"go back",
        r"can't stand",
        r"cant stand",
        r"get out",
        r"you (are|re) (stupid|idiot|idiots)",
        r"\bdisgusting\b",
        r"\bscum\b",
    ]

    hate = False
    for p in patterns:
        if re.search(p, t):
            hate = True
            break

    # Small heuristic: if message mentions protected groups generically, treat as hate-like
    if not hate and re.search(r"\b(people|they|them)\b", t) and re.search(r"\b(hate|can't stand|dislike)\b", t):
        hate = True

    # Confidence: random in requested range
    conf = round(random.uniform(0.94, 0.99), 4)
    label = "Hate" if hate else "Not Hate"
    return label, conf


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    text = data.get("text") or ""
    if not text.strip():
        return jsonify({"error": "Empty text"}), 400
    try:
        # Use the fake heuristic instead of loading/using a model file
        pred, score = fake_predict(text)
        return jsonify({"prediction": pred, "score": float(score)})
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": "prediction failed", "details": str(e), "trace": tb}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # NOTE: use a production WSGI server for deployment
    # Allow overriding the port and debug via environment variables for flexibility.
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") in ("1", "true", "True")
    # When starting the app in the background (as a job), the default reloader
    # can cause the shell to stop the process because the reloader spawns
    # subprocesses that attempt to access the controlling terminal. To make
    # background starts reliable, disable the reloader here.
    app.run(debug=debug, host="0.0.0.0", port=port, use_reloader=False)
