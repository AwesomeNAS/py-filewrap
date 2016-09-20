export VERSION=1

# Command line arguments:
#

VENV = $(PWD)/venv
VENV_PYTHON = $(VENV)/bin/python3.4
VENV_PIP = $(VENV)/bin/pip3.4
VENV_REQS = $(PWD)/requirements.txt

WORKDIR = $(VENV)/work

FREENAS_UTILS = py-freenas-utils
FREENAS_CLIENT = dispatcher-client
FILEWRAP = filewrap

.PHONY: example
example: env run_filebrowser

.PHONY: env 
env: $(VENV) install_utils install_dispatcher_client install_filewrap

.PHONY: clean
clean:
	@rm -rf $(VENV)

.PHONY: install_utils
install_utils: $(VENV)/$(FREENAS_UTILS)

.PHONY: install_dispatcher_client
install_dispatcher_client: $(VENV)/$(FREENAS_CLIENT)

.PHONY: install_filewrap
install_filewrap: $(WORKDIR)/$(FILEWRAP)

.PHONY: run_filebrowser
run_filebrowser:
	@clear
	@$(VENV_PYTHON) ./examples/filebrowser.py

$(VENV):
	@virtualenv $(VENV) --python=python3
	@$(VENV_PIP) install -Ur $(VENV_REQS)

$(VENV)/$(FREENAS_UTILS):
	@git clone https://github.com/freenas/py-freenas-utils $(VENV)/$(FREENAS_UTILS)
	@cd $(VENV)/$(FREENAS_UTILS) && $(VENV_PYTHON) setup.py install

$(VENV)/$(FREENAS_CLIENT):
	@git clone https://github.com/freenas/dispatcher-client $(VENV)/$(FREENAS_CLIENT)
	@cd $(VENV)/$(FREENAS_CLIENT)/python && $(VENV_PYTHON) setup.py install

$(WORKDIR)/$(FILEWRAP):
	@mkdir $(WORKDIR)
	@cp -r $(FILEWRAP) $(WORKDIR)/
	@cp setup.py $(WORKDIR)
	@cd $(WORKDIR) && $(VENV_PYTHON) setup.py install
