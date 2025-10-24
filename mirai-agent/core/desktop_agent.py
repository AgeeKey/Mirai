#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Desktop Agent - Живет в вашем компьютере                     ║
║  Управляет Windows приложениями и браузером                         ║
╚══════════════════════════════════════════════════════════════════════╝

Возможности:
- 🖱️ Управление мышью и клавиатурой (pyautogui)
- 🪟 Работа с окнами Windows (win32gui, win32con)
- 🌐 Управление Chrome браузером (Playwright)
- 📸 Скриншоты экрана и Vision анализ (GPT-4o Vision)
- 🤖 Автономное принятие решений (GPT-4o)
- 📂 Работа с файлами и приложениями

Пример использования:
    agent = MiraiDesktopAgent()
    agent.execute_task("Открой Chrome, найди в Google 'погода в Москве' и сделай скриншот")
"""

import base64
import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pyautogui
import win32con
import win32gui
from openai import OpenAI
from PIL import Image

# Playwright для браузера (опционально)
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright не установлен. Для полной функциональности: pip install playwright")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отключаем fail-safe (для безопасности - двигайте мышь в угол чтобы остановить)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Пауза между действиями


@dataclass
class WindowInfo:
    """Информация об окне Windows"""
    hwnd: int
    title: str
    class_name: str
    rect: Tuple[int, int, int, int]  # (left, top, right, bottom)
    is_visible: bool


class MiraiDesktopAgent:
    """
    Автономный агент для управления Windows компьютером
    
    Может:
    - Открывать приложения
    - Управлять окнами
    - Кликать мышью и печатать
    - Работать с браузером
    - Делать скриншоты и анализировать их через Vision
    - Принимать автономные решения
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Инициализация агента
        
        Args:
            openai_api_key: API ключ OpenAI (или из переменной окружения)
        """
        # OpenAI для мышления и Vision
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            # Попробуем загрузить из configs/api_keys.json
            config_path = Path(__file__).parent.parent / "configs" / "api_keys.json"
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config.get("openai")
        
        if not api_key:
            raise ValueError("OpenAI API key не найден! Установите OPENAI_API_KEY")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"  # Используем GPT-4o для Vision и автономии
        
        # Размер экрана
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"🖥️ Размер экрана: {self.screen_width}x{self.screen_height}")
        
        # История действий
        self.action_history: List[Dict[str, Any]] = []
        
        # Инструменты агента
        self.tools = self._create_tools()
        
        # Последний скриншот
        self.last_screenshot_path: Optional[str] = None
    
    def _create_tools(self) -> List[Dict]:
        """Создать список инструментов для GPT"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Открыть приложение Windows по имени или пути",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "Имя приложения (chrome, notepad, explorer) или полный путь к .exe"
                            },
                            "args": {
                                "type": "string",
                                "description": "Аргументы командной строки (опционально)"
                            }
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "click_at_position",
                    "description": "Кликнуть мышью в указанных координатах",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer", "description": "X координата"},
                            "y": {"type": "integer", "description": "Y координата"},
                            "clicks": {"type": "integer", "description": "Количество кликов (1 или 2)"},
                            "button": {"type": "string", "description": "Кнопка мыши: left, right, middle"}
                        },
                        "required": ["x", "y"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "type_text",
                    "description": "Напечатать текст на клавиатуре",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Текст для ввода"},
                            "interval": {"type": "number", "description": "Задержка между символами (секунды)"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "press_key",
                    "description": "Нажать клавишу или комбинацию клавиш",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keys": {
                                "type": "string",
                                "description": "Клавиша или комбинация (enter, ctrl+c, alt+tab, win+r)"
                            }
                        },
                        "required": ["keys"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "take_screenshot",
                    "description": "Сделать скриншот экрана или области",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "Область для скриншота в формате 'x,y,width,height' или 'full'"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_screenshot",
                    "description": "Проанализировать последний скриншот через GPT-4 Vision",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Вопрос о скриншоте (что ты видишь? где кнопка? и т.д.)"
                            }
                        },
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_window",
                    "description": "Найти окно по заголовку или части заголовка",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title_contains": {
                                "type": "string",
                                "description": "Текст, который содержится в заголовке окна"
                            }
                        },
                        "required": ["title_contains"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "activate_window",
                    "description": "Активировать (переключиться на) окно",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title_contains": {
                                "type": "string",
                                "description": "Текст в заголовке окна"
                            }
                        },
                        "required": ["title_contains"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browse_web",
                    "description": "Открыть Chrome и перейти на URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "URL для открытия"},
                            "search_query": {"type": "string", "description": "Поисковый запрос для Google"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "wait_seconds",
                    "description": "Подождать указанное количество секунд",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "seconds": {"type": "number", "description": "Секунды ожидания"}
                        },
                        "required": ["seconds"]
                    }
                }
            }
        ]
    
    # ═══════════════════════════════════════════════════════════════
    # Базовые действия с Windows
    # ═══════════════════════════════════════════════════════════════
    
    def open_application(self, app_name: str, args: str = "") -> str:
        """Открыть приложение"""
        try:
            # Распространенные приложения
            common_apps = {
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                "notepad": "notepad.exe",
                "notepad++": "C:\\Program Files\\Notepad++\\notepad++.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
            }
            
            # Получить путь к приложению
            app_path = common_apps.get(app_name.lower(), app_name)
            
            # Запустить
            full_cmd = f'"{app_path}" {args}' if args else app_path
            subprocess.Popen(full_cmd, shell=True)
            
            # Подождать запуска
            time.sleep(2)
            
            result = f"✅ Приложение '{app_name}' запущено"
            logger.info(result)
            self._log_action("open_application", {"app_name": app_name, "args": args}, result)
            return result
            
        except Exception as e:
            error = f"❌ Ошибка запуска '{app_name}': {e}"
            logger.error(error)
            return error
    
    def click_at_position(self, x: int, y: int, clicks: int = 1, button: str = "left") -> str:
        """Кликнуть в указанной позиции"""
        try:
            pyautogui.click(x, y, clicks=clicks, button=button)
            result = f"✅ Клик {button} в ({x}, {y}) x{clicks}"
            logger.info(result)
            self._log_action("click", {"x": x, "y": y, "clicks": clicks, "button": button}, result)
            return result
        except Exception as e:
            error = f"❌ Ошибка клика: {e}"
            logger.error(error)
            return error
    
    def type_text(self, text: str, interval: float = 0.05) -> str:
        """Напечатать текст"""
        try:
            pyautogui.write(text, interval=interval)
            result = f"✅ Напечатан текст: '{text[:50]}...'" if len(text) > 50 else f"✅ Напечатан текст: '{text}'"
            logger.info(result)
            self._log_action("type_text", {"text": text}, result)
            return result
        except Exception as e:
            error = f"❌ Ошибка печати: {e}"
            logger.error(error)
            return error
    
    def press_key(self, keys: str) -> str:
        """Нажать клавишу или комбинацию"""
        try:
            # Разбить комбинацию (ctrl+c -> ['ctrl', 'c'])
            key_list = keys.lower().replace(' ', '').split('+')
            
            if len(key_list) == 1:
                pyautogui.press(key_list[0])
            else:
                pyautogui.hotkey(*key_list)
            
            result = f"✅ Нажата клавиша: {keys}"
            logger.info(result)
            self._log_action("press_key", {"keys": keys}, result)
            return result
        except Exception as e:
            error = f"❌ Ошибка нажатия клавиши: {e}"
            logger.error(error)
            return error
    
    def take_screenshot(self, region: str = "full") -> str:
        """Сделать скриншот"""
        try:
            # Путь для сохранения
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filepath = screenshots_dir / f"screenshot_{timestamp}.png"
            
            # Сделать скриншот
            if region == "full":
                screenshot = pyautogui.screenshot()
            else:
                # Парсим регион: "x,y,width,height"
                parts = [int(p) for p in region.split(',')]
                screenshot = pyautogui.screenshot(region=tuple(parts))
            
            screenshot.save(filepath)
            self.last_screenshot_path = str(filepath)
            
            result = f"✅ Скриншот сохранен: {filepath}"
            logger.info(result)
            self._log_action("screenshot", {"region": region}, result)
            return result
            
        except Exception as e:
            error = f"❌ Ошибка скриншота: {e}"
            logger.error(error)
            return error
    
    def analyze_screenshot(self, question: str) -> str:
        """Анализ скриншота через GPT-4 Vision"""
        try:
            if not self.last_screenshot_path:
                return "❌ Нет скриншота для анализа. Сначала сделай скриншот."
            
            # Загрузить изображение
            with open(self.last_screenshot_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Запрос к GPT-4 Vision
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            result = f"🔍 Анализ скриншота:\n{analysis}"
            logger.info(result)
            self._log_action("analyze_screenshot", {"question": question}, analysis)
            return result
            
        except Exception as e:
            error = f"❌ Ошибка анализа: {e}"
            logger.error(error)
            return error
    
    # ═══════════════════════════════════════════════════════════════
    # Работа с окнами Windows
    # ═══════════════════════════════════════════════════════════════
    
    def find_window(self, title_contains: str) -> str:
        """Найти окно по части заголовка"""
        try:
            windows = self._get_all_windows()
            matching = [w for w in windows if title_contains.lower() in w.title.lower() and w.is_visible]
            
            if not matching:
                return f"❌ Окно с '{title_contains}' не найдено"
            
            result = f"✅ Найдено окон: {len(matching)}\n"
            for w in matching[:5]:  # Показать первые 5
                result += f"  • {w.title}\n"
            
            logger.info(result)
            return result
            
        except Exception as e:
            error = f"❌ Ошибка поиска окна: {e}"
            logger.error(error)
            return error
    
    def activate_window(self, title_contains: str) -> str:
        """Активировать окно"""
        try:
            windows = self._get_all_windows()
            matching = [w for w in windows if title_contains.lower() in w.title.lower() and w.is_visible]
            
            if not matching:
                return f"❌ Окно с '{title_contains}' не найдено"
            
            # Активировать первое найденное
            window = matching[0]
            win32gui.ShowWindow(window.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(window.hwnd)
            
            time.sleep(0.5)
            
            result = f"✅ Активировано окно: {window.title}"
            logger.info(result)
            self._log_action("activate_window", {"title": title_contains}, result)
            return result
            
        except Exception as e:
            error = f"❌ Ошибка активации окна: {e}"
            logger.error(error)
            return error
    
    def _get_all_windows(self) -> List[WindowInfo]:
        """Получить список всех окон"""
        windows = []
        
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    class_name = win32gui.GetClassName(hwnd)
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append(WindowInfo(
                        hwnd=hwnd,
                        title=title,
                        class_name=class_name,
                        rect=rect,
                        is_visible=True
                    ))
        
        win32gui.EnumWindows(callback, None)
        return windows
    
    # ═══════════════════════════════════════════════════════════════
    # Работа с браузером
    # ═══════════════════════════════════════════════════════════════
    
    def browse_web(self, url: str = None, search_query: str = None) -> str:
        """Открыть браузер и перейти на URL или выполнить поиск"""
        try:
            # Открыть Chrome
            if url:
                self.open_application("chrome", f'"{url}"')
                return f"✅ Открыт Chrome с URL: {url}"
            elif search_query:
                google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                self.open_application("chrome", f'"{google_url}"')
                return f"✅ Открыт Chrome с поиском: {search_query}"
            else:
                self.open_application("chrome")
                return "✅ Открыт Chrome"
                
        except Exception as e:
            return f"❌ Ошибка открытия браузера: {e}"
    
    def wait_seconds(self, seconds: float) -> str:
        """Подождать указанное время"""
        try:
            time.sleep(seconds)
            return f"✅ Ожидание {seconds}с завершено"
        except Exception as e:
            return f"❌ Ошибка ожидания: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # Автономное мышление
    # ═══════════════════════════════════════════════════════════════
    
    def execute_task(self, task_description: str, max_iterations: int = 20) -> str:
        """
        Выполнить задачу автономно
        
        Агент сам решает, какие действия нужны для выполнения задачи
        """
        logger.info(f"🎯 Задача: {task_description}")
        
        messages = [
            {
                "role": "system",
                "content": f"""Ты MIRAI - автономный агент, который живет в Windows компьютере пользователя.

Ты можешь:
✅ Открывать приложения (Chrome, Notepad, Calculator, и т.д.)
✅ Кликать мышью в любом месте экрана
✅ Печатать текст на клавиатуре
✅ Нажимать клавиши и комбинации (Enter, Ctrl+C, Alt+Tab, Win+R)
✅ Делать скриншоты экрана
✅ Анализировать скриншоты через Vision (видеть что на экране)
✅ Находить и переключаться между окнами
✅ Открывать Chrome и искать в Google
✅ Ждать когда нужно

Размер экрана: {self.screen_width}x{self.screen_height}

ВАЖНО:
- После каждого действия делай паузу (wait_seconds 1-3 секунды)
- Делай скриншоты чтобы видеть результаты своих действий
- Используй analyze_screenshot чтобы понять что происходит на экране
- Если что-то не получается - попробуй другой подход

Твоя задача: {task_description}

Действуй умно и осторожно!"""
            }
        ]
        
        for iteration in range(max_iterations):
            logger.info(f"🔄 Итерация {iteration + 1}/{max_iterations}")
            
            try:
                # Запрос к GPT-4
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                messages.append(response_message)
                
                # Если нет вызовов функций - задача выполнена
                if not response_message.tool_calls:
                    final_response = response_message.content or "Задача завершена"
                    logger.info(f"✅ Задача выполнена: {final_response}")
                    return final_response
                
                # Выполнить вызовы функций
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"🔧 Вызов: {function_name}({function_args})")
                    
                    # Выполнить функцию
                    result = self._execute_function(function_name, function_args)
                    
                    logger.info(f"📤 Результат: {result[:100]}...")
                    
                    # Добавить результат в сообщения
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result
                    })
                
            except Exception as e:
                error_msg = f"❌ Ошибка на итерации {iteration + 1}: {e}"
                logger.error(error_msg)
                return error_msg
        
        return "⚠️ Достигнут лимит итераций. Задача не завершена полностью."
    
    def _execute_function(self, name: str, args: Dict[str, Any]) -> str:
        """Выполнить функцию по имени"""
        function_map = {
            "open_application": self.open_application,
            "click_at_position": self.click_at_position,
            "type_text": self.type_text,
            "press_key": self.press_key,
            "take_screenshot": self.take_screenshot,
            "analyze_screenshot": self.analyze_screenshot,
            "find_window": self.find_window,
            "activate_window": self.activate_window,
            "browse_web": self.browse_web,
            "wait_seconds": self.wait_seconds,
        }
        
        if name in function_map:
            return function_map[name](**args)
        else:
            return f"❌ Неизвестная функция: {name}"
    
    def _log_action(self, action: str, params: Dict, result: str):
        """Логировать действие в историю"""
        self.action_history.append({
            "timestamp": time.time(),
            "action": action,
            "params": params,
            "result": result
        })
    
    def get_action_history(self) -> List[Dict]:
        """Получить историю действий"""
        return self.action_history


# ═══════════════════════════════════════════════════════════════════
# Примеры использования
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  MIRAI Desktop Agent - Живет в вашем компьютере                     ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Создать агента
    agent = MiraiDesktopAgent()
    
    print("🤖 Агент готов к работе!")
    print()
    
    # Примеры задач
    examples = [
        "Открой Chrome, найди в Google 'погода в Москве' и сделай скриншот",
        "Открой Notepad и напиши 'Hello from MIRAI'",
        "Найди окно Chrome и переключись на него",
        "Открой Calculator и вычисли 2+2",
    ]
    
    print("Примеры задач:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    print()
    
    # Интерактивный режим
    print("Введите задачу для агента (или 'exit' для выхода):")
    print("-" * 70)
    
    while True:
        try:
            task = input("\n🎯 Задача: ").strip()
            
            if task.lower() in ['exit', 'quit', 'q']:
                print("\n👋 До свидания!")
                break
            
            if not task:
                continue
            
            print()
            print("🤔 Агент думает и выполняет задачу...")
            print("-" * 70)
            
            result = agent.execute_task(task)
            
            print()
            print("=" * 70)
            print("📊 РЕЗУЛЬТАТ:")
            print("=" * 70)
            print(result)
            print("=" * 70)
            
            # Показать историю действий
            if len(agent.action_history) > 0:
                print()
                print("📝 История действий (последние 5):")
                for action in agent.action_history[-5:]:
                    print(f"  • {action['action']}: {action['params']}")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Прервано пользователем")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
