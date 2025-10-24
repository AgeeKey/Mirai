#!/usr/bin/env python3
"""
🔄 ПОДРАЗДЕЛ 1.2: DECOMPOSITION STRATEGIES (Шаги 16-30)
=======================================================

Различные стратегии разложения задач на подзадачи:
- Линейное разложение
- Иерархическое разложение
- Модульное разложение
- И другие подходы
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .task_decomposition import ParsedTask, Subtask, TaskType, ComplexityLevel

logger = logging.getLogger(__name__)


# ============================================================================
# БАЗОВЫЙ ИНТЕРФЕЙС
# ============================================================================

class DecompositionStrategy(ABC):
    """Базовый класс для всех стратегий разложения"""
    
    @abstractmethod
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Разложить задачу на подзадачи
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список подзадач в виде словарей
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Возвращает название стратегии"""
        pass


# ============================================================================
# СТРАТЕГИИ РАЗЛОЖЕНИЯ
# ============================================================================

class LinearDecomposer(DecompositionStrategy):
    """
    Шаг 16: Linear Decomposition
    
    Разложение задачи на последовательные шаги: A → B → C → D
    Простейший случай для линейных процессов.
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Линейное разложение задачи
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список последовательных шагов
        """
        logger.info(f"Шаг 16: Линейное разложение задачи '{task.goal}'")
        
        steps = []
        
        # Базовая последовательность для любой задачи
        base_steps = [
            {
                'id': f'{task.fingerprint}_0',
                'name': 'Подготовка',
                'description': 'Подготовить окружение и ресурсы',
                'type': 'preparation'
            },
            {
                'id': f'{task.fingerprint}_1',
                'name': 'Выполнение',
                'description': f'Выполнить основное действие: {task.goal}',
                'type': 'execution',
                'depends_on': [f'{task.fingerprint}_0']
            },
            {
                'id': f'{task.fingerprint}_2',
                'name': 'Проверка',
                'description': 'Проверить результат выполнения',
                'type': 'validation',
                'depends_on': [f'{task.fingerprint}_1']
            },
            {
                'id': f'{task.fingerprint}_3',
                'name': 'Завершение',
                'description': 'Сохранить результат и очистить ресурсы',
                'type': 'cleanup',
                'depends_on': [f'{task.fingerprint}_2']
            }
        ]
        
        return base_steps
    
    def get_strategy_name(self) -> str:
        return "Linear (Линейное)"


class HierarchicalDecomposer(DecompositionStrategy):
    """
    Шаг 17: Hierarchical Decomposition
    
    Разложение в иерархию (дерево): Top-level → Mid-level → Leaf tasks
    Используется для сложных задач с подзадачами на разных уровнях.
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Иерархическое разложение задачи
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Иерархический список задач
        """
        logger.info(f"Шаг 17: Иерархическое разложение задачи '{task.goal}'")
        
        # Создаем 3-уровневую иерархию
        hierarchy = []
        
        # Уровень 1: Главная задача разбита на фазы
        phases = ['Анализ', 'Планирование', 'Реализация', 'Проверка']
        
        for phase_idx, phase in enumerate(phases):
            phase_id = f'{task.fingerprint}_phase_{phase_idx}'
            
            # Добавляем фазу
            hierarchy.append({
                'id': phase_id,
                'name': phase,
                'description': f'Фаза {phase} для задачи {task.goal}',
                'type': 'phase',
                'level': 1,
                'parent': None,
                'children': []
            })
            
            # Уровень 2: Каждая фаза содержит подзадачи
            for subtask_idx in range(2):  # 2 подзадачи на фазу
                subtask_id = f'{phase_id}_sub_{subtask_idx}'
                
                hierarchy.append({
                    'id': subtask_id,
                    'name': f'{phase} - Подзадача {subtask_idx + 1}',
                    'description': f'Выполнить подзадачу {subtask_idx + 1} фазы {phase}',
                    'type': 'subtask',
                    'level': 2,
                    'parent': phase_id,
                    'depends_on': [f'{phase_id}_sub_{subtask_idx - 1}'] if subtask_idx > 0 else []
                })
        
        return hierarchy
    
    def get_strategy_name(self) -> str:
        return "Hierarchical (Иерархическое)"


class ModularDecomposer(DecompositionStrategy):
    """
    Шаг 18: Modular Decomposition
    
    Разложение на модули - каждый модуль независим и переиспользуем.
    Подходит для задач с логическими блоками.
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Модульное разложение задачи
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список модулей
        """
        logger.info(f"Шаг 18: Модульное разложение задачи '{task.goal}'")
        
        modules = []
        
        # Стандартные модули для большинства задач
        module_types = {
            'input': 'Модуль ввода данных',
            'processing': 'Модуль обработки',
            'validation': 'Модуль валидации',
            'output': 'Модуль вывода результатов'
        }
        
        for idx, (mod_type, description) in enumerate(module_types.items()):
            modules.append({
                'id': f'{task.fingerprint}_module_{mod_type}',
                'name': f'Модуль: {mod_type}',
                'description': description,
                'type': 'module',
                'module_type': mod_type,
                'reusable': True,
                'depends_on': []  # Модули максимально независимы
            })
        
        return modules
    
    def get_strategy_name(self) -> str:
        return "Modular (Модульное)"


class ProblemSolvingDecomposer(DecompositionStrategy):
    """
    Шаг 19: Problem-Solving Decomposition
    
    Разложение как в системе решения проблем:
    Define → Analyze → Solve → Verify
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Разложение через решение проблем
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список шагов решения проблемы
        """
        logger.info(f"Шаг 19: Problem-Solving разложение задачи '{task.goal}'")
        
        steps = [
            {
                'id': f'{task.fingerprint}_define',
                'name': 'Определение проблемы',
                'description': 'Четко определить что нужно решить',
                'type': 'define',
                'phase': 'definition'
            },
            {
                'id': f'{task.fingerprint}_analyze',
                'name': 'Анализ проблемы',
                'description': 'Проанализировать причины и контекст',
                'type': 'analyze',
                'phase': 'analysis',
                'depends_on': [f'{task.fingerprint}_define']
            },
            {
                'id': f'{task.fingerprint}_solve',
                'name': 'Решение проблемы',
                'description': f'Выполнить действие: {task.goal}',
                'type': 'solve',
                'phase': 'solution',
                'depends_on': [f'{task.fingerprint}_analyze']
            },
            {
                'id': f'{task.fingerprint}_verify',
                'name': 'Верификация решения',
                'description': 'Проверить что проблема решена',
                'type': 'verify',
                'phase': 'verification',
                'depends_on': [f'{task.fingerprint}_solve']
            }
        ]
        
        return steps
    
    def get_strategy_name(self) -> str:
        return "Problem-Solving (Решение проблем)"


class StateBasedDecomposer(DecompositionStrategy):
    """
    Шаг 20: State-Based Decomposition
    
    Разложение как переходы между состояниями:
    State1 → Action → State2 → Action → State3
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Разложение через состояния
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список переходов состояний
        """
        logger.info(f"Шаг 20: State-Based разложение задачи '{task.goal}'")
        
        states = []
        
        # Определяем состояния и переходы
        state_transitions = [
            ('initial', 'Начальное состояние', None),
            ('prepared', 'Состояние готовности', 'initial'),
            ('executing', 'Состояние выполнения', 'prepared'),
            ('completed', 'Завершенное состояние', 'executing')
        ]
        
        for state_name, description, from_state in state_transitions:
            state_id = f'{task.fingerprint}_state_{state_name}'
            
            step = {
                'id': state_id,
                'name': f'Переход в {state_name}',
                'description': description,
                'type': 'state_transition',
                'state': state_name,
                'depends_on': [f'{task.fingerprint}_state_{from_state}'] if from_state else []
            }
            
            states.append(step)
        
        return states
    
    def get_strategy_name(self) -> str:
        return "State-Based (На основе состояний)"


class GoalBasedDecomposer(DecompositionStrategy):
    """
    Шаг 21: Goal-Based Decomposition
    
    Разложение по подцелям (means-ends analysis):
    Главная цель → подцели → примитивные операции
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Разложение через цели
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Иерархия целей и подцелей
        """
        logger.info(f"Шаг 21: Goal-Based разложение задачи '{task.goal}'")
        
        goals = []
        
        # Главная цель
        main_goal_id = f'{task.fingerprint}_goal_main'
        goals.append({
            'id': main_goal_id,
            'name': 'Главная цель',
            'description': task.goal,
            'type': 'main_goal',
            'level': 0
        })
        
        # Подцели
        subgoals = [
            'Получить необходимую информацию',
            'Выполнить обработку',
            'Достичь результата'
        ]
        
        for idx, subgoal in enumerate(subgoals):
            subgoal_id = f'{task.fingerprint}_goal_sub_{idx}'
            goals.append({
                'id': subgoal_id,
                'name': f'Подцель {idx + 1}',
                'description': subgoal,
                'type': 'subgoal',
                'level': 1,
                'parent_goal': main_goal_id,
                'depends_on': [f'{task.fingerprint}_goal_sub_{idx - 1}'] if idx > 0 else []
            })
        
        return goals
    
    def get_strategy_name(self) -> str:
        return "Goal-Based (На основе целей)"


class DataFlowDecomposer(DecompositionStrategy):
    """
    Шаг 23: Data-Flow Decomposition
    
    Разложение по потокам данных:
    Откуда данные → обработка → куда выходят
    """
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Разложение через потоки данных
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Список этапов обработки данных
        """
        logger.info(f"Шаг 23: Data-Flow разложение задачи '{task.goal}'")
        
        flow_steps = [
            {
                'id': f'{task.fingerprint}_data_input',
                'name': 'Получение данных',
                'description': 'Получить входные данные',
                'type': 'data_input',
                'data_flow': 'input'
            },
            {
                'id': f'{task.fingerprint}_data_transform',
                'name': 'Трансформация данных',
                'description': 'Преобразовать данные в нужный формат',
                'type': 'data_transform',
                'data_flow': 'transform',
                'depends_on': [f'{task.fingerprint}_data_input']
            },
            {
                'id': f'{task.fingerprint}_data_process',
                'name': 'Обработка данных',
                'description': f'Обработать данные для {task.goal}',
                'type': 'data_process',
                'data_flow': 'process',
                'depends_on': [f'{task.fingerprint}_data_transform']
            },
            {
                'id': f'{task.fingerprint}_data_output',
                'name': 'Вывод результата',
                'description': 'Вывести обработанные данные',
                'type': 'data_output',
                'data_flow': 'output',
                'depends_on': [f'{task.fingerprint}_data_process']
            }
        ]
        
        return flow_steps
    
    def get_strategy_name(self) -> str:
        return "Data-Flow (Поток данных)"


class DomainSpecificDecomposer(DecompositionStrategy):
    """
    Шаг 24: Domain-Specific Decomposition
    
    Для каждого домена (Chrome, CapCut, etc.) свой способ разложения.
    """
    
    def __init__(self):
        self.domain_templates = {
            'chrome': self._chrome_decomposition,
            'browser': self._chrome_decomposition,
            'vscode': self._vscode_decomposition,
            'editor': self._vscode_decomposition,
            'file': self._file_decomposition,
            'api': self._api_decomposition,
        }
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Domain-specific разложение
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Специфичные для домена шаги
        """
        logger.info(f"Шаг 24: Domain-Specific разложение задачи '{task.goal}'")
        
        # Определяем домен из ресурсов или текста
        domain = self._identify_domain(task)
        
        # Получаем соответствующий шаблон
        decomposition_func = self.domain_templates.get(
            domain,
            self._default_decomposition
        )
        
        return decomposition_func(task)
    
    def _identify_domain(self, task: ParsedTask) -> str:
        """Определяет домен задачи"""
        text_lower = task.raw_text.lower()
        
        if any(word in text_lower for word in ['браузер', 'chrome', 'browser', 'сайт']):
            return 'chrome'
        elif any(word in text_lower for word in ['код', 'code', 'vscode']):
            return 'vscode'
        elif any(word in text_lower for word in ['файл', 'file']):
            return 'file'
        elif any(word in text_lower for word in ['api', 'запрос', 'request']):
            return 'api'
        
        return 'unknown'
    
    def _chrome_decomposition(self, task: ParsedTask) -> List[Dict]:
        """Разложение для работы с браузером"""
        return [
            {'id': f'{task.fingerprint}_chrome_0', 'name': 'Запуск браузера', 
             'description': 'Открыть Chrome с нужным профилем'},
            {'id': f'{task.fingerprint}_chrome_1', 'name': 'Навигация', 
             'description': 'Перейти на нужную страницу',
             'depends_on': [f'{task.fingerprint}_chrome_0']},
            {'id': f'{task.fingerprint}_chrome_2', 'name': 'Взаимодействие', 
             'description': f'Выполнить действие: {task.goal}',
             'depends_on': [f'{task.fingerprint}_chrome_1']},
            {'id': f'{task.fingerprint}_chrome_3', 'name': 'Получение результата', 
             'description': 'Извлечь результат со страницы',
             'depends_on': [f'{task.fingerprint}_chrome_2']},
        ]
    
    def _vscode_decomposition(self, task: ParsedTask) -> List[Dict]:
        """Разложение для работы с редактором кода"""
        return [
            {'id': f'{task.fingerprint}_vscode_0', 'name': 'Открыть VSCode', 
             'description': 'Запустить редактор'},
            {'id': f'{task.fingerprint}_vscode_1', 'name': 'Открыть файл', 
             'description': 'Открыть нужный файл',
             'depends_on': [f'{task.fingerprint}_vscode_0']},
            {'id': f'{task.fingerprint}_vscode_2', 'name': 'Редактирование', 
             'description': f'Выполнить: {task.goal}',
             'depends_on': [f'{task.fingerprint}_vscode_1']},
            {'id': f'{task.fingerprint}_vscode_3', 'name': 'Сохранение', 
             'description': 'Сохранить изменения',
             'depends_on': [f'{task.fingerprint}_vscode_2']},
        ]
    
    def _file_decomposition(self, task: ParsedTask) -> List[Dict]:
        """Разложение для работы с файлами"""
        return [
            {'id': f'{task.fingerprint}_file_0', 'name': 'Проверка существования', 
             'description': 'Проверить что файл существует'},
            {'id': f'{task.fingerprint}_file_1', 'name': 'Чтение/Запись', 
             'description': f'Выполнить: {task.goal}',
             'depends_on': [f'{task.fingerprint}_file_0']},
            {'id': f'{task.fingerprint}_file_2', 'name': 'Валидация', 
             'description': 'Проверить корректность операции',
             'depends_on': [f'{task.fingerprint}_file_1']},
        ]
    
    def _api_decomposition(self, task: ParsedTask) -> List[Dict]:
        """Разложение для работы с API"""
        return [
            {'id': f'{task.fingerprint}_api_0', 'name': 'Подготовка запроса', 
             'description': 'Сформировать параметры запроса'},
            {'id': f'{task.fingerprint}_api_1', 'name': 'Отправка запроса', 
             'description': 'Выполнить API запрос',
             'depends_on': [f'{task.fingerprint}_api_0']},
            {'id': f'{task.fingerprint}_api_2', 'name': 'Обработка ответа', 
             'description': 'Обработать полученные данные',
             'depends_on': [f'{task.fingerprint}_api_1']},
            {'id': f'{task.fingerprint}_api_3', 'name': 'Обработка ошибок', 
             'description': 'Проверить и обработать возможные ошибки',
             'depends_on': [f'{task.fingerprint}_api_2']},
        ]
    
    def _default_decomposition(self, task: ParsedTask) -> List[Dict]:
        """Разложение по умолчанию"""
        return [
            {'id': f'{task.fingerprint}_default_0', 'name': 'Подготовка'},
            {'id': f'{task.fingerprint}_default_1', 'name': 'Выполнение',
             'depends_on': [f'{task.fingerprint}_default_0']},
            {'id': f'{task.fingerprint}_default_2', 'name': 'Завершение',
             'depends_on': [f'{task.fingerprint}_default_1']},
        ]
    
    def get_strategy_name(self) -> str:
        return "Domain-Specific (По домену)"


class AdaptiveDecomposer(DecompositionStrategy):
    """
    Шаг 28: Adaptive Decomposition
    
    Выбирает стратегию разложения адаптивно в зависимости от типа задачи.
    """
    
    def __init__(self):
        self.strategies = {
            ComplexityLevel.SIMPLE: LinearDecomposer(),
            ComplexityLevel.MEDIUM: ModularDecomposer(),
            ComplexityLevel.COMPLEX: HierarchicalDecomposer(),
            ComplexityLevel.VERY_COMPLEX: GoalBasedDecomposer(),
        }
        
        self.type_strategies = {
            TaskType.SEARCH: DataFlowDecomposer(),
            TaskType.ANALYZE: ProblemSolvingDecomposer(),
            TaskType.EXECUTE: StateBasedDecomposer(),
        }
    
    def decompose(self, task: ParsedTask) -> List[Dict[str, Any]]:
        """
        Адаптивное разложение - выбор стратегии
        
        Args:
            task: Распарсенная задача
            
        Returns:
            Результат выбранной стратегии
        """
        logger.info(f"Шаг 28: Адаптивный выбор стратегии для задачи '{task.goal}'")
        
        # Сначала проверяем тип задачи
        if task.task_type in self.type_strategies:
            strategy = self.type_strategies[task.task_type]
            logger.info(f"Выбрана стратегия по типу: {strategy.get_strategy_name()}")
        # Иначе по сложности
        else:
            strategy = self.strategies.get(
                task.complexity,
                LinearDecomposer()
            )
            logger.info(f"Выбрана стратегия по сложности: {strategy.get_strategy_name()}")
        
        return strategy.decompose(task)
    
    def get_strategy_name(self) -> str:
        return "Adaptive (Адаптивное)"


class DecompositionValidator:
    """
    Шаг 29: Decomposition Validation
    
    Проверяет что разложение правильное:
    - Полнота
    - Непротиворечивость
    - Эффективность
    """
    
    def validate(
        self,
        decomposition: List[Dict[str, Any]],
        original_task: ParsedTask
    ) -> Dict[str, Any]:
        """
        Валидирует разложение задачи
        
        Args:
            decomposition: Результат разложения
            original_task: Исходная задача
            
        Returns:
            Результат валидации
        """
        logger.info("Шаг 29: Валидация разложения задачи")
        
        result = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'completeness': True,
            'consistency': True,
            'efficiency': 1.0
        }
        
        # Проверка полноты
        if len(decomposition) == 0:
            result['valid'] = False
            result['completeness'] = False
            result['issues'].append("Разложение пустое")
            return result
        
        # Проверка зависимостей (нет циклов)
        if self._has_dependency_cycle(decomposition):
            result['valid'] = False
            result['consistency'] = False
            result['issues'].append("Обнаружен цикл в зависимостях")
        
        # Проверка что все зависимости существуют
        all_ids = {step.get('id') for step in decomposition if 'id' in step}
        for step in decomposition:
            for dep in step.get('depends_on', []):
                if dep not in all_ids:
                    result['warnings'].append(
                        f"Зависимость '{dep}' не найдена в разложении"
                    )
        
        # Оценка эффективности (меньше шагов = лучше)
        step_count = len(decomposition)
        if step_count > 20:
            result['efficiency'] = 0.5
            result['warnings'].append("Слишком много шагов, возможно избыточность")
        elif step_count > 10:
            result['efficiency'] = 0.7
        else:
            result['efficiency'] = 1.0
        
        return result
    
    def _has_dependency_cycle(self, decomposition: List[Dict]) -> bool:
        """Проверяет наличие циклов в зависимостях"""
        graph = {}
        for step in decomposition:
            if 'id' in step:
                graph[step['id']] = step.get('depends_on', [])
        
        visited = set()
        rec_stack = set()
        
        def has_cycle_dfs(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if has_cycle_dfs(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if has_cycle_dfs(node):
                return True
        
        return False


class DecompositionOptimizer:
    """
    Шаг 30: Decomposition Optimization
    
    Оптимизирует разложение:
    - Минимум шагов
    - Максимум параллелизма
    - Минимум риска
    """
    
    def optimize(
        self,
        decomposition: List[Dict[str, Any]],
        optimization_goal: str = 'balanced'
    ) -> List[Dict[str, Any]]:
        """
        Оптимизирует разложение
        
        Args:
            decomposition: Исходное разложение
            optimization_goal: Цель оптимизации ('speed', 'safety', 'balanced')
            
        Returns:
            Оптимизированное разложение
        """
        logger.info(f"Шаг 30: Оптимизация разложения (цель: {optimization_goal})")
        
        optimized = decomposition.copy()
        
        if optimization_goal == 'speed':
            # Минимизируем количество шагов
            optimized = self._merge_sequential_steps(optimized)
        elif optimization_goal == 'safety':
            # Добавляем проверки и валидацию
            optimized = self._add_safety_checks(optimized)
        else:  # balanced
            # Баланс между скоростью и безопасностью
            optimized = self._balance_optimization(optimized)
        
        return optimized
    
    def _merge_sequential_steps(self, steps: List[Dict]) -> List[Dict]:
        """Объединяет последовательные однотипные шаги"""
        # Упрощенная реализация
        return steps
    
    def _add_safety_checks(self, steps: List[Dict]) -> List[Dict]:
        """Добавляет шаги проверки безопасности"""
        enhanced = []
        for step in steps:
            enhanced.append(step)
            # После каждого шага добавляем проверку
            if step.get('type') in ['execution', 'data_process']:
                check_step = {
                    'id': f"{step['id']}_safety_check",
                    'name': f"Проверка безопасности после {step.get('name', 'шага')}",
                    'description': 'Проверка корректности и безопасности',
                    'type': 'safety_check',
                    'depends_on': [step['id']]
                }
                enhanced.append(check_step)
        return enhanced
    
    def _balance_optimization(self, steps: List[Dict]) -> List[Dict]:
        """Балансирует оптимизацию"""
        # Комбинация обоих подходов
        return steps
