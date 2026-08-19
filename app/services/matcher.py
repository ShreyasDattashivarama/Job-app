from __future__ import annotations

import re

from app.models.schemas import ApplicationAnalysis, JobAnalysis, MatchType, RequirementMatch
from app.services.profile import PROFILE, evidence_for


def _mandatory(job: JobAnalysis, item: str) -> bool:
    return bool(re.search(rf"(must|required|mandatory).{{0,80}}{re.escape(item)}|{re.escape(item)}.{{0,80}}(must|required|mandatory)", job.source_text, re.I))


def match_job(job: JobAnalysis) -> ApplicationAnalysis:
    requirements = list(dict.fromkeys(job.required_skills + job.domain_requirements + job.languages))
    matches: list[RequirementMatch] = []
    for requirement in requirements:
        evidence = evidence_for(requirement)
        mandatory = _mandatory(job, requirement)
        if requirement.lower().startswith("german"):
            level = re.search(r"([ABC][12])", requirement, re.I)
            target = level.group(1).upper() if level else "B1"
            candidate = "B1"
            kind = MatchType.STRONG if target <= candidate else (MatchType.CRITICAL if mandatory else MatchType.GAP)
            evidence_labels = ["Verified language: German — B1, actively improving"]
        elif evidence:
            kind, evidence_labels = MatchType.STRONG, [item.label for item in evidence]
        elif requirement.lower() in {"data engineering", "cloud", "industrial", "iot", "engineering"}:
            kind, evidence_labels = MatchType.TRANSFERABLE, [item.label for item in evidence_for("industrial")][:2]
        else:
            kind, evidence_labels = (MatchType.CRITICAL if mandatory else MatchType.GAP), []
        matches.append(RequirementMatch(requirement=requirement, importance="high" if mandatory else "medium", mandatory=mandatory, match_type=kind, evidence=evidence_labels, explanation=("Direct verified evidence exists." if evidence_labels else "No verified evidence was found.")))
    critical = [m.requirement for m in matches if m.match_type == MatchType.CRITICAL]
    strong = [m.requirement for m in matches if m.match_type == MatchType.STRONG]
    transferable = [m.requirement for m in matches if m.match_type in {MatchType.TRANSFERABLE, MatchType.PARTIAL}]
    gaps = [m.requirement for m in matches if m.match_type == MatchType.GAP]
    technical = round(30 * len([m for m in matches if m.match_type == MatchType.STRONG]) / max(1, len(requirements)))
    experience = 22 if any(evidence_for(item) for item in requirements) else 8
    responsibilities = 12 if job.responsibilities else 7
    domain = 10 if any(x in ["industrial", "engineering"] for x in job.domain_requirements) else 6
    education, language, location, preferred = 5, (5 if not critical else 0), (5 if "Hamburg" in job.location or "Remote" in job.location else 3), 4
    score = min(100, technical + experience + responsibilities + domain + education + language + location + preferred)
    recommendation = "STRONGLY RECOMMEND APPLYING" if score >= 85 else "RECOMMEND APPLYING" if score >= 75 else "APPLY IF INTERESTED" if score >= 65 else "LOW PRIORITY" if score >= 55 else "NOT RECOMMENDED"
    if critical: recommendation = "APPLY WITH CAUTION"
    why = "Your verified experience maps directly to " + ", ".join(strong[:4]) + "." if strong else "The role has limited direct overlap with the verified profile."
    risk = (f"Critical requirement gap: {critical[0]}." if critical else (f"Main gap: {gaps[0]}." if gaps else "No clearly stated critical gap was identified."))
    return ApplicationAnalysis(fit_score=score, recommendation=recommendation, requirement_matches=matches, strong_matches=strong, transferable_matches=transferable, gaps=gaps, critical_gaps=critical, why_you_fit=why, main_risk=risk, score_breakdown={"Core technical requirements": technical, "Relevant experience": experience, "Responsibilities": responsibilities, "Domain": domain, "Education": education, "Language": language, "Location": location, "Preferred": preferred})
