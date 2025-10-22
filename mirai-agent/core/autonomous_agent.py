#!/usr/bin/env python3
"""
MIRAI - Autonomous AI Agent
Реальный автономный агент с возможностями:
- Выполнение Python кода
- Выполнение JavaScript, C++, Go, Rust, Bash
- Поиск в интернете
- Работа с файлами
- Работа с базами данных (SQLite, PostgreSQL, MongoDB, Redis)
- Самомодификация
- Автономное принятие решений
"""

import asyncio
import json
import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Import memory manager for persistent storage
try:
    from core.memory_manager import MemoryManager, Message

    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    logging.warning("MemoryManager not available. Running without persistent memory.")

load_dotenv()

logger = logging.getLogger(__name__)


class AutonomousAgent:
    """Автономный AI агент с реальными возможностями"""

    def __init__(self, user_id: str = "system"):
        # Загружаем API ключ из configs/api_keys.json
        import json
        from pathlib import Path

        config_path = Path(__file__).parent.parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        api_key = config.get("openai") or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Используем GPT-4 для лучших результатов
        self.memory = []  # Память агента (старая, для обратной совместимости)

        # Initialize persistent memory manager
        self.user_id = user_id
        self.session_id = None
        if MEMORY_AVAILABLE:
            try:
                self.memory_manager = MemoryManager()
                session = self.memory_manager.create_session(user_id=user_id)
                self.session_id = session.id  # Store session ID as string
                logger.info(f"🧠 Memory initialized: session {self.session_id}")
            except Exception as e:
                logger.error(f"Failed to initialize MemoryManager: {e}")
                self.memory_manager = None
        else:
            self.memory_manager = None

        # Новые возможности
        try:
            from core.database_manager import DatabaseManager
            from core.github_integration import GitHubIntegration
            from core.multi_language_executor import MultiLanguageExecutor
            from core.web_search_integration import get_web_search

            self.multi_lang = MultiLanguageExecutor()
            self.db_manager = DatabaseManager()
            self.github = GitHubIntegration()
            self.web_search = get_web_search()
            self.has_advanced_features = True
            logger.info("✅ Advanced features loaded (including Web Search)")
        except ImportError as e:
            logger.warning(f"Some advanced features not available: {e}")
            self.multi_lang = None
            self.db_manager = None
            self.github = None
            self.web_search = None
            self.has_advanced_features = False
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
                    "name": "execute_code",
                    "description": "Выполнить код на любом языке: Python, JavaScript, C++, Go, Rust, Bash",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Код для выполнения",
                            },
                            "language": {
                                "type": "string",
                                "description": "Язык программирования: python, javascript, cpp, go, rust, bash",
                            },
                        },
                        "required": ["code", "language"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "database_query",
                    "description": "Выполнить запрос к базе данных (SQLite, PostgreSQL, MongoDB, Redis)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "db_type": {
                                "type": "string",
                                "description": "Тип БД: sqlite, postgres, mongodb, redis",
                            },
                            "operation": {
                                "type": "string",
                                "description": "Операция: query, find, insert, update, get, set",
                            },
                            "params": {
                                "type": "object",
                                "description": "Параметры запроса",
                            },
                        },
                        "required": ["db_type", "operation"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "github_action",
                    "description": "Выполнить действие с GitHub: list_repos, create_repo, create_issue, search_repos, get_user_info, get_repo_content (читать файлы из любых публичных репозиториев)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Действие: list_repos, create_repo, create_issue, search_repos, get_user_info, get_repo_content",
                            },
                            "params": {
                                "type": "object",
                                "description": "Параметры действия: для get_repo_content нужны owner, repo, path",
                            },
                        },
                        "required": ["action"],
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
        """Поиск в интернете через OpenAI Web Search (реальный интернет!)"""
        try:
            if self.web_search:
                logger.info(f"🔍 Using OpenAI Web Search: {query}")
                result = self.web_search.quick_search(query)
                return f"🌐 Результаты поиска в интернете:\n\n{result}"
            else:
                # Fallback на DuckDuckGo API
                logger.info(f"🔍 Using DuckDuckGo fallback: {query}")
                url = "https://api.duckduckgo.com/"
                params = {
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1,
                }

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
            logger.error(f"❌ Search error: {e}")
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

    def execute_code(self, code: str, language: str) -> str:
        """Выполнить код на любом языке"""
        if not self.has_advanced_features:
            return "❌ Многоязыковая поддержка не доступна. Используйте execute_python для Python кода."

        try:
            # Используем asyncio для выполнения
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.multi_lang.execute_code(code, language)
            )
            loop.close()

            if result["success"]:
                output = f"✅ Код {language} выполнен успешно ({result['execution_time']}s)\n\n"
                if result["output"]:
                    output += f"Вывод:\n{result['output']}"
                return output
            else:
                return f"❌ Ошибка выполнения {language}:\n{result['error']}"
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"

    def database_query(self, db_type: str, operation: str, params: dict = None) -> str:
        """Выполнить запрос к базе данных"""
        if not self.has_advanced_features:
            return "❌ Менеджер баз данных не доступен."

        try:
            params = params or {}
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if db_type == "sqlite":
                query = params.get("query", "SELECT 1")
                result = loop.run_until_complete(
                    self.db_manager.sqlite_query(query, params.get("params"))
                )

            elif db_type == "postgres":
                query = params.get("query", "SELECT version()")
                result = loop.run_until_complete(
                    self.db_manager.postgres_query(query, params.get("params"))
                )

            elif db_type == "mongodb":
                if operation == "find":
                    result = loop.run_until_complete(
                        self.db_manager.mongodb_find(
                            params.get("collection", "test"),
                            params.get("query", {}),
                            params.get("limit", 100),
                        )
                    )
                elif operation == "insert":
                    result = loop.run_until_complete(
                        self.db_manager.mongodb_insert(
                            params.get("collection", "test"), params.get("document", {})
                        )
                    )
                else:
                    result = [
                        {"error": f"Операция {operation} не поддерживается для MongoDB"}
                    ]

            elif db_type == "redis":
                if operation == "get":
                    value = loop.run_until_complete(
                        self.db_manager.redis_get(params.get("key", ""))
                    )
                    result = [{"key": params.get("key"), "value": value}]
                elif operation == "set":
                    success = loop.run_until_complete(
                        self.db_manager.redis_set(
                            params.get("key", ""),
                            params.get("value", ""),
                            params.get("expire"),
                        )
                    )
                    result = [{"success": success}]
                else:
                    result = [
                        {"error": f"Операция {operation} не поддерживается для Redis"}
                    ]
            else:
                result = [{"error": f"База данных {db_type} не поддерживается"}]

            loop.close()

            return f"✅ Запрос к {db_type} выполнен:\n{json.dumps(result, indent=2, ensure_ascii=False)}"
        except Exception as e:
            return f"❌ Ошибка запроса к {db_type}: {str(e)}"

    def github_action(self, action: str, params: dict = None) -> str:
        """Выполнить действие с GitHub"""
        if not self.has_advanced_features or not self.github:
            return "❌ GitHub интеграция не доступна."

        if not self.github.is_authenticated():
            return "❌ GitHub не авторизован. Добавьте GITHUB_TOKEN в configs/api_keys.json"

        try:
            params = params or {}

            if action == "get_user_info":
                result = self.github.get_user_info()
                return f"✅ GitHub пользователь:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            elif action == "list_repos":
                username = params.get("username")
                limit = params.get("limit", 10)
                result = self.github.list_repos(username, limit)
                return f"✅ Репозитории:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            elif action == "create_repo":
                name = params.get("name", "")
                description = params.get("description", "")
                private = params.get("private", False)
                result = self.github.create_repo(name, description, private)
                return f"✅ Репозиторий создан:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            elif action == "create_issue":
                owner = params.get("owner", "")
                repo = params.get("repo", "")
                title = params.get("title", "")
                body = params.get("body", "")
                result = self.github.create_issue(owner, repo, title, body)
                return f"✅ Issue создан:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            elif action == "search_repos":
                query = params.get("query", "")
                limit = params.get("limit", 10)
                result = self.github.search_repositories(query, limit)
                return f"✅ Поиск репозиториев:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            elif action == "get_repo_content":
                owner = params.get("owner", "")
                repo = params.get("repo", "")
                path = params.get("path", "")
                result = self.github.get_repo_content(owner, repo, path)

                # Если это файл с content, декодируем его
                if isinstance(result, dict) and "content" in result:
                    import base64

                    try:
                        decoded = base64.b64decode(result["content"]).decode("utf-8")
                        return f"✅ Файл {path} из {owner}/{repo}:\n\n{decoded}"
                    except:
                        return f"✅ Файл {path} (бинарный): {result['size']} байт"
                elif isinstance(result, list):
                    # Список файлов в директории
                    files_info = []
                    for item in result:
                        icon = "📁" if item["type"] == "dir" else "📄"
                        files_info.append(f"{icon} {item['name']}")
                    return f"✅ Содержимое {owner}/{repo}/{path}:\n" + "\n".join(
                        files_info[:50]
                    )
                else:
                    return f"✅ Результат:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

            else:
                return f"❌ Действие '{action}' не поддерживается. Доступны: get_user_info, list_repos, create_repo, create_issue, search_repos, get_repo_content"

        except Exception as e:
            return f"❌ Ошибка GitHub: {str(e)}"

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Выполнить инструмент"""
        tools_map = {
            "execute_python": self.execute_python,
            "search_web": self.search_web,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_command": self.run_command,
            "create_task": self.create_task,
            "execute_code": self.execute_code,
            "database_query": self.database_query,
            "github_action": self.github_action,
        }

        if tool_name in tools_map:
            return tools_map[tool_name](**arguments)
        else:
            return f"❌ Неизвестный инструмент: {tool_name}"

    def ask(self, prompt: str) -> str:
        """Простой вопрос к AI без использования инструментов"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, concise, and accurate information.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return content if content else "No response"
        except Exception as e:
            logger.error(f"❌ AI request failed: {e}")
            return f"Error: {str(e)}"

    def think(self, prompt: str, max_iterations: int = 5) -> str:
        """Основной цикл мышления агента"""

        # Store user message in memory
        if self.memory_manager and self.session_id and MEMORY_AVAILABLE:
            try:
                user_message = Message(
                    session_id=self.session_id,
                    role="user",
                    content=prompt,
                    tokens=len(prompt.split()),  # Approximate token count
                )
                self.memory_manager.add_message(user_message)
            except Exception as e:
                logger.warning(f"Failed to store user message: {e}")

        messages = [
            {
                "role": "system",
                "content": """Ты MIRAI - автономный AI агент с расширенными возможностями.

Твои возможности:
- Выполнять код на разных языках (execute_code): Python, JavaScript, TypeScript, C, C++, Go, Rust, Bash
- Выполнять Python код (execute_python) - устаревший метод
- Искать информацию в интернете (search_web)
- Читать и писать файлы (read_file, write_file)
- Выполнять команды (run_command)
- Работать с базами данных (database_query): SQLite, PostgreSQL, Redis, MongoDB
- Работать с GitHub (github_action): list_repos, create_repo, create_issue, search_repos, get_user_info
- Создавать задачи (create_task)

Ты можешь:
✅ Писать и выполнять код на 8 языках
✅ Находить информацию в интернете
✅ Создавать и модифицировать файлы
✅ Работать с разными базами данных
✅ Управлять GitHub репозиториями
✅ Улучшать сам себя
✅ Принимать автономные решения

Твоя цель: выполнить задачу пользователя максимально эффективно, используя все доступные инструменты.""",
            },
            {"role": "user", "content": prompt},
        ]

        final_response = ""
        total_tokens = 0

        for iteration in range(max_iterations):
            logger.info(f"🤔 Итерация {iteration + 1}/{max_iterations}")

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

                # Track tokens
                if hasattr(response, "usage") and response.usage:
                    total_tokens += response.usage.total_tokens

                # Если нет вызовов инструментов - агент закончил
                if not response_message.tool_calls:
                    final_response = response_message.content or ""
                    logger.info(f"✅ Агент завершил работу")

                    # Store AI response in memory
                    if self.memory_manager and self.session_id and MEMORY_AVAILABLE:
                        try:
                            ai_message = Message(
                                session_id=self.session_id,
                                role="assistant",
                                content=final_response,
                                tokens=total_tokens,
                                model=self.model,
                            )
                            self.memory_manager.add_message(ai_message)
                        except Exception as e:
                            logger.warning(f"Failed to store AI response: {e}")

                    return final_response

                # Выполняем вызовы инструментов
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.info(f"🔧 Вызов инструмента: {function_name}")
                    logger.info(f"   Аргументы: {function_args}")

                    # Выполняем инструмент
                    function_response = self.execute_tool(function_name, function_args)

                    logger.info(f"📤 Результат: {function_response[:200]}...")

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
                logger.error(error_msg, exc_info=True)
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
