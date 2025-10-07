# Mirai Agent (Modular Layout)

Unified autonomous trading agent with MasterAgent orchestrator and modular codebase.

## Structure

- `core/` – MasterAgent, AI engine, configuration loader.
- `modules/agent/` – autonomous agent logic, safety rules, explainability tools.
- `modules/trading/` – trading loop, brokers, risk engines, strategies.
- `modules/api/` – FastAPI services (main API, trading API, web dashboard) and AI endpoints.
- `modules/security/` – secrets manager and enterprise security utilities.
- `modules/performance/` – performance optimization helpers.
- `modules/telegram_bot/` – Telegram bot / notifier layers.
- `scripts/` – deployment helpers (`run_master_agent.py`, `backup.sh`, `deploy.sh`, `health_check.sh`, setup scripts).
- `data/` – runtime state (databases, logs, backups).
- `configs/` – environment configuration (`production.yaml`, `.env`).

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure secrets
cp .env.template .env
# Prefer environment variables (env-first). Alternatively, create keys file:
# cp configs/api_keys.example.json configs/api_keys.json
# and fill in values. Environment (OPENAI_API_KEY / GROK_API_KEY) has priority.
scripts/setup_secrets.sh

# Run MasterAgent
# Recommended run (ensures package imports):
python -m core.master_agent
```

## Health Checks & Backups

- `scripts/health_check.sh` – checks systemd service and `/health` endpoint.
- `scripts/backup.sh` – archives code and database into `data/backups`.
- `scripts/deploy.sh` – pull & restart services on Linux VPS.

## Development

- `scripts/setup_autonomous_mode.sh` – adds aliases under Linux (mi-start, mi-api, etc.).
- `scripts/activate_autonomous_env.sh` – exports MIRAI environment variables.
- `scripts/cli.py` – lightweight CLI for dry-run checks (`python scripts/cli.py dry-run-check`).

## TODO

- Update legacy shell automation (`scripts/deploy_days_3-7.sh`, etc.) to new module paths.
- Add Ruff/Mypy configs and automated CI pipeline.
