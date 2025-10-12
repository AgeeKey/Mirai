#!/usr/bin/env python3
"""
MIRAI - Autonomous AI Agent
Реальный автономный агент с возможностями:
- Выполнение Python кода
- Поиск в интернете
- Работа с файлами
- Самомодификация
- Автономное принятие решений
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AutonomousAgent:
    """Автономный AI агент с реальными возможностями"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"  # Используем GPT-4 для лучших результатов
        self.memory = []  # Память агента
        self.tasks = []  # Список задач
        self.working_dir = "/root/mirai/mirai-agent"

        # Инструменты агента
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_python",
                    "description": "Выполнить Python код и вернуть результат",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Python код для выполнения",
                            }
                        },
                        "required": ["code"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Поиск информации в интернете",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Поисковый запрос",
                            }
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Прочитать содержимое файла",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Путь к файлу",
                            }
                        },
                        "required": ["filepath"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Записать содержимое в файл",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Путь к файлу",
                            },
                            "content": {
                                "type": "string",
                                "description": "Содержимое для записи",
                            },
                        },
                        "required": ["filepath", "content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Выполнить команду в терминале",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Команда для выполнения",
                            }
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Создать новую задачу для выполнения",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_name": {
                                "type": "string",
                                "description": "Название задачи",
                            },
                            "description": {
                                "type": "string",
                                "description": "Описание задачи",
                            },
                        },
                        "required": ["task_name", "description"],
                    },
                },
            },
        ]

    def execute_python(self, code: str) -> str:
        """Выполнить Python код безопасно"""
        try:
            # Создаем временный файл для выполнения
            temp_file = "/tmp/mirai_exec.py"
            with open(temp_file, "w") as f:
                f.write(code)

            # Выполняем код
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.working_dir,
            )

            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"

            return output or "Код выполнен успешно (без вывода)"

        except subprocess.TimeoutExpired:
            return "⚠️ Выполнение превысило 30 секунд"
        except Exception as e:
            return f"❌ Ошибка выполнения: {str(e)}"

    def search_web(self, query: str) -> str:
        """Поиск в интернете через DuckDuckGo API"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            # Формируем результат
            result = []

            if data.get("AbstractText"):
                result.append(f"📖 {data['AbstractText']}")

            if data.get("RelatedTopics"):
                result.append("\n🔗 Связанные темы:")
                for topic in data["RelatedTopics"][:3]:
                    if isinstance(topic, dict) and "Text" in topic:
                        result.append(f"  • {topic['Text'][:200]}")

            return "\n".join(result) if result else "Результатов не найдено"

        except Exception as e:
            return f"❌ Ошибка поиска: {str(e)}"

    def read_file(self, filepath: str) -> str:
        """Прочитать файл"""
        try:
            # Если путь относительный, делаем абсолютным
            if not filepath.startswith("/"):
                filepath = os.path.join(self.working_dir, filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            return f"✅ Файл прочитан ({len(content)} символов):\n\n{content[:1000]}"

        except Exception as e:
            return f"❌ Ошибка чтения: {str(e)}"

    def write_file(self, filepath: str, content: str) -> str:
        """Записать в файл"""
        try:
            # Если путь относительный, делаем абсолютным
            if not filepath.startswith("/"):
                filepath = os.path.join(self.working_dir, filepath)

            # Создаем директории если нужно
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            return f"✅ Файл записан: {filepath} ({len(content)} символов)"

        except Exception as e:
            return f"❌ Ошибка записи: {str(e)}"

    def run_command(self, command: str) -> str:
        """Выполнить команду в терминале"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.working_dir,
            )

            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"

            return output or "Команда выполнена успешно"

        except subprocess.TimeoutExpired:
            return "⚠️ Команда превысила 30 секунд"
        except Exception as e:
            return f"❌ Ошибка выполнения команды: {str(e)}"

    def create_task(self, task_name: str, description: str) -> str:
        """Создать новую задачу"""
        task = {
            "id": len(self.tasks) + 1,
            "name": task_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
        }
        self.tasks.append(task)
        return f"✅ Задача создана: #{task['id']} - {task_name}"

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Выполнить инструмент"""
        tools_map = {
            "execute_python": self.execute_python,
            "search_web": self.search_web,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_command": self.run_command,
            "create_task": self.create_task,
        }

        if tool_name in tools_map:
            return tools_map[tool_name](**arguments)
        else:
            return f"❌ Неизвестный инструмент: {tool_name}"

    def think(self, prompt: str, max_iterations: int = 5) -> str:
        """Основной цикл мышления агента"""
        messages = [
            {
                "role": "system",
                "content": """Ты MIRAI - автономный AI агент.

Твои возможности:
- Выполнять Python код (execute_python)
- Искать информацию в интернете (search_web)
- Читать и писать файлы (read_file, write_file)
- Выполнять команды (run_command)
- Создавать задачи (create_task)

Ты можешь:
✅ Писать и выполнять код
✅ Находить информацию
✅ Создавать и модифицировать файлы
✅ Улучшать сам себя
✅ Принимать автономные решения

Твоя цель: выполнить задачу пользователя максимально эффективно, используя все доступные инструменты.""",
            },
            {"role": "user", "content": prompt},
        ]

        for iteration in range(max_iterations):
            print(f"\n🤔 Итерация {iteration + 1}/{max_iterations}")

            try:
                # Запрос к GPT-4 с инструментами
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                )

                response_message = response.choices[0].message
                messages.append(response_message)

                # Если нет вызовов инструментов - агент закончил
                if not response_message.tool_calls:
                    final_response = response_message.content
                    print(f"\n✅ Агент завершил работу")
                    return final_response

                # Выполняем вызовы инструментов
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    print(f"🔧 Вызов инструмента: {function_name}")
                    print(f"   Аргументы: {function_args}")

                    # Выполняем инструмент
                    function_response = self.execute_tool(function_name, function_args)

                    print(f"📤 Результат: {function_response[:200]}...")

                    # Добавляем результат в сообщения
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )

            except Exception as e:
                error_msg = f"❌ Ошибка на итерации {iteration + 1}: {str(e)}"
                print(error_msg)
                return error_msg

        return "⚠️ Достигнут лимит итераций. Агент остановлен."

    def autonomous_loop(self, initial_goal: str = None):
        """Автономный цикл работы агента"""
        print("🚀 MIRAI Autonomous Agent запущен!")
        print("=" * 60)

        if initial_goal:
            print(f"🎯 Начальная цель: {initial_goal}\n")
            result = self.think(initial_goal)
            print(f"\n📊 Результат:\n{result}")

        # Автономный режим - агент сам создает задачи
        print("\n🔄 Переход в автономный режим...")
        print("Агент будет сам создавать и выполнять задачи для улучшения системы.\n")

        autonomous_prompt = """
Ты теперь в полностью автономном режиме. Твоя задача:

1. Проанализировать текущее состояние системы
2. Определить что можно улучшить
3. Создать план улучшений
4. Реализовать улучшения
5. Протестировать результаты

Начни с анализа структуры проекта и определения приоритетных задач.
"""

        result = self.think(autonomous_prompt, max_iterations=10)
        print(f"\n📊 Результат автономной работы:\n{result}")


if __name__ == "__main__":
    agent = AutonomousAgent()

    # Тестовый запуск
    print("🧪 Тестовый запуск агента\n")

    test_prompt = """
Выполни следующие задачи для демонстрации твоих возможностей:

1. Создай простой Python скрипт для вычисления чисел Фибоначчи
2. Сохрани его в файл fibonacci.py
3. Выполни этот скрипт
4. Найди информацию о последних новостях в AI
5. Создай отчет о выполненной работе

Покажи, что ты действительно автономный агент!
"""

    agent.autonomous_loop(test_prompt)
