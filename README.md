# Astra Export Parser

Astra Export Parser parses an Astra Export XML file (`data/export_full.xml`) and extracts product and spare-part information. It provides a command-line interface and a lightweight Flask web UI for exploring results.

---

## Features

1. CLI tool (`astra_parser.py`) supports:
   1. Counting products
   1. Listing product names (with image if present)
   1. Listing spare parts per product
1. Flask web UI (`app.py`) with routes `/`, `/count`, `/names`, `/parts`
   - `/names` and `/parts` support pagination with query parameters: `?page=1&per_page=10`
1. Streaming XML parsing for memory efficiency on large files (e.g., 89MB+)
1. Pagination support for web UI to handle large datasets without performance issues
1. Unit tests (`test_astra_parser.py`)
1. Development tooling & CI (Black, isort, Ruff, Flake8, Mypy, Pylint, pre-commit, GitHub Actions)
1. Dockerfile for containerized runs and simple start/kill scripts

---

## Project Structure

- `astra_parser.py` — Parser core and CLI
- `app.py` — Flask web app
- `templates/index.html` — UI template
- `data/export_full.xml` — Example XML dataset
- `test_astra_parser.py` — Unit tests
- `start-server.sh` / `kill-server.sh` — Local server management
- `Dockerfile` — Container build configuration
- `requirements.txt` / `requirements_dev.txt` — dependencies
- `.pre-commit-config.yaml` — pre-commit hooks
- `.github/workflows/lint.yml` — CI workflow

---

## Quick Start

1. Clone the repo and change to the project folder.
1. Create and activate a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

1. Run the CLI parser:

```bash
python3 astra_parser.py
```

1. Run the Flask app:

```bash
python3 app.py
# Visit: http://127.0.0.1:5000
```

1. Optional: Background server for local testing:

```bash
./start-server.sh
# Check server.log and server.pid
./kill-server.sh
```

---

## Docker

```bash
docker build -t astra-export .
docker run -p 5000:5000 astra-export
```

---

## Development & Linting

Run the standard linters and formatters from the project root (with venv activated):

```bash
black --check .
isort --check-only .
ruff check .
flake8 .
mypy .
pylint astra_parser.py app.py test_astra_parser.py
```

Install & run pre-commit hooks:

```bash
pre-commit install
pre-commit run --all-files
```

---

## Deployment

The app is optimized for low-memory usage and can be deployed to platforms like Render.com or Heroku using the provided Dockerfile. It uses streaming XML parsing and pagination to handle large XML files (e.g., 89MB+) efficiently without loading entire datasets into memory.

---
