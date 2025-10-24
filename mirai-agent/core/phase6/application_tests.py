#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: Application Tests - Тесты модуля                     ║
║  Comprehensive tests for all 150 steps                               ║
╚══════════════════════════════════════════════════════════════════════╝

Тесты для всех компонентов Phase 6:
- Application Manager
- App Detector
- App Launcher
- VSCode Controller
- System App Controller

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import sys
from pathlib import Path

# Добавляем путь к модулям MIRAI
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.phase6.application_manager import ApplicationManager, ApplicationInfo, get_application_manager
from core.phase6.app_detector import AppDetector, detect_applications
from core.phase6.app_launcher import AppLauncher, launch_application, close_application
from core.phase6.vscode_controller import VSCodeController, get_vscode_controller
from core.phase6.system_app_controller import SystemAppController, get_system_app_controller

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestApplicationManager:
    """Тесты для Application Manager (Шаг 10)"""
    
    def test_initialization(self):
        """Тест инициализации"""
        logger.info("🧪 Тест: Инициализация Application Manager")
        
        manager = ApplicationManager()
        
        assert manager is not None, "Manager не создан"
        assert len(manager.applications) == 0, "Начальный список приложений не пуст"
        assert not manager.initialized, "Manager инициализирован преждевременно"
        
        logger.info("✅ Тест пройден")
    
    def test_register_application(self):
        """Тест регистрации приложения"""
        logger.info("🧪 Тест: Регистрация приложения")
        
        manager = ApplicationManager()
        
        app_info = ApplicationInfo(
            name="test_app",
            path=Path("/usr/bin/test"),
            category="test"
        )
        
        result = manager.register_application(app_info)
        
        assert result is True, "Регистрация не успешна"
        assert "test_app" in manager.applications, "Приложение не добавлено"
        assert manager.get_application("test_app") == app_info, "Информация не совпадает"
        
        logger.info("✅ Тест пройден")
    
    def test_statistics(self):
        """Тест получения статистики"""
        logger.info("🧪 Тест: Статистика приложений")
        
        manager = ApplicationManager()
        
        # Добавляем тестовые приложения
        for i in range(3):
            app_info = ApplicationInfo(
                name=f"app_{i}",
                category="test"
            )
            manager.register_application(app_info)
        
        stats = manager.get_statistics()
        
        assert stats['total_applications'] == 3, "Неверное количество приложений"
        assert 'test' in stats['categories'], "Категория не найдена"
        
        logger.info("✅ Тест пройден")


class TestAppDetector:
    """Тесты для App Detector (Шаги 1-20)"""
    
    def test_detection(self):
        """Тест обнаружения приложений"""
        logger.info("🧪 Тест: Обнаружение приложений")
        
        detector = AppDetector()
        results = detector.discover_all()
        
        assert results is not None, "Результаты не получены"
        assert 'installed_count' in results, "Нет информации о количестве"
        assert results['discovery_complete'] is True, "Обнаружение не завершено"
        
        logger.info(f"📊 Обнаружено приложений: {results['installed_count']}")
        logger.info("✅ Тест пройден")
    
    def test_known_apps(self):
        """Тест обнаружения известных приложений"""
        logger.info("🧪 Тест: Обнаружение известных приложений")
        
        results = detect_applications()
        
        # Проверяем что хотя бы одно системное приложение найдено
        # (Notepad на Windows или другие на Linux/Mac)
        assert results['installed_count'] > 0, "Ни одно приложение не найдено"
        
        logger.info(f"✅ Найдено приложений: {results['installed_apps']}")
        logger.info("✅ Тест пройден")


class TestAppLauncher:
    """Тесты для App Launcher (Шаги 21-35)"""
    
    def test_launcher_initialization(self):
        """Тест инициализации launcher"""
        logger.info("🧪 Тест: Инициализация App Launcher")
        
        launcher = AppLauncher()
        
        assert launcher is not None, "Launcher не создан"
        assert launcher.readiness_waiter is not None, "ReadinessWaiter не создан"
        assert launcher.error_handler is not None, "ErrorHandler не создан"
        
        logger.info("✅ Тест пройден")
    
    def test_launch_nonexistent_app(self):
        """Тест запуска несуществующего приложения"""
        logger.info("🧪 Тест: Запуск несуществующего приложения")
        
        result = launch_application("nonexistent_app_12345", wait_ready=False)
        
        assert result.success is False, "Запуск должен был провалиться"
        assert result.error is not None, "Должна быть ошибка"
        
        logger.info("✅ Тест пройден (ошибка корректно обработана)")


class TestVSCodeController:
    """Тесты для VSCode Controller (Шаги 76-105)"""
    
    def test_controller_initialization(self):
        """Тест инициализации VSCode контроллера"""
        logger.info("🧪 Тест: Инициализация VSCode Controller")
        
        controller = VSCodeController()
        
        assert controller is not None, "Controller не создан"
        assert controller.app_name == "vscode", "Неверное имя приложения"
        assert controller.is_launched is False, "Не должен быть запущен"
        
        logger.info("✅ Тест пройден")
    
    def test_vscode_registered(self):
        """Тест регистрации handler в manager"""
        logger.info("🧪 Тест: Регистрация VSCode handler")
        
        controller = get_vscode_controller()
        manager = get_application_manager()
        
        handler = manager.get_handler("vscode")
        
        assert handler is not None, "Handler не зарегистрирован"
        
        logger.info("✅ Тест пройден")


class TestSystemAppController:
    """Тесты для System App Controller (Шаги 121-135)"""
    
    def test_controller_initialization(self):
        """Тест инициализации System App контроллера"""
        logger.info("🧪 Тест: Инициализация System App Controller")
        
        controller = SystemAppController()
        
        assert controller is not None, "Controller не создан"
        assert controller.notepad is not None, "Notepad controller не создан"
        assert controller.calculator is not None, "Calculator controller не создан"
        assert controller.task_manager is not None, "Task Manager controller не создан"
        assert controller.cmd is not None, "CMD controller не создан"
        
        logger.info("✅ Тест пройден")
    
    def test_notepad_controller(self):
        """Тест Notepad контроллера"""
        logger.info("🧪 Тест: Notepad Controller")
        
        controller = get_system_app_controller()
        notepad = controller.get_notepad()
        
        assert notepad is not None, "Notepad controller не получен"
        assert notepad.app_name == "notepad", "Неверное имя приложения"
        
        logger.info("✅ Тест пройден")
    
    def test_cmd_execute(self):
        """Тест выполнения команды"""
        logger.info("🧪 Тест: Выполнение CMD команды")
        
        controller = get_system_app_controller()
        cmd = controller.get_cmd()
        
        # Выполняем простую команду
        output = cmd.execute_command("echo Hello MIRAI")
        
        assert output is not None, "Вывод не получен"
        assert "MIRAI" in output or "Hello" in output, "Вывод не содержит ожидаемый текст"
        
        logger.info("✅ Тест пройден")


def run_all_tests():
    """Запустить все тесты"""
    logger.info("=" * 70)
    logger.info("🚀 ЗАПУСК ТЕСТОВ PHASE 6: APPLICATION CONTROL")
    logger.info("=" * 70)
    
    test_classes = [
        TestApplicationManager,
        TestAppDetector,
        TestAppLauncher,
        TestVSCodeController,
        TestSystemAppController
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        logger.info(f"\n📦 Тестирование: {test_class.__name__}")
        logger.info("-" * 70)
        
        test_instance = test_class()
        
        # Получаем все методы теста
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            
            try:
                method = getattr(test_instance, method_name)
                method()
                passed_tests += 1
            except Exception as e:
                failed_tests += 1
                logger.error(f"❌ Тест {method_name} провален: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    logger.info("=" * 70)
    logger.info(f"Всего тестов: {total_tests}")
    logger.info(f"✅ Пройдено: {passed_tests}")
    logger.info(f"❌ Провалено: {failed_tests}")
    logger.info(f"📈 Успешность: {(passed_tests/total_tests*100):.1f}%")
    logger.info("=" * 70)
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
