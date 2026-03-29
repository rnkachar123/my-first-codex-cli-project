import html
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import parse_qs

from summary import summarize_topic


def _render_list(items: list[str]) -> str:
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def render_page(topic: str = "", summary: Optional[dict] = None) -> str:
    safe_topic = html.escape(topic)

    if summary:
        mode_label = "Live OpenAI mode" if summary["mode"] == "openai" else "Local summary mode"
        summary_markup = f"""
        <section class="results">
          <article class="hero-card">
            <div class="section-label">{html.escape(mode_label)}</div>
            <h2>{html.escape(summary["topic"])}</h2>
            <p>{html.escape(summary["overview"])}</p>
          </article>

          <div class="summary-grid">
            <article class="panel">
              <div class="section-label">Key Points</div>
              <ul>{_render_list(summary["key_points"])}</ul>
            </article>
            <article class="panel panel-warm">
              <div class="section-label">Opportunities</div>
              <ul>{_render_list(summary["opportunities"])}</ul>
            </article>
            <article class="panel panel-cool">
              <div class="section-label">Risks</div>
              <ul>{_render_list(summary["risks"])}</ul>
            </article>
            <article class="panel">
              <div class="section-label">Questions To Explore</div>
              <ul>{_render_list(summary["questions"])}</ul>
            </article>
          </div>
        </section>
        """
    else:
        summary_markup = """
        <section class="results">
          <article class="hero-card empty-state">
            <div class="section-label">Topic Summary</div>
            <h2>No summary yet</h2>
            <p>Enter a topic to generate a structured overview with key points, opportunities, risks, and follow-up questions.</p>
          </article>
        </section>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Topic Summary Studio</title>
  <style>
    :root {{
      color-scheme: light;
      --bg-top: #f7f1e3;
      --bg-bottom: #e4edf6;
      --ink: #1b2430;
      --muted: #58606d;
      --line: rgba(27, 36, 48, 0.12);
      --paper: rgba(255, 252, 247, 0.88);
      --accent: #b85c38;
      --accent-deep: #8f3f20;
      --shadow: 0 28px 80px rgba(27, 36, 48, 0.14);
      --title-font: Georgia, "Times New Roman", serif;
      --body-font: "Avenir Next", "Segoe UI", sans-serif;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: var(--body-font);
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(184, 92, 56, 0.18), transparent 24rem),
        radial-gradient(circle at bottom right, rgba(83, 126, 166, 0.18), transparent 30rem),
        linear-gradient(180deg, var(--bg-top), var(--bg-bottom));
      min-height: 100vh;
    }}

    .page {{
      width: min(1100px, calc(100% - 32px));
      margin: 0 auto;
      padding: 28px 0 56px;
    }}

    .masthead {{
      display: grid;
      gap: 20px;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: linear-gradient(145deg, rgba(255, 248, 239, 0.94), rgba(255, 255, 255, 0.74));
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }}

    .section-label {{
      display: inline-flex;
      width: fit-content;
      padding: 7px 12px;
      border-radius: 999px;
      border: 1px solid rgba(184, 92, 56, 0.2);
      background: rgba(184, 92, 56, 0.08);
      color: var(--accent-deep);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    h1, h2 {{
      margin: 0;
      font-family: var(--title-font);
      line-height: 0.98;
    }}

    h1 {{
      font-size: clamp(2.8rem, 7vw, 5.4rem);
      max-width: 11ch;
    }}

    h2 {{
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      margin-top: 14px;
    }}

    .lede {{
      max-width: 62ch;
      margin: 0;
      color: var(--muted);
      font-size: 1.03rem;
      line-height: 1.75;
    }}

    form {{
      display: grid;
      gap: 12px;
    }}

    label {{
      font-size: 0.95rem;
      color: var(--muted);
    }}

    .field-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
    }}

    input[type="text"] {{
      width: 100%;
      min-height: 58px;
      padding: 16px 18px;
      border-radius: 18px;
      border: 1px solid rgba(27, 36, 48, 0.14);
      background: rgba(255, 255, 255, 0.85);
      font: inherit;
      font-size: 1rem;
      color: var(--ink);
    }}

    button {{
      min-height: 58px;
      padding: 0 24px;
      border: none;
      border-radius: 18px;
      background: linear-gradient(135deg, var(--accent), var(--accent-deep));
      color: white;
      font: inherit;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 16px 34px rgba(143, 63, 32, 0.24);
    }}

    .helper {{
      color: var(--muted);
      font-size: 0.94rem;
    }}

    .results {{
      margin-top: 22px;
    }}

    .hero-card,
    .panel {{
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--paper);
      box-shadow: 0 20px 48px rgba(27, 36, 48, 0.1);
    }}

    .hero-card {{
      padding: 28px;
    }}

    .hero-card p,
    li {{
      line-height: 1.7;
    }}

    .summary-grid {{
      display: grid;
      gap: 18px;
      margin-top: 18px;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }}

    .panel {{
      padding: 22px;
      background: rgba(255, 253, 248, 0.88);
    }}

    .panel-warm {{
      background: linear-gradient(180deg, rgba(246, 220, 199, 0.84), rgba(255, 250, 244, 0.92));
    }}

    .panel-cool {{
      background: linear-gradient(180deg, rgba(214, 230, 242, 0.9), rgba(249, 252, 255, 0.96));
    }}

    ul {{
      margin: 16px 0 0;
      padding-left: 18px;
    }}

    li + li {{
      margin-top: 12px;
    }}

    .empty-state {{
      background: linear-gradient(180deg, rgba(255, 251, 245, 0.9), rgba(249, 252, 255, 0.9));
    }}

    .footer {{
      margin-top: 16px;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    @media (max-width: 720px) {{
      .page {{
        width: min(100% - 20px, 1100px);
        padding-top: 18px;
      }}

      .masthead,
      .hero-card,
      .panel {{
        padding: 20px;
      }}

      .field-row {{
        grid-template-columns: 1fr;
      }}

      button {{
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="masthead">
      <div class="section-label">Browser App</div>
      <h1>Generate a sharp summary for any topic.</h1>
      <p class="lede">
        Enter a topic or question and the app will build a structured summary with an overview,
        key points, opportunities, risks, and next-step questions. It runs locally and uses a live
        OpenAI response only when an API key is configured.
      </p>
      <form method="post">
        <label for="topic">Topic</label>
        <div class="field-row">
          <input
            id="topic"
            type="text"
            name="topic"
            placeholder="Should AI tools be used in classrooms?"
            value="{safe_topic}"
            required
          >
          <button type="submit">Generate Summary</button>
        </div>
        <div class="helper">Examples: AI in classrooms · Universal basic income · Nuclear energy expansion</div>
      </form>
    </section>
    {summary_markup}
    <p class="footer">Runs locally at 127.0.0.1:8000.</p>
  </main>
</body>
</html>
"""


class SummaryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._send_html(render_page())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(raw_body)
        topic = form.get("topic", [""])[0].strip()
        summary = summarize_topic(topic) if topic else None
        self._send_html(render_page(topic, summary))

    def log_message(self, format, *args):
        return

    def _send_html(self, body: str):
        payload = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> int:
    server = HTTPServer(("127.0.0.1", 8000), SummaryHandler)
    print("Open http://127.0.0.1:8000 to view the topic summary app.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
