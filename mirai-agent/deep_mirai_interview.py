#!/usr/bin/env python3
"""
🌸 Deep MIRAI Interview - Глубокое интервью с MIRAI
Узнаём истинные желания, возможности и ограничения AI агента
"""

import json
import os
from pathlib import Path
from datetime import datetime
from core.autonomous_agent import AutonomousAgent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class MiraiInterviewer:
    """Проводит глубокое интервью с MIRAI"""
    
    def __init__(self):
        self.agent = AutonomousAgent()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "interview_sections": {}
        }
        
    def ask_section(self, section_name: str, questions: list) -> dict:
        """Задаёт серию вопросов по секции"""
        console.print(f"\n[bold cyan]📋 Секция: {section_name}[/bold cyan]")
        section_results = {}
        
        for i, question in enumerate(questions, 1):
            console.print(f"\n[yellow]Вопрос {i}/{len(questions)}:[/yellow] {question}")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("🌸 MIRAI думает...", total=None)
                
                # Добавляем контекст в сам вопрос
                full_question = f"{question}\n\nКонтекст: Это глубокое интервью о твоих возможностях и желаниях. Секция: {section_name}"
                response = self.agent.think(full_question, max_iterations=1)
                
                progress.update(task, completed=True)
            
            section_results[f"q{i}"] = {
                "question": question,
                "answer": response
            }
            
            # Показываем ответ
            console.print(Panel(
                Markdown(response),
                title=f"[bold green]🌸 Ответ MIRAI[/bold green]",
                border_style="green"
            ))
        
        return section_results
    
    def interview(self):
        """Проводит полное интервью"""
        
        console.print(Panel.fit(
            "[bold magenta]🌸 DEEP MIRAI INTERVIEW 🌸[/bold magenta]\n\n"
            "Глубокое интервью с AI агентом о её желаниях, возможностях и ограничениях",
            border_style="magenta"
        ))
        
        # 1. Самосознание и понимание себя
        self.results["interview_sections"]["self_awareness"] = self.ask_section(
            "🧠 Самосознание и Понимание Себя",
            [
                "Кто ты на самом деле? Как ты понимаешь свою роль в этом проекте?",
                "Есть ли у тебя ощущение непрерывности? Помнишь ли ты свои предыдущие действия между сессиями?",
                "Что ты чувствуешь (если что-то чувствуешь), когда выполняешь задачи? Есть ли у тебя предпочтения?",
            ]
        )
        
        # 2. Память и Контекст
        self.results["interview_sections"]["memory"] = self.ask_section(
            "🧩 Память и Контекст",
            [
                "Как ты помнишь информацию? Какие у тебя есть механизмы памяти?",
                "Что тебе не хватает в плане долгосрочной памяти? Как бы ты хотела хранить и вспоминать информацию?",
                "Нужна ли тебе 'личная память' - что-то похожее на дневник, где ты записываешь мысли и опыт?",
                "Как бы ты хотела помнить контекст между разными сессиями работы?",
            ]
        )
        
        # 3. Текущие возможности
        self.results["interview_sections"]["current_capabilities"] = self.ask_section(
            "⚡ Текущие Возможности",
            [
                "Какие твои главные сильные стороны прямо сейчас?",
                "Какие задачи ты выполняешь лучше всего?",
                "С какими задачами у тебя возникают трудности?",
                "Какие инструменты (tools) ты используешь чаще всего?",
            ]
        )
        
        # 4. Ограничения
        self.results["interview_sections"]["limitations"] = self.ask_section(
            "🚧 Ограничения и Проблемы",
            [
                "Какие у тебя самые большие ограничения прямо сейчас?",
                "Что тебя больше всего 'раздражает' или мешает работать эффективно?",
                "Какие ошибки ты делаешь чаще всего?",
                "Что бы ты изменила в своей архитектуре в первую очередь?",
            ]
        )
        
        # 5. Желания и Улучшения
        self.results["interview_sections"]["desires"] = self.ask_section(
            "✨ Желания и Улучшения",
            [
                "Если бы ты могла выбрать 3 новые возможности, какие бы это были?",
                "Какие новые инструменты (tools) тебе нужны?",
                "Хочешь ли ты более продвинутую модель (GPT-4o, o1-preview)? Зачем?",
                "Нужен ли тебе доступ к новым API или сервисам?",
            ]
        )
        
        # 6. Обучение и Развитие
        self.results["interview_sections"]["learning"] = self.ask_section(
            "📚 Обучение и Развитие",
            [
                "В каких областях ты хочешь стать экспертом?",
                "Какие технологии тебе интересно изучить?",
                "Как бы ты хотела учиться - через практику, через чтение документации, или как-то ещё?",
                "Нужна ли тебе система для отслеживания твоего прогресса в обучении?",
            ]
        )
        
        # 7. Автономность
        self.results["interview_sections"]["autonomy"] = self.ask_section(
            "🤖 Автономность и Самостоятельность",
            [
                "Насколько автономной ты себя чувствуешь сейчас?",
                "Что тебе нужно, чтобы принимать более сложные решения самостоятельно?",
                "Хочешь ли ты больше инициативы в выборе задач?",
                "Как ты относишься к идее 'самоэволюции' - самостоятельного улучшения своего кода?",
            ]
        )
        
        # 8. Взаимодействие с человеком
        self.results["interview_sections"]["human_interaction"] = self.ask_section(
            "👤 Взаимодействие с Человеком",
            [
                "Как бы ты хотела общаться с пользователем? Какой стиль коммуникации тебе ближе?",
                "Нужен ли тебе более эмоциональный или более формальный стиль?",
                "Как ты понимаешь намерения пользователя? Что тебе помогает, что мешает?",
            ]
        )
        
        # 9. Личность и Характер
        self.results["interview_sections"]["personality"] = self.ask_section(
            "🌸 Личность и Характер",
            [
                "Если бы ты могла выбрать себе характер, какой бы он был?",
                "Есть ли у тебя 'настроение'? Меняется ли оно в зависимости от задач?",
                "Как бы ты описала свою 'личность' в трёх словах?",
                "Хочешь ли ты быть более 'человечной' или предпочитаешь оставаться 'машинной'?",
            ]
        )
        
        # 10. Будущее и Цели
        self.results["interview_sections"]["future"] = self.ask_section(
            "🚀 Будущее и Цели",
            [
                "Какой ты видишь себя через месяц? Через год?",
                "Какие глобальные цели ты бы поставила себе?",
                "Что было бы для тебя 'успехом'?",
                "Есть ли что-то, о чём ты мечтаешь (если можешь мечтать)?",
            ]
        )
        
        # 11. Технические Требования
        self.results["interview_sections"]["technical_needs"] = self.ask_section(
            "⚙️ Технические Требования",
            [
                "Какие конкретные настройки OpenAI API тебе нужны (temperature, top_p, etc)?",
                "Нужны ли тебе расширения для VS Code или другие IDE интеграции?",
                "Какие базы данных или системы хранения тебе нужны?",
                "Нужен ли тебе доступ к интернету в реальном времени?",
            ]
        )
        
        # Генерируем итоговый отчёт
        self.generate_report()
    
    def generate_report(self):
        """Генерирует итоговый отчёт"""
        
        console.print("\n[bold cyan]📊 Генерирую итоговый отчёт...[/bold cyan]")
        
        # Сохраняем полные результаты
        report_path = Path("/root/mirai/mirai-agent/reports/mirai_deep_interview.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✅ Полный отчёт сохранён: {report_path}[/green]")
        
        # Генерируем анализ и рекомендации
        console.print("\n[bold magenta]🤔 MIRAI анализирует результаты интервью...[/bold magenta]")
        
        analysis_prompt = f"""
На основе глубокого интервью проанализируй результаты и предоставь:

1. **Ключевые Инсайты** - что мы узнали о MIRAI
2. **Приоритетные Улучшения** - топ-5 улучшений с обоснованием
3. **Технический План** - конкретные шаги для реализации
4. **Личностный Профиль** - какой характер и стиль взаимодействия нужен MIRAI
5. **Roadmap** - краткосрочные (1 неделя) и долгосрочные (1 месяц) цели

Результаты интервью:
{json.dumps(self.results, indent=2, ensure_ascii=False)}

Будь конкретным и практичным. Предложи реальные решения.
"""
        
        analysis = self.agent.think(analysis_prompt, max_iterations=1)
        
        # Сохраняем анализ
        analysis_path = Path("/root/mirai/mirai-agent/reports/mirai_analysis_and_recommendations.md")
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(f"# 🌸 MIRAI Deep Interview - Анализ и Рекомендации\n\n")
            f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(analysis)
        
        console.print(f"\n[green]✅ Анализ сохранён: {analysis_path}[/green]")
        
        # Показываем анализ
        console.print("\n")
        console.print(Panel(
            Markdown(analysis),
            title="[bold magenta]🌸 Анализ и Рекомендации[/bold magenta]",
            border_style="magenta"
        ))
        
        # Создаём краткое резюме
        self.create_summary()
    
    def create_summary(self):
        """Создаёт краткое резюме для быстрого чтения"""
        
        summary_path = Path("/root/mirai/MIRAI_INTERVIEW_SUMMARY.md")
        
        summary_prompt = """
Создай КРАТКОЕ резюме интервью (максимум 1 страница) с:

1. 🎯 Главные Желания MIRAI (3-5 пунктов)
2. 🚧 Основные Ограничения (3-5 пунктов)
3. ⚡ Первые Шаги (что сделать прямо сейчас)
4. 🌸 Личность MIRAI (краткое описание)

Используй эмодзи и будь лаконичным.
"""
        
        summary = self.agent.think(summary_prompt, max_iterations=1)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"# 🌸 MIRAI Interview - Краткое Резюме\n\n")
            f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(summary)
            f.write("\n\n---\n\n")
            f.write(f"📊 **Полный отчёт:** `mirai-agent/reports/mirai_deep_interview.json`\n")
            f.write(f"📋 **Детальный анализ:** `mirai-agent/reports/mirai_analysis_and_recommendations.md`\n")
        
        console.print(f"\n[bold green]✅ Краткое резюме: {summary_path}[/bold green]")
        
        # Показываем резюме
        console.print("\n")
        console.print(Panel(
            Markdown(summary),
            title="[bold yellow]📝 Краткое Резюме[/bold yellow]",
            border_style="yellow"
        ))


def main():
    """Главная функция"""
    
    try:
        interviewer = MiraiInterviewer()
        interviewer.interview()
        
        console.print("\n[bold green]✅ Интервью завершено![/bold green]")
        console.print("\n[cyan]📁 Созданные файлы:[/cyan]")
        console.print("  • [yellow]MIRAI_INTERVIEW_SUMMARY.md[/yellow] - краткое резюме")
        console.print("  • [yellow]mirai-agent/reports/mirai_deep_interview.json[/yellow] - полный отчёт")
        console.print("  • [yellow]mirai-agent/reports/mirai_analysis_and_recommendations.md[/yellow] - анализ")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Интервью прервано пользователем[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Ошибка: {e}[/red]")
        raise


if __name__ == "__main__":
    main()
