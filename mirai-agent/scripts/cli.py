#!/usr/bin/env python3
"""Mirai Agent CLI."""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import click
import yaml

from modules.agent.loop import AgentLoop
from modules.trading.binance_client import BinanceClient


def setup_logging() -> None:
    config_path = Path("configs/logging.yaml")
    if config_path.exists():
        with config_path.open() as handle:
            config = yaml.safe_load(handle)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


@click.group()
@click.version_option(version="0.1.0", prog_name="mirai-agent")
def cli() -> None:
    """Mirai Agent - AI-driven trading assistant."""
    setup_logging()


@cli.command()
@click.option("--config", "config_path", default="configs/strategies.yaml", help="Strategy config path")
def dry_run_check(config_path: str) -> None:
    """Perform a dry run of the trading system."""
    click.echo("🔍 Starting dry-run check...")

    try:
        client = BinanceClient(dry_run=True)
        agent = AgentLoop(client)

        click.echo("📡 Testing Binance connection...")
        if client.test_connection():
            click.echo("✅ Binance connection successful")
        else:
            click.echo("❌ Binance connection failed")
            return

        click.echo("🤖 Testing agent decision making...")
        decision = agent.make_decision()
        click.echo(f"📊 Agent decision: {decision}")

        cfg_file = Path(config_path)
        if cfg_file.exists():
            with cfg_file.open() as handle:
                strategies = yaml.safe_load(handle)
            count = len(strategies.get("strategies", []))
            click.echo(f"📋 Loaded {count} strategies")
        else:
            click.echo(f"⚠️ Strategy config not found: {config_path}")

        click.echo("✅ Dry-run check completed successfully!")
    except Exception as exc:  # noqa: BLE001
        click.echo(f"❌ Dry-run check failed: {exc}")


if __name__ == "__main__":
    cli()
