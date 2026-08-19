from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    label: str
    skills: tuple[str, ...]
    text: str


PROFILE = {
    "name": "Shreyas Dattashivarama",
    "location": "Hamburg, Germany",
    "positioning": "Data & AI / Machine Learning / Data Engineering",
    "languages": {"English": "Fluent", "German": "B1, actively improving", "Kannada": "Fluent"},
    "education": [
        "MBA in Technology Management, NIT Northern Institute of Technology Management, TU Hamburg (2025–2027)",
        "MSc Information and Communication Systems, TU Hamburg (2019–2023)",
        "BTech Electronics and Communication Engineering, Nitte Meenakshi Institute of Technology (2014–2018)",
    ],
    "skills": ["Python", "SQL", "C#", "REST APIs", "Flask", "FastAPI", "TensorFlow", "PyTorch", "Scikit-learn", "HuggingFace", "OpenAI APIs", "LangChain", "Power BI", "EDA", "Feature Engineering", "ETL Workflows", "Azure ML", "Databricks", "Docker", "GitHub", "CI/CD"],
}

EVIDENCE = [
    Evidence("Finches.ai — Working Student AI & Data Engineer", ("Python", "ETL", "data pipelines", "Palantir Foundry", "LLM", "chatbot", "automation", "reporting", "business requirements"), "Designed and maintained ETL workflows and data pipelines to support AI applications; structured business data in Palantir Foundry and built an LLM-powered domain-knowledge chatbot."),
    Evidence("Edison Labs — AI Engineer", ("Python", "Scikit-learn", "PyTorch", "Machine Learning", "classification", "forecasting", "Power BI", "Streamlit", "Docker", "model deployment"), "Implemented ML techniques for classification, forecasting and automation; built Power BI and Streamlit dashboards and collaborated on Docker-based production deployment."),
    Evidence("Herrenknecht AG — AI Engineer", ("Python", "SQL", "Machine Learning", "sensor data", "industrial data", "ETL", "Power BI", "Tableau", "predictive analytics", "simulation"), "Developed ML predictions using tunnel-boring-machine sensor data, created Python/SQL dashboards, and improved ETL pipelines, reducing processing time by 30%."),
    Evidence("Olympus Surgical Technologies Europe — Data Analyst Intern", ("Python", "FastAPI", "IoT", "AI", "real-time analytics", "data integration", "reporting", "dashboards"), "Developed IoT-based AI solutions for real-time analytics using Python and FastAPI; supported data integration and reporting."),
    Evidence("Resume Feedback Assistant — Project", ("OpenAI APIs", "spaCy", "Regex", "Streamlit", "ATS"), "Built a GPT-powered resume feedback application with parsing and personalized ATS recommendations."),
    Evidence("Deep Learning Image Classification — Project", ("TensorFlow", "Keras", "transfer learning", "Grad-CAM", "Streamlit"), "Built an EfficientNetB0 image-classification application with explainability and Streamlit deployment."),
]


def evidence_for(requirement: str) -> list[Evidence]:
    normalized = requirement.lower().replace("workflows", "").strip()
    aliases = {"machine learning": ("ml", "machine learning"), "data engineering": ("etl", "data pipelines"), "cloud": ("azure ml", "databricks"), "industrial": ("industrial", "sensor data"), "german": ("german",)}
    terms = aliases.get(normalized, (normalized,))
    return [item for item in EVIDENCE if any(term in " ".join(item.skills).lower() or term in item.text.lower() for term in terms)]


def master_cv_text() -> str:
    return "\n".join([f"{item.label}\n{item.text}" for item in EVIDENCE[:4]])
