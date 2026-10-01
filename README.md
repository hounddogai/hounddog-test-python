# HoundDog.ai Test Repository: Python

A medical data management app for patients, health metrics, medical records, and analytics, with an AI assistant. It is
a scan target for the [HoundDog.ai](https://hounddog.ai) scanner, so its code deliberately leaks fake sensitive data. Do
not deploy it or copy its patterns.

## Tech stack

- Python 3.14 with uv, Streamlit, SQLAlchemy 2 (SQLite by default)
- LangChain with OpenAI, Sentry, pandas, Plotly, pypdf
- Ruff for linting and formatting

## Run

```sh
uv sync
cp .env.example .env               # set OPENAI_API_KEY and, optionally, SENTRY_DSN
uv run scripts/init_db.py          # create the tables in data.db
uv run scripts/seed_db.py          # optional: add 20 sample patients
uv run streamlit run app.py
```

Open <http://localhost:8501>.

## Check

```sh
uv lock --check
uv run ruff check
uv run ruff format --check
```

uv only resolves releases that are at least 7 days old (`exclude-newer` in `pyproject.toml`).
