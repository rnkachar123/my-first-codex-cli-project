# Quick Topic Summarizer: Plain-English Guide

## What this app does

This app lets you type any topic (for example, `Artificial intelligence in healthcare`) and instantly get a short, readable summary.

Think of it as a simple “quick explain” tool in your browser.

## How to use it

Run:

```bash
python web_app.py
```

Then open:

`http://127.0.0.1:8000`

On the page:

1. Type a topic.
2. Click **Summarize**.
3. Read the generated quick summary.

## What “local mock mode” means

The app supports two modes:

- **OpenAI mode**: if `OPENAI_API_KEY` is set, the app requests a model-generated summary.
- **Local mock mode**: if no API key is set, the app still works using local Python summary logic.

So even without a key, you can still use and demo the app.

## What `127.0.0.1:8000` means

- `127.0.0.1` means your own computer (localhost).
- `8000` is a local port (a numbered doorway).

This is not a public website on the internet.

## What server is running

When you run `python web_app.py`, Python starts a small built-in web server (`HTTPServer`).

That server:

1. serves the web page,
2. receives your topic submission,
3. generates a summary,
4. returns the updated page.

## Main files

- `web_app.py`: browser UI + web server logic
- `summarize.py`: summary generation logic (OpenAI or local fallback)
- `README.md`: setup and run instructions

## One-sentence explanation

This is a local browser app that asks for a topic and returns a quick summary, using OpenAI if available and local fallback logic if not.
