import html
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from debate import debate


def render_page(topic: str = "", history=None) -> str:
    safe_topic = html.escape(topic)
    cards = ""

    if history:
        rendered = []
        for index, (side, text) in enumerate(history, start=1):
            label = "For" if side == "pro" else "Against"
            css_class = "card-pro" if side == "pro" else "card-con"
            rendered.append(
                f"""
                <article class="card {css_class}">
                    <div class="meta">Round {index} · {label}</div>
                    <p>{html.escape(text)}</p>
                </article>
                """
            )
        cards = "\n".join(rendered)
    else:
        cards = """
        <article class="empty-state">
            <p>Enter a topic to generate a local debate view.</p>
        </article>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>News Debate</title>
  <style>
    :root {{
      --bg: #f5efe6;
      --surface: rgba(255, 252, 247, 0.88);
      --text: #1f2933;
      --muted: #52606d;
      --pro: #1f7a5a;
      --con: #a23e2f;
      --accent: #f0b429;
      --border: rgba(31, 41, 51, 0.12);
      --shadow: 0 20px 50px rgba(31, 41, 51, 0.12);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(240, 180, 41, 0.25), transparent 35%),
        radial-gradient(circle at bottom right, rgba(31, 122, 90, 0.18), transparent 35%),
        linear-gradient(135deg, #f7f1e8, #ece3d4);
      min-height: 100vh;
    }}

    .page {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 20px 56px;
    }}

    .hero {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 28px;
      box-shadow: var(--shadow);
      padding: 32px;
      backdrop-filter: blur(8px);
    }}

    h1 {{
      margin: 0 0 12px;
      font-size: clamp(2.2rem, 5vw, 4.6rem);
      line-height: 0.95;
      letter-spacing: -0.03em;
    }}

    .lead {{
      margin: 0 0 24px;
      max-width: 48rem;
      color: var(--muted);
      font-size: 1.05rem;
      line-height: 1.6;
    }}

    form {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
    }}

    input {{
      width: 100%;
      padding: 16px 18px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.92);
      font: inherit;
      font-size: 1rem;
    }}

    button {{
      border: 0;
      border-radius: 16px;
      background: linear-gradient(135deg, #1f7a5a, #155d46);
      color: white;
      font: inherit;
      font-weight: 600;
      padding: 16px 22px;
      cursor: pointer;
    }}

    .topic {{
      margin: 28px 0 16px;
      color: var(--muted);
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .cards {{
      display: grid;
      gap: 14px;
      margin-top: 18px;
    }}

    .card,
    .empty-state {{
      background: rgba(255, 255, 255, 0.82);
      border: 1px solid var(--border);
      border-radius: 22px;
      box-shadow: var(--shadow);
      padding: 22px;
    }}

    .card-pro {{
      border-left: 8px solid var(--pro);
    }}

    .card-con {{
      border-left: 8px solid var(--con);
    }}

    .meta {{
      color: var(--muted);
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}

    .card p,
    .empty-state p {{
      margin: 0;
      font-size: 1.04rem;
      line-height: 1.7;
    }}

    .footer {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 0.92rem;
    }}

    @media (max-width: 720px) {{
      .page {{
        padding-top: 28px;
      }}

      .hero {{
        padding: 22px;
        border-radius: 22px;
      }}

      form {{
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
    <section class="hero">
      <h1>Debate a headline in local mock mode.</h1>
      <p class="lead">
        Type a topic and this app will generate a reasoned offline debate with alternating
        supporting and opposing arguments plus closing rebuttals.
      </p>
      <form method="post">
        <input
          type="text"
          name="topic"
          placeholder="Should AI tools be used in classrooms?"
          value="{safe_topic}"
          required
        >
        <button type="submit">Generate Debate</button>
      </form>
      <div class="topic">Current topic: {safe_topic or "None yet"}</div>
      <section class="cards">
        {cards}
      </section>
      <p class="footer">Local mode runs without `OPENAI_API_KEY` and keeps the existing CLI intact.</p>
    </section>
  </main>
</body>
</html>
"""


class DebateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._send_html(render_page())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(raw_body)
        topic = form.get("topic", [""])[0].strip()
        history = debate(topic) if topic else None
        self._send_html(render_page(topic, history))

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
    server = HTTPServer(("127.0.0.1", 8000), DebateHandler)
    print("Open http://127.0.0.1:8000 to view the debate app.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
