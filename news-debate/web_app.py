import html
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from summarize import summarize_topic


def render_page(topic: str = "", summary: str = "") -> str:
    safe_topic = html.escape(topic)

    if summary:
        content = f"""
        <article class=\"summary-card\">
          <h2>Quick Summary</h2>
          <p>{html.escape(summary)}</p>
        </article>
        """
    else:
        content = """
        <article class=\"empty-state\">
          <p>Enter a topic to generate a quick summary.</p>
        </article>
        """

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Quick Topic Summarizer</title>
  <style>
    :root {{
      --bg: #eef3ff;
      --surface: rgba(255, 255, 255, 0.9);
      --text: #1f2933;
      --muted: #52606d;
      --accent: #4458d8;
      --border: rgba(31, 41, 51, 0.15);
      --shadow: 0 18px 45px rgba(31, 41, 51, 0.12);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: Inter, Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(68, 88, 216, 0.2), transparent 35%),
        radial-gradient(circle at bottom right, rgba(45, 160, 190, 0.2), transparent 35%),
        linear-gradient(135deg, #f4f7ff, #eaf3ff);
      min-height: 100vh;
    }}

    .page {{
      max-width: 860px;
      margin: 0 auto;
      padding: 48px 20px 56px;
    }}

    .panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 28px;
    }}

    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 4.5vw, 3.2rem);
      line-height: 1.05;
    }}

    .lead {{
      margin: 0 0 22px;
      color: var(--muted);
      line-height: 1.55;
      max-width: 45rem;
    }}

    form {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
    }}

    input {{
      width: 100%;
      padding: 14px 16px;
      border-radius: 12px;
      border: 1px solid var(--border);
      font: inherit;
      font-size: 1rem;
    }}

    button {{
      border: 0;
      border-radius: 12px;
      background: linear-gradient(135deg, #4458d8, #3247c3);
      color: #fff;
      font: inherit;
      font-weight: 600;
      padding: 14px 18px;
      cursor: pointer;
    }}

    .topic {{
      margin: 22px 0 14px;
      color: var(--muted);
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .summary-card,
    .empty-state {{
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: var(--shadow);
      padding: 20px;
    }}

    .summary-card h2 {{
      margin: 0 0 10px;
      font-size: 1.2rem;
    }}

    .summary-card p,
    .empty-state p {{
      margin: 0;
      line-height: 1.65;
    }}

    .footer {{
      margin-top: 16px;
      color: var(--muted);
      font-size: 0.92rem;
    }}

    @media (max-width: 700px) {{
      .page {{ padding-top: 26px; }}
      .panel {{ padding: 20px; }}
      form {{ grid-template-columns: 1fr; }}
      button {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <main class=\"page\">
    <section class=\"panel\">
      <h1>Generate a quick topic summary.</h1>
      <p class=\"lead\">
        Enter any topic and this browser app creates a concise summary you can read in seconds.
      </p>
      <form method=\"post\">
        <input
          type=\"text\"
          name=\"topic\"
          placeholder=\"Artificial intelligence in healthcare\"
          value=\"{safe_topic}\"
          required
        >
        <button type=\"submit\">Summarize</button>
      </form>
      <div class=\"topic\">Current topic: {safe_topic or "None yet"}</div>
      {content}
      <p class=\"footer\">Uses OpenAI when <code>OPENAI_API_KEY</code> is set; otherwise uses local mock mode.</p>
    </section>
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
        summary = summarize_topic(topic) if topic else ""
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
    print("Open http://127.0.0.1:8000 to view the quick summary app.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
