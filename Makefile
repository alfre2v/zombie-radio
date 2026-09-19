# Zombie-Radio — everything runnable in one place. `make help` lists targets.

ENV ?=
ANS_ARGS ?=

ANSIBLE_DIR := $(CURDIR)/deploy/ansible
# Absolute on purpose: ansible.cfg is discovered relative to the CWD (and
# silently ignored in world-writable dirs); exporting pins it for every target.
export ANSIBLE_CONFIG = $(ANSIBLE_DIR)/ansible.cfg

ZR_CONF_DIR := $(HOME)/.config/zombie-radio
ANS_LOG_DIR := $(ZR_CONF_DIR)/logs
ANS_LOG_STAMP := $(shell date +%Y%m%d-%H%M%S)
ANS_VERBOSITY := $(if $(ANS_VERBOSE),-v,)

# Same SSH posture as the deployment's ansible_ssh_common_args (99-cloud.yml):
# only the declared key, auto-accept unknown hosts, alarm on changed ones.
SSH_TOFU_OPTS := -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new \
                 -o UserKnownHostsFile=$(ZR_CONF_DIR)/known_hosts

.PHONY: help install ans-deps ans-config ans-lint ans-deploy ans-check-syntax check ssh-tunnel

help:
	@echo "Available targets:"
	@echo "  install             install/sync tooling dependencies into .venv (uv)"
	@echo "  ans-deps            install pinned Ansible collections (project-local)"
	@echo "  ans-config          show which ansible.cfg is loaded + resolved paths"
	@echo "  ans-lint            lint the deployment (playbook + roles)"
	@echo "  ans-deploy ENV=x    converge env x's GPU box(es): run site.yml [ANS_ARGS=...]"
	@echo "                      (runs logged to ~/.config/zombie-radio/logs/; ANS_VERBOSE=1 adds -v)"
	@echo "  ans-check-syntax ENV=x  hostless syntax parse of site.yml against env x"
	@echo "  check               health-check all services from the laptop, through the tunnel"
	@echo "  ssh-tunnel          open the SSH tunnel to the cloud box (IP from cloud inventory)"

install:
	uv sync
	git config core.hooksPath .githooks

ans-deps:
	uv run ansible-galaxy collection install -r $(ANSIBLE_DIR)/collections/requirements.yml

ans-config:
	@uv run ansible-config dump | grep -E 'CONFIG_FILE|COLLECTIONS_PATHS|ANY_UNPARSED'

ans-lint:
	uv run ansible-lint $(ANSIBLE_DIR)

define require_ansible_env
	@test -n "$(ENV)" || { echo "usage: make $(1) ENV=<environment>"; exit 2; }
	@test -d "$(ANSIBLE_DIR)/inventories/$(ENV)" || { \
	    echo "unknown environment '$(ENV)': no such inventory directory"; \
	    echo "known environments:"; \
	    find "$(ANSIBLE_DIR)/inventories" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sed 's/^/  /'; \
	    exit 2; }
endef

ans-deploy:
	$(call require_ansible_env,ans-deploy)
	@mkdir -p $(ANS_LOG_DIR)
	ANSIBLE_LOG_PATH="$${ANSIBLE_LOG_PATH:-$(ANS_LOG_DIR)/$(ENV)-deploy-$(ANS_LOG_STAMP).log}" \
	uv run ansible-playbook -i $(ANSIBLE_DIR)/inventories/$(ENV) \
	    $(ANSIBLE_DIR)/site.yml $(ANS_VERBOSITY) $(ANS_ARGS)

ans-check-syntax:
	$(call require_ansible_env,ans-check-syntax)
	uv run ansible-playbook -i $(ANSIBLE_DIR)/inventories/$(ENV) \
	    $(ANSIBLE_DIR)/site.yml --syntax-check

check:
	@curl -sf http://localhost:8080/health > /dev/null && echo "llama:   ok" || echo "llama:   FAIL"
	@curl -sf -o /dev/null http://localhost:8001/capabilities && echo "tts:     ok" || echo "tts:     FAIL"
	@curl -sf -o /dev/null http://localhost:8002/docs && echo "whisper: ok" || echo "whisper: FAIL"

ssh-tunnel:
	@mkdir -p $(ZR_CONF_DIR)
	@host="$$(awk '/ansible_host:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/cloud/hosts.yml")"; \
	 user="$$(awk '/^ansible_user:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/common_vars.yml")"; \
	 key="$$(awk -F'"' '/^ansible_ssh_private_key_file:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/common_vars.yml")"; \
	 case "$$key" in "~"*) key="$$HOME$${key#\~}";; esac; \
	 test -n "$$host" || { echo "no ansible_host found in inventories/cloud/hosts.yml"; exit 2; }; \
	 case "$$host" in REPLACE_ME*) echo "cloud hosts.yml still carries the REPLACE_ME sentinel"; exit 2;; esac; \
	 test -n "$$key" || { echo "no ansible_ssh_private_key_file found in inventories/common_vars.yml"; exit 2; }; \
	 echo "Tunnel to $$host: llama :8080 / tts :8001 / whisper :8002   (Ctrl-C closes it)"; \
	 ssh -N -o ExitOnForwardFailure=yes -i "$$key" $(SSH_TOFU_OPTS) \
	     -L 8080:127.0.0.1:8080 -L 8001:127.0.0.1:8001 -L 8002:127.0.0.1:8002 "$$user@$$host"
