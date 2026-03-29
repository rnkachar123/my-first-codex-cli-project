# Quick Topic Summarizer (Python)

For a plain-English explanation of the app behavior, see `NONCODER_GUIDE.md`.

## Setup

1. Create or activate the virtual environment at the repo root.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: set your OpenAI API key for live summaries:

```bash
export OPENAI_API_KEY='your-key'
```

If no API key is set, the app runs in local mock mode and generates an offline summary.

## Run (Browser App)

```bash
python web_app.py
```

Then open `http://127.0.0.1:8000`.

## How it works

- Enter a topic in the form.
- Click **Summarize**.
- The app returns a quick, readable summary.
- With `OPENAI_API_KEY`, it calls the OpenAI API for a model-generated summary.
- Without the key, it uses local deterministic summary logic.
