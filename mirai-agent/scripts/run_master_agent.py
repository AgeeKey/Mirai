#!/usr/bin/env python3
"""CLI wrapper for starting Mirai MasterAgent."""

import asyncio

from core.master_agent import MasterAgent


async def main() -> None:
    agent = MasterAgent()
    try:
        await agent.start()
    except KeyboardInterrupt:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
