import os
import re


DEFAULT_DOMAIN = {
    "name": "general decision-making",
    "drivers": ("clarity", "feasibility", "long-term value"),
    "opportunities": (
        "reduce confusion about the core tradeoffs",
        "help people compare approaches more consistently",
        "turn a vague idea into a more actionable plan",
    ),
    "risks": (
        "overlook important edge cases",
        "treat context-specific issues as universal",
        "sound more certain than the evidence supports",
    ),
    "questions": (
        "Who is most affected if this goes well or badly?",
        "What constraints would make the topic harder in practice?",
        "What evidence would meaningfully change the conclusion?",
    ),
}

DOMAIN_PROFILES = {
    "education": {
        "keywords": ("school", "student", "classroom", "teacher", "education", "college", "homework"),
        "name": "education",
        "drivers": ("learning outcomes", "access", "instructional quality"),
        "opportunities": (
            "support teachers with clearer priorities and tools",
            "improve student access to guidance or resources",
            "create more consistent classroom experiences",
        ),
        "risks": (
            "weaken deep learning if convenience replaces understanding",
            "increase inequity between students with different support systems",
            "create trust problems around grading or accountability",
        ),
        "questions": (
            "How would this change student behavior over time?",
            "What safeguards would teachers need to use it well?",
            "How would schools evaluate whether it is actually helping?",
        ),
    },
    "work": {
        "keywords": ("work", "office", "employee", "job", "workplace", "remote", "manager"),
        "name": "work and management",
        "drivers": ("productivity", "coordination", "employee experience"),
        "opportunities": (
            "remove friction from routine work",
            "expand flexibility or recruiting options",
            "make team expectations easier to communicate",
        ),
        "risks": (
            "hurt collaboration if workflows are not redesigned carefully",
            "blur accountability when ownership is unclear",
            "create uneven outcomes across roles or teams",
        ),
        "questions": (
            "Which parts of the work benefit most from this change?",
            "What metrics would show whether performance improved?",
            "How would managers handle exceptions fairly?",
        ),
    },
    "technology": {
        "keywords": ("ai", "technology", "software", "app", "automation", "algorithm", "robot"),
        "name": "technology adoption",
        "drivers": ("speed", "reliability", "human oversight"),
        "opportunities": (
            "scale useful capabilities to more people",
            "save time on repetitive or low-leverage tasks",
            "unlock new ways to analyze or deliver services",
        ),
        "risks": (
            "spread mistakes quickly if quality controls are weak",
            "hide important decisions inside opaque systems",
            "reduce human judgment in cases that need nuance",
        ),
        "questions": (
            "What failure modes matter most here?",
            "Where should humans stay directly responsible?",
            "What evidence would justify broader rollout?",
        ),
    },
    "health": {
        "keywords": ("health", "medical", "doctor", "hospital", "medicine", "mental health", "vaccine"),
        "name": "health policy",
        "drivers": ("access", "safety", "clinical practicality"),
        "opportunities": (
            "improve access to care or earlier intervention",
            "reduce administrative strain on care teams",
            "focus attention on prevention or continuity of care",
        ),
        "risks": (
            "flatten complex medical decisions into simplistic rules",
            "introduce trust issues if tradeoffs are not explained clearly",
            "produce uneven outcomes across patient groups",
        ),
        "questions": (
            "Which patients benefit most and which face more risk?",
            "How would clinicians override the system when needed?",
            "What evidence standard is appropriate before expansion?",
        ),
    },
    "environment": {
        "keywords": ("climate", "carbon", "energy", "environment", "pollution", "electric", "green"),
        "name": "environmental policy",
        "drivers": ("sustainability", "cost", "transition realism"),
        "opportunities": (
            "reduce long-term environmental damage",
            "encourage investment in cleaner infrastructure",
            "lower future adaptation costs if adopted early enough",
        ),
        "risks": (
            "raise near-term costs before alternatives are ready",
            "shift burdens unevenly across households or industries",
            "trigger backlash if the rollout feels disconnected from reality",
        ),
        "questions": (
            "Who pays first and who benefits later?",
            "What infrastructure has to exist for this to work well?",
            "How should policymakers balance speed against disruption?",
        ),
    },
    "economy": {
        "keywords": ("economy", "inflation", "interest rate", "jobs", "market", "tax", "gdp"),
        "name": "economic policy",
        "drivers": ("household impact", "market stability", "long-term growth"),
        "opportunities": (
            "improve planning confidence for families and businesses",
            "direct resources toward high-impact sectors",
            "balance short-term relief with long-term resilience",
        ),
        "risks": (
            "produce uneven outcomes across income groups",
            "trade long-term stability for short-term gains",
            "increase uncertainty if policy signals are inconsistent",
        ),
        "questions": (
            "Which groups feel the first-order effects most strongly?",
            "What tradeoffs emerge over one, three, and five years?",
            "How will decision-makers adjust if conditions change quickly?",
        ),
    },
}


def _has_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def _get_client():
    from openai import OpenAI

    return OpenAI()


def _normalize_topic(topic: str) -> str:
    normalized = re.sub(r"\s+", " ", topic).strip()
    return normalized or "Untitled topic"


def _detect_domain(topic: str) -> dict:
    lowered = topic.lower()
    best_profile = DEFAULT_DOMAIN
    best_score = 0

    for profile in DOMAIN_PROFILES.values():
        score = sum(1 for keyword in profile["keywords"] if keyword in lowered)
        if score > best_score:
            best_profile = profile
            best_score = score

    return best_profile


def _topic_label(topic: str) -> str:
    return topic.strip().rstrip("?.!")


def _build_overview(topic: str, domain: dict) -> str:
    label = _topic_label(topic)
    driver_a, driver_b, driver_c = domain["drivers"]
    return (
        f"{label} sits mainly in the {domain['name']} space. A useful summary starts by treating it as a question "
        f"about {driver_a}, {driver_b}, and {driver_c} rather than as a purely abstract opinion. The strongest "
        f"interpretation is usually that people are trying to decide whether the idea is practical, who benefits, "
        f"and what tradeoffs appear once it moves beyond a simple headline."
    )


def _build_key_points(topic: str, domain: dict) -> list[str]:
    label = _topic_label(topic)
    return [
        f"The topic is easier to evaluate when {label.lower()} is translated into a concrete policy, tool, or behavior change.",
        f"The strongest arguments usually depend on whether expected gains in {domain['drivers'][0]} show up in real conditions, not just in theory.",
        "Disagreement usually comes from different assumptions about who bears the cost, how exceptions are handled, and what counts as success.",
    ]


def _build_takeaway(topic: str, opportunities: list[str], risks: list[str]) -> str:
    label = _topic_label(topic)
    return (
        f"A balanced read of {label.lower()} is to pursue {opportunities[0].lower()} while explicitly guarding "
        f"against {risks[0].lower()}."
    )


def _mock_summary(topic: str) -> dict:
    clean_topic = _normalize_topic(topic)
    domain = _detect_domain(clean_topic)
    opportunities = list(domain["opportunities"])
    risks = list(domain["risks"])
    return {
        "topic": clean_topic,
        "mode": "local",
        "overview": _build_overview(clean_topic, domain),
        "key_points": _build_key_points(clean_topic, domain),
        "opportunities": opportunities,
        "risks": risks,
        "questions": list(domain["questions"]),
        "takeaway": _build_takeaway(clean_topic, opportunities, risks),
    }


def _split_lines(text: str, expected: int) -> list[str]:
    lines = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
    return lines[:expected]


def _ensure_items(items: list[str], expected: int, fallback: list[str]) -> list[str]:
    cleaned = []
    seen = set()
    for item in items:
        normalized = re.sub(r"\s+", " ", item).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        cleaned.append(normalized)
        seen.add(key)
        if len(cleaned) == expected:
            return cleaned

    for fallback_item in fallback:
        key = fallback_item.lower()
        if key in seen:
            continue
        cleaned.append(fallback_item)
        seen.add(key)
        if len(cleaned) == expected:
            return cleaned

    return cleaned[:expected]


def _openai_summary(topic: str) -> dict:
    client = _get_client()
    response = client.responses.create(
        model="gpt-5",
        input=(
            "Create a concise structured topic summary.\n"
            f"Topic: {topic}\n\n"
            "Return plain text in exactly this format:\n"
            "OVERVIEW: one paragraph\n"
            "KEY POINTS:\n"
            "- item\n"
            "- item\n"
            "- item\n"
            "OPPORTUNITIES:\n"
            "- item\n"
            "- item\n"
            "- item\n"
            "RISKS:\n"
            "- item\n"
            "- item\n"
            "- item\n"
            "QUESTIONS:\n"
            "- item\n"
            "- item\n"
            "- item"
        ),
    )
    output = response.output_text

    sections = {"OVERVIEW": "", "KEY POINTS": "", "OPPORTUNITIES": "", "RISKS": "", "QUESTIONS": ""}
    current = None
    buffer = []

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if line in {"### KEY POINTS", "### OPPORTUNITIES", "### RISKS", "### QUESTIONS"}:
            line = f"{line.replace('### ', '')}:"
        if line.startswith("OVERVIEW:"):
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = "OVERVIEW"
            buffer = [line.split(":", 1)[1].strip()]
            continue
        if line in {"KEY POINTS:", "OPPORTUNITIES:", "RISKS:", "QUESTIONS:"}:
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = line.rstrip(":")
            buffer = []
            continue
        if current:
            buffer.append(line)

    if current:
        sections[current] = "\n".join(buffer).strip()

    fallback = _mock_summary(topic)
    key_points = _ensure_items(_split_lines(sections["KEY POINTS"], 5), 3, fallback["key_points"])
    opportunities = _ensure_items(_split_lines(sections["OPPORTUNITIES"], 5), 3, fallback["opportunities"])
    risks = _ensure_items(_split_lines(sections["RISKS"], 5), 3, fallback["risks"])
    questions = _ensure_items(_split_lines(sections["QUESTIONS"], 5), 3, fallback["questions"])
    return {
        "topic": _normalize_topic(topic),
        "mode": "openai",
        "overview": sections["OVERVIEW"] or fallback["overview"],
        "key_points": key_points,
        "opportunities": opportunities,
        "risks": risks,
        "questions": questions,
        "takeaway": _build_takeaway(topic, opportunities, risks),
    }


def summarize_topic(topic: str) -> dict:
    if _has_api_key():
        return _openai_summary(topic)

    return _mock_summary(topic)
