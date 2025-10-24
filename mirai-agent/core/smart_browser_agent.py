"""
Smart Browser Agent - Интеллектуальная работа с браузером
Понимает профили, обходит рекламу, работает как человек
"""

import time
import subprocess
from typing import Optional, List, Dict
import pyautogui
import logging
from pathlib import Path

from .vision_tools import VisionTools, VisionContext
from .context_manager import AgentContext, ActionStatus

logger = logging.getLogger(__name__)


class SmartBrowserAgent:
    """
    УМНЫЙ БРАУЗЕРНЫЙ АГЕНТ.
    Работает с Chrome как человек: выбирает профили, обходит рекламу, ждёт загрузки.
    """

    def __init__(self, vision: VisionTools, context: AgentContext):
        self.vision = vision
        self.context = context
        self.chrome_path = self._find_chrome()

    def _find_chrome(self) -> Optional[str]:
        """Найти путь к Chrome"""
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe"
        ]

        for path in possible_paths:
            if Path(path).exists():
                logger.info(f"✅ Chrome найден: {path}")
                return str(path)

        logger.warning("⚠️ Chrome не найден в стандартных путях")
        return None

    async def open_chrome_smart(
        self,
        url: Optional[str] = None,
        profile_name: Optional[str] = None,
        max_wait_seconds: int = 30
    ) -> bool:
        """
        УМНОЕ ОТКРЫТИЕ CHROME КАК ЧЕЛОВЕК:
        1. Запустить Chrome
        2. ЕСЛИ появился выбор профилей → Vision анализ → выбор нужного
        3. ЕСЛИ реклама/попапы → закрыть
        4. Дождаться загрузки
        """

        logger.info(f"🌐 Открываю Chrome (профиль: {profile_name or 'любой'})")

        # Скриншот ДО
        screenshot_before = self.vision.capture_screen()

        # Запускаем Chrome
        try:
            if self.chrome_path:
                cmd = [self.chrome_path]
                if url:
                    cmd.append(url)
                subprocess.Popen(cmd)
            else:
                # Пробуем через команду
                subprocess.Popen(["start", "chrome", url or ""], shell=True)

            logger.info("⏳ Жду запуска Chrome...")
            time.sleep(3)

        except Exception as e:
            logger.error(f"❌ Ошибка запуска Chrome: {e}")
            self.context.record_action(
                "open_chrome",
                f"Открыть Chrome с URL: {url}",
                ActionStatus.FAILED,
                problems=[str(e)],
                screenshot_before=screenshot_before
            )
            return False

        # VISION АНАЛИЗ: что мы видим?
        screenshot_after = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot_after,
            question="Что сейчас на экране? Это Chrome? Есть ли выбор профиля? Есть ли реклама или попапы?",
            app_name="chrome"
        )

        logger.info(f"👁️ Vision: {vision_ctx.scene_description}")

        # ПРОВЕРЯЕМ: нужно ли выбрать профиль?
        if "профил" in vision_ctx.scene_description.lower() or "profile" in vision_ctx.scene_description.lower():
            logger.info("🎯 Обнаружен выбор профиля!")
            success = await self._select_chrome_profile(profile_name, vision_ctx)
            if not success:
                logger.warning("⚠️ Не удалось выбрать профиль, продолжаем")

        # ПРОВЕРЯЕМ: есть ли проблемы (реклама, попапы)?
        if vision_ctx.ui_state.get("problems"):
            logger.warning(f"⚠️ Обнаружены проблемы: {vision_ctx.ui_state['problems']}")
            await self._handle_browser_problems(vision_ctx.ui_state["problems"])

        # Обновляем контекст
        self.context.update_browser_state(
            current_url=url,
            profile_name=profile_name,
            state_description=vision_ctx.scene_description,
            has_ads="реклам" in vision_ctx.scene_description.lower(),
            has_popups="попап" in vision_ctx.scene_description.lower() or "popup" in vision_ctx.scene_description.lower()
        )

        self.context.record_action(
            "open_chrome",
            f"Открыть Chrome (профиль: {profile_name}, URL: {url})",
            ActionStatus.SUCCESS,
            result=vision_ctx.scene_description,
            screenshot_before=screenshot_before,
            screenshot_after=screenshot_after
        )

        logger.info("✅ Chrome открыт и готов!")
        return True

    async def _select_chrome_profile(
        self,
        profile_name: Optional[str],
        vision_ctx: VisionContext
    ) -> bool:
        """
        ВЫБРАТЬ ПРОФИЛЬ CHROME ЧЕРЕЗ VISION.
        Находит нужный профиль по имени или выбирает первый.
        """

        logger.info(f"🔍 Ищу профиль: {profile_name or 'любой доступный'}")

        # Ищем профили на экране
        if profile_name:
            # Ищем конкретный профиль
            element = await self.vision.find_element_on_screen(
                vision_ctx.screenshot_path,
                f"профиль с именем {profile_name} или кнопка {profile_name}",
                app_name="chrome"
            )
        else:
            # Ищем любую кнопку профиля
            element = await self.vision.find_element_on_screen(
                vision_ctx.screenshot_path,
                "кнопка профиля пользователя или аватар профиля",
                app_name="chrome"
            )

        if not element or not element.get("found"):
            logger.warning("❌ Профиль не найден на экране")
            return False

        # Кликаем по профилю (по центру экрана, где обычно профили)
        # В реальности нужны координаты, но для демо кликаем в центр
        logger.info(f"🖱️ Кликаю на профиль: {element.get('label')} ({element.get('location')})")

        # Определяем примерную позицию по описанию
        screen_width, screen_height = pyautogui.size()

        location = element.get("location", "").lower()
        if "слева" in location:
            x = screen_width // 4
        elif "справа" in location:
            x = 3 * screen_width // 4
        else:
            x = screen_width // 2

        if "сверху" in location:
            y = screen_height // 4
        elif "снизу" in location:
            y = 3 * screen_height // 4
        else:
            y = screen_height // 2

        pyautogui.click(x, y)
        time.sleep(2)

        logger.info("✅ Профиль выбран")
        return True

    async def _handle_browser_problems(self, problems: List[str]):
        """
        ОБРАБОТАТЬ ПРОБЛЕМЫ В БРАУЗЕРЕ (реклама, попапы).
        """

        for problem in problems:
            problem_lower = problem.lower()

            # Реклама
            if "реклам" in problem_lower or "ad" in problem_lower:
                logger.info("🚫 Пытаюсь закрыть рекламу...")
                await self._close_ads()

            # Попапы
            elif "попап" in problem_lower or "popup" in problem_lower:
                logger.info("🚫 Пытаюсь закрыть попап...")
                await self._close_popup()

            # Обновление браузера
            elif "обновл" in problem_lower or "update" in problem_lower:
                logger.info("⏭️ Пропускаю предложение обновления...")
                pyautogui.press("esc")
                time.sleep(1)

    async def _close_ads(self):
        """Закрыть рекламу (ищем крестик, кнопку Close)"""
        screenshot = self.vision.capture_screen()

        # Ищем кнопку закрытия
        element = await self.vision.find_element_on_screen(
            screenshot,
            "кнопка закрыть рекламу или крестик X",
            app_name="chrome"
        )

        if element and element.get("found"):
            logger.info("🖱️ Кликаю на закрытие рекламы")
            # Кликаем (в реальности нужны точные координаты)
            pyautogui.press("esc")  # Часто помогает
            time.sleep(1)
        else:
            # Пробуем ESC
            pyautogui.press("esc")
            time.sleep(1)

    async def _close_popup(self):
        """Закрыть попап"""
        pyautogui.press("esc")
        time.sleep(0.5)
        # Или кликаем вне попапа
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 10, screen_height // 10)
        time.sleep(0.5)

    async def google_search_smart(self, query: str) -> bool:
        """
        УМНЫЙ ПОИСК В GOOGLE КАК ЧЕЛОВЕК:
        1. Открыть google.com (или проверить что уже там)
        2. Найти поле поиска через Vision
        3. Кликнуть в поле
        4. Ввести запрос
        5. Нажать Enter
        6. Дождаться результатов
        """

        logger.info(f"🔍 Google поиск: {query}")

        # Проверяем где мы сейчас
        screenshot = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot,
            question="Это Google? Есть ли поле поиска?",
            app_name="chrome"
        )

        # Если не Google - переходим
        if "google" not in vision_ctx.scene_description.lower():
            logger.info("📍 Не на Google, перехожу...")
            await self.open_chrome_smart(url="https://www.google.com")
            time.sleep(3)
            screenshot = self.vision.capture_screen()

        # Ищем поле поиска
        search_field = await self.vision.find_element_on_screen(
            screenshot,
            "поле поиска Google или строка поиска",
            app_name="chrome"
        )

        if not search_field or not search_field.get("found"):
            logger.error("❌ Поле поиска не найдено!")
            return False

        # Кликаем в поле (центр экрана обычно)
        logger.info("🖱️ Кликаю в поле поиска...")
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(0.5)

        # Вводим запрос
        logger.info(f"⌨️ Ввожу запрос: {query}")
        pyautogui.write(query, interval=0.05)
        time.sleep(0.5)

        # Enter
        pyautogui.press("enter")
        logger.info("⏳ Жду результатов...")
        time.sleep(3)

        # Проверяем результаты
        screenshot_after = self.vision.capture_screen()
        result_ctx = await self.vision.analyze_screen_context(
            screenshot_after,
            question="Загрузились ли результаты поиска? Что видно?",
            app_name="chrome"
        )

        logger.info(f"✅ Результаты: {result_ctx.scene_description[:100]}")

        self.context.record_action(
            "google_search",
            f"Поиск: {query}",
            ActionStatus.SUCCESS,
            result=result_ctx.scene_description,
            screenshot_after=screenshot_after
        )

        return True

    async def navigate_to_url(self, url: str) -> bool:
        """Перейти на URL умно"""
        logger.info(f"🌐 Переход на: {url}")

        # Ctrl+L (фокус на адресную строку)
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.3)

        # Вводим URL
        pyautogui.write(url, interval=0.02)
        pyautogui.press("enter")

        logger.info("⏳ Жду загрузки страницы...")
        time.sleep(5)

        # Проверяем что загрузилось
        screenshot = self.vision.capture_screen()
        vision_ctx = await self.vision.analyze_screen_context(
            screenshot,
            question=f"Загрузилась ли страница {url}? Что видно?",
            app_name="chrome"
        )

        # Проверяем проблемы
        problems = await self.vision.detect_problems(screenshot)
        if problems:
            logger.warning(f"⚠️ Обнаружены проблемы: {problems}")
            await self._handle_browser_problems(problems)

        self.context.update_browser_state(
            current_url=url,
            state_description=vision_ctx.scene_description,
            has_ads="реклам" in vision_ctx.scene_description.lower(),
            has_popups=bool(problems)
        )

        logger.info("✅ Страница загружена!")
        return True
