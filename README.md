<p align="center">
  <img src="https://cariai.com/wp-content/uploads/2025/05/cari-logo-optimisado.svg" alt="Cari AI" width="160" />
</p>
<h1 align="center">Python Developer Technical Test - Cari AI</h1>
<p align="center">
  Lightweight FastAPI service that suggests answers from a FAQ knowledge base and keeps in-memory
  history.
</p>
<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.127.0-009688" />
  <img alt="uv" src="https://img.shields.io/badge/uv-0.40.0-4B8BBE" />
  <img alt="Coverage" src="coverage.svg" />
</p>
<p align="center">
  <a href="https://technical-test-cari-ai.onrender.com/api/v1/docs">Live Demo</a>
</p>

## Installation
### System Dependencies
You will need the following system dependencies to run this project:

- **[Git](https://git-scm.com/downloads)**: To clone this repository.
- **[Docker](https://docs.docker.com/engine/install/)** (Optional): To build and run the project.
- **[uv](https://github.com/astral-sh/uv)** (Optional): To install the project dependencies for local development.

### Option 1: pip
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Option 2: uv
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --all-extras
```

`uv sync` uses `.venv` by default. You can run commands with `uv run` without activating the
virtual environment.

### Lockfile (uv)
- Dependencies are declared in `pyproject.toml`.
- Update the lockfile: `uv lock`.
- Install from the lockfile: `uv sync --all-extras`.

## Run
```bash
uvicorn main:app --reload
```
Alternative with uv:
```bash
uv run uvicorn main:app --reload
```
By default, the knowledge base is loaded from `app/resources/knowledge_base.json`.

### Environment variables
- `KNOWLEDGE_BASE_PATH`: Path to a custom JSON knowledge base file.
- `FALLBACK_MESSAGE`: Override the default fallback suggestion.
- `CORS_ORIGINS`: JSON list of allowed origins for CORS.
- `API_V1_PREFIX`: API prefix for all routes (default: `/api/v1`).
- `DOCS_ENABLED`: Toggle `/docs`, `/redoc`, and `/openapi.json` (default: `true`).
- `ENV`: Set to `dev` to allow all CORS origins (default: `dev`).

Example:
```bash
export KNOWLEDGE_BASE_PATH=app/resources/knowledge_base.json
export FALLBACK_MESSAGE="No encontré coincidencias. ¿Puedes dar más detalles?"
export CORS_ORIGINS='["http://localhost:3000","https://tu-dominio.com"]'
export API_V1_PREFIX=/api/v1
export DOCS_ENABLED=true
export ENV=dev
```
Or use a `.env` file:
```bash
cp .env.example .env
uvicorn main:app --reload --env-file .env
```
Settings load `.env` automatically if present, so `--env-file` is optional.

## Docker
```bash
docker build -t cari-ai-faq .
docker run --rm -p 8000:8000 cari-ai-faq
```
With environment variables:
```bash
docker run --rm -p 8000:8000 --env-file .env cari-ai-faq
```

### Quality (linting and types)
- Install hooks: `pre-commit install`
- Run checks manually:
  - `uv run ruff check .` (or `python -m ruff check .`)
  - `uv run ruff format .`
  - `uv run mypy app`

## Main endpoints
- `POST /api/v1/suggest` - Body: `{"query": "¿Cómo cambio mi contraseña?"}`. Returns the best suggestion
  and stores the query in history.
- `GET /api/v1/history` - Lists previous queries and suggestions in arrival order.
- `POST /api/v1/knowledge` - (Optional) Adds a FAQ item with `{"pregunta": "...", "respuesta": "..."}`.
- `GET /api/v1/knowledge` - (Optional) Returns the current knowledge base.

## Tests
```bash
pytest
```
Alternative with uv:
```bash
uv run pytest
```

## Notes
- Similarity uses `difflib.SequenceMatcher` with a configurable threshold.
- History is stored in memory; restarting the process clears it.
- The default knowledge base uses Spanish entries with `pregunta`/`respuesta` keys to match the test.
- To change or translate the knowledge base, edit `app/resources/knowledge_base.json` and restart.
