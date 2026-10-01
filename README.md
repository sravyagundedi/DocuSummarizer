# DocuSummarizer

Implementation of  **DocuSummarizer — AI-Powered Meeting Intelligence Platform**.

## Required flow
Upload TXT/DOCX/PDF -> normalize -> speaker-aware chunk -> LangChain LLM summaries -> global executive summary -> Pydantic structured extraction -> token/cost tracking -> Streamlit tabs -> JSON/PDF export -> ROUGE evaluation -> pytest.

## Setup
Use Python 3.11+.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Run tests:
```powershell
pytest -q
```

## Important
Put API keys only in `.env`. Never hardcode them.

The supplied brief requires support for up to 50,000 words, speaker-aware chunking, retryable Pydantic parsing, token/cost logging, PDF/JSON export, 5 sample transcripts, ROUGE evaluation, tests, and documentation. This scaffold includes each required area so implementation can proceed module-by-module.

## Learning path
1. `schemas.py` — understand output structure.
2. `ingestion.py` — understand file parsing.
3. `chunking.py` — understand context windows.
4. `prompts.py` — understand prompt design.
5. `llm_client.py` — understand LangChain + parser retry.
6. `pipeline.py` — understand orchestration.
7. `app.py` — understand Streamlit.
8. `exporters.py` — understand PDF/JSON.
9. `evaluation.py` + `tests/` — understand quality and reliability.
