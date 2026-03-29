import os
import re


def _has_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def _get_client():
    from openai import OpenAI

    return OpenAI()


def _normalize_topic(topic: str) -> str:
    return re.sub(r"\s+", " ", topic).strip()


def _detect_category(topic: str) -> str:
    lowered = topic.lower()

    categories = {
        "technology": ("ai", "software", "app", "automation", "tech", "algorithm"),
        "business": ("business", "company", "startup", "market", "finance", "sales"),
        "health": ("health", "medical", "doctor", "hospital", "medicine", "wellness"),
        "education": ("school", "student", "teacher", "classroom", "learning", "college"),
        "environment": ("climate", "environment", "energy", "carbon", "green", "pollution"),
    }

    for category, keywords in categories.items():
        if any(keyword in lowered for keyword in keywords):
            return category

    return "general"


def _mock_summary(topic: str) -> str:
    clean_topic = _normalize_topic(topic)
    category = _detect_category(clean_topic)

    focus_by_category = {
        "technology": "how it improves speed and access while introducing reliability and oversight concerns",
        "business": "tradeoffs between growth opportunities, cost pressures, and execution risks",
        "health": "potential public benefits, individual outcomes, and safety considerations",
        "education": "effects on learning quality, fairness, and classroom implementation",
        "environment": "long-term sustainability gains versus near-term transition costs",
        "general": "the main benefits, risks, and practical considerations people should evaluate",
    }

    return (
        f"Quick summary: {clean_topic} is an important {category} topic. "
        f"Most discussions focus on {focus_by_category[category]}. "
        "A balanced view is to start with clear goals, measure outcomes over time, "
        "and adjust the approach as real-world evidence appears."
    )


def _openai_summary(topic: str) -> str:
    client = _get_client()
    response = client.responses.create(
        model="gpt-5",
        input=(
            "Provide a concise, neutral summary in 3-4 sentences for the topic below. "
            "Highlight the main idea, key benefits, and key concerns.\n\n"
            f"Topic: {topic}"
        ),
    )
    return response.output_text.strip()


def summarize_topic(topic: str) -> str:
    if _has_api_key():
        return _openai_summary(topic)

    return _mock_summary(topic)
