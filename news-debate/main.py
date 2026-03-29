import os
import sys

from debate import debate


def _has_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def main() -> int:
    if _has_api_key():
        print("Using OpenAI debate mode.")
    else:
        print("OPENAI_API_KEY not found. Using local mock debate mode.")

    topic = " ".join(sys.argv[1:]).strip()
    if not topic:
        topic = input("Enter a debate topic: ").strip()

    if not topic:
        print("No topic provided.")
        return 1

    try:
        history = debate(topic)
    except RuntimeError as exc:
        print(str(exc))
        return 1

    for side, text in history:
        print(f"\n[{side.upper()}]\n{text}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
