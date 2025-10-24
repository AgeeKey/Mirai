#!/usr/bin/env python3
"""
🎯 Action Handlers Registry - Реестр обработчиков действий
Шаг 5 из 150: Register Action Handlers

Dispatch mechanism для разных типов действий
"""

import logging
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class HandlerInfo:
    """Информация об обработчике"""
    name: str
    handler: Callable
    description: str
    action_types: list


class ActionHandlerRegistry:
    """
    Реестр обработчиков действий
    
    Функции:
    - Регистрация handlers для каждого типа action
    - Dispatch actions к правильному handler
    - Валидация handlers
    """
    
    def __init__(self):
        self.handlers: Dict[str, HandlerInfo] = {}
        self.type_to_handler: Dict[str, str] = {}
        self._register_default_handlers()
        logger.info("🎯 ActionHandlerRegistry создан")
    
    def register_handler(
        self,
        name: str,
        handler: Callable,
        action_types: list,
        description: str = ""
    ) -> bool:
        """
        Зарегистрировать обработчик
        
        Args:
            name: Имя обработчика
            handler: Функция-обработчик
            action_types: Типы действий которые обрабатывает
            description: Описание
            
        Returns:
            bool: True если зарегистрирован успешно
        """
        try:
            # Создаем HandlerInfo
            handler_info = HandlerInfo(
                name=name,
                handler=handler,
                description=description or f"Handler for {name}",
                action_types=action_types
            )
            
            # Сохраняем в реестр
            self.handlers[name] = handler_info
            
            # Связываем типы действий с обработчиком
            for action_type in action_types:
                self.type_to_handler[action_type] = name
            
            logger.info(f"✅ Зарегистрирован handler: {name} для {action_types}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации handler: {e}")
            return False
    
    def get_handler(self, action_type: str) -> Optional[Callable]:
        """
        Получить обработчик для типа действия
        
        Args:
            action_type: Тип действия
            
        Returns:
            Callable handler или None
        """
        handler_name = self.type_to_handler.get(action_type)
        if not handler_name:
            logger.warning(f"⚠️ Handler не найден для типа: {action_type}")
            return None
        
        handler_info = self.handlers.get(handler_name)
        if not handler_info:
            logger.error(f"❌ HandlerInfo не найден: {handler_name}")
            return None
        
        return handler_info.handler
    
    def dispatch(self, action_type: str, **kwargs) -> Any:
        """
        Диспатчить действие к обработчику
        
        Args:
            action_type: Тип действия
            **kwargs: Параметры действия
            
        Returns:
            Результат выполнения handler
        """
        handler = self.get_handler(action_type)
        if not handler:
            raise ValueError(f"Нет обработчика для типа: {action_type}")
        
        try:
            logger.debug(f"🎯 Диспатч {action_type} -> {handler.__name__}")
            result = handler(**kwargs)
            return result
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения handler: {e}")
            raise
    
    def _register_default_handlers(self):
        """Регистрация дефолтных обработчиков"""
        
        # Mouse handlers
        def handle_mouse_click(**kwargs):
            logger.info(f"🖱️ Mouse click: {kwargs}")
            return {'success': True, 'action': 'mouse_click'}
        
        def handle_mouse_drag(**kwargs):
            logger.info(f"🖱️ Mouse drag: {kwargs}")
            return {'success': True, 'action': 'mouse_drag'}
        
        def handle_mouse_scroll(**kwargs):
            logger.info(f"🖱️ Mouse scroll: {kwargs}")
            return {'success': True, 'action': 'mouse_scroll'}
        
        # Keyboard handlers
        def handle_keyboard_type(**kwargs):
            logger.info(f"⌨️ Keyboard type: {kwargs}")
            return {'success': True, 'action': 'keyboard_type'}
        
        def handle_keyboard_shortcut(**kwargs):
            logger.info(f"⌨️ Keyboard shortcut: {kwargs}")
            return {'success': True, 'action': 'keyboard_shortcut'}
        
        # Window handlers
        def handle_window_focus(**kwargs):
            logger.info(f"🪟 Window focus: {kwargs}")
            return {'success': True, 'action': 'window_focus'}
        
        def handle_window_maximize(**kwargs):
            logger.info(f"🪟 Window maximize: {kwargs}")
            return {'success': True, 'action': 'window_maximize'}
        
        # Application handlers
        def handle_application_open(**kwargs):
            logger.info(f"📱 Application open: {kwargs}")
            return {'success': True, 'action': 'application_open'}
        
        def handle_application_close(**kwargs):
            logger.info(f"📱 Application close: {kwargs}")
            return {'success': True, 'action': 'application_close'}
        
        # Browser handlers
        def handle_browser_navigate(**kwargs):
            logger.info(f"🌐 Browser navigate: {kwargs}")
            return {'success': True, 'action': 'browser_navigate'}
        
        # File handlers
        def handle_file_open(**kwargs):
            logger.info(f"📁 File open: {kwargs}")
            return {'success': True, 'action': 'file_open'}
        
        # Регистрируем все handlers
        self.register_handler('mouse_handler', handle_mouse_click, ['mouse_click'])
        self.register_handler('mouse_drag_handler', handle_mouse_drag, ['mouse_drag'])
        self.register_handler('mouse_scroll_handler', handle_mouse_scroll, ['mouse_scroll'])
        self.register_handler('keyboard_handler', handle_keyboard_type, ['keyboard_type'])
        self.register_handler('shortcut_handler', handle_keyboard_shortcut, ['keyboard_shortcut'])
        self.register_handler('window_focus_handler', handle_window_focus, ['window_focus'])
        self.register_handler('window_maximize_handler', handle_window_maximize, ['window_maximize'])
        self.register_handler('app_open_handler', handle_application_open, ['application_open'])
        self.register_handler('app_close_handler', handle_application_close, ['application_close'])
        self.register_handler('browser_handler', handle_browser_navigate, ['browser_navigate'])
        self.register_handler('file_handler', handle_file_open, ['file_open'])
    
    def list_handlers(self) -> list:
        """Список всех handlers"""
        return [
            {
                'name': info.name,
                'types': info.action_types,
                'description': info.description
            }
            for info in self.handlers.values()
        ]
    
    def get_stats(self) -> dict:
        """Статистика реестра"""
        return {
            'total_handlers': len(self.handlers),
            'total_action_types': len(self.type_to_handler),
            'handlers': self.list_handlers()
        }


# Тесты
if __name__ == "__main__":
    registry = ActionHandlerRegistry()
    
    print("\n" + "="*60)
    print("🎯 ЗАРЕГИСТРИРОВАННЫЕ HANDLERS")
    print("="*60)
    
    stats = registry.get_stats()
    print(f"Всего handlers: {stats['total_handlers']}")
    print(f"Типов действий: {stats['total_action_types']}")
    
    print("\n" + "="*60)
    print("🧪 ТЕСТИРОВАНИЕ ДИСПАТЧА")
    print("="*60)
    
    # Тест 1: Mouse click
    result1 = registry.dispatch('mouse_click', x=100, y=200)
    print(f"✓ Mouse click: {result1}")
    
    # Тест 2: Keyboard type
    result2 = registry.dispatch('keyboard_type', text='Hello')
    print(f"✓ Keyboard type: {result2}")
    
    # Тест 3: Window focus
    result3 = registry.dispatch('window_focus', window_title='Chrome')
    print(f"✓ Window focus: {result3}")
    
    print("\n✅ Все тесты пройдены")
