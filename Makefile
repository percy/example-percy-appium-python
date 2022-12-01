VENV=.venv/bin
NPM=node_modules/.bin
REQUIREMENTS=$(wildcard requirements.txt)
MARKER=.initialized-with-makefile
VENVDEPS=$(REQUIREMENTS setup.py)
NPMDEPS=$(package-lock.json)

$(VENV):
	python -m venv .venv
	$(VENV)/python -m pip install --upgrade pip

$(VENV)/$(MARKER): $(VENVDEPS) | $(VENV)
	$(VENV)/pip install $(foreach path,$(REQUIREMENTS),-r $(path))
	touch $(VENV)/$(MARKER)

$(NPM): $(NPMDEPS)
	npm install

.PHONY: venv npm install clean test-android test-ios

venv: $(VENV)/$(MARKER)
npm: $(NPM)

install: npm venv

clean:
	rm -rf $$(cat .gitignore)

test-android: install
	$(NPM)/percy app:exec -- $(VENV)/python tests/android.py

test-ios: install
	$(NPM)/percy app:exec -- $(VENV)/python tests/ios.py
