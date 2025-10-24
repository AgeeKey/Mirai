"""
Smart Desktop Agent - Умный агент управления компьютером
Каждое действие с Vision анализом: ПОНИМАЕТ куда кликать, где печатать
"""

import time
import pyautogui
import subprocess
import logging
from typing import Optional, Dict, List
from pathlib import Path

from .vision_tools import VisionTools, VisionContext
from .context_manager import AgentContext, ActionStatus
from .smart_browser_agent import SmartBrowserAgent

logger = logging.getLogger(__name__)


class SmartDesktopAgent:
    """
    УМНЫЙ ДЕСКТОПНЫЙ АГЕНТ С ЧЕЛОВЕЧЕСКИМ ИНТЕЛЛЕКТОМ.

    ПРИНЦИП РАБОТЫ:
    Каждое действие = Vision → Понимание → Решение → Действие → Проверка

    Не просто "открыть Notepad", а:
    1. Скриншот → Vision анализ: "Где я?"
    2. Решение: "Как открыть Notepad отсюда?"
    3. Действие: открытие
    4. Скриншот → Проверка: "Открылся ли Notepad?"
    """

    def __init__(self, vision: VisionTools, context: AgentContext):
        self.vision = vision
        self.context = context
        self.browser = SmartBrowserAgent(vision, context)

        pyautogui.FAILSAFE = False  # Для автоматизации
        pyautogui.PAUSE = 0.5

    async def smart_open_application(self, app_name: str) -> bool:
        """
        УМНОЕ ОТКРЫТИЕ ПРИЛОЖЕНИЯ КАК ЧЕЛОВЕК:
        1. Vision: "Уже открыто?"
        2. Если нет - открыть через меню Пуск
        3. Vision: "Открылось ли?"
        """

        logger.info(f"🚀 Умное открытие: {app_name}")

        # ШАГ 1: Проверяем что сейчас на экране
        screenshot_before = self.vision.capture_screen()
        vision_before = await self.vision.analyze_screen_context(
            screenshot_before,
            question=f"Открыто ли приложение {app_name}? Что видно на экране?",
            app_name=app_name
        )

        logger.info(f"👁️ Vision ДО: {vision_before.scene_description[:100]}")

        # Если уже открыто - активируем
        if app_name.lower() in vision_before.scene_description.lower():
            logger.info(f"✅ {app_name} уже открыт, активирую...")
            await self._activate_window_smart(app_name)
            return True

        # ШАГ 2: Открываем через Win Search
        logger.info("🔍 Открываю через поиск Windows...")

        # Win+S или Win (поиск)
        pyautogui.press("win")
        time.sleep(1.5)

        # Печатаем название приложения
        logger.info(f"⌨️ Ввожу: {app_name}")
        pyautogui.write(app_name, interval=0.05)
        time.sleep(1)

        # Enter
        pyautogui.press("enter")
        logger.info("⏳ Жду запуска...")
        time.sleep(3)

        # ШАГ 3: Проверяем что открылось
        screenshot_after = self.vision.capture_screen()
        vision_after = await self.vision.analyze_screen_context(
            screenshot_after,
            question=f"Открылось ли приложение {app_name}? Я вижу интерфейс {app_name}?",
            app_name=app_name
        )

        logger.info(f"👁️ Vision ПОСЛЕ: {vision_after.scene_description[:100]}")

        # Проверяем результат
        success = app_name.lower() in vision_after.scene_description.lower()

        if success:
            logger.info(f"✅ {app_name} успешно открыт!")
            self.context.update_application_state(
                app_name=app_name,
                window_title=vision_after.window_title or app_name,
                is_active=True,
                state_description=vision_after.scene_description,
                detected_elements=vision_after.detected_elements
            )
        else:
            logger.error(f"❌ Не удалось открыть {app_name}")

        self.context.record_action(
            "open_application",
            f"Открыть {app_name}",
            ActionStatus.SUCCESS if success else ActionStatus.FAILED,
            result=vision_after.scene_description,
            screenshot_before=screenshot_before,
            screenshot_after=screenshot_after
        )

        return success

    async def smart_type_text(self, text: str, target_app: Optional[str] = None) -> bool:
        """
        УМНАЯ ПЕЧАТЬ ТЕКСТА:
        1. Vision: "Где я? Это текстовое поле?"
        2. Если нет - найти текстовое поле
        3. Кликнуть в поле
        4. Печатать
        5. Vision: "Текст напечатался?"
        """

        logger.info(f"⌨️ Умная печать текста ({len(text)} символов)")

        # ШАГ 1: Понимаем где мы
        screenshot = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot,
            question="Где находится текстовое поле для ввода? Могу ли я сейчас печатать?",
            app_name=target_app
        )

        logger.info(f"👁️ Vision: {vision_ctx.scene_description[:150]}")

        # ШАГ 2: Ищем текстовое поле
        text_field = await self.vision.find_element_on_screen(
            screenshot,
            "текстовое поле для ввода или область редактирования текста",
            app_name=target_app
        )

        if text_field and text_field.get("found"):
            # Кликаем в поле
            logger.info(f"🖱️ Кликаю в текстовое поле: {text_field.get('location')}")
            await self._click_element_smart(text_field)
            time.sleep(0.5)
        else:
            # Кликаем в центр экрана (обычно там поле ввода)
            logger.warning("⚠️ Текстовое поле не найдено, кликаю в центр")
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 2, screen_height // 2)
            time.sleep(0.5)

        # ШАГ 3: Печатаем текст
        logger.info(f"⌨️ Печатаю текст: {text[:50]}...")
        screenshot_before_type = self.vision.capture_screen()

        pyautogui.write(text, interval=0.03)  # Быстрая печать
        time.sleep(0.5)

        # ШАГ 4: Проверяем результат
        screenshot_after = self.vision.capture_screen()
        verification = await self.vision.verify_action_result(
            screenshot_before_type,
            screenshot_after,
            f"напечатать текст: {text[:50]}..."
        )

        success = verification.get("success", False)

        if success:
            logger.info("✅ Текст напечатан успешно!")
        else:
            logger.warning(f"⚠️ Проблемы при печати: {verification.get('problems')}")

        self.context.record_action(
            "type_text",
            f"Напечатать текст ({len(text)} символов)",
            ActionStatus.SUCCESS if success else ActionStatus.PARTIAL,
            result=f"Напечатано: {len(text)} символов",
            problems=verification.get("problems", []),
            screenshot_before=screenshot_before_type,
            screenshot_after=screenshot_after
        )

        return success

    async def smart_click(self, element_description: str) -> bool:
        """
        УМНЫЙ КЛИК ПО ЭЛЕМЕНТУ:
        1. Vision: найти элемент
        2. Определить где он
        3. Кликнуть
        4. Vision: проверить результат
        """

        logger.info(f"🖱️ Умный клик: {element_description}")

        # ШАГ 1: Ищем элемент
        screenshot = self.vision.capture_screen()
        element = await self.vision.find_element_on_screen(
            screenshot,
            element_description
        )

        if not element or not element.get("found"):
            logger.error(f"❌ Элемент не найден: {element_description}")
            return False

        # ШАГ 2: Кликаем
        await self._click_element_smart(element)
        time.sleep(1)

        # ШАГ 3: Проверяем
        screenshot_after = self.vision.capture_screen()
        verification = await self.vision.verify_action_result(
            screenshot,
            screenshot_after,
            f"кликнуть на {element_description}"
        )

        success = verification.get("success", False)
        logger.info(f"✅ Клик выполнен: {verification.get('changes_detected')}")

        return success

    async def _click_element_smart(self, element: Dict):
        """Кликнуть по элементу основываясь на его описании"""
        location = element.get("location", "").lower()
        screen_width, screen_height = pyautogui.size()

        # Определяем примерную позицию
        if "слева" in location and "сверху" in location:
            x, y = screen_width // 4, screen_height // 4
        elif "справа" in location and "сверху" in location:
            x, y = 3 * screen_width // 4, screen_height // 4
        elif "слева" in location and "снизу" in location:
            x, y = screen_width // 4, 3 * screen_height // 4
        elif "справа" in location and "снизу" in location:
            x, y = 3 * screen_width // 4, 3 * screen_height // 4
        elif "центр" in location or "middle" in location:
            x, y = screen_width // 2, screen_height // 2
        elif "слева" in location:
            x, y = screen_width // 4, screen_height // 2
        elif "справа" in location:
            x, y = 3 * screen_width // 4, screen_height // 2
        elif "сверху" in location:
            x, y = screen_width // 2, screen_height // 4
        elif "снизу" in location:
            x, y = screen_width // 2, 3 * screen_height // 4
        else:
            x, y = screen_width // 2, screen_height // 2

        logger.info(f"🖱️ Кликаю по координатам: ({x}, {y})")
        pyautogui.click(x, y)

    async def _activate_window_smart(self, app_name: str):
        """Активировать окно приложения"""
        # Alt+Tab для переключения (упрощённо)
        pyautogui.hotkey("alt", "tab")
        time.sleep(0.5)

    async def smart_execute_task(self, task_description: str) -> Dict:
        """
        УМНОЕ ВЫПОЛНЕНИЕ ЛЮБОЙ ЗАДАЧИ:
        AI анализирует что нужно сделать и выполняет поэтапно с Vision контролем.
        """

        logger.info(f"🎯 Умная задача: {task_description}")

        # Анализируем текущее состояние
        screenshot = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot,
            question=f"Что нужно сделать для выполнения: {task_description}? Какие шаги?"
        )

        logger.info(f"📋 Рекомендации Vision: {vision_ctx.recommendations}")

        # Выполняем рекомендованные действия
        results = []
        for i, action in enumerate(vision_ctx.recommendations[:3], 1):  # Макс 3 шага
            logger.info(f"▶️ Шаг {i}: {action}")

            # Выполняем шаг (упрощённо)
            if "открыть" in action.lower():
                app = action.split("открыть")[-1].strip().split()[0]
                success = await self.smart_open_application(app)
            elif "ввести" in action.lower() or "напечатать" in action.lower():
                # Извлекаем текст (упрощённо)
                success = await self.smart_type_text("test text")
            elif "кликнуть" in action.lower() or "нажать" in action.lower():
                # Извлекаем элемент (упрощённо)
                element = action.split("на")[-1].strip() if "на" in action else "кнопка"
                success = await self.smart_click(element)
            else:
                success = False

            results.append({"step": action, "success": success})
            time.sleep(1)

        overall_success = all(r["success"] for r in results)

        self.context.record_action(
            "execute_task",
            task_description,
            ActionStatus.SUCCESS if overall_success else ActionStatus.PARTIAL,
            result=f"Выполнено {len(results)} шагов",
            screenshot_before=screenshot
        )

        return {
            "success": overall_success,
            "steps": results,
            "recommendations": vision_ctx.recommendations
        }

    async def analyze_current_situation(self) -> VisionContext:
        """
        ПОЛНЫЙ АНАЛИЗ ТЕКУЩЕЙ СИТУАЦИИ:
        Что открыто, что можно делать, какие проблемы.
        """

        logger.info("🔍 Анализирую текущую ситуацию...")

        screenshot = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot,
            question="""Полный анализ:
            1. Какие приложения открыты?
            2. Что активно сейчас?
            3. Какие действия доступны?
            4. Есть ли проблемы (ошибки, попапы, блокировки)?
            5. Что я могу сделать СЕЙЧАС?"""
        )

        # Обновляем контекст
        if vision_ctx.ui_state.get("app"):
            self.context.update_application_state(
                app_name=vision_ctx.ui_state["app"],
                window_title=vision_ctx.window_title or "Unknown",
                is_active=True,
                state_description=vision_ctx.scene_description,
                detected_elements=vision_ctx.detected_elements
            )

        logger.info(f"📊 Ситуация: {vision_ctx.scene_description[:150]}")
        logger.info(f"🎯 Доступные действия: {vision_ctx.ui_state.get('possible_actions', [])}")

        if vision_ctx.ui_state.get("problems"):
            logger.warning(f"⚠️ Обнаружены проблемы: {vision_ctx.ui_state['problems']}")

        return vision_ctx
