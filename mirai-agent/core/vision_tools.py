"""
MIRAI Vision Tools - Инструменты компьютерного зрения для умного AI агента
Анализирует каждый шаг, понимает контекст, принимает решения как человек
"""

import asyncio
import base64
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import pyautogui
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


@dataclass
class VisionContext:
    """Контекст того что видит агент"""
    screenshot_path: str
    timestamp: datetime
    app_name: Optional[str] = None
    window_title: Optional[str] = None
    
    # Результаты анализа
    scene_description: str = ""
    detected_elements: List[Dict] = None
    text_found: List[str] = None
    ui_state: Dict = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.detected_elements is None:
            self.detected_elements = []
        if self.text_found is None:
            self.text_found = []
        if self.ui_state is None:
            self.ui_state = {}
        if self.recommendations is None:
            self.recommendations = []


class VisionTools:
    """
    Продвинутые инструменты Vision для умного AI агента.
    Каждое действие сопровождается пониманием контекста.
    """
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
    def capture_screen(self, region: str = 'full') -> str:
        """Сделать скриншот с метаданными"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"vision_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filepath))
        
        logger.info(f"📸 Скриншот сохранён: {filename}")
        return str(filepath)
    
    def _encode_image(self, image_path: str) -> str:
        """Закодировать изображение в base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    async def analyze_screen_context(
        self, 
        screenshot_path: str,
        question: str = "Что я вижу на экране? Опиши детально интерфейс, элементы, текст.",
        app_name: Optional[str] = None,
        window_title: Optional[str] = None
    ) -> VisionContext:
        """
        УМНЫЙ АНАЛИЗ ЭКРАНА КАК ЧЕЛОВЕК.
        Понимает контекст, элементы UI, возможные действия.
        """
        
        context = VisionContext(
            screenshot_path=screenshot_path,
            timestamp=datetime.now(),
            app_name=app_name,
            window_title=window_title
        )
        
        # Кодируем изображение
        base64_image = self._encode_image(screenshot_path)
        
        # Умный промпт для GPT-4 Vision
        system_prompt = """Ты - эксперт по анализу интерфейсов и компьютерному зрению.
        Твоя задача - понять ЧТО видит AI агент и КАК с этим взаимодействовать.
        
        Анализируй как человек:
        1. Какое приложение/сайт открыт?
        2. Какие элементы интерфейса видны? (кнопки, поля, меню)
        3. Где находятся важные элементы? (координаты не нужны, просто "сверху слева", "в центре")
        4. Какой текст виден на экране?
        5. Что можно сделать СЕЙЧАС? (доступные действия)
        6. Есть ли проблемы? (ошибки, рекламы, попапы, выбор профиля)
        
        Ответь в JSON формате:
        {
            "scene": "Краткое описание что видно",
            "app_detected": "Название приложения",
            "elements": [
                {"type": "button", "label": "текст кнопки", "location": "где находится"},
                {"type": "textfield", "label": "название поля", "location": "где"}
            ],
            "text_visible": ["текст1", "текст2"],
            "possible_actions": ["действие1", "действие2"],
            "problems_detected": ["проблема1 если есть"],
            "recommendations": ["что делать дальше"]
        }
        """
        
        user_prompt = f"""Вопрос: {question}

Контекст:
- Приложение: {app_name or 'неизвестно'}
- Заголовок окна: {window_title or 'неизвестно'}

Проанализируй скриншот и ответь в JSON."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.3  # Низкая температура для точности
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Парсим JSON из ответа
            # Иногда GPT возвращает текст + JSON, извлекаем JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(result_text)
            
            # Заполняем контекст
            context.scene_description = analysis.get("scene", "")
            context.detected_elements = analysis.get("elements", [])
            context.text_found = analysis.get("text_visible", [])
            context.ui_state = {
                "app": analysis.get("app_detected", ""),
                "possible_actions": analysis.get("possible_actions", []),
                "problems": analysis.get("problems_detected", [])
            }
            context.recommendations = analysis.get("recommendations", [])
            
            logger.info(f"🧠 Vision анализ завершён: {context.scene_description[:100]}")
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Ошибка Vision анализа: {e}")
            context.scene_description = f"Ошибка анализа: {e}"
            return context
    
    async def find_element_on_screen(
        self,
        screenshot_path: str,
        element_description: str,
        app_name: Optional[str] = None
    ) -> Optional[Dict]:
        """
        НАЙТИ КОНКРЕТНЫЙ ЭЛЕМЕНТ НА ЭКРАНЕ (кнопку, поле ввода и т.д.)
        Возвращает где находится и как с ним взаимодействовать.
        """
        
        base64_image = self._encode_image(screenshot_path)
        
        prompt = f"""Найди на экране: {element_description}

Опиши где находится этот элемент (сверху/снизу/слева/справа/в центре).
Это кнопка, поле ввода, ссылка или что-то другое?
Какой текст на этом элементе?

Ответь в JSON:
{{
    "found": true/false,
    "element_type": "button/textfield/link/menu/other",
    "label": "текст элемента",
    "location": "подробное описание где находится",
    "how_to_interact": "как взаимодействовать (click/type/select)"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            result = response.choices[0].message.content.strip()
            
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            
            element_info = json.loads(result)
            
            if element_info.get("found"):
                logger.info(f"✅ Элемент найден: {element_info.get('label')} ({element_info.get('location')})")
                return element_info
            else:
                logger.warning(f"❌ Элемент не найден: {element_description}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка поиска элемента: {e}")
            return None
    
    async def verify_action_result(
        self,
        before_screenshot: str,
        after_screenshot: str,
        intended_action: str
    ) -> Dict:
        """
        ПРОВЕРИТЬ ЧТО ДЕЙСТВИЕ ВЫПОЛНИЛОСЬ ПРАВИЛЬНО.
        Сравнивает "до" и "после", понимает что изменилось.
        """
        
        before_image = self._encode_image(before_screenshot)
        after_image = self._encode_image(after_screenshot)
        
        prompt = f"""Действие было: {intended_action}

Сравни ДО и ПОСЛЕ. Что изменилось? Выполнилось ли действие успешно?

Ответь в JSON:
{{
    "success": true/false,
    "changes_detected": "что изменилось",
    "action_completed": true/false,
    "problems": ["проблемы если есть"],
    "next_steps": ["что делать дальше"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Скриншот ДО действия:"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{before_image}"}
                            },
                            {"type": "text", "text": "Скриншот ПОСЛЕ действия:"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{after_image}"}
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            
            verification = json.loads(result)
            
            if verification.get("success"):
                logger.info(f"✅ Действие выполнено: {verification.get('changes_detected')}")
            else:
                logger.warning(f"⚠️ Проблема при выполнении: {verification.get('problems')}")
            
            return verification
            
        except Exception as e:
            logger.error(f"❌ Ошибка проверки результата: {e}")
            return {
                "success": False,
                "changes_detected": "Не удалось проверить",
                "problems": [str(e)]
            }
    
    async def detect_problems(self, screenshot_path: str) -> List[str]:
        """
        ОБНАРУЖИТЬ ПРОБЛЕМЫ: реклама, ошибки, попапы, неожиданные окна.
        """
        
        base64_image = self._encode_image(screenshot_path)
        
        prompt = """Проанализируй экран на наличие ПРОБЛЕМ:
        - Реклама (баннеры, попапы)
        - Ошибки (сообщения об ошибке)
        - Неожиданные окна (выбор профиля, обновления)
        - Блокировки (требуется действие пользователя)
        
        Ответь списком JSON:
        ["проблема1", "проблема2"] или [] если проблем нет
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            result = response.choices[0].message.content.strip()
            
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            problems = json.loads(result)
            
            if problems:
                logger.warning(f"⚠️ Обнаружены проблемы: {problems}")
            else:
                logger.info("✅ Проблем не обнаружено")
            
            return problems
            
        except Exception as e:
            logger.error(f"❌ Ошибка детекции проблем: {e}")
            return []
