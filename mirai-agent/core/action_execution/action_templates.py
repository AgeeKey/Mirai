#!/usr/bin/env python3
"""
📝 Action Templates - Шаблоны действий
Шаг 4 из 150: Load Action Templates

Загружает templates для базовых actions:
- Click, Type, Navigate, Select, etc.
"""

import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ActionTemplate:
    """Шаблон действия"""
    
    def __init__(
        self,
        name: str,
        action_type: str,
        default_params: Dict[str, Any],
        required_params: list,
        description: str
    ):
        self.name = name
        self.action_type = action_type
        self.default_params = default_params
        self.required_params = required_params
        self.description = description
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Валидация параметров"""
        for param in self.required_params:
            if param not in params:
                logger.error(f"❌ Отсутствует обязательный параметр: {param}")
                return False
        return True
    
    def create_action(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Создать действие из шаблона"""
        # Объединяем дефолтные и переданные параметры
        action_params = {**self.default_params, **params}
        
        if not self.validate_params(action_params):
            raise ValueError(f"Невалидные параметры для {self.name}")
        
        return {
            'type': self.action_type,
            'params': action_params,
            'description': self.description
        }


class ActionTemplateLoader:
    """
    Загрузчик шаблонов действий
    
    Предоставляет готовые шаблоны для:
    - Действий мыши (клик, drag, scroll)
    - Действий клавиатуры (type, shortcut, key press)
    - Действий окон (focus, maximize, close)
    - Действий приложений (open, close, switch)
    - Браузерных действий (navigate, click link, fill form)
    - Файловых операций (open, save, delete)
    """
    
    def __init__(self):
        self.templates: Dict[str, ActionTemplate] = {}
        self._load_default_templates()
        logger.info("📝 ActionTemplateLoader создан")
    
    def _load_default_templates(self):
        """Загрузить дефолтные шаблоны"""
        
        # === MOUSE ACTIONS ===
        self.templates['click'] = ActionTemplate(
            name='click',
            action_type='mouse_click',
            default_params={'button': 'left', 'clicks': 1},
            required_params=['x', 'y'],
            description='Клик мышью'
        )
        
        self.templates['double_click'] = ActionTemplate(
            name='double_click',
            action_type='mouse_click',
            default_params={'button': 'left', 'clicks': 2},
            required_params=['x', 'y'],
            description='Двойной клик'
        )
        
        self.templates['right_click'] = ActionTemplate(
            name='right_click',
            action_type='mouse_click',
            default_params={'button': 'right', 'clicks': 1},
            required_params=['x', 'y'],
            description='Правый клик'
        )
        
        self.templates['drag'] = ActionTemplate(
            name='drag',
            action_type='mouse_drag',
            default_params={'duration': 0.5},
            required_params=['x1', 'y1', 'x2', 'y2'],
            description='Перетащить мышью'
        )
        
        self.templates['scroll'] = ActionTemplate(
            name='scroll',
            action_type='mouse_scroll',
            default_params={'clicks': 3},
            required_params=['direction'],
            description='Скроллить'
        )
        
        # === KEYBOARD ACTIONS ===
        self.templates['type'] = ActionTemplate(
            name='type',
            action_type='keyboard_type',
            default_params={'interval': 0.05},
            required_params=['text'],
            description='Напечатать текст'
        )
        
        self.templates['press'] = ActionTemplate(
            name='press',
            action_type='keyboard_press',
            default_params={},
            required_params=['key'],
            description='Нажать клавишу'
        )
        
        self.templates['shortcut'] = ActionTemplate(
            name='shortcut',
            action_type='keyboard_shortcut',
            default_params={},
            required_params=['keys'],
            description='Комбинация клавиш'
        )
        
        self.templates['paste'] = ActionTemplate(
            name='paste',
            action_type='keyboard_paste',
            default_params={'shortcut': 'ctrl+v'},
            required_params=[],
            description='Вставить из буфера'
        )
        
        # === WINDOW ACTIONS ===
        self.templates['focus_window'] = ActionTemplate(
            name='focus_window',
            action_type='window_focus',
            default_params={},
            required_params=['window_title'],
            description='Переключиться на окно'
        )
        
        self.templates['maximize'] = ActionTemplate(
            name='maximize',
            action_type='window_maximize',
            default_params={},
            required_params=['window_title'],
            description='Максимизировать окно'
        )
        
        self.templates['minimize'] = ActionTemplate(
            name='minimize',
            action_type='window_minimize',
            default_params={},
            required_params=['window_title'],
            description='Минимизировать окно'
        )
        
        self.templates['close_window'] = ActionTemplate(
            name='close_window',
            action_type='window_close',
            default_params={},
            required_params=['window_title'],
            description='Закрыть окно'
        )
        
        # === APPLICATION ACTIONS ===
        self.templates['open_app'] = ActionTemplate(
            name='open_app',
            action_type='application_open',
            default_params={'wait_for_load': True},
            required_params=['app_name'],
            description='Открыть приложение'
        )
        
        self.templates['close_app'] = ActionTemplate(
            name='close_app',
            action_type='application_close',
            default_params={'force': False},
            required_params=['app_name'],
            description='Закрыть приложение'
        )
        
        # === BROWSER ACTIONS ===
        self.templates['navigate'] = ActionTemplate(
            name='navigate',
            action_type='browser_navigate',
            default_params={'wait_for_load': True},
            required_params=['url'],
            description='Перейти по URL'
        )
        
        self.templates['fill_form'] = ActionTemplate(
            name='fill_form',
            action_type='browser_fill_form',
            default_params={},
            required_params=['fields'],
            description='Заполнить форму'
        )
        
        # === FILE ACTIONS ===
        self.templates['open_file'] = ActionTemplate(
            name='open_file',
            action_type='file_open',
            default_params={'app': None},
            required_params=['path'],
            description='Открыть файл'
        )
        
        self.templates['save_file'] = ActionTemplate(
            name='save_file',
            action_type='file_save',
            default_params={},
            required_params=['path'],
            description='Сохранить файл'
        )
        
        logger.info(f"✅ Загружено {len(self.templates)} шаблонов действий")
    
    def get_template(self, name: str) -> Optional[ActionTemplate]:
        """Получить шаблон по имени"""
        return self.templates.get(name)
    
    def list_templates(self) -> list:
        """Список всех шаблонов"""
        return [
            {
                'name': name,
                'type': tmpl.action_type,
                'description': tmpl.description
            }
            for name, tmpl in self.templates.items()
        ]
    
    def create_from_template(self, template_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Создать действие из шаблона"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Шаблон не найден: {template_name}")
        
        return template.create_action(params)


# Тесты
if __name__ == "__main__":
    loader = ActionTemplateLoader()
    
    print("\n" + "="*60)
    print("📝 ДОСТУПНЫЕ ШАБЛОНЫ ДЕЙСТВИЙ")
    print("="*60)
    
    templates = loader.list_templates()
    for tmpl in templates:
        print(f"• {tmpl['name']}: {tmpl['description']}")
    
    print("\n" + "="*60)
    print("🧪 ТЕСТИРОВАНИЕ СОЗДАНИЯ ДЕЙСТВИЙ")
    print("="*60)
    
    # Тест 1: Клик
    action1 = loader.create_from_template('click', {'x': 100, 'y': 200})
    print(f"✓ Клик: {action1}")
    
    # Тест 2: Печать
    action2 = loader.create_from_template('type', {'text': 'Hello World'})
    print(f"✓ Печать: {action2}")
    
    # Тест 3: Комбинация клавиш
    action3 = loader.create_from_template('shortcut', {'keys': ['ctrl', 'c']})
    print(f"✓ Shortcut: {action3}")
    
    print("\n✅ Все тесты пройдены")
