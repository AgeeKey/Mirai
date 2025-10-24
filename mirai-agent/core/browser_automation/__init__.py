"""
🌐 BROWSER AUTOMATION - ФАЗА 5 (200 ШАГОВ)
Полная система автоматизации браузера как человек

Модули:
- browser_detection.py: Обнаружение и настройка браузеров (Шаги 1-15)
- profile_management.py: Управление профилями Chrome (Шаги 16-40)
- navigation.py: Навигация и загрузка страниц (Шаги 41-60)
- form_interaction.py: Поиск и работа с формами (Шаги 61-90)
- ads_popup_handling.py: Обработка рекламы и попапов (Шаги 91-110)
- downloads_uploads.py: Загрузки и выгрузки файлов (Шаги 111-130)
- media_capture.py: Скриншоты и запись (Шаги 131-140)
- cookie_management.py: Управление cookies и кешем (Шаги 141-160)
- security_privacy.py: Безопасность и приватность (Шаги 161-180)
- testing_integration.py: Тестирование и интеграция (Шаги 181-200)
"""

__version__ = "1.0.0"
__author__ = "MIRAI Team"

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    """Ленивая загрузка модулей"""
    if name in _BROWSER_DETECTION_CLASSES:
        from .browser_detection import (
            BrowserDetector,
            BrowserVersionChecker,
            CompatibilityChecker,
            BrowserExecutableLocator,
            BrowserConfigLoader,
            WebDriverInitializer,
            BrowserLogger,
            BrowserSessionManager,
            BrowserReadinessChecker,
            BrowserMonitor,
            ExtensionLoader,
            PermissionConfigurator,
            ProxyConfigurator,
            CookieManager,
            BrowserStartupValidator,
        )
        return locals()[name]
    
    elif name in _PROFILE_MANAGEMENT_CLASSES:
        from .profile_management import (
            ChromeProfileDetector,
            ChromeProfileParser,
            ProfileMetadataReader,
            ProfileIdentifier,
            ProfilePathExtractor,
            ActiveProfileDetector,
            ProfileSelectionUI,
            ProfileClickHandler,
            SelectionConfirmationDetector,
            ProfileLoadWaiter,
            ProfileVerifier,
            ProfileSwitcher,
            ProfilePreferenceManager,
            MissingProfileHandler,
            ProfileSelectionRecovery,
            ProfileSettingsLoader,
            ProfileSyncManager,
            IncognitoModeHandler,
            FirstTimeProfileDetector,
            ProfileSelectionValidator,
            ProfileContextStorage,
            ProfileLockHandler,
            ProfileChangeMonitor,
            ProfileStateBackup,
            ProfileSetupValidator,
        )
        return locals()[name]
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Browser Detection (Steps 1-15)
_BROWSER_DETECTION_CLASSES = {
    "BrowserDetector",
    "BrowserVersionChecker",
    "CompatibilityChecker",
    "BrowserExecutableLocator",
    "BrowserConfigLoader",
    "WebDriverInitializer",
    "BrowserLogger",
    "BrowserSessionManager",
    "BrowserReadinessChecker",
    "BrowserMonitor",
    "ExtensionLoader",
    "PermissionConfigurator",
    "ProxyConfigurator",
    "CookieManager",
    "BrowserStartupValidator",
}

# Profile Management (Steps 16-40)
_PROFILE_MANAGEMENT_CLASSES = {
    "ChromeProfileDetector",
    "ChromeProfileParser",
    "ProfileMetadataReader",
    "ProfileIdentifier",
    "ProfilePathExtractor",
    "ActiveProfileDetector",
    "ProfileSelectionUI",
    "ProfileClickHandler",
    "SelectionConfirmationDetector",
    "ProfileLoadWaiter",
    "ProfileVerifier",
    "ProfileSwitcher",
    "ProfilePreferenceManager",
    "MissingProfileHandler",
    "ProfileSelectionRecovery",
    "ProfileSettingsLoader",
    "ProfileSyncManager",
    "IncognitoModeHandler",
    "FirstTimeProfileDetector",
    "ProfileSelectionValidator",
    "ProfileContextStorage",
    "ProfileLockHandler",
    "ProfileChangeMonitor",
    "ProfileStateBackup",
    "ProfileSetupValidator",
}

__all__ = list(_BROWSER_DETECTION_CLASSES | _PROFILE_MANAGEMENT_CLASSES)
