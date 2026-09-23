# Zombie-Radio — everything runnable in one place. `make help` lists targets.

ENV ?=
ANS_ARGS ?=

ANSIBLE_DIR := $(CURDIR)/deploy/ansible
# Absolute on purpose: ansible.cfg is discovered relative to the CWD (and
# silently ignored in world-writable dirs); exporting pins it for every target.
export ANSIBLE_CONFIG = $(ANSIBLE_DIR)/ansible.cfg

# Deliberately redundant with zr_control_dir (common_vars.yml) for
# readability — keep the two in sync. The extracting alternative:
# ZR_CONF_DIR := $(patsubst ~%,$(HOME)%,$(shell awk -F'"' '/^zr_control_dir:/ {print $$2; exit}' $(ANSIBLE_DIR)/inventories/common_vars.yml))
ZR_CONF_DIR := $(HOME)/.config/zombie-radio
ANS_LOG_DIR := $(ZR_CONF_DIR)/logs
ANS_LOG_STAMP := $(shell date +%Y%m%d-%H%M%S)
ANS_VERBOSITY := $(if $(ANS_VERBOSE),-v,)

# Same SSH posture as the deployment's ansible_ssh_common_args (common_vars):
# only the declared key, auto-accept unknown hosts, alarm on changed ones.
SSH_TOFU_OPTS := -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new \
                 -o UserKnownHostsFile=$(ZR_CONF_DIR)/known_hosts

.PHONY: help install ans-deps ans-config ans-lint ans-deploy ans-check-syntax check ssh-tunnel client-mac ans-set ans-unset

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
	@echo "  ans-set ENV=x IP=y  wire env x's hosts.yml to box IP y (replaces the sentinel)"
	@echo "  ans-unset ENV=x     restore env x's hosts.yml to the committed sentinel"
	@echo "  ssh-tunnel ENV=x    open the SSH tunnel to env x's box (IP from its inventory)"
	@echo "  client-mac          install the TalkWithZombies client on this Mac (standalone, inventory-free)"

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

# Guarantees the control-node state dir (logs + the ssh known_hosts parent).
define ensure_control_dirs
	@mkdir -p "$(ANS_LOG_DIR)"
endef

ans-deploy:
	$(call require_ansible_env,ans-deploy)
	$(call ensure_control_dirs)
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

# Wire/unwire the box address. ans-set substitutes the REPLACE_ME sentinel in
# the env's hosts.yml (refuses if already wired); ans-unset restores the file
# to its committed sentinel state. The never-commit hook keeps guarding a
# wired file in between.
ans-set:
	$(call require_ansible_env,ans-set)
	@test -n "$(IP)" || { echo "usage: make ans-set ENV=<environment> IP=<box-ip>"; exit 2; }
	@hosts="$(ANSIBLE_DIR)/inventories/$(ENV)/hosts.yml"; \
	 if ! grep -q "REPLACE_ME_box_ip" "$$hosts"; then \
	    current="$$(awk '/ansible_host:/ {print $$2; exit}' "$$hosts")"; \
	    echo "$(ENV) hosts.yml carries no sentinel (ansible_host: $$current) — make ans-unset ENV=$(ENV) first"; \
	    exit 2; \
	 fi; \
	 sed -i '' 's/REPLACE_ME_box_ip/$(IP)/' "$$hosts"; \
	 echo "wired: $(ENV) ansible_host -> $(IP)"

ans-unset:
	$(call require_ansible_env,ans-unset)
	@git restore --staged --worktree -- "$(ANSIBLE_DIR)/inventories/$(ENV)/hosts.yml" 2>/dev/null \
	    || git restore --worktree -- "$(ANSIBLE_DIR)/inventories/$(ENV)/hosts.yml"; \
	 echo "unwired: $(ENV) hosts.yml restored to the committed sentinel"

# Standalone and inventory-free BY DESIGN (no ENV, no -i): the client playbook
# must never read the deployment inventories.
client-mac:
	$(call ensure_control_dirs)
	ANSIBLE_LOG_PATH="$${ANSIBLE_LOG_PATH:-$(ANS_LOG_DIR)/client-mac-$(ANS_LOG_STAMP).log}" \
	uv run ansible-playbook $(ANSIBLE_DIR)/client-talkwithme-mac.yml $(ANS_VERBOSITY) $(ANS_ARGS)

ssh-tunnel:
	$(call require_ansible_env,ssh-tunnel)
	$(call ensure_control_dirs)
	@host="$$(awk '/ansible_host:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/$(ENV)/hosts.yml")"; \
	 user="$$(awk '/^ansible_user:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/common_vars.yml")"; \
	 key="$$(awk -F'"' '/^ansible_ssh_private_key_file:/ {print $$2; exit}' "$(ANSIBLE_DIR)/inventories/common_vars.yml")"; \
	 case "$$key" in "~"*) key="$$HOME$${key#\~}";; esac; \
	 test -n "$$host" || { echo "no ansible_host found in inventories/$(ENV)/hosts.yml"; exit 2; }; \
	 case "$$host" in REPLACE_ME*) echo "$(ENV) hosts.yml still carries the REPLACE_ME sentinel"; exit 2;; esac; \
	 test -n "$$key" || { echo "no ansible_ssh_private_key_file found in inventories/common_vars.yml"; exit 2; }; \
	 echo "Tunnel to $$host: llama :8080 / tts :8001 / whisper :8002   (Ctrl-C closes it)"; \
	 ssh -N -o ExitOnForwardFailure=yes -i "$$key" $(SSH_TOFU_OPTS) \
	     -L 8080:127.0.0.1:8080 -L 8001:127.0.0.1:8001 -L 8002:127.0.0.1:8002 "$$user@$$host"
