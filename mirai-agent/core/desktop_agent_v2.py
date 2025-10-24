#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Desktop Agent V2 - Полный контроль над компьютером           ║
║  NASA-level Architecture for Desktop Automation                     ║
╚══════════════════════════════════════════════════════════════════════╝

Возможности:
- 🖱️ Управление мышью и клавиатурой (pyautogui + native API)
- 🪟 Работа с окнами (кроссплатформенная)
- 🌐 Браузер автоматизация (интеграция с browser_automation.py)
- 📸 Скриншоты + GPT-4 Vision анализ
- 🔍 OCR для распознавания текста на экране (pytesseract)
- 👁️ Computer Vision для поиска элементов (OpenCV)
- 🤖 Автономное принятие решений (GPT-4o)
- 🧠 Интеграция с RAG и Long-term Memory
- 🔒 Безопасность и ограничения
- 📊 Метрики и логирование

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import base64
import json
import logging
import os
import platform
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import pyautogui
from openai import OpenAI
from PIL import Image, ImageGrab

# OCR
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ pytesseract не установлен. OCR недоступен. Установите: pip install pytesseract")

# Windows-specific
if platform.system() == "Windows":
    try:
        import win32con
        import win32gui
        import win32process
        WINDOWS_API_AVAILABLE = True
    except ImportError:
        WINDOWS_API_AVAILABLE = False
        print("⚠️ pywin32 не установлен. Функции Windows API недоступны.")
else:
    WINDOWS_API_AVAILABLE = False

# MIRAI core imports
try:
    from core.autonomous_agent import AutonomousAgent
    from core.browser_automation import BrowserAutomation
    from core.memory_manager import get_memory_manager, Message
    MIRAI_CORE_AVAILABLE = True
except ImportError:
    MIRAI_CORE_AVAILABLE = False
    print("⚠️ MIRAI core modules не найдены. Работаю в standalone режиме.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Безопасность
pyautogui.FAILSAFE = True  # Двигай мышь в угол экрана чтобы остановить
pyautogui.PAUSE = 0.3  # Пауза между действиями


@dataclass
class ScreenRegion:
    """Область экрана для работы"""
    x: int
    y: int
    width: int
    height: int
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)
    
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)


@dataclass
class WindowInfo:
    """Информация об окне приложения"""
    handle: int  # hwnd на Windows, window ID на Linux
    title: str
    class_name: str = ""
    process_name: str = ""
    rect: Optional[Tuple[int, int, int, int]] = None  # (left, top, right, bottom)
    is_visible: bool = True
    is_minimized: bool = False
    
    def to_region(self) -> Optional[ScreenRegion]:
        """Конвертировать в ScreenRegion"""
        if self.rect:
            left, top, right, bottom = self.rect
            return ScreenRegion(left, top, right - left, bottom - top)
        return None


@dataclass
class DesktopAction:
    """Действие агента на рабочем столе"""
    timestamp: float
    action_type: str  # click, type, screenshot, etc.
    params: Dict[str, Any]
    result: str
    screenshot_path: Optional[str] = None
    duration: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "action_type": self.action_type,
            "params": self.params,
            "result": self.result,
            "screenshot_path": self.screenshot_path,
            "duration": self.duration
        }


class SafetyLimits:
    """Ограничения безопасности для агента"""
    
    # Ограничения на действия
    MAX_CLICKS_PER_MINUTE = 60
    MAX_KEYSTROKES_PER_MINUTE = 300
    MAX_SCREENSHOTS_PER_MINUTE = 30
    
    # Запрещенные зоны экрана (например, кнопка выключения)
    FORBIDDEN_REGIONS: List[ScreenRegion] = []
    
    # Запрещенные приложения для закрытия
    PROTECTED_PROCESSES = ["explorer.exe", "System", "svchost.exe", "csrss.exe"]
    
    # Запрещенные клавиши
    FORBIDDEN_KEYS = ["power", "sleep"]
    
    @classmethod
    def check_action_allowed(cls, action_type: str, params: Dict) -> Tuple[bool, str]:
        """
        Проверить, разрешено ли действие
        
        Returns:
            (allowed, reason)
        """
        # Проверка на запрещенные регионы
        if action_type == "click":
            x, y = params.get("x", 0), params.get("y", 0)
            for region in cls.FORBIDDEN_REGIONS:
                if (region.x <= x <= region.x + region.width and
                    region.y <= y <= region.y + region.height):
                    return False, f"Клик в запрещенной зоне: {region}"
        
        # Проверка на запрещенные клавиши
        if action_type == "press_key":
            keys = params.get("keys", "").lower()
            if any(forbidden in keys for forbidden in cls.FORBIDDEN_KEYS):
                return False, f"Запрещенная клавиша: {keys}"
        
        return True, "OK"


class MiraiDesktopAgent:
    """
    Автономный агент для управления рабочим столом
    
    Архитектура:
    ┌─────────────────────────────────────────────────────────┐
    │                  MIRAI Desktop Agent                    │
    ├─────────────────────────────────────────────────────────┤
    │  Vision & OCR    │  Input Control  │  Window Manager   │
    │  - GPT-4 Vision  │  - Mouse        │  - Find/Activate  │
    │  - pytesseract   │  - Keyboard     │  - Resize/Move    │
    │  - OpenCV        │  - Hotkeys      │  - List/Monitor   │
    ├─────────────────────────────────────────────────────────┤
    │              Autonomous Decision Engine                 │
    │              (GPT-4o + RAG + Memory)                    │
    ├─────────────────────────────────────────────────────────┤
    │        Safety Layer (Limits + Forbidden Actions)        │
    └─────────────────────────────────────────────────────────┘
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        enable_safety: bool = True,
        enable_memory: bool = True,
        screenshots_dir: str = "screenshots",
        user_id: str = "desktop_user"
    ):
        """
        Инициализация Desktop Agent
        
        Args:
            openai_api_key: API ключ OpenAI
            enable_safety: Включить проверки безопасности
            enable_memory: Включить долговременную память
            screenshots_dir: Директория для скриншотов
            user_id: ID пользователя для memory system
        """
        logger.info("🚀 Инициализация MIRAI Desktop Agent V2...")
        
        # API ключ OpenAI
        self.api_key = self._load_api_key(openai_api_key)
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"
        
        # Настройки
        self.enable_safety = enable_safety
        self.enable_memory = enable_memory
        self.user_id = user_id
        
        # Директория для скриншотов
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(exist_ok=True, parents=True)
        
        # Информация о системе
        self.os_type = platform.system()
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"🖥️ ОС: {self.os_type}, Экран: {self.screen_width}x{self.screen_height}")
        
        # Интеграция с MIRAI core
        self.autonomous_agent = None
        self.browser_automation = None
        self.memory_manager = None
        
        if MIRAI_CORE_AVAILABLE:
            try:
                self.autonomous_agent = AutonomousAgent(user_id=user_id)
                self.browser_automation = BrowserAutomation(headless=False)
                if enable_memory:
                    self.memory_manager = get_memory_manager()
                logger.info("✅ MIRAI core интегрирован")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось интегрировать MIRAI core: {e}")
        
        # История действий
        self.action_history: List[DesktopAction] = []
        self.last_screenshot_path: Optional[str] = None
        
        # Счетчики для rate limiting
        self._action_timestamps: Dict[str, List[float]] = {
            "click": [],
            "type": [],
            "screenshot": []
        }
        
        # Инструменты для GPT
        self.tools = self._create_tools()
        
        logger.info("✅ Desktop Agent готов к работе!")
    
    def _load_api_key(self, provided_key: Optional[str]) -> str:
        """Загрузить API ключ OpenAI"""
        # 1. Из параметра
        if provided_key:
            return provided_key
        
        # 2. Из переменной окружения
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key:
            return env_key
        
        # 3. Из configs/api_keys.json
        config_path = Path(__file__).parent.parent / "configs" / "api_keys.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    key = config.get("openai")
                    if key:
                        return key
            except Exception as e:
                logger.warning(f"Не удалось загрузить API ключ из {config_path}: {e}")
        
        raise ValueError(
            "OpenAI API key не найден! Установите:\n"
            "1. OPENAI_API_KEY environment variable\n"
            "2. configs/api_keys.json с ключом 'openai'\n"
            "3. Передайте через параметр openai_api_key"
        )
    
    def _create_tools(self) -> List[Dict]:
        """Создать список инструментов для GPT Function Calling"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "click_at_position",
                    "description": "Кликнуть мышью в указанных координатах экрана",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer", "description": "X координата (0 до screen_width)"},
                            "y": {"type": "integer", "description": "Y координата (0 до screen_height)"},
                            "clicks": {"type": "integer", "description": "Количество кликов (1 или 2)", "default": 1},
                            "button": {"type": "string", "enum": ["left", "right", "middle"], "description": "Кнопка мыши"}
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
                            "interval": {"type": "number", "description": "Задержка между символами (секунды)", "default": 0.05}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "press_key",
                    "description": "Нажать клавишу или комбинацию клавиш (например: enter, ctrl+c, alt+tab)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keys": {"type": "string", "description": "Клавиша или комбинация"}
                        },
                        "required": ["keys"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "take_screenshot",
                    "description": "Сделать скриншот экрана или его области",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {"type": "string", "description": "Область: 'full' или 'x,y,width,height'", "default": "full"}
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
                            "question": {"type": "string", "description": "Вопрос о скриншоте"}
                        },
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_text_on_screen",
                    "description": "Найти текст на экране с помощью OCR",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Текст для поиска"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_image_on_screen",
                    "description": "Найти изображение на экране с помощью Computer Vision",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "image_path": {"type": "string", "description": "Путь к изображению-шаблону"}
                        },
                        "required": ["image_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Открыть приложение по имени или пути",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string", "description": "Имя приложения или путь к .exe"},
                            "args": {"type": "string", "description": "Аргументы командной строки", "default": ""}
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_window",
                    "description": "Найти окно приложения по заголовку",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title_contains": {"type": "string", "description": "Текст в заголовке окна"}
                        },
                        "required": ["title_contains"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "activate_window",
                    "description": "Активировать (переключиться на) окно приложения",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title_contains": {"type": "string", "description": "Текст в заголовке окна"}
                        },
                        "required": ["title_contains"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "move_mouse",
                    "description": "Переместить курсор мыши в указанную позицию",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer", "description": "X координата"},
                            "y": {"type": "integer", "description": "Y координата"},
                            "duration": {"type": "number", "description": "Длительность движения (секунды)", "default": 0.5}
                        },
                        "required": ["x", "y"]
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_mouse_position",
                    "description": "Получить текущую позицию курсора мыши",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]
        
        # Добавить browser tools если доступен
        if self.browser_automation:
            tools.append({
                "type": "function",
                "function": {
                    "name": "browse_web",
                    "description": "Открыть браузер и перейти на URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "URL для открытия"}
                        },
                        "required": ["url"]
                    }
                }
            })
        
        return tools
    
    # ═══════════════════════════════════════════════════════════════
    # Базовые действия - Мышь и клавиатура
    # ═══════════════════════════════════════════════════════════════
    
    def click_at_position(
        self,
        x: int,
        y: int,
        clicks: int = 1,
        button: str = "left"
    ) -> str:
        """Кликнуть в указанной позиции"""
        start_time = time.time()
        
        try:
            # Проверка безопасности
            if self.enable_safety:
                allowed, reason = SafetyLimits.check_action_allowed(
                    "click",
                    {"x": x, "y": y, "clicks": clicks, "button": button}
                )
                if not allowed:
                    return f"❌ Действие запрещено: {reason}"
            
            # Rate limiting
            if not self._check_rate_limit("click", SafetyLimits.MAX_CLICKS_PER_MINUTE):
                return "❌ Превышен лимит кликов в минуту"
            
            # Выполнить клик
            pyautogui.click(x, y, clicks=clicks, button=button)
            
            duration = time.time() - start_time
            result = f"✅ Клик {button} в ({x}, {y}) x{clicks}"
            
            # Логирование
            self._log_action("click", {"x": x, "y": y, "clicks": clicks, "button": button}, result, duration)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка клика: {e}", exc_info=True)
            return f"❌ Ошибка клика: {e}"
    
    def type_text(self, text: str, interval: float = 0.05) -> str:
        """Напечатать текст"""
        start_time = time.time()
        
        try:
            # Rate limiting
            estimated_keystrokes = len(text)
            if not self._check_rate_limit("type", SafetyLimits.MAX_KEYSTROKES_PER_MINUTE, estimated_keystrokes):
                return "❌ Превышен лимит нажатий клавиш в минуту"
            
            # Напечатать
            pyautogui.write(text, interval=interval)
            
            duration = time.time() - start_time
            result = f"✅ Напечатан текст ({len(text)} символов)"
            
            # Логирование (не логируем сам текст для безопасности)
            self._log_action("type_text", {"length": len(text)}, result, duration)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка печати: {e}", exc_info=True)
            return f"❌ Ошибка печати: {e}"
    
    def press_key(self, keys: str) -> str:
        """Нажать клавишу или комбинацию"""
        start_time = time.time()
        
        try:
            # Проверка безопасности
            if self.enable_safety:
                allowed, reason = SafetyLimits.check_action_allowed("press_key", {"keys": keys})
                if not allowed:
                    return f"❌ Действие запрещено: {reason}"
            
            # Разбить комбинацию (ctrl+c -> ['ctrl', 'c'])
            key_list = keys.lower().replace(' ', '').split('+')
            
            if len(key_list) == 1:
                pyautogui.press(key_list[0])
            else:
                pyautogui.hotkey(*key_list)
            
            duration = time.time() - start_time
            result = f"✅ Нажата клавиша: {keys}"
            
            self._log_action("press_key", {"keys": keys}, result, duration)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка нажатия клавиши: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> str:
        """Переместить курсор"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return f"✅ Курсор перемещен в ({x}, {y})"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    def get_mouse_position(self) -> str:
        """Получить позицию курсора"""
        try:
            x, y = pyautogui.position()
            return f"✅ Позиция курсора: ({x}, {y})"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    def wait_seconds(self, seconds: float) -> str:
        """Подождать"""
        try:
            time.sleep(seconds)
            return f"✅ Ожидание {seconds}с завершено"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # Скриншоты и Vision
    # ═══════════════════════════════════════════════════════════════
    
    def take_screenshot(self, region: str = "full") -> str:
        """Сделать скриншот"""
        start_time = time.time()
        
        try:
            # Rate limiting
            if not self._check_rate_limit("screenshot", SafetyLimits.MAX_SCREENSHOTS_PER_MINUTE):
                return "❌ Превышен лимит скриншотов в минуту"
            
            # Имя файла
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            
            # Сделать скриншот
            if region == "full":
                screenshot = pyautogui.screenshot()
            else:
                # Парсим регион: "x,y,width,height"
                parts = [int(p.strip()) for p in region.split(',')]
                if len(parts) != 4:
                    return "❌ Неверный формат региона. Используйте: x,y,width,height"
                screenshot = pyautogui.screenshot(region=tuple(parts))
            
            # Сохранить
            screenshot.save(filepath)
            self.last_screenshot_path = str(filepath)
            
            duration = time.time() - start_time
            result = f"✅ Скриншот: {filepath.name}"
            
            self._log_action("screenshot", {"region": region}, result, duration, str(filepath))
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка скриншота: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    def analyze_screenshot(self, question: str) -> str:
        """Анализ скриншота через GPT-4 Vision"""
        try:
            if not self.last_screenshot_path:
                return "❌ Нет скриншота. Сначала сделай скриншот (take_screenshot)"
            
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
            result = f"🔍 Vision анализ:\n{analysis}"
            
            self._log_action("analyze_screenshot", {"question": question}, analysis)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка анализа: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # OCR и Computer Vision
    # ═══════════════════════════════════════════════════════════════
    
    def find_text_on_screen(self, text: str) -> str:
        """Найти текст на экране с помощью OCR"""
        try:
            if not OCR_AVAILABLE:
                return "❌ OCR недоступен. Установите pytesseract"
            
            # Сделать скриншот
            screenshot = pyautogui.screenshot()
            
            # OCR
            ocr_text = pytesseract.image_to_string(screenshot)
            
            # Поиск текста
            if text.lower() in ocr_text.lower():
                # Найти координаты (упрощенно - через поиск в тексте)
                return f"✅ Текст '{text}' найден на экране\nOCR результат:\n{ocr_text[:200]}..."
            else:
                return f"❌ Текст '{text}' не найден на экране"
            
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}", exc_info=True)
            return f"❌ Ошибка OCR: {e}"
    
    def find_image_on_screen(self, image_path: str) -> str:
        """Найти изображение на экране с помощью OpenCV"""
        try:
            # Проверить существование файла
            if not Path(image_path).exists():
                return f"❌ Файл не найден: {image_path}"
            
            # Загрузить шаблон
            template = cv2.imread(image_path)
            if template is None:
                return f"❌ Не удалось загрузить изображение: {image_path}"
            
            # Скриншот экрана
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Template matching
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Порог совпадения
            threshold = 0.8
            if max_val >= threshold:
                x, y = max_loc
                h, w = template.shape[:2]
                center_x, center_y = x + w // 2, y + h // 2
                
                return f"✅ Изображение найдено в ({center_x}, {center_y}), совпадение: {max_val:.2%}"
            else:
                return f"❌ Изображение не найдено (лучшее совпадение: {max_val:.2%})"
            
        except Exception as e:
            logger.error(f"Ошибка поиска изображения: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # Работа с приложениями и окнами
    # ═══════════════════════════════════════════════════════════════
    
    def open_application(self, app_name: str, args: str = "") -> str:
        """Открыть приложение"""
        try:
            # Распространенные приложения
            common_apps = {
                # Браузеры
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                # Редакторы
                "notepad": "notepad.exe",
                "notepad++": "C:\\Program Files\\Notepad++\\notepad++.exe",
                "vscode": "C:\\Program Files\\Microsoft VS Code\\Code.exe",
                # Системные
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                # Утилиты
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "mspaint": "mspaint.exe",
            }
            
            # Получить путь
            app_path = common_apps.get(app_name.lower(), app_name)
            
            # Запустить
            if args:
                subprocess.Popen(f'"{app_path}" {args}', shell=True)
            else:
                subprocess.Popen(app_path, shell=True)
            
            # Подождать запуска
            time.sleep(2)
            
            result = f"✅ Приложение '{app_name}' запущено"
            self._log_action("open_application", {"app_name": app_name, "args": args}, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка запуска приложения: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    def find_window(self, title_contains: str) -> str:
        """Найти окно по заголовку"""
        try:
            windows = self._get_all_windows()
            matching = [w for w in windows if title_contains.lower() in w.title.lower() and w.is_visible]
            
            if not matching:
                return f"❌ Окно с '{title_contains}' не найдено"
            
            result = f"✅ Найдено окон: {len(matching)}\n"
            for i, w in enumerate(matching[:5], 1):
                result += f"  {i}. {w.title}\n"
            
            return result.strip()
            
        except Exception as e:
            logger.error(f"Ошибка поиска окна: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    def activate_window(self, title_contains: str) -> str:
        """Активировать окно"""
        try:
            windows = self._get_all_windows()
            matching = [w for w in windows if title_contains.lower() in w.title.lower() and w.is_visible]
            
            if not matching:
                return f"❌ Окно с '{title_contains}' не найдено"
            
            # Активировать первое найденное
            window = matching[0]
            
            if WINDOWS_API_AVAILABLE:
                win32gui.ShowWindow(window.handle, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(window.handle)
            else:
                # Кроссплатформенный способ (менее надежный)
                pyautogui.hotkey('alt', 'tab')
            
            time.sleep(0.5)
            
            result = f"✅ Активировано: {window.title}"
            self._log_action("activate_window", {"title": title_contains}, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка активации окна: {e}", exc_info=True)
            return f"❌ Ошибка: {e}"
    
    def _get_all_windows(self) -> List[WindowInfo]:
        """Получить список всех окон"""
        windows = []
        
        if WINDOWS_API_AVAILABLE:
            def callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        try:
                            class_name = win32gui.GetClassName(hwnd)
                            rect = win32gui.GetWindowRect(hwnd)
                            is_minimized = win32gui.IsIconic(hwnd)
                            
                            # Получить имя процесса
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            process_name = ""
                            
                            windows.append(WindowInfo(
                                handle=hwnd,
                                title=title,
                                class_name=class_name,
                                process_name=process_name,
                                rect=rect,
                                is_visible=True,
                                is_minimized=is_minimized
                            ))
                        except Exception:
                            pass
            
            win32gui.EnumWindows(callback, None)
        else:
            # Кроссплатформенная реализация (ограниченная)
            logger.warning("Windows API недоступен, функции работы с окнами ограничены")
        
        return windows
    
    # ═══════════════════════════════════════════════════════════════
    # Интеграция с браузером
    # ═══════════════════════════════════════════════════════════════
    
    def browse_web(self, url: str) -> str:
        """Открыть URL в браузере"""
        try:
            if self.browser_automation:
                # Использовать BrowserAutomation
                self.browser_automation.navigate(url)
                return f"✅ Открыт URL: {url}"
            else:
                # Fallback - открыть через системный браузер
                self.open_application("chrome", f'"{url}"')
                return f"✅ Открыт URL в Chrome: {url}"
        except Exception as e:
            return f"❌ Ошибка: {e}"
    
    # ═══════════════════════════════════════════════════════════════
    # Автономное выполнение задач
    # ═══════════════════════════════════════════════════════════════
    
    def execute_task(self, task_description: str, max_iterations: int = 20) -> str:
        """
        Автономно выполнить задачу на рабочем столе
        
        Args:
            task_description: Описание задачи
            max_iterations: Максимум итераций
        
        Returns:
            Результат выполнения
        """
        logger.info(f"🎯 Задача: {task_description}")
        
        # Сохранить в память
        if self.memory_manager:
            self.memory_manager.add_message(
                user_id=self.user_id,
                role="user",
                content=f"[Desktop Task] {task_description}"
            )
        
        # Системный промпт
        system_prompt = f"""Ты MIRAI Desktop Agent - автономный AI агент, который управляет компьютером пользователя.

ВОЗМОЖНОСТИ:
✅ Управление мышью (click, move, get_position)
✅ Управление клавиатурой (type_text, press_key)
✅ Скриншоты и Vision анализ (take_screenshot, analyze_screenshot)
✅ OCR - распознавание текста (find_text_on_screen)
✅ Computer Vision - поиск изображений (find_image_on_screen)
✅ Управление приложениями (open_application, find_window, activate_window)
✅ Управление браузером (browse_web)
✅ Утилиты (wait_seconds, get_mouse_position)

СИСТЕМА:
- ОС: {self.os_type}
- Экран: {self.screen_width}x{self.screen_height}
- Безопасность: {'Включена' if self.enable_safety else 'Отключена'}

ВАЖНО:
1. После каждого действия делай паузу (wait_seconds 1-3 сек)
2. Используй скриншоты чтобы видеть результат своих действий
3. Используй analyze_screenshot для понимания что на экране
4. Если не получается - попробуй другой подход
5. Будь осторожен с кликами - проверяй координаты

ЗАДАЧА: {task_description}

Действуй умно и осторожно! Решай задачу пошагово."""

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
                    final_response = response_message.content or "Задача завершена"
                    logger.info(f"✅ Задача выполнена: {final_response}")
                    
                    # Сохранить в память
                    if self.memory_manager:
                        self.memory_manager.add_message(
                            user_id=self.user_id,
                            role="assistant",
                            content=f"[Desktop Result] {final_response}"
                        )
                    
                    return final_response
                
                # Выполнить tool calls
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"🔧 Вызов: {function_name}({function_args})")
                    
                    # Выполнить функцию
                    result = self._execute_function(function_name, function_args)
                    
                    logger.info(f"📤 Результат: {result[:100]}...")
                    
                    # Добавить результат
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result
                    })
            
            except Exception as e:
                error_msg = f"❌ Ошибка на итерации {iteration + 1}: {e}"
                logger.error(error_msg, exc_info=True)
                return error_msg
        
        return "⚠️ Достигнут лимит итераций. Задача не завершена полностью."
    
    def _execute_function(self, name: str, args: Dict[str, Any]) -> str:
        """Выполнить функцию по имени"""
        function_map = {
            "click_at_position": self.click_at_position,
            "type_text": self.type_text,
            "press_key": self.press_key,
            "move_mouse": self.move_mouse,
            "get_mouse_position": self.get_mouse_position,
            "take_screenshot": self.take_screenshot,
            "analyze_screenshot": self.analyze_screenshot,
            "find_text_on_screen": self.find_text_on_screen,
            "find_image_on_screen": self.find_image_on_screen,
            "open_application": self.open_application,
            "find_window": self.find_window,
            "activate_window": self.activate_window,
            "browse_web": self.browse_web,
            "wait_seconds": self.wait_seconds,
        }
        
        if name in function_map:
            return function_map[name](**args)
        else:
            return f"❌ Неизвестная функция: {name}"
    
    # ═══════════════════════════════════════════════════════════════
    # Утилиты и логирование
    # ═══════════════════════════════════════════════════════════════
    
    def _check_rate_limit(self, action_type: str, limit_per_minute: int, count: int = 1) -> bool:
        """Проверить rate limit"""
        if not self.enable_safety:
            return True
        
        now = time.time()
        minute_ago = now - 60
        
        # Очистить старые записи
        self._action_timestamps[action_type] = [
            t for t in self._action_timestamps[action_type]
            if t > minute_ago
        ]
        
        # Проверить лимит
        if len(self._action_timestamps[action_type]) + count > limit_per_minute:
            logger.warning(f"Rate limit exceeded for {action_type}")
            return False
        
        # Добавить новые timestamps
        self._action_timestamps[action_type].extend([now] * count)
        return True
    
    def _log_action(
        self,
        action_type: str,
        params: Dict[str, Any],
        result: str,
        duration: float = 0.0,
        screenshot_path: Optional[str] = None
    ):
        """Логировать действие"""
        action = DesktopAction(
            timestamp=time.time(),
            action_type=action_type,
            params=params,
            result=result,
            screenshot_path=screenshot_path,
            duration=duration
        )
        
        self.action_history.append(action)
        logger.info(f"Action logged: {action_type}")
    
    def get_action_history(self, limit: int = 10) -> List[Dict]:
        """Получить историю действий"""
        return [action.to_dict() for action in self.action_history[-limit:]]
    
    def save_action_history(self, filepath: str):
        """Сохранить историю в файл"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.get_action_history(limit=1000), f, indent=2, ensure_ascii=False)
            logger.info(f"История сохранена: {filepath}")
        except Exception as e:
            logger.error(f"Ошибка сохранения истории: {e}")
    
    def collect_learning_data(self) -> Dict[str, Any]:
        """
        Собрать данные для самообучения MIRAI
        
        Анализирует экран, открытые приложения, историю действий
        для улучшения понимания пользовательских паттернов
        """
        logger.info("🧠 MIRAI собирает данные для самообучения...")
        
        learning_data = {
            "timestamp": time.time(),
            "screen_analysis": {},
            "open_windows": [],
            "user_patterns": [],
            "action_insights": [],
            "learning_opportunities": []
        }
        
        try:
            # 1. Анализ экрана через Vision
            screenshot_result = self.take_screenshot()
            if "✅" in screenshot_result:
                vision_analysis = self.analyze_screenshot(
                    "Опиши подробно что ты видишь на экране. "
                    "Какие приложения открыты? Что делает пользователь? "
                    "Есть ли полезная информация для обучения?"
                )
                learning_data["screen_analysis"] = {
                    "description": vision_analysis,
                    "screenshot_path": self.last_screenshot_path
                }
            
            # 2. Анализ открытых окон
            if WINDOWS_API_AVAILABLE:
                windows = self._get_all_windows()
                learning_data["open_windows"] = [
                    {
                        "title": w.title,
                        "class_name": w.class_name,
                        "process_name": w.process_name
                    } for w in windows[:10]  # Ограничим до 10 окон
                ]
            
            # 3. Анализ паттернов действий
            if len(self.action_history) > 5:
                recent_actions = self.action_history[-10:]
                action_types = [a.action_type for a in recent_actions]
                
                # Найти паттерны
                if action_types.count("screenshot") > 3:
                    learning_data["user_patterns"].append("Пользователь часто делает скриншоты")
                
                if action_types.count("click") > 5:
                    learning_data["user_patterns"].append("Пользователь активно кликает мышью")
                
                if "analyze_screenshot" in action_types:
                    learning_data["user_patterns"].append("Пользователь использует Vision анализ")
            
            # 4. Предложения для улучшения
            learning_data["learning_opportunities"] = [
                "Изучить часто используемые приложения",
                "Оптимизировать последовательности действий",
                "Предугадывать следующие действия пользователя",
                "Улучшить понимание контекста экрана"
            ]
            
            # 5. Сохранить в память если доступна
            if self.memory_manager:
                from core.memory_manager import Message
                learning_summary = f"Собраны данные обучения: {len(learning_data['open_windows'])} окон, анализ экрана, {len(learning_data['user_patterns'])} паттернов"
                
                msg = Message(
                    session_id=self.memory_manager.create_session(user_id=self.user_id).id,
                    role="system",
                    content=f"[LEARNING DATA] {learning_summary}",
                    metadata=learning_data
                )
                self.memory_manager.add_message(msg)
            
            logger.info(f"✅ Собрано {len(learning_data)} категорий данных обучения")
            return learning_data
            
        except Exception as e:
            logger.error(f"Ошибка сбора данных обучения: {e}")
            return {"error": str(e)}
    
    def autonomous_learning_loop(self, interval_minutes: int = 30):
        """
        Автономный цикл обучения
        
        Периодически собирает данные о поведении пользователя
        для улучшения своих способностей
        """
        logger.info(f"🚀 Запуск автономного обучения (интервал: {interval_minutes} мин)")
        
        while True:
            try:
                # Собрать данные
                learning_data = self.collect_learning_data()
                
                # Проанализировать и улучшить себя
                if learning_data.get("screen_analysis"):
                    self._learn_from_screen_analysis(learning_data["screen_analysis"])
                
                if learning_data.get("user_patterns"):
                    self._learn_from_patterns(learning_data["user_patterns"])
                
                # Сохранить прогресс
                self._save_learning_progress(learning_data)
                
                logger.info(f"🧠 Обучение завершено. Следующий цикл через {interval_minutes} мин")
                
                # Подождать до следующего цикла
                time.sleep(interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Ошибка в цикле обучения: {e}")
                time.sleep(300)  # Подождать 5 минут при ошибке
    
    def _learn_from_screen_analysis(self, screen_data: Dict):
        """Извлечь уроки из анализа экрана"""
        description = screen_data.get("description", "")
        
        # Идентифицировать часто используемые приложения
        if "chrome" in description.lower():
            logger.info("🔍 Обнаружено использование Chrome - оптимизировать браузерные задачи")
        
        if "vscode" in description.lower() or "code" in description.lower():
            logger.info("🔍 Обнаружено использование VS Code - улучшить программирование")
    
    def _learn_from_patterns(self, patterns: List[str]):
        """Извлечь уроки из паттернов поведения"""
        for pattern in patterns:
            if "скриншоты" in pattern:
                logger.info("📸 Пользователь часто делает скриншоты - улучшить Vision анализ")
            
            if "кликает" in pattern:
                logger.info("🖱️ Пользователь активно использует мышь - оптимизировать клики")
    
    def _save_learning_progress(self, learning_data: Dict):
        """Сохранить прогресс обучения"""
        try:
            progress_file = Path("learning_progress.json")
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
            else:
                progress = {"sessions": []}
            
            progress["sessions"].append({
                "timestamp": learning_data["timestamp"],
                "insights": len(learning_data.get("action_insights", [])),
                "patterns": len(learning_data.get("user_patterns", [])),
                "opportunities": learning_data.get("learning_opportunities", [])
            })
            
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
            
            logger.info("💾 Прогресс обучения сохранен")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения прогресса: {e}")


# ═══════════════════════════════════════════════════════════════════
# CLI интерфейс
# ═══════════════════════════════════════════════════════════════════

def main():
    """CLI интерфейс для Desktop Agent"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║         MIRAI Desktop Agent V2 - Полный контроль над ПК            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Создать агента
        agent = MiraiDesktopAgent(
            enable_safety=True,
            enable_memory=True
        )
        
        print(f"🖥️ Система: {agent.os_type}")
        print(f"📐 Экран: {agent.screen_width}x{agent.screen_height}")
        print(f"🔒 Безопасность: Включена")
        print(f"🧠 Память: {'Включена' if agent.enable_memory else 'Отключена'}")
        print()
        
        # Примеры задач
        examples = [
            "Открой Chrome и найди в Google 'погода в Москве'",
            "Открой Notepad и напиши 'Hello from MIRAI'",
            "Сделай скриншот и опиши что на нем",
            "Найди окно Chrome и переключись на него",
            "Открой Calculator",
        ]
        
        print("📋 Примеры задач:")
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example}")
        print()
        
        print("Введите задачу для агента (или 'exit' для выхода):")
        print("-" * 70)
        
        # Интерактивный режим
        while True:
            try:
                task = input("\n🎯 Задача: ").strip()
                
                if task.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 До свидания!")
                    break
                
                if not task:
                    continue
                
                print("\n🤔 Агент думает и выполняет задачу...")
                print("-" * 70)
                
                result = agent.execute_task(task)
                
                print("\n" + "=" * 70)
                print("📊 РЕЗУЛЬТАТ:")
                print("=" * 70)
                print(result)
                print("=" * 70)
                
                # История действий
                if len(agent.action_history) > 0:
                    print("\n📝 Последние действия:")
                    for action in agent.action_history[-5:]:
                        print(f"  • {action.action_type}: {action.result[:50]}")
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Прервано пользователем")
                break
            except Exception as e:
                print(f"\n❌ Ошибка: {e}")
                logger.error("Error in main loop", exc_info=True)
    
    except Exception as e:
        print(f"\n❌ Ошибка инициализации: {e}")
        logger.error("Initialization error", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
