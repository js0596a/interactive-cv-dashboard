PYTHON ?= python3
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python
VENV_PIP ?= $(VENV)/bin/pip
PORT ?= 8050

.PHONY: install install-dev run check test link-check demo-gif

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

install-dev: install
	$(VENV_PIP) install -r requirements-dev.txt
	$(VENV_PY) -m playwright install chromium

run:
	$(VENV_PY) -c "from app import app; app.run(debug=True, port=$(PORT))"

check:
	$(VENV_PY) -m py_compile app.py cv_data.py
	$(VENV_PY) scripts/validate_cv_data.py

test:
	$(VENV_PY) -m pytest -q

link-check:
	bash scripts/check_links.sh

demo-gif:
	$(VENV_PY) scripts/capture_demo.py --duration 1.05 --hold-start 7 --hold-middle 5 --hold-end 10
