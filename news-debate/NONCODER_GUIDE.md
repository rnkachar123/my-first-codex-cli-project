# Topic Summary Browser App: Plain-English Guide

## What this app does

This app lets you type in a topic, such as:

- `Should AI tools be used in classrooms?`
- `Should remote work be mandatory?`

It then creates a short summary with:

- an overview
- key points
- opportunities
- risks
- follow-up questions

Think of it as a simple topic briefing tool.

## Two ways to use it

### 1. Terminal version

This is the text-only version.

You run:

```bash
python main.py
```

Then the app asks for a topic and prints the original debate output in the terminal window.

### 2. Browser version

This is the visual version.

You run:

```bash
python web_app.py
```

Then you open this address in your browser:

`http://127.0.0.1:8000`

This version gives you a page with a text box, a button, and styled summary panels.

## What the page is showing

The browser version has a few simple parts:

- A title at the top that explains the app.
- A short description telling you it runs locally.
- A text box where you type the topic.
- A `Generate Summary` button that sends your topic to the app.
- A structured result area underneath.

The result area shows:

- one overview paragraph
- a list of key points
- a list of opportunities
- a list of risks
- a list of follow-up questions

## What “local summary mode” means

This app can work in two different ways:

### OpenAI mode

If you have a real OpenAI API key, the app can send requests to OpenAI and get model-generated responses.

### Local summary mode

If you do not have an API key, the app still works offline.

In local summary mode:

- nothing is sent to OpenAI
- no internet connection is required for the summary engine
- the app generates a structured summary using local Python code

## What `127.0.0.1:8000` means

This address looks technical, but it is simple once broken down:

- `127.0.0.1` means “this same computer”
- it is also called `localhost`
- it does **not** mean a public website on the internet
- only someone on your machine can open it

The `:8000` part is the port number.

A port is just a numbered doorway that lets one program talk to another on the same computer.

So:

- `127.0.0.1` = your own machine
- `8000` = the specific doorway used by this app

## What server was running

When you started the browser version with:

```bash
python web_app.py
```

Python launched a small built-in web server called `HTTPServer`.

That server does three important jobs:

1. It keeps listening for browser requests.
2. It sends the web page to the browser.
3. It receives the topic you typed and generates the summary.

This is the process that “keeps the app open.”

## How the app works behind the scenes

Here is the browser app in very simple steps:

1. You open the page in the browser.
2. The browser talks to the local Python server.
3. You enter a topic and press the button.
4. The server sends that topic into the summary engine.
5. The summary engine creates the overview and lists.
6. The server builds a new HTML page with those results.
7. The browser displays the formatted summary panels.

## Main files in the project

These are the most important files:

- `main.py`
  - runs the original terminal debate version
- `web_app.py`
  - runs the browser version and local web server
- `summary.py`
  - creates the structured topic summary
- `debate.py`
  - keeps the earlier terminal debate flow intact
- `README.md`
  - quick setup and run instructions

## If you want to explain it in one sentence

This is a local browser app that runs on your own computer and turns any topic into a readable structured summary using a small Python server.
