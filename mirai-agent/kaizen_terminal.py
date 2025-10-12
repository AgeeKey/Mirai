#!/usr/bin/env python3
"""
🤖 KAIZEN Terminal - Interactive CLI Interface
Based on: yoda, PyInquirer, prompt-toolkit
KAIZEN живёт в терминале, MIRAI работает в фоне
"""

import sys
import asyncio
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/root/mirai/mirai-agent')

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import print as rprint

from core.autonomous_agent import AutonomousAgent
from core.cicd_monitor import CICDMonitor
import json


class KaizenTerminal:
    """Интерактивный терминальный интерфейс для KAIZEN"""
    
    def __init__(self):
        self.console = Console()
        self.kaizen = AutonomousAgent()
        
        # Load config
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)
        
        self.monitor = CICDMonitor(
            github_token=config["GITHUB_TOKEN"],
            repo_owner="AgeeKey",
            repo_name="mirai-showcase"
        )
        
        # Commands autocomplete
        self.commands = WordCompleter([
            'help', 'exit', 'quit',
            'status', 'cicd', 'health',
            'mirai', 'ask mirai', 'consult',
            'metrics', 'logs', 'runs',
            'improve', 'optimize',
            'clear', 'history'
        ], ignore_case=True)
        
        # Prompt style
        self.style = Style.from_dict({
            'prompt': '#00aa00 bold',
            'user': '#00aaff',
        })
        
        # Session with history
        self.session = PromptSession(
            history=FileHistory('/tmp/kaizen_terminal_history.txt'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.commands,
            style=self.style,
        )
        
        self.running = True
    
    def show_welcome(self):
        """Приветственное сообщение"""
        welcome = """
╔══════════════════════════════════════════════════════════════════════╗
║          🤖 KAIZEN TERMINAL - Interactive AI Interface               ║
╚══════════════════════════════════════════════════════════════════════╝

Привет! Я KAIZEN (改善), старший брат MIRAI.

MIRAI работает автономно в фоне, а я здесь чтобы помочь тебе!

📋 Доступные команды:
   • status     - статус систем
   • cicd       - проверить CI/CD
   • mirai      - спросить MIRAI
   • metrics    - показать метрики
   • runs       - последние workflow runs
   • help       - справка
   • exit       - выход

💡 Просто пиши что тебе нужно, я пойму!

改善 - Continuous Improvement
        """
        self.console.print(Panel(welcome, border_style="green"))
    
    def show_help(self):
        """Справка"""
        table = Table(title="🤖 KAIZEN Commands")
        table.add_column("Команда", style="cyan")
        table.add_column("Описание", style="white")
        
        table.add_row("status", "Показать статус всех систем")
        table.add_row("cicd / health", "Проверить здоровье CI/CD")
        table.add_row("mirai [вопрос]", "Спросить совета у MIRAI")
        table.add_row("metrics", "Показать метрики CI/CD")
        table.add_row("runs", "Последние workflow runs")
        table.add_row("logs", "Показать логи MIRAI (автономная работа)")
        table.add_row("improve", "Попросить MIRAI предложить улучшения")
        table.add_row("clear", "Очистить экран")
        table.add_row("help", "Эта справка")
        table.add_row("exit / quit", "Выход")
        
        self.console.print(table)
    
    def cmd_status(self):
        """Статус систем"""
        self.console.print("\n[bold cyan]📊 Проверяю статус систем...[/bold cyan]")
        
        # CI/CD status
        health = self.monitor.check_health()
        
        if health['is_healthy']:
            status_icon = "🟢"
            status_text = "HEALTHY"
            color = "green"
        else:
            status_icon = "🔴"
            status_text = "UNHEALTHY"
            color = "red"
        
        self.console.print(f"\n{status_icon} [bold {color}]CI/CD: {status_text}[/bold {color}]")
        self.console.print(f"   Grade: [bold]{health['grade']}[/bold]")
        self.console.print(f"   Success Rate: {health['metrics']['success_rate']}%")
        self.console.print(f"   Total Runs: {health['metrics']['total_runs']}")
        self.console.print(f"   Failed: {health['metrics']['failed']}")
        
        # MIRAI autonomous service status
        try:
            with open('/tmp/kaizen_mirai_metrics.jsonl', 'r') as f:
                lines = f.readlines()
                if lines:
                    last = json.loads(lines[-1])
                    self.console.print(f"\n🌸 [bold magenta]MIRAI Autonomous Service:[/bold magenta]")
                    self.console.print(f"   Last Cycle: {last['timestamp']}")
                    self.console.print(f"   Cycle #: {last['cycle']}")
                    self.console.print("   Status: 🟢 ACTIVE")
                else:
                    self.console.print("\n🌸 MIRAI: Нет данных")
        except FileNotFoundError:
            self.console.print("\n🌸 MIRAI: Автономный сервис не запущен")
    
    def cmd_cicd(self):
        """Проверить CI/CD"""
        self.console.print("\n[bold cyan]🔍 Проверяю CI/CD pipeline...[/bold cyan]")
        
        health = self.monitor.check_health()
        metrics = health['metrics']
        
        table = Table(title="CI/CD Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Health", health['status'])
        table.add_row("Grade", health['grade'])
        table.add_row("Success Rate", f"{metrics['success_rate']}%")
        table.add_row("Total Runs", str(metrics['total_runs']))
        table.add_row("Successful", str(metrics['successful']))
        table.add_row("Failed", str(metrics['failed']))
        table.add_row("Avg Duration", f"{metrics['avg_duration_minutes']} min")
        
        self.console.print(table)
        
        if not health['is_healthy']:
            self.console.print("\n[bold red]⚠️  Pipeline нездоров! Упавшие workflows:[/bold red]")
            failures = self.monitor.get_failing_workflows()
            for f in failures[:3]:
                self.console.print(f"   ❌ {f['name']} #{f['run_number']}")
    
    def cmd_mirai(self, question: str):
        """Спросить MIRAI"""
        if not question:
            question = "Что делать дальше для улучшения системы?"
        
        self.console.print(f"\n[bold magenta]💭 Консультируюсь с MIRAI...[/bold magenta]")
        self.console.print(f"[dim]Вопрос: {question}[/dim]\n")
        
        # Create MIRAI agent for consultation
        mirai = AutonomousAgent()
        response = mirai.think(question, max_iterations=1)
        
        panel = Panel(
            response,
            title="🌸 MIRAI",
            border_style="magenta"
        )
        self.console.print(panel)
    
    def cmd_metrics(self):
        """Показать метрики"""
        self.console.print("\n[bold cyan]📈 Читаю метрики из истории...[/bold cyan]")
        
        try:
            with open('/tmp/kaizen_mirai_metrics.jsonl', 'r') as f:
                lines = f.readlines()[-10:]  # Last 10
                
            table = Table(title="Last 10 Cycles Metrics")
            table.add_column("Cycle", style="cyan")
            table.add_column("Time", style="white")
            table.add_column("Success %", style="green")
            table.add_column("Failed", style="red")
            
            for line in lines:
                data = json.loads(line)
                time_str = datetime.fromisoformat(data['timestamp']).strftime("%H:%M:%S")
                table.add_row(
                    str(data['cycle']),
                    time_str,
                    f"{data['success_rate']}%",
                    str(data['failed'])
                )
            
            self.console.print(table)
        except FileNotFoundError:
            self.console.print("[yellow]Нет данных метрик[/yellow]")
    
    def cmd_runs(self):
        """Последние runs"""
        self.console.print("\n[bold cyan]🔄 Последние workflow runs...[/bold cyan]")
        
        runs = self.monitor.get_workflow_runs(limit=5)
        
        for run in runs:
            emoji = "✅" if run['conclusion'] == 'success' else "❌" if run['conclusion'] == 'failure' else "⏳"
            self.console.print(f"\n{emoji} [bold]{run['name']}[/bold] #{run['run_number']}")
            self.console.print(f"   Status: {run['status']} → {run['conclusion'] or 'running'}")
            self.console.print(f"   Commit: {run['head_commit']['message'].split(chr(10))[0][:60]}")
    
    def cmd_logs(self):
        """Показать логи MIRAI"""
        self.console.print("\n[bold cyan]📄 Последние 20 строк логов MIRAI:[/bold cyan]\n")
        
        try:
            with open('/tmp/kaizen_mirai.log', 'r') as f:
                lines = f.readlines()[-20:]
            for line in lines:
                print(line, end='')
        except FileNotFoundError:
            self.console.print("[yellow]Логи не найдены[/yellow]")
    
    async def process_command(self, user_input: str):
        """Обработка команды"""
        cmd = user_input.lower().strip()
        
        if cmd in ['exit', 'quit', 'q']:
            self.console.print("\n[bold green]👋 До встречи! 改善[/bold green]\n")
            self.running = False
        
        elif cmd in ['help', 'h', '?']:
            self.show_help()
        
        elif cmd == 'status':
            self.cmd_status()
        
        elif cmd in ['cicd', 'health', 'ci']:
            self.cmd_cicd()
        
        elif cmd.startswith('mirai'):
            question = cmd[5:].strip() if len(cmd) > 5 else ""
            self.cmd_mirai(question)
        
        elif cmd in ['metrics', 'stats']:
            self.cmd_metrics()
        
        elif cmd in ['runs', 'workflows']:
            self.cmd_runs()
        
        elif cmd == 'logs':
            self.cmd_logs()
        
        elif cmd == 'improve':
            self.cmd_mirai("Что можно улучшить в системе? Дай 3 конкретных предложения.")
        
        elif cmd == 'clear':
            self.console.clear()
        
        elif cmd == 'history':
            self.console.print("\n[dim]История в /tmp/kaizen_terminal_history.txt[/dim]")
        
        elif cmd:
            # Свободный вопрос - отправляем KAIZEN AI
            self.console.print(f"\n[bold cyan]🤖 KAIZEN думает...[/bold cyan]\n")
            response = self.kaizen.think(user_input, max_iterations=1)
            
            panel = Panel(
                response,
                title="🤖 KAIZEN",
                border_style="cyan"
            )
            self.console.print(panel)
    
    async def run(self):
        """Главный цикл"""
        self.show_welcome()
        
        while self.running:
            try:
                user_input = await asyncio.to_thread(
                    self.session.prompt,
                    [('class:prompt', '🤖 KAIZEN'), ('class:user', ' > ')]
                )
                
                if user_input.strip():
                    await self.process_command(user_input)
            
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Используй 'exit' для выхода[/yellow]")
            except EOFError:
                break


async def main():
    """Entry point"""
    terminal = KaizenTerminal()
    await terminal.run()


if __name__ == '__main__':
    asyncio.run(main())
