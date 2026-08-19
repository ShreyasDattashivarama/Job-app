from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

from app.models.database import list_applications, save_application, save_job
from app.services.checkers import ats_check, consistency_check, recruiter_check, truth_check
from app.services.documents import export_docx
from app.services.job_extractor import extract_from_url
from app.services.job_parser import parse_job
from app.services.matcher import match_job
from app.services.profile import EVIDENCE, PROFILE, master_cv_text
from app.services.tailoring import draft_cover_letter, suggest_cv_changes

st.set_page_config(page_title="Job Application Copilot", page_icon="✦", layout="wide")
st.title("Job Application Copilot")
st.caption("Evidence-based tailoring for German-market applications. No automatic submission.")

page = st.sidebar.radio("Navigate", ["Dashboard", "New job", "Career profile", "Applications"])

if page == "Career profile":
    st.subheader(PROFILE["name"])
    st.write(f"{PROFILE['location']} · {PROFILE['positioning']}")
    st.write("**Languages:** " + " · ".join(f"{name}: {level}" for name, level in PROFILE["languages"].items()))
    st.write("**Verified skills:** " + ", ".join(PROFILE["skills"]))
    st.subheader("Evidence base")
    for item in EVIDENCE:
        with st.expander(item.label): st.write(item.text)

elif page == "Applications":
    st.subheader("Application tracker")
    rows = list_applications()
    if rows:
        st.dataframe([{"Company": r.company, "Role": r.role, "Fit": r.fit_score, "Status": r.status, "Follow-up": r.follow_up_date, "Notes": r.notes} for r in rows], use_container_width=True)
    else: st.info("No saved applications yet.")

elif page == "Dashboard":
    st.subheader("Today’s attention")
    rows = list_applications(); today = date.today()
    due = [r for r in rows if r.follow_up_date and r.follow_up_date <= today]
    c1, c2, c3 = st.columns(3)
    c1.metric("Follow-ups due", len(due)); c2.metric("Applications tracked", len(rows)); c3.metric("Awaiting final review", len([r for r in rows if r.status == "Draft"]))
    if due: st.warning("Follow-up due: " + ", ".join(f"{r.company} — {r.role}" for r in due))
    st.info("Start with **New job** to analyze a role.")

else:
    st.subheader("Analyze a job")
    url = st.text_input("Public job URL (optional)")
    source = st.text_area("Job description", height=260, placeholder="Paste the complete job description here.")
    if st.button("Analyze job", type="primary"):
        try:
            text = source or extract_from_url(url)
            job = parse_job(text, url)
            analysis = match_job(job)
            save_job(job.company, job.title, text, job.model_dump(), url or None)
            st.session_state.update(job=job, analysis=analysis)
        except Exception as exc:
            st.error("I couldn't reliably extract this job posting. Please paste the job description or upload the PDF.")
            st.caption(str(exc))
    if "analysis" in st.session_state:
        job, analysis = st.session_state.job, st.session_state.analysis
        st.divider(); left, right = st.columns([1, 2])
        with left:
            st.metric("Application Fit Score", f"{analysis.fit_score}/100")
            st.success(analysis.recommendation) if not analysis.critical_gaps else st.warning(analysis.recommendation)
            st.write("**Main risk:** " + analysis.main_risk)
        with right:
            st.write(f"**{job.company}** · {job.title} · {job.location}")
            st.write("**Why you fit:** " + analysis.why_you_fit)
            st.write("**Strong matches:** " + (", ".join(analysis.strong_matches) or "None identified"))
            if analysis.gaps: st.write("**Gaps:** " + ", ".join(analysis.gaps))
            if analysis.critical_gaps: st.error("Critical gaps: " + ", ".join(analysis.critical_gaps))
        with st.expander("Requirement-by-requirement evidence"):
            st.dataframe([m.model_dump() for m in analysis.requirement_matches], use_container_width=True)
        st.subheader("Review tailored application")
        changes = suggest_cv_changes(job)
        accepted = []
        for i, change in enumerate(changes):
            with st.expander(f"{change.section}: {change.reason}", expanded=True):
                st.caption("CURRENT"); st.write(change.original); st.caption("PROPOSED"); edited = st.text_area("Edit proposal", change.proposed, key=f"change_{i}"); st.caption("Evidence: " + "; ".join(change.evidence));
                if st.checkbox("Accept this change", key=f"accept_{i}"): accepted.append(edited)
        letter = st.text_area("Tailored cover letter", draft_cover_letter(job), height=360)
        cv = master_cv_text() + "\n\n" + "\n".join(accepted)
        checks = [truth_check(cv + "\n" + letter), ats_check(cv, job.source_text), recruiter_check(analysis.main_risk), consistency_check()]
        st.subheader("Quality checks")
        st.dataframe([c.model_dump() for c in checks], use_container_width=True)
        truth_ok = checks[0].passed
        if not truth_ok: st.error("Truthfulness check must pass before export.")
        if st.button("Generate DOCX documents", disabled=not truth_ok):
            cv_path = export_docx(job.company, job.title, "CV", cv, Path("data/exports")); letter_path = export_docx(job.company, job.title, "Cover_Letter", letter, Path("data/exports"))
            st.success("Documents generated.")
            st.download_button("Download CV", cv_path.read_bytes(), file_name=cv_path.name); st.download_button("Download cover letter", letter_path.read_bytes(), file_name=letter_path.name)
        st.subheader("Save application")
        follow = st.date_input("Follow-up date", value=None)
        notes = st.text_area("Notes", key="notes")
        if st.button("Save to tracker"):
            save_application(job.company, job.title, analysis.fit_score, url or None, follow, notes); st.success("Saved to application tracker.")
