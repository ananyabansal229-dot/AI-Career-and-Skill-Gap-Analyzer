
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_roles():
    path = DATA_DIR / "career_roles.json"
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_opportunities():
    path = DATA_DIR / "opportunities.json"
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)["opportunities"]


SKILL_ALIASES = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "py": "Python",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "node": "Node.js",
    "nodejs": "Node.js",
    "reactjs": "React",
    "react.js": "React",
    "html5": "HTML",
    "css3": "CSS",
    "oop": "OOP",
    "object oriented programming": "OOP",
    "data viz": "Data Visualization",
    "problem-solving": "Problem Solving"
}


def normalize_skill(skill):
    value = skill.strip().lower()
    return SKILL_ALIASES.get(value, value.title())


def extract_skills(text, known_skills=None):
    if not text:
        return []

    if known_skills is None:
        roles = load_roles()
        known_skills = set()

        for role in roles.values():
            known_skills.update(role["skills"].keys())

        known_skills.update([
            "Artificial Intelligence",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "Git",
            "Docker",
            "Linux",
            "Networking",
            "Django",
            "Flask",
            "Scikit-learn",
            "PyTorch",
            "TensorFlow",
            "OOP",
            "Problem Solving",
            "Communication",
            "Excel",
            "Bash"
        ])

    found = set()
    text_lower = text.lower()

    for skill in known_skills:
        pattern = r"(?<![a-z0-9])" + re.escape(
            skill.lower()
        ) + r"(?![a-z0-9])"

        if re.search(pattern, text_lower):
            found.add(normalize_skill(skill))

    return sorted(found)


def analyze_career(
    target_role,
    current_skills,
    interests="",
    job_description=""
):
    roles = load_roles()

    if target_role not in roles:
        raise ValueError("Please select a valid career role.")

    role_data = roles[target_role]

    required_skills = role_data["skills"]

    current = {
        normalize_skill(skill)
        for skill in current_skills
        if skill.strip()
    }

    if job_description.strip():
        job_skills = extract_skills(
            job_description,
            set(required_skills.keys())
        )

        for skill in job_skills:
            current.discard(skill)

        target_skills = set(job_skills)

        # If the job description contains no recognized
        # skills, fall back to the selected career profile.
        if not target_skills:
            target_skills = set(required_skills)
    else:
        target_skills = set(required_skills)

    matched = []
    missing = []

    for skill in sorted(target_skills):
        if skill in current:
            matched.append(skill)
        else:
            missing.append(skill)

    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    missing.sort(
        key=lambda skill: priority_order.get(
            required_skills.get(skill, "medium"),
            2
        )
    )

    total = len(target_skills)

    match_percentage = (
        round(len(matched) / total * 100)
        if total else 0
    )

    roadmap = []

    for index, skill in enumerate(missing, start=1):
        level = required_skills.get(skill, "medium")

        roadmap.append({
            "step": index,
            "skill": skill,
            "priority": level,
            "action": (
                f"Learn {skill} fundamentals and complete "
                f"a practical exercise."
            )
        })

    return {
        "target_role": target_role,
        "industry": role_data["industry"],
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_percentage,
        "roadmap": roadmap,
        "projects": role_data["projects"],
        "languages": role_data["languages"],
        "learning": role_data["learning"],
        "interests": interests
    }


def recommend_opportunities(skills, audience="Student"):
    opportunities = load_opportunities()

    user_skills = {
        normalize_skill(skill)
        for skill in skills
    }

    recommendations = []

    for item in opportunities:
        if audience not in item["audience"]:
            continue

        opportunity_skills = {
            normalize_skill(skill)
            for skill in item["skills"]
        }

        overlap = user_skills.intersection(
            opportunity_skills
        )

        score = len(overlap)

        recommendations.append({
            **item,
            "match_score": score,
            "matched_skills": sorted(overlap)
        })

    return sorted(
        recommendations,
        key=lambda item: item["match_score"],
        reverse=True
    )


def build_founder_roadmap(product_idea):
    return [
        {
            "phase": "01. Problem Discovery",
            "task": "Identify the problem and target audience.",
            "output": "Problem statement and user research"
        },
        {
            "phase": "02. Market Research",
            "task": "Study competitors and validate demand.",
            "output": "Market research document"
        },
        {
            "phase": "03. Product Planning",
            "task": "Define features and build an MVP.",
            "output": "Product requirements and prototype"
        },
        {
            "phase": "04. Development",
            "task": "Develop and test the product.",
            "output": "Working product"
        },
        {
            "phase": "05. Validation",
            "task": "Collect feedback from potential users.",
            "output": "User feedback and improvements"
        },
        {
            "phase": "06. Pitch Preparation",
            "task": "Prepare a pitch deck and business model.",
            "output": "Pitch deck and business plan"
        },
        {
            "phase": "07. Growth",
            "task": "Explore ideathons, accelerators and startup programs.",
            "output": "Applications and networking"
        }
    ]
