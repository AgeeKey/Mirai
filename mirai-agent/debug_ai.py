#!/usr/bin/env python3
"""Debug AI Agent responses"""

import sys

sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent

print("Testing AI Agent...")

agent = AutonomousAgent()

prompt = """Research JSON and provide comprehensive documentation:

## OVERVIEW
What is JSON? (3 sentences)

## KEY CONCEPTS
List 3 core features

## BASIC EXAMPLE
Show simple Python code"""

print("\n🤖 Sending prompt to AI...\n")
print("=" * 80)
print(prompt)
print("=" * 80)

response = agent.think(prompt, max_iterations=1)

print("\n📝 AI Response:")
print("=" * 80)
print(response)
print("=" * 80)
print(f"\nResponse length: {len(response)} chars")
