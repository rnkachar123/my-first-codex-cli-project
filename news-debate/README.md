# News Debate (Python)

For a plain-English explanation of the whole app, read `NONCODER_GUIDE.md`.

## Setup

1. Create or activate the virtual environment at the repo root.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: set your OpenAI API key for live model responses:

```bash
export OPENAI_API_KEY='your-key'
```

If no API key is set, the app runs in local mock mode and generates an offline debate.
If you want a template file, copy `.env.example` to `.env` and fill in your key locally.

## Run

```bash
python main.py "Should remote work be mandatory?"
```

## Visualize In Browser

```bash
python web_app.py
```

Then open `http://127.0.0.1:8000`.

## Plain-English Guide

If you want a non-technical explanation of:

- what the app does
- how the UI works
- what `127.0.0.1:8000` means
- what server is running in the background

see `NONCODER_GUIDE.md`.
