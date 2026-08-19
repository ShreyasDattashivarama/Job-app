from __future__ import annotations

from app.models.schemas import CVChange, JobAnalysis
from app.services.profile import EVIDENCE, PROFILE


def suggest_cv_changes(job: JobAnalysis) -> list[CVChange]:
    keywords = {x.lower() for x in job.required_skills + job.domain_requirements}
    changes = [CVChange(section="Professional profile", original=PROFILE["positioning"], proposed=f"Data & AI professional with verified experience in {', '.join(job.required_skills[:4]) or 'machine learning and data engineering'}, applying Python-based data and AI solutions across industrial and enterprise environments.", reason="Aligns the opening profile with the job's terminology without adding unverified claims.", evidence=[e.label for e in EVIDENCE[:3]])]
    if {"etl", "data pipelines"} & keywords:
        changes.append(CVChange(section="Finches.ai", original="Designed and maintained ETL workflows and data pipelines to support AI applications.", proposed="Designed and maintained ETL workflows and data pipelines supporting AI applications and automated data preparation.", reason="Makes verified data-engineering work more prominent.", evidence=[EVIDENCE[0].label]))
    if {"industrial", "engineering", "machine learning"} & keywords:
        changes.append(CVChange(section="Herrenknecht AG", original="Developed ML models and improved ETL pipelines.", proposed="Developed machine-learning models using industrial sensor data and improved ETL pipelines, reducing processing time by 30%.", reason="Uses the verified quantified industrial achievement.", evidence=[EVIDENCE[2].label]))
    return changes


def draft_cover_letter(job: JobAnalysis) -> str:
    skills = ", ".join(job.required_skills[:4]) or "data and AI"
    return f"""Dear Hiring Team,

I am applying for the {job.title} role at {job.company}. The opportunity to contribute to work involving {skills} fits well with my verified background in data engineering and applied machine learning.

I am currently pursuing an MBA in Technology Management at TU Hamburg and have built practical experience across industrial, enterprise and healthcare-related environments. At Finches.ai, I designed ETL workflows and data pipelines supporting AI applications, worked with business data in Palantir Foundry, and developed an LLM-powered chatbot for domain knowledge access.

Previously, at Herrenknecht AG, I developed machine-learning models using tunnel-boring-machine sensor data and improved ETL processing time by 30%. At Edison Labs, I worked across the AI lifecycle—from data preparation and model development to Docker-supported deployment—using Python, Scikit-learn and PyTorch.

I would bring a practical working style: understanding requirements with stakeholders, translating them into maintainable data solutions, and communicating clearly across technical and business contexts. My German is B1 and actively improving; I am fluent in English.

I would welcome the opportunity to discuss how this experience could support your team.

Kind regards,
Shreyas Dattashivarama"""

