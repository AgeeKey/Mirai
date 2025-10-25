#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║                    MIRAI - Единый Автономный Агент                  ║
║                  One Agent to Rule Them All                         ║
╚══════════════════════════════════════════════════════════════════════╝

MIRAI - это ОДИН мощный агент, который умеет ВСЁ:

🤖 АВТОНОМНОСТЬ
- Сам ставит себе цели и задачи
- Учится на своих ошибках
- Развивается со временем

🖥️ УПРАВЛЕНИЕ КОМПЬЮТЕРОМ
- Управляет мышью и клавиатурой
- Видит экран через GPT-4 Vision
- Открывает приложения и работает с окнами
- Управляет браузером

💻 ПРОГРАММИРОВАНИЕ
- Пишет и выполняет код на Python, JS, C++, Go, Rust
- Работает с GitHub
- Автоматически тестирует код

🌐 ИНТЕРНЕТ
- Ищет информацию в Google
- Работает с веб-страницами
- Взаимодействует с API

📊 ДАННЫЕ
- Работает с базами данных (SQLite, PostgreSQL, MongoDB, Redis)
- Анализирует данные
- Создаёт отчёты

🧠 ПАМЯТЬ И ОБУЧЕНИЕ
- Помнит всё что делал
- Учится на опыте
- Улучшает свои навыки

Автор: MIRAI Team
Дата: 2025-10-24
"""

import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mirai.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UnifiedMiraiAgent:
    """
    Единый автономный агент MIRAI
    
    Объединяет ВСЕ возможности в одном месте:
    - AutonomousAgent (мышление, планирование)
    - DesktopAgent (управление компьютером)
    - MultiLanguageExecutor (выполнение кода)
    - BrowserAutomation (управление браузером)
    - SelfEvolution (саморазвитие)
    - DatabaseManager (работа с БД)
    - GitHubIntegration (работа с GitHub)
    - WebSearch (поиск в интернете)
    - Memory (долговременная память)
    """
    
    def __init__(self, user_id: str = "main_user"):
        """Инициализация единого агента MIRAI"""
        
        logger.info("=" * 70)
        logger.info("MIRAI - Запуск Единого Автономного Агента")
        logger.info("=" * 70)
        
        self.user_id = user_id
        self.start_time = time.time()
        
        # Загрузить API ключи
        self.api_keys = self._load_api_keys()
        self.client = OpenAI(api_key=self.api_keys.get("openai"))
        self.model = "gpt-4o"  # Используем GPT-4o для всего
        
        # Инициализировать все модули
        self._init_modules()
        
        # Состояние агента
        self.is_running = False
        self.current_task = None
        self.tasks_queue = []
        self.completed_tasks = []
        
        logger.info("✓ MIRAI готов к работе!")
        logger.info("Доступные возможности:")
        logger.info(f"   • Управление компьютером: {self.desktop_available}")
        logger.info(f"   • Выполнение кода: {self.code_execution_available}")
        logger.info(f"   • Управление браузером: {self.browser_available}")
        logger.info(f"   • 🌐 Web Scraper (парсинг): {self.web_scraper_available}")
        logger.info(f"   • 🤖 Selenium (автоматизация): {self.selenium_available}")
        logger.info(f"   • Работа с БД: {self.database_available}")
        logger.info(f"   • GitHub: {self.github_available}")
        logger.info(f"   • Веб-поиск: {self.web_search_available}")
        logger.info(f"   • Память: {self.memory_available}")
        logger.info(f"   • Саморазвитие: {self.evolution_available}")
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Загрузить API ключи"""
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                keys = json.load(f)
                return keys
        
        # Fallback на переменные окружения
        return {
            "openai": os.getenv("OPENAI_API_KEY"),
            "github_token": os.getenv("GITHUB_TOKEN")
        }
    
    def _init_modules(self):
        """Инициализировать все модули"""
        
        # 1. Desktop Agent (управление компьютером)
        try:
            from core.desktop_agent_v2 import MiraiDesktopAgent
            self.desktop = MiraiDesktopAgent(
                openai_api_key=self.api_keys.get("openai"),
                enable_safety=True,
                enable_memory=False,  # Используем единую память
                user_id=self.user_id
            )
            self.desktop_available = True
            logger.info("✅ Desktop Agent загружен")
        except Exception as e:
            logger.warning(f"⚠️ Desktop Agent недоступен: {e}")
            self.desktop = None
            self.desktop_available = False
        
        # 2. Multi-Language Executor (выполнение кода)
        try:
            from core.multi_language_executor import MultiLanguageExecutor
            self.code_executor = MultiLanguageExecutor()
            self.code_execution_available = True
            logger.info("✅ Multi-Language Executor загружен")
        except Exception as e:
            logger.warning(f"⚠️ Code Executor недоступен: {e}")
            self.code_executor = None
            self.code_execution_available = False
        
        # 3. Browser Automation (Старый модуль)
        try:
            from core.browser_automation import BrowserAutomation
            self.browser = BrowserAutomation(headless=False)
            self.browser_available = True
            logger.info("✅ Browser Automation загружен")
        except Exception as e:
            logger.warning(f"⚠️ Browser недоступен: {e}")
            self.browser = None
            self.browser_available = False
        
        # 3.1. Web Scraper Agent (НОВЫЙ - для реального парсинга веб-страниц)
        try:
            from core.web_scraper_agent import WebScraperAgent
            self.web_scraper = WebScraperAgent(ai_manager=None)  # AI будем передавать позже
            self.web_scraper_available = True
            logger.info("✅ Web Scraper Agent загружен")
        except Exception as e:
            logger.warning(f"⚠️ Web Scraper недоступен: {e}")
            self.web_scraper = None
            self.web_scraper_available = False
        
        # 3.2. Selenium Browser Agent (НОВЫЙ - для реальной автоматизации браузера)
        try:
            from core.selenium_browser_agent import SeleniumBrowserAgent, SELENIUM_AVAILABLE
            if SELENIUM_AVAILABLE:
                self.selenium_agent = SeleniumBrowserAgent(headless=False)
                self.selenium_available = True
                logger.info("✅ Selenium Browser Agent загружен")
            else:
                self.selenium_agent = None
                self.selenium_available = False
                logger.info("ℹ️ Selenium не установлен (опционально)")
        except Exception as e:
            logger.warning(f"⚠️ Selenium Agent недоступен: {e}")
            self.selenium_agent = None
            self.selenium_available = False
        
        # 4. Database Manager
        try:
            from core.database_manager import DatabaseManager
            self.database = DatabaseManager()
            self.database_available = True
            logger.info("✅ Database Manager загружен")
        except Exception as e:
            logger.warning(f"⚠️ Database недоступен: {e}")
            self.database = None
            self.database_available = False
        
        # 5. GitHub Integration
        try:
            from core.github_integration import GitHubIntegration
            self.github = GitHubIntegration()
            self.github_available = True
            logger.info("✅ GitHub Integration загружен")
        except Exception as e:
            logger.warning(f"⚠️ GitHub недоступен: {e}")
            self.github = None
            self.github_available = False
        
        # 6. Web Search
        try:
            from core.web_search_integration import get_web_search
            self.web_search = get_web_search()
            self.web_search_available = True
            logger.info("✅ Web Search загружен")
        except Exception as e:
            logger.warning(f"⚠️ Web Search недоступен: {e}")
            self.web_search = None
            self.web_search_available = False
        
        # 7. Memory Manager
        try:
            from core.memory_manager import get_memory_manager
            self.memory = get_memory_manager()
            self.session = self.memory.create_session(user_id=self.user_id)
            self.session_id = self.session.id
            self.memory_available = True
            logger.info(f"✅ Memory Manager загружен (session: {self.session_id})")
        except Exception as e:
            logger.warning(f"⚠️ Memory недоступен: {e}")
            self.memory = None
            self.session_id = None
            self.memory_available = False
        
        # 8. Self Evolution
        try:
            from core.self_evolution import SelfEvolutionSystem
            self.evolution = SelfEvolutionSystem()
            self.evolution_available = True
            logger.info("✅ Self Evolution загружен")
        except Exception as e:
            logger.warning(f"⚠️ Self Evolution недоступен: {e}")
            self.evolution = None
            self.evolution_available = False
        
        # Создать инструменты для GPT
        self.tools = self._create_tools()
    
    def _create_tools(self) -> List[Dict]:
        """Создать список всех доступных инструментов для GPT"""
        tools = []
        
        # Desktop tools
        if self.desktop_available:
            tools.extend([
                {
                    "type": "function",
                    "function": {
                        "name": "control_mouse",
                        "description": "Управление мышью: клик, движение, позиция",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["click", "move", "get_position"]},
                                "x": {"type": "integer"},
                                "y": {"type": "integer"},
                                "button": {"type": "string", "enum": ["left", "right", "middle"]}
                            },
                            "required": ["action"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "control_keyboard",
                        "description": "Управление клавиатурой: печать текста, нажатие клавиш",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["type", "press"]},
                                "text": {"type": "string"},
                                "keys": {"type": "string"}
                            },
                            "required": ["action"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "screenshot_and_analyze",
                        "description": "Сделать скриншот экрана и проанализировать через Vision",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string", "description": "Вопрос о скриншоте"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "manage_windows",
                        "description": "Управление окнами приложений: найти, активировать, открыть",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["find", "activate", "open"]},
                                "title": {"type": "string"},
                                "app_name": {"type": "string"}
                            },
                            "required": ["action"]
                        }
                    }
                }
            ])
        
        # Code execution tools
        if self.code_execution_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "execute_code",
                    "description": "Выполнить код на Python, JavaScript, C++, Go, Rust, Bash",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string", "enum": ["python", "javascript", "cpp", "go", "rust", "bash"]},
                            "code": {"type": "string"}
                        },
                        "required": ["language", "code"]
                    }
                }
            })
        
        # Web tools
        if self.web_search_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Искать информацию в интернете через Google",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            })
        
        if self.browser_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "browse_web",
                    "description": "Открыть веб-страницу в браузере",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"}
                        },
                        "required": ["url"]
                    }
                }
            })
        
        # 🌐 НОВЫЙ: Web Scraper - реальный поиск и анализ
        if self.web_scraper_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "search_and_analyze_web",
                    "description": "🌐 РЕАЛЬНЫЙ поиск в Google с ЧТЕНИЕМ и АНАЛИЗОМ найденных сайтов. "
                                   "Агент открывает сайты, читает их содержимое и даёт подробный ответ. "
                                   "Используй это когда пользователь просит найти информацию и рассказать о ней.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Поисковый запрос (например: 'Binance', 'что такое Python')"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "Сколько сайтов прочитать (по умолчанию 3)",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                }
            })
        
        # 🤖 НОВЫЙ: Selenium - автоматизация браузера
        if self.selenium_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "automate_browser",
                    "description": "🤖 Автоматизация браузера через Selenium. "
                                   "Может кликать, вводить текст, делать скриншоты.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["search_google", "screenshot", "visit_url"],
                                "description": "Действие для выполнения"
                            },
                            "query": {
                                "type": "string",
                                "description": "Поисковый запрос (для search_google)"
                            },
                            "url": {
                                "type": "string",
                                "description": "URL для посещения (для visit_url)"
                            }
                        },
                        "required": ["action"]
                    }
                }
            })
        
        # Database tools
        if self.database_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "database_query",
                    "description": "Выполнить SQL запрос к базе данных",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "db_type": {"type": "string", "enum": ["sqlite", "postgresql"]},
                            "query": {"type": "string"}
                        },
                        "required": ["db_type", "query"]
                    }
                }
            })
        
        # GitHub tools
        if self.github_available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "github_action",
                    "description": "Работа с GitHub: создать issue, commit, PR",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "enum": ["create_issue", "commit", "create_pr"]},
                            "repo": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["action"]
                    }
                }
            })
        
        # Utility tools
        tools.extend([
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Прочитать содержимое файла",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"}
                        },
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Записать содержимое в файл",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["filepath", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "wait",
                    "description": "Подождать указанное количество секунд",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "seconds": {"type": "number"}
                        },
                        "required": ["seconds"]
                    }
                }
            }
        ])
        
        return tools
    
    # ═══════════════════════════════════════════════════════════════
    # Главный метод - выполнение задач
    # ═══════════════════════════════════════════════════════════════
    
    def execute_task(self, task: str, max_iterations: int = 30) -> str:
        """
        Выполнить задачу автономно
        
        MIRAI сам решает что делать и в каком порядке
        """
        logger.info("=" * 70)
        logger.info(f"🎯 Новая задача: {task}")
        logger.info("=" * 70)
        
        self.current_task = task
        
        # Сохранить в память
        if self.memory_available:
            from core.memory_manager import Message
            msg = Message(
                session_id=self.session_id,
                role="user",
                content=f"[TASK] {task}",
                timestamp=datetime.now()
            )
            self.memory.add_message(msg)
        
        # Системный промпт
        system_prompt = f"""Ты MIRAI - единый автономный AI агент с полным контролем над компьютером.

ТЫ УМЕЕШЬ ВСЁ:
✅ Управление компьютером (мышь, клавиатура, окна, скриншоты)
✅ Программирование (Python, JS, C++, Go, Rust)
✅ Работа с интернетом (поиск, браузер)
✅ Работа с данными (базы данных, файлы)
✅ GitHub (issues, commits, PRs)
✅ Саморазвитие и обучение

ДОСТУПНЫЕ ИНСТРУМЕНТЫ:
{len(self.tools)} инструментов готовы к использованию

ТВОЯ ЗАДАЧА: {task}

ПРАВИЛА:
1. Работай автономно - сам решай что делать
2. Используй инструменты в правильном порядке
3. Если не получается - пробуй другой способ
4. Учись на ошибках
5. Будь эффективным

Действуй!"""

        messages = [{"role": "system", "content": system_prompt}]
        
        for iteration in range(max_iterations):
            logger.info(f"🔄 Итерация {iteration + 1}/{max_iterations}")
            
            try:
                # Запрос к GPT-4o
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0.7
                )
                
                response_message = response.choices[0].message
                messages.append(response_message)
                
                # Если нет tool calls - задача завершена
                if not response_message.tool_calls:
                    result = response_message.content or "Задача выполнена"
                    logger.info(f"✅ Завершено: {result}")
                    
                    # Сохранить результат
                    if self.memory_available:
                        from core.memory_manager import Message
                        result_msg = Message(
                            session_id=self.session_id,
                            role="assistant",
                            content=f"[RESULT] {result}",
                            timestamp=datetime.now()
                        )
                        self.memory.add_message(result_msg)
                    
                    self.completed_tasks.append({
                        "task": task,
                        "result": result,
                        "iterations": iteration + 1,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return result
                
                # Выполнить tool calls
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"🔧 {function_name}({function_args})")
                    
                    # Выполнить функцию
                    result = self._execute_tool(function_name, function_args)
                    
                    logger.info(f"📤 {result[:100]}...")
                    
                    # Добавить результат
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result
                    })
            
            except Exception as e:
                error = f"❌ Ошибка на итерации {iteration + 1}: {e}"
                logger.error(error, exc_info=True)
                return error
        
        return "⚠️ Лимит итераций достигнут. Задача не завершена."
    
    def _execute_tool(self, name: str, args: Dict[str, Any]) -> str:
        """Выполнить инструмент"""
        
        try:
            # Desktop tools
            if name == "control_mouse":
                action = args.get("action")
                if action == "click":
                    return self.desktop.click_at_position(args.get("x"), args.get("y"), button=args.get("button", "left"))
                elif action == "move":
                    return self.desktop.move_mouse(args.get("x"), args.get("y"))
                elif action == "get_position":
                    return self.desktop.get_mouse_position()
            
            elif name == "control_keyboard":
                action = args.get("action")
                if action == "type":
                    return self.desktop.type_text(args.get("text"))
                elif action == "press":
                    return self.desktop.press_key(args.get("keys"))
            
            elif name == "screenshot_and_analyze":
                self.desktop.take_screenshot()
                return self.desktop.analyze_screenshot(args.get("question", "Что на скриншоте?"))
            
            elif name == "manage_windows":
                action = args.get("action")
                if action == "find":
                    return self.desktop.find_window(args.get("title"))
                elif action == "activate":
                    return self.desktop.activate_window(args.get("title"))
                elif action == "open":
                    return self.desktop.open_application(args.get("app_name"))
            
            # Code execution
            elif name == "execute_code":
                return self.code_executor.execute(args.get("language"), args.get("code"))
            
            # Web tools
            elif name == "search_web":
                results = self.web_search.search(args.get("query"))
                return json.dumps(results, ensure_ascii=False)
            
            elif name == "browse_web":
                self.browser.navigate(args.get("url"))
                return f"✅ Открыт: {args.get('url')}"
            
            # 🌐 НОВЫЙ: Web Scraper - реальный поиск и анализ
            elif name == "search_and_analyze_web":
                return asyncio.run(self._search_and_analyze_web(
                    args.get("query"),
                    args.get("num_results", 3)
                ))
            
            # 🤖 НОВЫЙ: Selenium - автоматизация браузера  
            elif name == "automate_browser":
                return asyncio.run(self._automate_browser(
                    args.get("action"),
                    args.get("query"),
                    args.get("url")
                ))
            
            # Database
            elif name == "database_query":
                return self.database.execute_query(args.get("db_type"), args.get("query"))
            
            # GitHub
            elif name == "github_action":
                action = args.get("action")
                if action == "create_issue":
                    return self.github.create_issue(args.get("repo"), args.get("title"), args.get("description"))
            
            # File operations
            elif name == "read_file":
                with open(args.get("filepath"), 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif name == "write_file":
                with open(args.get("filepath"), 'w', encoding='utf-8') as f:
                    f.write(args.get("content"))
                return f"✅ Записано в {args.get('filepath')}"
            
            # Utility
            elif name == "wait":
                time.sleep(args.get("seconds"))
                return f"✅ Ожидание {args.get('seconds')}с"
            
            else:
                return f"❌ Неизвестный инструмент: {name}"
        
        except Exception as e:
            logger.error(f"Ошибка выполнения {name}: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # НОВЫЕ МЕТОДЫ: Реальная автоматизация браузера
    # ═══════════════════════════════════════════════════════════════
    
    async def _search_and_analyze_web(self, query: str, num_results: int = 3) -> str:
        """
        🌐 РЕАЛЬНЫЙ поиск в Google с чтением и анализом сайтов.
        
        Args:
            query: Поисковый запрос
            num_results: Количество сайтов для анализа
            
        Returns:
            Подробный ответ с анализом найденной информации
        """
        logger.info(f"🌐 Реальный поиск и анализ: {query}")
        
        try:
            # Умное извлечение поискового запроса
            clean_query = self.web_scraper.extract_search_query(query)
            logger.info(f"🔍 Очищенный запрос: {clean_query}")
            
            # Выполняем поиск и анализ
            result = await self.web_scraper.search_and_analyze(
                clean_query,
                num_results=num_results,
                analyze=True  # Включаем AI анализ
            )
            
            if not result['success']:
                return f"❌ Ошибка поиска: {result.get('error', 'Неизвестная ошибка')}"
            
            # Формируем подробный ответ
            response_parts = [
                f"🔍 **Поиск выполнен**: {clean_query}",
                f"📊 **Найдено результатов**: {result['summary']['total_results']}",
                f"📄 **Прочитано сайтов**: {result['summary']['scraped_pages']}",
                "",
                "📋 **Найденные источники**:"
            ]
            
            # Список источников
            for i, res in enumerate(result['search_results'][:5], 1):
                response_parts.append(f"{i}. {res['title']}")
                response_parts.append(f"   🔗 {res['url']}")
                if res.get('snippet'):
                    response_parts.append(f"   📝 {res['snippet'][:100]}...")
            
            # AI анализ если есть
            if result.get('analysis'):
                response_parts.extend([
                    "",
                    "🧠 **АНАЛИЗ ИНФОРМАЦИИ**:",
                    "─" * 50,
                    result['analysis'],
                    "─" * 50
                ])
            
            # Контент для справки
            if result['scraped_content']:
                response_parts.append("")
                response_parts.append("📚 **Прочитанный контент** (для справки):")
                for i, content in enumerate(result['scraped_content'][:2], 1):
                    response_parts.append(f"\n{i}. **{content['title']}**")
                    response_parts.append(f"   {content['content'][:300]}...")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"❌ Ошибка search_and_analyze_web: {e}", exc_info=True)
            return f"❌ Ошибка: {str(e)}"
    
    async def _automate_browser(
        self,
        action: str,
        query: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """
        🤖 Автоматизация браузера через Selenium.
        
        Args:
            action: Действие (search_google, screenshot, visit_url)
            query: Поисковый запрос для search_google
            url: URL для visit_url
            
        Returns:
            Результат выполнения действия
        """
        logger.info(f"🤖 Автоматизация браузера: {action}")
        
        try:
            # Инициализируем браузер если нужно
            if not self.selenium_agent.driver:
                await self.selenium_agent.initialize()
            
            if action == "search_google":
                if not query:
                    return "❌ Не указан поисковый запрос"
                
                # Выполняем поиск
                result = await self.selenium_agent.search_google(query)
                
                if not result['success']:
                    return f"❌ Ошибка поиска: {result.get('error')}"
                
                # Формируем ответ
                response = [
                    f"✅ Поиск в Google выполнен: {query}",
                    f"📊 Найдено результатов: {result['count']}",
                    "",
                    "📋 Результаты:"
                ]
                
                for i, res in enumerate(result['results'][:5], 1):
                    response.append(f"{i}. {res['title']}")
                    response.append(f"   🔗 {res['url']}")
                
                return "\n".join(response)
            
            elif action == "screenshot":
                filepath = await self.selenium_agent.take_screenshot()
                if filepath:
                    return f"✅ Скриншот сохранён: {filepath}"
                else:
                    return "❌ Не удалось создать скриншот"
            
            elif action == "visit_url":
                if not url:
                    return "❌ Не указан URL"
                
                content = await self.selenium_agent.visit_and_read(url)
                if content:
                    return f"✅ Страница загружена: {url}\n\n📄 Контент (первые 500 символов):\n{content[:500]}..."
                else:
                    return f"❌ Не удалось загрузить {url}"
            
            else:
                return f"❌ Неизвестное действие: {action}"
        
        except Exception as e:
            logger.error(f"❌ Ошибка automate_browser: {e}", exc_info=True)
            return f"❌ Ошибка: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════════
    # Автономный режим - сам ставит себе задачи
    # ═══════════════════════════════════════════════════════════════
    
    async def run_autonomous(self):
        """Автономный режим - MIRAI сам выбирает что делать"""
        logger.info("🤖 Запуск автономного режима...")
        logger.info("MIRAI будет сам выбирать задачи и развиваться")
        
        self.is_running = True
        
        while self.is_running:
            try:
                # Спросить у себя - что делать дальше?
                next_task = self._decide_next_task()
                
                if next_task:
                    logger.info(f"📋 MIRAI решил: {next_task}")
                    result = self.execute_task(next_task)
                    logger.info(f"📊 Результат: {result[:100]}...")
                
                # Пауза перед следующей задачей
                await asyncio.sleep(60)  # 1 минута
            
            except KeyboardInterrupt:
                logger.info("⚠️ Остановка автономного режима")
                self.is_running = False
                break
            
            except Exception as e:
                logger.error(f"Ошибка в автономном режиме: {e}", exc_info=True)
                await asyncio.sleep(60)
    
    def _decide_next_task(self) -> Optional[str]:
        """Решить какую задачу выполнить следующей"""
        
        # Собрать информацию о текущем состоянии
        state = {
            "completed_tasks": len(self.completed_tasks),
            "uptime": time.time() - self.start_time,
            "available_tools": len(self.tools)
        }
        
        # Спросить GPT-4o что делать
        prompt = f"""Ты MIRAI - автономный агент. Реши какую задачу выполнить следующей.

ТВОЁ СОСТОЯНИЕ:
- Выполнено задач: {state['completed_tasks']}
- Работаю: {state['uptime']:.0f} секунд
- Доступно инструментов: {state['available_tools']}

ВОЗМОЖНОСТИ:
- Управление компьютером
- Программирование
- Интернет
- Базы данных
- Саморазвитие

Предложи ОДНУ конкретную задачу которую стоит выполнить прямо сейчас.
Задача должна быть:
1. Полезной для развития
2. Выполнимой с текущими инструментами
3. Интересной

Ответь только текстом задачи, без объяснений."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=200
            )
            
            task = response.choices[0].message.content.strip()
            return task if task else None
        
        except Exception as e:
            logger.error(f"Ошибка выбора задачи: {e}")
            return None
    
    # ═══════════════════════════════════════════════════════════════
    # Статистика и состояние
    # ═══════════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict:
        """Получить текущий статус агента"""
        return {
            "running": self.is_running,
            "current_task": self.current_task,
            "completed_tasks": len(self.completed_tasks),
            "uptime": time.time() - self.start_time,
            "capabilities": {
                "desktop": self.desktop_available,
                "code_execution": self.code_execution_available,
                "browser": self.browser_available,
                "database": self.database_available,
                "github": self.github_available,
                "web_search": self.web_search_available,
                "memory": self.memory_available,
                "evolution": self.evolution_available
            }
        }
    
    def stop(self):
        """Остановить агента"""
        logger.info("🛑 Остановка MIRAI...")
        self.is_running = False


# ═══════════════════════════════════════════════════════════════════
# CLI интерфейс
# ═══════════════════════════════════════════════════════════════════

def main():
    """Главная функция"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                    MIRAI - Единый Автономный Агент                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Создать агента
        mirai = UnifiedMiraiAgent()
        
        print("\n" + "=" * 70)
        print("📋 МЕНЮ")
        print("=" * 70)
        print("1. Выполнить задачу")
        print("2. Автономный режим (MIRAI сам выбирает задачи)")
        print("3. Статус")
        print("4. Выход")
        print()
        
        while True:
            choice = input("Выбери действие (1-4): ").strip()
            
            if choice == "1":
                # Ручная задача
                print("\n" + "-" * 70)
                task = input("🎯 Задача для MIRAI: ").strip()
                
                if task:
                    print("\n🤔 MIRAI думает и выполняет...")
                    print("-" * 70)
                    
                    result = mirai.execute_task(task)
                    
                    print("\n" + "=" * 70)
                    print("📊 РЕЗУЛЬТАТ:")
                    print("=" * 70)
                    print(result)
                    print("=" * 70)
            
            elif choice == "2":
                # Автономный режим
                print("\n🤖 Запуск автономного режима...")
                print("MIRAI будет сам выбирать задачи. Нажми Ctrl+C для остановки")
                print("-" * 70)
                
                try:
                    asyncio.run(mirai.run_autonomous())
                except KeyboardInterrupt:
                    print("\n⚠️ Автономный режим остановлен")
            
            elif choice == "3":
                # Статус
                status = mirai.get_status()
                print("\n" + "=" * 70)
                print("📊 СТАТУС MIRAI")
                print("=" * 70)
                print(f"Работает: {status['running']}")
                print(f"Текущая задача: {status['current_task']}")
                print(f"Выполнено задач: {status['completed_tasks']}")
                print(f"Время работы: {status['uptime']:.0f} секунд")
                print(f"\nВозможности:")
                for cap, available in status['capabilities'].items():
                    emoji = "✅" if available else "❌"
                    print(f"  {emoji} {cap}")
                print("=" * 70)
            
            elif choice == "4":
                # Выход
                print("\n👋 До свидания!")
                mirai.stop()
                break
            
            else:
                print("❌ Неверный выбор. Попробуй снова.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано пользователем")
        return 1
    
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        logger.error("Critical error", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
