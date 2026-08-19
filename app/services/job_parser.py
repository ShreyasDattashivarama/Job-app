from __future__ import annotations

import re

from app.models.schemas import JobAnalysis

SKILLS = ["Python", "SQL", "ETL", "data pipelines", "Machine Learning", "Power BI", "Docker", "PyTorch", "TensorFlow", "Scikit-learn", "Azure", "Databricks", "Palantir Foundry", "FastAPI", "Streamlit", "CI/CD", "LLM", "Generative AI"]
DOMAINS = ["industrial", "manufacturing", "healthcare", "automotive", "engineering", "IoT", "enterprise"]


def _lines(text: str) -> list[str]:
    return [line.strip(" •\t") for line in text.splitlines() if line.strip()]


def _find_label(lines: list[str], label: str) -> str | None:
    match = next((re.split(r"[:–-]", line, maxsplit=1)[-1].strip() for line in lines if line.lower().startswith(label.lower())), None)
    return match or None


def parse_job(text: str, url: str | None = None) -> JobAnalysis:
    lines = _lines(text)
    company = _find_label(lines, "Company") or "Unknown company"
    title = _find_label(lines, "Role") or _find_label(lines, "Title") or next((line for line in lines if re.search(r"(engineer|analyst|scientist|working student|intern)", line, re.I)), "Untitled role")
    location = _find_label(lines, "Location") or ("Hamburg" if re.search("hamburg", text, re.I) else "Not specified")
    employment = _find_label(lines, "Employment type") or ("Working Student" if re.search("working student", text, re.I) else "Not specified")
    found_skills = [skill for skill in SKILLS if re.search(rf"\b{re.escape(skill)}\b", text, re.I)]
    found_domains = [item for item in DOMAINS if re.search(rf"\b{re.escape(item)}\b", text, re.I)]
    languages = [f"German {m.group(1).upper()}" for m in re.finditer(r"German\s*(A[12]|B[12]|C[12])?", text, re.I)]
    if re.search(r"English", text, re.I): languages.append("English")
    mandatory_lines = [line for line in lines if re.search(r"(must|required|mandatory|your profile|requirements)", line, re.I)]
    preferred_lines = [line for line in lines if re.search(r"(preferred|nice to have|plus|desirable)", line, re.I)]
    responsibilities = [line for line in lines if re.search(r"(develop|build|design|maintain|analy[sz]|collaborate|support|implement)", line, re.I)][:8]
    return JobAnalysis(company=company, title=title, location=location, employment_type=employment, seniority="Not specified", responsibilities=responsibilities, required_skills=found_skills, preferred_skills=[s for s in found_skills if any(s.lower() in line.lower() for line in preferred_lines)], languages=list(dict.fromkeys(languages)), education_requirements=[line for line in lines if re.search(r"(degree|master|bachelor|student)", line, re.I)][:4], experience_requirements=[line for line in lines if re.search(r"\d+\+? years", line, re.I)], domain_requirements=found_domains, keywords={"technical": found_skills, "domain": found_domains, "business": ["business requirements"] if re.search("business requirements", text, re.I) else [], "soft_skills": [x for x in ["communication", "teamwork", "problem solving"] if re.search(x, text, re.I)], "language": list(dict.fromkeys(languages))}, source_text=text)

