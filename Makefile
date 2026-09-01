VENV = a_maze_ing
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate  # Update timestamp to match requirements.txt

install: $(VENV)/bin/activate

run: install
	$(PYTHON) a_maze_ing.py config.txt

debug:

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint: install
	@$(FLAKE8) . --exclude $(VENV)
	@$(MYPY) . --warn-return-any\
			  --warn-unused-ignores\
			  --ignore-missing-imports\
			  --disallow-untyped-defs\
			  --check-untyped-defs\
			  --exclude $(VENV)

lint-strict: install
	@$(FLAKE8) . --exclude $(VENV)
	@$(MYPY) . --strict --exclude $(VENV)
