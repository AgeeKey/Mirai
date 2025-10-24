#!/usr/bin/env python3
"""
⏭️ РАЗДЕЛ 2: SEQUENTIAL PLANNING (Шаги 41-80)
==============================================

Подразделы:
2.1: Ordering & Sequencing (Шаги 41-55) - Упорядочивание и последовательность
2.2: Plan Refinement (Шаги 56-70) - Уточнение плана
2.3: Adaptive Planning (Шаги 71-80) - Адаптивное планирование
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================================
# ПОДРАЗДЕЛ 2.1: ORDERING & SEQUENCING (Шаги 41-55)
# ============================================================================

class ExecutionOrderDeterminer:
    """
    Шаг 41: Determine Execution Order
    
    Определяет порядок выполнения подзадач на основе зависимостей.
    Использует топологическую сортировку.
    """
    
    def determine_order(self, tasks: List[Dict[str, Any]]) -> List[str]:
        """
        Определяет порядок выполнения задач
        
        Args:
            tasks: Список задач с зависимостями
            
        Returns:
            Упорядоченный список ID задач
        """
        logger.info("Шаг 41: Определение порядка выполнения задач")
        
        # Строим граф зависимостей
        graph = {}
        in_degree = {}
        
        for task in tasks:
            task_id = task.get('id', '')
            graph[task_id] = task.get('depends_on', [])
            in_degree[task_id] = len(task.get('depends_on', []))
        
        # Топологическая сортировка (алгоритм Кана)
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        order = []
        
        while queue:
            current = queue.popleft()
            order.append(current)
            
            # Уменьшаем in-degree для зависимых задач
            for task in tasks:
                if current in task.get('depends_on', []):
                    task_id = task.get('id', '')
                    in_degree[task_id] -= 1
                    if in_degree[task_id] == 0:
                        queue.append(task_id)
        
        # Проверка на циклы
        if len(order) != len(tasks):
            logger.warning("Обнаружен цикл в графе зависимостей!")
        
        logger.info(f"Определен порядок для {len(order)} задач")
        return order


class CriticalPathFinder:
    """
    Шаг 42: Identify Critical Path
    
    Находит критический путь - последовательность задач,
    которая определяет минимальное время выполнения всего плана.
    """
    
    def find_critical_path(
        self,
        tasks: List[Dict[str, Any]],
        execution_order: List[str]
    ) -> Tuple[List[str], float]:
        """
        Находит критический путь в графе задач
        
        Args:
            tasks: Список задач
            execution_order: Порядок выполнения
            
        Returns:
            Кортеж (критический путь, общая длительность)
        """
        logger.info("Шаг 42: Поиск критического пути")
        
        # Создаем словарь задач для быстрого доступа
        task_map = {t.get('id'): t for t in tasks}
        
        # Вычисляем earliest start time для каждой задачи
        earliest_start = {}
        earliest_finish = {}
        
        for task_id in execution_order:
            task = task_map.get(task_id, {})
            duration = task.get('estimated_duration', 10.0)
            
            # Начало = максимум из окончаний зависимых задач
            deps = task.get('depends_on', [])
            if deps:
                start_time = max(earliest_finish.get(dep, 0) for dep in deps)
            else:
                start_time = 0
            
            earliest_start[task_id] = start_time
            earliest_finish[task_id] = start_time + duration
        
        # Находим задачу с максимальным временем окончания
        if not earliest_finish:
            return [], 0.0
        
        end_task = max(earliest_finish, key=earliest_finish.get)
        total_duration = earliest_finish[end_task]
        
        # Восстанавливаем критический путь (идем назад)
        critical_path = [end_task]
        current = end_task
        
        while task_map.get(current, {}).get('depends_on'):
            deps = task_map[current].get('depends_on', [])
            # Выбираем зависимость с максимальным временем окончания
            if deps:
                prev = max(deps, key=lambda d: earliest_finish.get(d, 0))
                critical_path.insert(0, prev)
                current = prev
            else:
                break
        
        logger.info(f"Критический путь содержит {len(critical_path)} задач, "
                   f"длительность: {total_duration:.1f}с")
        
        return critical_path, total_duration


class ParallelizationAnalyzer:
    """
    Шаг 43: Identify Parallelization Opportunities
    
    Находит задачи, которые можно выполнять параллельно.
    """
    
    def find_parallel_groups(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[List[str]]:
        """
        Находит группы задач для параллельного выполнения
        
        Args:
            tasks: Список задач
            
        Returns:
            Список групп задач (каждая группа выполняется параллельно)
        """
        logger.info("Шаг 43: Поиск возможностей для параллелизации")
        
        # Группируем задачи по уровням (level-based scheduling)
        levels = defaultdict(list)
        task_map = {t.get('id'): t for t in tasks}
        
        # Вычисляем уровень каждой задачи
        task_levels = {}
        
        def compute_level(task_id: str) -> int:
            if task_id in task_levels:
                return task_levels[task_id]
            
            task = task_map.get(task_id, {})
            deps = task.get('depends_on', [])
            
            if not deps:
                level = 0
            else:
                level = max(compute_level(dep) for dep in deps) + 1
            
            task_levels[task_id] = level
            return level
        
        # Вычисляем уровни для всех задач
        for task in tasks:
            task_id = task.get('id')
            if task_id:
                level = compute_level(task_id)
                levels[level].append(task_id)
        
        # Преобразуем в список групп
        parallel_groups = [levels[i] for i in sorted(levels.keys())]
        
        logger.info(f"Найдено {len(parallel_groups)} уровней параллелизации")
        for i, group in enumerate(parallel_groups):
            logger.info(f"  Уровень {i}: {len(group)} задач(и)")
        
        return parallel_groups


class SequentialPlanCreator:
    """
    Шаг 44: Create Sequential Plan
    
    Создает последовательный план выполнения (если параллелизм невозможен).
    """
    
    def create_plan(
        self,
        tasks: List[Dict[str, Any]],
        execution_order: List[str]
    ) -> Dict[str, Any]:
        """
        Создает последовательный план
        
        Args:
            tasks: Список задач
            execution_order: Порядок выполнения
            
        Returns:
            Словарь с планом выполнения
        """
        logger.info("Шаг 44: Создание последовательного плана")
        
        task_map = {t.get('id'): t for t in tasks}
        
        plan = {
            'type': 'sequential',
            'steps': [],
            'total_duration': 0.0,
            'parallelism': 1
        }
        
        current_time = 0.0
        
        for task_id in execution_order:
            task = task_map.get(task_id, {})
            duration = task.get('estimated_duration', 10.0)
            
            step = {
                'task_id': task_id,
                'name': task.get('name', ''),
                'start_time': current_time,
                'end_time': current_time + duration,
                'duration': duration
            }
            
            plan['steps'].append(step)
            current_time += duration
        
        plan['total_duration'] = current_time
        
        logger.info(f"Последовательный план: {len(plan['steps'])} шагов, "
                   f"{plan['total_duration']:.1f}с")
        
        return plan


class ParallelPlanCreator:
    """
    Шаг 45: Create Parallel Execution Plan
    
    Создает план с параллельным выполнением задач.
    """
    
    def create_plan(
        self,
        tasks: List[Dict[str, Any]],
        parallel_groups: List[List[str]]
    ) -> Dict[str, Any]:
        """
        Создает параллельный план
        
        Args:
            tasks: Список задач
            parallel_groups: Группы для параллельного выполнения
            
        Returns:
            Словарь с планом выполнения
        """
        logger.info("Шаг 45: Создание плана с параллельным выполнением")
        
        task_map = {t.get('id'): t for t in tasks}
        
        plan = {
            'type': 'parallel',
            'stages': [],
            'total_duration': 0.0,
            'max_parallelism': max(len(g) for g in parallel_groups) if parallel_groups else 1
        }
        
        current_time = 0.0
        
        for stage_idx, group in enumerate(parallel_groups):
            # Находим максимальную длительность в группе
            stage_duration = 0.0
            stage_tasks = []
            
            for task_id in group:
                task = task_map.get(task_id, {})
                duration = task.get('estimated_duration', 10.0)
                stage_duration = max(stage_duration, duration)
                
                stage_tasks.append({
                    'task_id': task_id,
                    'name': task.get('name', ''),
                    'duration': duration,
                    'parallel': True
                })
            
            stage = {
                'stage': stage_idx,
                'start_time': current_time,
                'end_time': current_time + stage_duration,
                'duration': stage_duration,
                'tasks': stage_tasks,
                'parallelism': len(group)
            }
            
            plan['stages'].append(stage)
            current_time += stage_duration
        
        plan['total_duration'] = current_time
        
        logger.info(f"Параллельный план: {len(plan['stages'])} стадий, "
                   f"{plan['total_duration']:.1f}с, "
                   f"макс. параллелизм: {plan['max_parallelism']}")
        
        return plan


class TransitionMinimizer:
    """
    Шаг 49: Minimize Transitions
    
    Минимизирует переходы между различными приложениями/контекстами.
    """
    
    def minimize_transitions(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Переупорядочивает задачи для минимизации переходов
        
        Args:
            tasks: Исходный список задач
            
        Returns:
            Переупорядоченный список задач
        """
        logger.info("Шаг 49: Минимизация переходов между контекстами")
        
        # Группируем задачи по типу/домену
        groups = defaultdict(list)
        
        for task in tasks:
            domain = task.get('domain', task.get('type', 'default'))
            groups[domain].append(task)
        
        # Переупорядочиваем: сначала выполняем все задачи одного домена
        reordered = []
        for domain, domain_tasks in groups.items():
            logger.info(f"  Группа '{domain}': {len(domain_tasks)} задач(и)")
            reordered.extend(domain_tasks)
        
        logger.info(f"Минимизация переходов: {len(groups)} групп, "
                   f"примерно {len(groups)-1} переходов")
        
        return reordered


class CheckpointIdentifier:
    """
    Шаг 51: Identify Checkpoints
    
    Определяет точки сохранения состояния (checkpoints) для восстановления.
    """
    
    def identify_checkpoints(
        self,
        tasks: List[Dict[str, Any]],
        checkpoint_interval: int = 5
    ) -> List[str]:
        """
        Определяет checkpoints в плане
        
        Args:
            tasks: Список задач
            checkpoint_interval: Интервал между checkpoints
            
        Returns:
            Список ID задач, которые являются checkpoints
        """
        logger.info(f"Шаг 51: Определение checkpoints (интервал: {checkpoint_interval})")
        
        checkpoints = []
        
        for i, task in enumerate(tasks):
            task_id = task.get('id')
            
            # Checkpoint каждые N задач
            if i > 0 and (i + 1) % checkpoint_interval == 0:
                checkpoints.append(task_id)
            
            # Checkpoint перед рискованными операциями
            if task.get('risk_level') in ['high', 'critical']:
                if task_id not in checkpoints:
                    checkpoints.append(task_id)
        
        logger.info(f"Определено {len(checkpoints)} checkpoints")
        
        return checkpoints


# ============================================================================
# ПОДРАЗДЕЛ 2.2: PLAN REFINEMENT (Шаги 56-70)
# ============================================================================

class ErrorHandlerAdder:
    """
    Шаг 56: Add Error Handlers
    
    Добавляет обработчики ошибок для каждой подзадачи.
    """
    
    def add_handlers(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Добавляет error handlers к задачам
        
        Args:
            tasks: Список задач
            
        Returns:
            Задачи с добавленными handlers
        """
        logger.info("Шаг 56: Добавление обработчиков ошибок")
        
        for task in tasks:
            if 'error_handler' not in task:
                task['error_handler'] = {
                    'max_retries': 3,
                    'retry_delay': 5.0,
                    'fallback_action': 'skip',
                    'notify_on_failure': True
                }
        
        logger.info(f"Добавлены error handlers для {len(tasks)} задач")
        
        return tasks


class ValidationStepAdder:
    """
    Шаг 60: Add Validation Steps
    
    Добавляет шаги валидации после каждой подзадачи.
    """
    
    def add_validation_steps(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Добавляет validation steps
        
        Args:
            tasks: Список задач
            
        Returns:
            Задачи с добавленными validation steps
        """
        logger.info("Шаг 60: Добавление шагов валидации")
        
        enhanced_tasks = []
        
        for task in tasks:
            # Добавляем исходную задачу
            enhanced_tasks.append(task)
            
            # Добавляем validation step после важных задач
            if task.get('type') in ['execution', 'data_process', 'critical']:
                validation_step = {
                    'id': f"{task.get('id')}_validation",
                    'name': f"Валидация: {task.get('name', '')}",
                    'type': 'validation',
                    'description': 'Проверка корректности выполнения',
                    'depends_on': [task.get('id')],
                    'validation_criteria': [
                        'Результат не null',
                        'Нет ошибок',
                        'Postconditions выполнены'
                    ]
                }
                enhanced_tasks.append(validation_step)
        
        logger.info(f"Добавлено {len(enhanced_tasks) - len(tasks)} validation steps")
        
        return enhanced_tasks


class LoggingPointAdder:
    """
    Шаг 61: Add Logging Points
    
    Добавляет точки логирования прогресса.
    """
    
    def add_logging(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Добавляет logging points
        
        Args:
            tasks: Список задач
            
        Returns:
            Задачи с добавленным логированием
        """
        logger.info("Шаг 61: Добавление точек логирования")
        
        for task in tasks:
            if 'logging' not in task:
                task['logging'] = {
                    'log_start': True,
                    'log_end': True,
                    'log_errors': True,
                    'log_level': 'INFO'
                }
        
        return tasks


class SafetyCheckAdder:
    """
    Шаг 64: Add Safety Checks
    
    Добавляет проверки безопасности перед рискованными операциями.
    """
    
    def add_safety_checks(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Добавляет safety checks
        
        Args:
            tasks: Список задач
            
        Returns:
            Задачи с добавленными safety checks
        """
        logger.info("Шаг 64: Добавление проверок безопасности")
        
        enhanced_tasks = []
        
        for task in tasks:
            safety_check = None
            
            # Добавляем safety check перед рискованными операциями
            if task.get('risk_level') in ['high', 'critical']:
                safety_check = {
                    'id': f"{task.get('id')}_safety_check",
                    'name': f"Проверка безопасности перед {task.get('name', '')}",
                    'type': 'safety_check',
                    'description': 'Проверка безопасности операции',
                    'checks': [
                        'Проверить preconditions',
                        'Проверить доступность ресурсов',
                        'Создать backup (если нужно)',
                        'Подтвердить операцию'
                    ]
                }
                enhanced_tasks.append(safety_check)
            
            # Добавляем исходную задачу
            task_copy = task.copy()
            if safety_check:
                if 'depends_on' not in task_copy:
                    task_copy['depends_on'] = []
                task_copy['depends_on'].append(safety_check['id'])
            enhanced_tasks.append(task_copy)
        
        logger.info(f"Добавлено safety checks для рискованных операций")
        
        return enhanced_tasks


# ============================================================================
# ПОДРАЗДЕЛ 2.3: ADAPTIVE PLANNING (Шаги 71-80)
# ============================================================================

class ReplanningTriggerDetector:
    """
    Шаг 71: Dynamic Replanning Trigger
    
    Определяет когда нужен переплан.
    """
    
    def should_replan(
        self,
        execution_context: Dict[str, Any],
        original_plan: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Определяет нужен ли переплан
        
        Args:
            execution_context: Текущий контекст выполнения
            original_plan: Оригинальный план
            
        Returns:
            Кортеж (нужен_переплан, причина)
        """
        logger.info("Шаг 71: Проверка необходимости переплана")
        
        # Проверяем различные условия
        
        # 1. Слишком много ошибок
        error_rate = execution_context.get('error_rate', 0.0)
        if error_rate > 0.5:
            return True, "Высокий процент ошибок (>50%)"
        
        # 2. Изменились доступные ресурсы
        if execution_context.get('resources_changed'):
            return True, "Изменились доступные ресурсы"
        
        # 3. Превышен таймаут
        actual_time = execution_context.get('elapsed_time', 0)
        expected_time = original_plan.get('total_duration', float('inf'))
        if actual_time > expected_time * 1.5:
            return True, "Превышено ожидаемое время выполнения"
        
        # 4. Критическая задача провалилась
        if execution_context.get('critical_failure'):
            return True, "Критическая задача провалилась"
        
        return False, ""


class IncrementalReplanner:
    """
    Шаг 72: Incremental Replanning
    
    Выполняет инкрементальный переплан (минимальные изменения).
    """
    
    def replan(
        self,
        original_plan: Dict[str, Any],
        failed_task: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Выполняет инкрементальный переплан
        
        Args:
            original_plan: Оригинальный план
            failed_task: ID провалившейся задачи
            context: Контекст выполнения
            
        Returns:
            Обновленный план
        """
        logger.info(f"Шаг 72: Инкрементальный переплан после сбоя {failed_task}")
        
        # Копируем оригинальный план
        new_plan = original_plan.copy()
        
        # Находим провалившуюся задачу и зависимые от нее
        # В упрощенной версии просто помечаем для retry
        if 'tasks' in new_plan:
            for task in new_plan['tasks']:
                if task.get('id') == failed_task:
                    # Добавляем retry
                    task['retry_count'] = task.get('retry_count', 0) + 1
                    task['status'] = 'pending'
                    logger.info(f"Задача {failed_task} будет повторена "
                               f"(попытка {task['retry_count']})")
        
        return new_plan


class PlanBacktracker:
    """
    Шаг 76: Plan Backtracking
    
    Откатывается на предыдущий шаг и пробует альтернативу.
    """
    
    def backtrack(
        self,
        plan: Dict[str, Any],
        current_task: str
    ) -> Optional[str]:
        """
        Выполняет backtracking
        
        Args:
            plan: Текущий план
            current_task: Текущая задача
            
        Returns:
            ID задачи для возврата или None
        """
        logger.info(f"Шаг 76: Backtracking от задачи {current_task}")
        
        # Находим предыдущую задачу
        tasks = plan.get('tasks', [])
        task_ids = [t.get('id') for t in tasks]
        
        try:
            current_idx = task_ids.index(current_task)
            if current_idx > 0:
                previous_task = task_ids[current_idx - 1]
                logger.info(f"Возврат к задаче {previous_task}")
                return previous_task
        except ValueError:
            pass
        
        logger.info("Невозможно выполнить backtracking")
        return None


class RealityAdapter:
    """
    Шаг 80: Plan Adaptation for Reality
    
    Адаптирует план к реальному состоянию системы.
    """
    
    def adapt_to_reality(
        self,
        plan: Dict[str, Any],
        reality: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Адаптирует план к реальности
        
        Args:
            plan: Исходный план
            reality: Реальное состояние системы
            
        Returns:
            Адаптированный план
        """
        logger.info("Шаг 80: Адаптация плана к реальности")
        
        adapted_plan = plan.copy()
        
        # Проверяем различия между ожиданиями и реальностью
        expected_state = plan.get('expected_state', {})
        actual_state = reality.get('current_state', {})
        
        differences = []
        for key in expected_state:
            if key in actual_state:
                if expected_state[key] != actual_state[key]:
                    differences.append(key)
                    logger.info(f"  Различие: {key} "
                               f"ожидалось={expected_state[key]}, "
                               f"реальность={actual_state[key]}")
        
        # Адаптируем план если есть различия
        if differences:
            adapted_plan['adapted'] = True
            adapted_plan['differences'] = differences
            adapted_plan['adaptation_reason'] = "Несоответствие реальности ожиданиям"
        
        return adapted_plan
