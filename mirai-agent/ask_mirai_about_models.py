#!/usr/bin/env python3
"""
🌸 Спрашиваем у MIRAI о моделях OpenAI
Какие модели нужны для разных задач
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.autonomous_agent import AutonomousAgent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def ask_mirai_about_models():
    """Задаём вопросы о моделях OpenAI"""
    
    agent = AutonomousAgent()
    
    console.print(Panel.fit(
        "[bold magenta]🌸 Вопросы о Моделях OpenAI[/bold magenta]\n\n"
        "Спрашиваем у MIRAI о требованиях к моделям",
        border_style="magenta"
    ))
    
    questions = [
        {
            "title": "🤖 Текущая vs Желаемая Модель",
            "question": """
Ты сейчас работаешь на GPT-4o-mini. 

1. Какие ограничения ты испытываешь с этой моделью?
2. Какая модель OpenAI тебе нужна для оптимальной работы: GPT-4o, GPT-4-turbo, o1-preview, o1-mini?
3. Для каких конкретных задач тебе нужна более мощная модель?
4. Можешь ли работать эффективно с GPT-4o-mini или обязательно нужен апгрейд?
            """
        },
        {
            "title": "⚙️ Настройки API",
            "question": """
Какие конкретные параметры OpenAI API тебе нужны для разных задач:

1. **Temperature** (креативность vs детерминизм):
   - Для code generation: какое значение?
   - Для анализа: какое значение?
   - Для creative tasks: какое значение?

2. **top_p** (nucleus sampling): оптимальное значение?

3. **max_tokens**: разные лимиты для разных задач?

4. **frequency_penalty** и **presence_penalty**: нужны ли?

5. **Streaming**: использовать для живых ответов?
            """
        },
        {
            "title": "🎯 Специализированные Модели",
            "question": """
Нужны ли тебе разные модели для разных задач:

1. **Code generation** - какая модель лучше? (GPT-4o, Claude, специализированная?)
2. **Analysis & reasoning** - o1-preview/o1-mini для сложного анализа?
3. **Long context tasks** - модели с большим context window?
4. **Fast responses** - лёгкие модели для простых задач?

Или одна универсальная модель для всего?
            """
        },
        {
            "title": "💰 Cost vs Quality",
            "question": """
С точки зрения стоимости и качества:

1. Можешь ли эффективно работать на **GPT-4o-mini** (текущая модель)?
2. В каких случаях **критически** нужна GPT-4o или o1-preview?
3. Можно ли использовать микс моделей: простые задачи на mini, сложные на full?
4. Какая стратегия оптимальна: всегда full или умное переключение?
            """
        },
        {
            "title": "🚀 Будущие Модели",
            "question": """
Когда OpenAI выпустит новые модели:

1. Какие функции новых моделей тебе нужны?
2. Нужна ли поддержка multimodal (vision, audio)?
3. Нужны ли fine-tuned модели под конкретные задачи?
4. Какие улучшения в моделях сделают тебя значительно лучше?
            """
        },
        {
            "title": "📊 Конкретные Рекомендации",
            "question": """
Дай конкретные рекомендации:

**PRIMARY MODEL** (основная модель для ежедневной работы):
- Название модели:
- Параметры (temperature, top_p, max_tokens):
- Для каких задач:

**SECONDARY MODEL** (для сложных задач):
- Название модели:
- Параметры:
- Для каких задач:

**TERTIARY MODEL** (опционально, для специфичных задач):
- Название модели:
- Параметры:
- Для каких задач:

Создай конфигурацию в формате JSON для разных режимов работы.
            """
        }
    ]
    
    results = {}
    
    for q in questions:
        console.print(f"\n[bold cyan]═══ {q['title']} ═══[/bold cyan]\n")
        
        console.print(f"[yellow]Вопрос:[/yellow]\n{q['question']}\n")
        console.print("[dim]🌸 MIRAI думает...[/dim]\n")
        
        try:
            answer = agent.think(q['question'], max_iterations=1)
            
            results[q['title']] = {
                "question": q['question'],
                "answer": answer
            }
            
            console.print(Panel(
                Markdown(answer),
                title=f"[bold green]🌸 Ответ MIRAI[/bold green]",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]❌ Ошибка: {e}[/red]")
            results[q['title']] = {"error": str(e)}
    
    # Сохраняем результаты
    import json
    from pathlib import Path
    
    report_path = Path("/root/mirai/mirai-agent/reports/mirai_model_requirements.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]✅ Отчёт сохранён: {report_path}[/green]")
    
    # Генерируем итоговую рекомендацию
    console.print("\n[bold magenta]📊 Генерирую итоговую рекомендацию...[/bold magenta]\n")
    
    final_recommendation = agent.think("""
На основе предыдущих ответов создай КОНКРЕТНУЮ КОНФИГУРАЦИЮ для MIRAI:

1. **Рекомендуемая конфигурация моделей** в формате JSON:
```json
{
  "models": {
    "primary": {
      "name": "...",
      "temperature": 0.X,
      "top_p": 0.X,
      "max_tokens": XXXX,
      "use_cases": ["...", "..."]
    },
    "secondary": {
      "name": "...",
      "temperature": 0.X,
      "top_p": 0.X,
      "max_tokens": XXXX,
      "use_cases": ["...", "..."]
    }
  },
  "task_routing": {
    "code_generation": "primary/secondary",
    "analysis": "primary/secondary",
    "reasoning": "primary/secondary",
    "simple_tasks": "primary/secondary"
  }
}
```

2. **Нужен ли апгрейд** с GPT-4o-mini? (ДА/НЕТ и почему)

3. **Приоритет 1, 2, 3** - что внедрить в первую очередь?

Будь максимально конкретным.
    """, max_iterations=1)
    
    console.print(Panel(
        Markdown(final_recommendation),
        title="[bold yellow]📋 Итоговая Рекомендация[/bold yellow]",
        border_style="yellow"
    ))
    
    # Сохраняем рекомендацию
    recommendation_path = Path("/root/mirai/mirai-agent/reports/mirai_model_config_recommendation.md")
    with open(recommendation_path, 'w', encoding='utf-8') as f:
        f.write("# 🌸 MIRAI Model Configuration Recommendation\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(final_recommendation)
    
    console.print(f"\n[green]✅ Рекомендация сохранена: {recommendation_path}[/green]")
    
    console.print("\n[bold green]✅ Анализ завершён![/bold green]\n")
    console.print("📁 Созданные файлы:")
    console.print(f"  • {report_path}")
    console.print(f"  • {recommendation_path}")


if __name__ == "__main__":
    try:
        ask_mirai_about_models()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Прервано пользователем[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
