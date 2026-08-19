from pathlib import Path

from app.services.checkers import truth_check
from app.services.documents import export_docx
from app.services.job_parser import parse_job
from app.services.matcher import match_job

SAMPLE = """Company: Example Industrial AI GmbH
Role: Working Student Data & AI
Location: Hamburg
Requirements:
Python
SQL
Data pipelines
Machine Learning
Power BI
German B1+
Engineering environment"""


def test_job_parser_extracts_expected_fields():
    job = parse_job(SAMPLE)
    assert job.company == "Example Industrial AI GmbH"
    assert "Python" in job.required_skills
    assert "German B1" in job.languages


def test_matcher_recommends_sample_job():
    analysis = match_job(parse_job(SAMPLE))
    assert analysis.fit_score >= 75
    assert "Python" in analysis.strong_matches
    assert analysis.recommendation in {"STRONGLY RECOMMEND APPLYING", "RECOMMEND APPLYING"}


def test_truth_check_rejects_unsupported_claim():
    assert not truth_check("I have 10 years of experience and C1 German.").passed


def test_truth_check_accepts_supported_content():
    assert truth_check("Designed ETL workflows supporting AI applications using Python.").passed


def test_docx_export(tmp_path: Path):
    output = export_docx("Example", "Data Engineer", "CV", "A truthful CV.", tmp_path)
    assert output.exists() and output.suffix == ".docx"
