VENV=.venv/bin
NPM=node_modules/.bin

.PHONY: install clean test test-advanced

$(VENV):
	python3 -m venv .venv
	$(VENV)/python3 -m pip install --upgrade pip

$(VENV)/.deps: requirements.txt | $(VENV)
	$(VENV)/pip install -r requirements.txt
	touch $(VENV)/.deps

$(NPM):
	npm install --no-save @percy/cli@^1.31.13

install: $(VENV)/.deps $(NPM)

clean:
	rm -rf .venv node_modules .pytest_cache __pycache__ tests/__pycache__

# Run against BrowserStack App Automate hub. Requires AA_USERNAME,
# AA_ACCESS_KEY, APP, PERCY_TOKEN env vars.
test test-advanced: install
	$(NPM)/percy app:exec -- $(VENV)/python3 -m pytest tests/ -v
