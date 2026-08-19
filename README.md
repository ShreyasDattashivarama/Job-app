# Job Application Copilot

A local-first Streamlit application for evidence-based, Germany-focused job applications. It stores a verified career profile, extracts requirements from pasted job descriptions or public URLs, produces a transparent fit score, proposes minimal CV changes, writes a natural cover letter, performs quality checks, exports DOCX documents, and tracks applications.

## Install and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app/main.py
```

The app works without an API key using local, deterministic parsing and drafting. `.env.example` reserves the configuration for a future OpenAI structured-analysis adapter. That adapter should use the Responses API and structured outputs, as supported by the official [GPT-5.4 model documentation](https://developers.openai.com/api/docs/models/gpt-5.4), rather than storing unstructured model output in database fields.

## Deploy to Streamlit Community Cloud

1. Create a **private** GitHub repository and upload this entire project. Do not upload `.env`, `data/database.sqlite`, or `.streamlit/secrets.toml`.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub and select **Create app**.
3. Select the repository and branch, then use `app/main.py` as the entrypoint.
4. Open **Advanced settings**, choose Python **3.12**, and paste any secrets from `.streamlit/secrets.toml.example` only if you later add an API integration.
5. Deploy. Streamlit will install the pinned packages in `requirements.txt` and give you a `*.streamlit.app` URL.

Community Cloud runs the app from the repository root, supports an entrypoint in a subdirectory, and reads `requirements.txt` from the project root. Your GitHub repository remains the source of truth: pushes update the hosted app. These deployment details follow the [official Streamlit deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [dependency documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

## Workflow

1. Open **New job**, paste a description or a public URL, and analyze it.
2. Review the transparent fit score, evidence, gaps, and recommendation.
3. Review each CV change, edit/accept only truthful edits, and review the cover letter.
4. Run quality checks, export DOCX files, and save the application with a follow-up date.

## Data and privacy

All profile, analysis, and application data is stored in `data/database.sqlite` on this machine. Master profile data is seeded from the supplied verified specification and is never overwritten during tailoring. Do not commit `.env` or the database. URL extraction only requests the supplied public URL; if it fails, paste the description instead.

### Community Cloud storage limitation

SQLite is suitable for local use, but Community Cloud filesystem storage is not a durable database. The hosted version can reset saved applications after a restart, redeploy, or platform maintenance. The initial hosted deployment is therefore best used for analysis and document generation. For a durable hosted application tracker, connect the SQLAlchemy storage layer to a managed PostgreSQL provider before relying on it for application history.

## Database

SQLite tables: `career_profile`, `jobs`, `applications`, and `document_versions`. Job analyses and check results are JSON columns so future interview-preparation data can be added without breaking existing records.

## Testing

```powershell
pytest
```

## Known V1 limitations

PDF export is intentionally optional; DOCX export is implemented. URL extraction is best-effort and respects that some career pages cannot be reliably parsed. OpenAI analysis is optional and the local baseline does not make external company claims.
