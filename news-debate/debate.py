# debate.py
import os
import re


DEFAULT_DOMAIN = {
    "name": "public policy",
    "pro_values": ("efficiency", "access", "long-term planning"),
    "con_values": ("fairness", "local context", "unintended consequences"),
    "stakeholders": ("the public", "institutions", "people directly affected"),
    "pro_effects": (
        "set clearer expectations",
        "make coordination easier",
        "improve outcomes over time",
    ),
    "con_effects": (
        "reduce flexibility",
        "shift costs onto vulnerable groups",
        "create implementation problems",
    ),
}

DOMAIN_PROFILES = {
    "education": {
        "keywords": ("school", "student", "classroom", "teacher", "education", "college", "homework"),
        "name": "education",
        "pro_values": ("learning support", "teacher productivity", "broader access"),
        "con_values": ("critical thinking", "equity", "academic integrity"),
        "stakeholders": ("students", "teachers", "families"),
        "pro_effects": (
            "free teachers to spend more time on coaching",
            "give students faster feedback",
            "expand access to tutoring-like support",
        ),
        "con_effects": (
            "weaken deep learning habits",
            "widen gaps between well-supported and under-supported students",
            "make evaluation less trustworthy",
        ),
    },
    "work": {
        "keywords": ("work", "office", "employee", "job", "workplace", "remote", "manager"),
        "name": "work and management",
        "pro_values": ("productivity", "flexibility", "talent access"),
        "con_values": ("coordination", "culture", "accountability"),
        "stakeholders": ("employees", "managers", "customers"),
        "pro_effects": (
            "reduce avoidable friction in daily work",
            "help organizations recruit more broadly",
            "let teams focus on outputs rather than routine",
        ),
        "con_effects": (
            "make collaboration harder to sustain",
            "blur responsibility when problems appear",
            "hurt onboarding and informal learning",
        ),
    },
    "technology": {
        "keywords": ("ai", "technology", "software", "app", "automation", "algorithm", "robot"),
        "name": "technology adoption",
        "pro_values": ("speed", "scalability", "innovation"),
        "con_values": ("safety", "reliability", "human judgment"),
        "stakeholders": ("users", "builders", "affected communities"),
        "pro_effects": (
            "help people handle repetitive tasks faster",
            "scale useful services to more users",
            "unlock new forms of problem-solving",
        ),
        "con_effects": (
            "introduce errors at scale",
            "make systems harder to question once deployed",
            "displace judgment in situations that need nuance",
        ),
    },
    "health": {
        "keywords": ("health", "medical", "doctor", "hospital", "medicine", "mental health", "vaccine"),
        "name": "health policy",
        "pro_values": ("prevention", "access", "public benefit"),
        "con_values": ("consent", "risk management", "individual variation"),
        "stakeholders": ("patients", "clinicians", "public health systems"),
        "pro_effects": (
            "expand access to care",
            "improve early intervention",
            "reduce pressure on overstretched systems",
        ),
        "con_effects": (
            "oversimplify complex clinical decisions",
            "create trust problems when tradeoffs are hidden",
            "affect people differently across settings",
        ),
    },
    "environment": {
        "keywords": ("climate", "carbon", "energy", "environment", "pollution", "electric", "green"),
        "name": "environmental policy",
        "pro_values": ("sustainability", "resilience", "future cost reduction"),
        "con_values": ("affordability", "transition risk", "implementation realism"),
        "stakeholders": ("households", "businesses", "future generations"),
        "pro_effects": (
            "reduce long-run environmental damage",
            "encourage investment in cleaner systems",
            "lower the future cost of adaptation",
        ),
        "con_effects": (
            "raise near-term costs for households",
            "move faster than infrastructure can support",
            "create backlash if burdens are unevenly shared",
        ),
    },
}

PRO_LENSES = (
    "practical impact",
    "institutional benefits",
    "long-term upside",
)

CON_LENSES = (
    "implementation risk",
    "fairness concerns",
    "second-order effects",
)


def _has_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def _get_client():
    from openai import OpenAI

    return OpenAI()


def _normalize_topic(topic: str) -> str:
    return re.sub(r"\s+", " ", topic).strip()


def _base_subject(topic: str) -> str:
    lowered = topic.strip().rstrip("?.!")
    prefixes = ("should ", "must ", "is ", "are ", "do ", "does ", "can ")
    for prefix in prefixes:
        if lowered.lower().startswith(prefix):
            lowered = lowered[len(prefix):]
            break
    return lowered or topic


def _position_phrase(topic: str) -> str:
    stripped = topic.strip().rstrip("?.!")

    match = re.match(r"^should (.+?) be used in (.+)$", stripped, re.IGNORECASE)
    if match:
        return f"using {match.group(1)} in {match.group(2)}"

    match = re.match(r"^should (.+?) be required$", stripped, re.IGNORECASE)
    if match:
        return f"requiring {match.group(1)}"

    match = re.match(r"^should (.+?) be mandatory$", stripped, re.IGNORECASE)
    if match:
        return f"making {match.group(1)} mandatory"

    match = re.match(r"^should (.+)$", stripped, re.IGNORECASE)
    if match:
        return f"adopting {match.group(1)}"

    match = re.match(r"^can (.+?) be used in (.+)$", stripped, re.IGNORECASE)
    if match:
        return f"using {match.group(1)} in {match.group(2)}"

    return f"pursuing {stripped}"


def _with_article(phrase: str) -> str:
    article = "an" if phrase[0].lower() in "aeiou" else "a"
    return f"{article} {phrase}"


def _detect_domain(topic: str):
    lowered = topic.lower()
    best_profile = DEFAULT_DOMAIN
    best_score = 0

    for profile in DOMAIN_PROFILES.values():
        score = sum(1 for keyword in profile["keywords"] if keyword in lowered)
        if score > best_score:
            best_profile = profile
            best_score = score

    return best_profile


def _build_pro_argument(topic: str, domain: dict, round_index: int) -> str:
    position = _position_phrase(topic)
    value = domain["pro_values"][round_index]
    effect = domain["pro_effects"][round_index]
    stakeholder = domain["stakeholders"][round_index]
    lens = PRO_LENSES[round_index]

    return (
        f"From {_with_article(lens)} perspective, the best case for {position} is that it can "
        f"{effect}. That matters because {stakeholder} usually benefit when decisions are built "
        f"around {value} rather than inertia. Even if the change is imperfect at first, supporters "
        f"would argue that clear adoption creates a foundation for learning, iteration, and better "
        f"results over time."
    )


def _build_con_argument(topic: str, domain: dict, round_index: int) -> str:
    position = _position_phrase(topic)
    value = domain["con_values"][round_index]
    effect = domain["con_effects"][round_index]
    stakeholder = domain["stakeholders"][round_index]
    lens = CON_LENSES[round_index]

    return (
        f"From {_with_article(lens)} perspective, the strongest objection to {position} is that it could "
        f"{effect}. Opponents would say the real issue is not whether the idea sounds promising, but "
        f"whether it respects {value} once real constraints appear. If the burden falls hardest on "
        f"{stakeholder}, then a policy that looks sensible in theory may still be the wrong choice in practice."
    )


def _build_rebuttal(topic: str, domain: dict, side: str) -> str:
    position = _position_phrase(topic)
    pro_value = domain["pro_values"][0]
    con_value = domain["con_values"][0]

    if side == "pro":
        return (
            f"Supporters of {position} would answer that the risks are manageable if leaders phase the change in, "
            f"measure results openly, and keep humans responsible for edge cases. In that view, concerns about "
            f"{con_value} are real, but they are reasons to design better safeguards, not reasons to reject the idea outright."
        )

    return (
        f"Critics of {position} would answer that promised gains in {pro_value} often look stronger in pilots than in wide deployment. "
        f"They would argue that once incentives, budgets, and uneven execution enter the picture, the tradeoffs become harder than advocates admit."
    )


def _mock_debate(topic: str):
    clean_topic = _normalize_topic(topic)
    domain = _detect_domain(clean_topic)

    history = []
    for round_index in range(3):
        history.append(("pro", _build_pro_argument(clean_topic, domain, round_index)))
        history.append(("con", _build_con_argument(clean_topic, domain, round_index)))

    history.append(("pro", _build_rebuttal(clean_topic, domain, "pro")))
    history.append(("con", _build_rebuttal(clean_topic, domain, "con")))
    return history


def _openai_debate(topic):
    client = _get_client()
    history = []

    prompt = f"Topic: {topic}\n\nTake a strong position FOR this."

    for _ in range(3):
        response = client.responses.create(model="gpt-5", input=prompt)
        argument = response.output_text
        history.append(("pro", argument))

        prompt = f"""
        Topic: {topic}
        Here is an argument FOR:
        {argument}

        Now provide a strong COUNTER-ARGUMENT.
        """

        response = client.responses.create(model="gpt-5", input=prompt)
        counter = response.output_text
        history.append(("con", counter))

        prompt = f"""
        Topic: {topic}

        Refine both sides:

        PRO:
        {argument}

        CON:
        {counter}

        Improve both arguments.
        """

    return history


def debate(topic):
    if _has_api_key():
        return _openai_debate(topic)

    return _mock_debate(topic)
