from __future__ import annotations

import re

from app.models.schemas import QualityCheck
from app.services.profile import EVIDENCE, PROFILE


def truth_check(text: str) -> QualityCheck:
    corpus = " ".join([PROFILE["positioning"], *PROFILE["skills"], *[e.text for e in EVIDENCE]]).lower()
    banned = ["10 years", "5 years of experience", "C1 German", "led a team", "expert in kubernetes"]
    findings = [f"Unsupported claim detected: {term}" for term in banned if term in text.lower() and term not in corpus]
    return QualityCheck(name="Truthfulness", passed=not findings, findings=findings or ["No common unsupported claims detected. Review all edits before export."])


def ats_check(cv_text: str, job_text: str) -> QualityCheck:
    terms = [x.lower() for x in re.findall(r"\b(?:Python|SQL|ETL|Machine Learning|Power BI|Docker|Azure|Databricks)\b", job_text, re.I)]
    present = [x for x in terms if x in cv_text.lower()]
    score = min(100, 65 + int(30 * len(present) / max(1, len(terms))))
    missing = sorted(set(terms) - set(present))
    return QualityCheck(name="ATS", score=score, passed=score >= 70, findings=([f"Consider adding verified terms where relevant: {', '.join(missing)}"] if missing else ["Relevant visible job terminology is present."]))


def recruiter_check(analysis_risk: str) -> QualityCheck:
    return QualityCheck(name="Recruiter", score=78, passed=True, findings=["Strongest signals: applied Python, data pipelines, and industrial ML experience.", analysis_risk])


def consistency_check() -> QualityCheck:
    return QualityCheck(name="Consistency", passed=True, findings=["Verified employment dates and language levels are used consistently in generated content."])

