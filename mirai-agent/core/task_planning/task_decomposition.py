#!/usr/bin/env python3
"""
📋 РАЗДЕЛ 1: TASK DECOMPOSITION (Шаги 1-40)
==========================================

Подразделы:
1.1: Task Analysis (Шаги 1-15) - Анализ задачи
1.2: Decomposition Strategies (Шаги 16-30) - Стратегии разложения
1.3: Subtask Creation (Шаги 31-40) - Создание подзадач
"""

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# ============================================================================
# БАЗОВЫЕ ТИПЫ ДАННЫХ
# ============================================================================

class TaskType(Enum):
    """Шаг 3: Классификация типа задачи"""
    SEARCH = "search"          # Поиск информации
    EDIT = "edit"              # Редактирование
    ANALYZE = "analyze"        # Анализ
    EXECUTE = "execute"        # Выполнение команд
    CREATE = "create"          # Создание чего-то нового
    DELETE = "delete"          # Удаление
    NAVIGATE = "navigate"      # Навигация
    COMMUNICATE = "communicate" # Коммуникация
    UNKNOWN = "unknown"        # Неизвестно


class ComplexityLevel(Enum):
    """Шаг 4: Уровень сложности задачи"""
    SIMPLE = 1      # 1-3 шага
    MEDIUM = 2      # 4-10 шагов
    COMPLEX = 3     # 11+ шагов
    VERY_COMPLEX = 4  # 50+ шагов


class RiskLevel(Enum):
    """Шаг 10: Уровень риска"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TaskConstraint:
    """Шаг 2: Ограничения задачи"""
    time_limit: Optional[float] = None  # секунды
    budget: Optional[float] = None
    resources: List[str] = field(default_factory=list)
    safety_level: str = "normal"
    max_retries: int = 3


@dataclass
class TaskParameters:
    """Шаг 12: Параметры задачи"""
    search_query: Optional[str] = None
    file_path: Optional[str] = None
    output_format: Optional[str] = None
    target_app: Optional[str] = None
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedTask:
    """Результат парсинга задачи (Шаг 1)"""
    raw_text: str
    goal: str
    target: str
    scope: str
    task_type: TaskType
    complexity: ComplexityLevel
    constraints: TaskConstraint
    parameters: TaskParameters
    risk_level: RiskLevel
    fingerprint: str
    parsed_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# ПОДРАЗДЕЛ 1.1: TASK ANALYSIS (Шаги 1-15)
# ============================================================================

class TaskParser:
    """
    Шаг 1: Parse High-Level Task
    
    Парсит высокоуровневую задачу пользователя в структурированный формат.
    
    Пример:
        Вход: "Найди информацию о Python"
        Выход: goal="find info", target="Python", scope="general"
    """
    
    def __init__(self):
        self.action_keywords = {
            'search': ['найди', 'поищи', 'search', 'find', 'lookup'],
            'edit': ['измени', 'отредактируй', 'edit', 'modify', 'change'],
            'analyze': ['проанализируй', 'analyze', 'examine', 'review'],
            'execute': ['запусти', 'выполни', 'execute', 'run', 'start'],
            'create': ['создай', 'сделай', 'create', 'make', 'build'],
            'delete': ['удали', 'delete', 'remove', 'clear'],
        }
    
    def parse(self, user_task: str) -> ParsedTask:
        """
        Парсит задачу пользователя
        
        Args:
            user_task: Текст задачи от пользователя
            
        Returns:
            ParsedTask с распарсенной информацией
        """
        logger.info(f"Шаг 1: Парсинг задачи: {user_task}")
        
        # Определяем тип действия
        task_type = self._identify_task_type(user_task)
        
        # Извлекаем цель, объект и область
        goal, target, scope = self._extract_components(user_task, task_type)
        
        # Создаем объект с базовыми параметрами
        parsed = ParsedTask(
            raw_text=user_task,
            goal=goal,
            target=target,
            scope=scope,
            task_type=task_type,
            complexity=ComplexityLevel.SIMPLE,  # Будет переопределено позже
            constraints=TaskConstraint(),
            parameters=TaskParameters(),
            risk_level=RiskLevel.LOW,
            fingerprint=""
        )
        
        return parsed
    
    def _identify_task_type(self, text: str) -> TaskType:
        """Определяет тип задачи по ключевым словам"""
        text_lower = text.lower()
        
        for task_type, keywords in self.action_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return TaskType(task_type)
        
        return TaskType.UNKNOWN
    
    def _extract_components(self, text: str, task_type: TaskType) -> tuple:
        """Извлекает компоненты: цель, объект, область"""
        # Упрощенная логика - в реальности можно использовать NLP
        words = text.split()
        
        goal = task_type.value if task_type != TaskType.UNKNOWN else "process"
        target = words[-1] if words else "unknown"
        scope = "general"
        
        return goal, target, scope


class ConstraintExtractor:
    """
    Шаг 2: Extract Task Constraints
    
    Извлекает ограничения на выполнение задачи:
    - Временные лимиты
    - Бюджет
    - Доступные ресурсы
    """
    
    def extract(self, task_text: str) -> TaskConstraint:
        """
        Извлекает ограничения из текста задачи
        
        Args:
            task_text: Текст задачи
            
        Returns:
            TaskConstraint с ограничениями
        """
        logger.info("Шаг 2: Извлечение ограничений задачи")
        
        constraints = TaskConstraint()
        
        # Поиск временных ограничений
        time_match = re.search(r'(\d+)\s*(секунд|минут|час)', task_text.lower())
        if time_match:
            amount = int(time_match.group(1))
            unit = time_match.group(2)
            
            if 'секунд' in unit:
                constraints.time_limit = amount
            elif 'минут' in unit:
                constraints.time_limit = amount * 60
            elif 'час' in unit:
                constraints.time_limit = amount * 3600
        
        # Поиск упоминаний безопасности
        if any(word in task_text.lower() for word in ['осторожно', 'безопасно', 'careful', 'safe']):
            constraints.safety_level = "high"
        
        return constraints


class TaskTypeClassifier:
    """
    Шаг 3: Identify Task Type Classification
    
    Классифицирует тип задачи и подбирает шаблон решения.
    """
    
    def __init__(self):
        self.type_templates = {
            TaskType.SEARCH: self._search_template,
            TaskType.EDIT: self._edit_template,
            TaskType.ANALYZE: self._analyze_template,
            TaskType.EXECUTE: self._execute_template,
            TaskType.CREATE: self._create_template,
        }
    
    def classify(self, parsed_task: ParsedTask) -> Dict[str, Any]:
        """
        Классифицирует задачу и возвращает шаблон
        
        Args:
            parsed_task: Распарсенная задача
            
        Returns:
            Словарь с шаблоном выполнения
        """
        logger.info(f"Шаг 3: Классификация типа задачи: {parsed_task.task_type}")
        
        template_func = self.type_templates.get(
            parsed_task.task_type,
            self._default_template
        )
        
        return template_func(parsed_task)
    
    def _search_template(self, task: ParsedTask) -> Dict:
        """Шаблон для поисковых задач"""
        return {
            'type': 'search',
            'steps': [
                'Определить источник поиска',
                'Сформировать поисковый запрос',
                'Выполнить поиск',
                'Обработать результаты',
                'Вернуть информацию'
            ],
            'tools': ['browser', 'api', 'database']
        }
    
    def _edit_template(self, task: ParsedTask) -> Dict:
        """Шаблон для задач редактирования"""
        return {
            'type': 'edit',
            'steps': [
                'Открыть файл/приложение',
                'Найти место редактирования',
                'Выполнить изменения',
                'Сохранить результат',
                'Проверить изменения'
            ],
            'tools': ['file_system', 'editor', 'validator']
        }
    
    def _analyze_template(self, task: ParsedTask) -> Dict:
        """Шаблон для аналитических задач"""
        return {
            'type': 'analyze',
            'steps': [
                'Собрать данные',
                'Обработать данные',
                'Применить анализ',
                'Сформировать выводы',
                'Создать отчет'
            ],
            'tools': ['data_processor', 'analyzer', 'reporter']
        }
    
    def _execute_template(self, task: ParsedTask) -> Dict:
        """Шаблон для задач выполнения"""
        return {
            'type': 'execute',
            'steps': [
                'Проверить preconditions',
                'Подготовить окружение',
                'Выполнить команду',
                'Проверить результат',
                'Cleanup'
            ],
            'tools': ['executor', 'validator', 'monitor']
        }
    
    def _create_template(self, task: ParsedTask) -> Dict:
        """Шаблон для задач создания"""
        return {
            'type': 'create',
            'steps': [
                'Определить требования',
                'Создать структуру',
                'Заполнить содержимым',
                'Валидировать результат',
                'Сохранить'
            ],
            'tools': ['creator', 'validator', 'storage']
        }
    
    def _default_template(self, task: ParsedTask) -> Dict:
        """Шаблон по умолчанию"""
        return {
            'type': 'unknown',
            'steps': [
                'Проанализировать задачу',
                'Определить подход',
                'Выполнить действия',
                'Проверить результат'
            ],
            'tools': ['generic_processor']
        }


class ComplexityAnalyzer:
    """
    Шаг 4: Determine Task Complexity Level
    
    Определяет уровень сложности задачи:
    - Простая (1-3 шага)
    - Средняя (4-10 шагов)
    - Сложная (11+ шагов)
    """
    
    def analyze(self, parsed_task: ParsedTask, template: Dict) -> ComplexityLevel:
        """
        Анализирует сложность задачи
        
        Args:
            parsed_task: Распарсенная задача
            template: Шаблон выполнения
            
        Returns:
            ComplexityLevel
        """
        logger.info("Шаг 4: Определение уровня сложности")
        
        # Считаем факторы сложности
        step_count = len(template.get('steps', []))
        tool_count = len(template.get('tools', []))
        has_constraints = parsed_task.constraints.time_limit is not None
        
        # Вычисляем общий балл
        score = step_count
        score += tool_count * 0.5
        if has_constraints:
            score += 2
        
        # Определяем уровень
        if score <= 3:
            return ComplexityLevel.SIMPLE
        elif score <= 10:
            return ComplexityLevel.MEDIUM
        elif score <= 25:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.VERY_COMPLEX


class ResourceIdentifier:
    """
    Шаг 5: Identify Required Resources
    
    Определяет какие приложения/файлы/API нужны для выполнения задачи.
    """
    
    def __init__(self):
        self.app_keywords = {
            'chrome': ['браузер', 'chrome', 'browser', 'сайт', 'website'],
            'vscode': ['vscode', 'код', 'code', 'редактор', 'editor'],
            'terminal': ['терминал', 'terminal', 'команда', 'command'],
            'notepad': ['блокнот', 'notepad', 'текст', 'text'],
        }
    
    def identify(self, parsed_task: ParsedTask, template: Dict) -> List[str]:
        """
        Определяет необходимые ресурсы
        
        Args:
            parsed_task: Распарсенная задача
            template: Шаблон выполнения
            
        Returns:
            Список необходимых ресурсов
        """
        logger.info("Шаг 5: Определение необходимых ресурсов")
        
        resources = set()
        
        # Из шаблона
        resources.update(template.get('tools', []))
        
        # Из текста задачи
        text_lower = parsed_task.raw_text.lower()
        for app, keywords in self.app_keywords.items():
            if any(kw in text_lower for kw in keywords):
                resources.add(app)
        
        return list(resources)


class ResourceAvailabilityChecker:
    """
    Шаг 6: Check Resource Availability
    
    Проверяет доступность необходимых ресурсов.
    """
    
    def check(self, resources: List[str]) -> Dict[str, bool]:
        """
        Проверяет доступность ресурсов
        
        Args:
            resources: Список ресурсов для проверки
            
        Returns:
            Словарь {ресурс: доступен}
        """
        logger.info("Шаг 6: Проверка доступности ресурсов")
        
        availability = {}
        
        for resource in resources:
            # В реальной системе здесь была бы проверка
            # Пока возвращаем True для всех
            availability[resource] = True
        
        return availability


class DependencyAnalyzer:
    """
    Шаг 7: Analyze Task Dependencies
    
    Анализирует зависимости между подзадачами.
    """
    
    def analyze(self, subtasks: List[Dict]) -> Dict[str, List[str]]:
        """
        Анализирует зависимости
        
        Args:
            subtasks: Список подзадач
            
        Returns:
            Граф зависимостей
        """
        logger.info("Шаг 7: Анализ зависимостей задач")
        
        dependencies = {}
        
        for i, task in enumerate(subtasks):
            task_id = task.get('id', f'task_{i}')
            dependencies[task_id] = task.get('depends_on', [])
        
        return dependencies


class SuccessCriteriaDefiner:
    """
    Шаг 8: Determine Task Success Criteria
    
    Определяет критерии успешного выполнения задачи.
    """
    
    def define(self, parsed_task: ParsedTask, template: Dict) -> List[str]:
        """
        Определяет критерии успеха
        
        Args:
            parsed_task: Распарсенная задача
            template: Шаблон выполнения
            
        Returns:
            Список критериев
        """
        logger.info("Шаг 8: Определение критериев успеха")
        
        criteria = [
            "Все шаги выполнены без ошибок",
            "Результат соответствует ожиданиям",
            "Нет побочных эффектов"
        ]
        
        # Добавляем специфичные для типа задачи
        if parsed_task.task_type == TaskType.SEARCH:
            criteria.append("Информация найдена и релевантна")
        elif parsed_task.task_type == TaskType.CREATE:
            criteria.append("Объект создан и валиден")
        
        return criteria


class DurationEstimator:
    """
    Шаг 9: Estimate Task Duration
    
    Оценивает длительность выполнения задачи.
    """
    
    def estimate(self, complexity: ComplexityLevel, step_count: int) -> float:
        """
        Оценивает длительность в секундах
        
        Args:
            complexity: Уровень сложности
            step_count: Количество шагов
            
        Returns:
            Оценка времени в секундах
        """
        logger.info("Шаг 9: Оценка длительности задачи")
        
        # Базовое время на шаг в зависимости от сложности
        base_time_per_step = {
            ComplexityLevel.SIMPLE: 5,
            ComplexityLevel.MEDIUM: 10,
            ComplexityLevel.COMPLEX: 20,
            ComplexityLevel.VERY_COMPLEX: 30
        }
        
        base = base_time_per_step.get(complexity, 15)
        estimated = base * step_count
        
        # Добавляем накладные расходы
        overhead = estimated * 0.2
        
        return estimated + overhead


class RiskAssessor:
    """
    Шаг 10: Assess Task Risk Level
    
    Оценивает уровень риска задачи.
    """
    
    def assess(self, parsed_task: ParsedTask, resources: List[str]) -> RiskLevel:
        """
        Оценивает риск
        
        Args:
            parsed_task: Распарсенная задача
            resources: Необходимые ресурсы
            
        Returns:
            RiskLevel
        """
        logger.info("Шаг 10: Оценка уровня риска")
        
        risk_score = 0
        
        # Риск от типа задачи
        if parsed_task.task_type in [TaskType.DELETE, TaskType.EXECUTE]:
            risk_score += 2
        elif parsed_task.task_type in [TaskType.EDIT]:
            risk_score += 1
        
        # Риск от сложности
        risk_score += parsed_task.complexity.value - 1
        
        # Риск от количества ресурсов
        if len(resources) > 3:
            risk_score += 1
        
        # Определяем уровень
        if risk_score <= 1:
            return RiskLevel.LOW
        elif risk_score <= 3:
            return RiskLevel.MEDIUM
        elif risk_score <= 5:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL


class TaskFingerprinter:
    """
    Шаг 15: Task Fingerprinting
    
    Создает уникальный отпечаток задачи для поиска похожих.
    """
    
    def create_fingerprint(self, parsed_task: ParsedTask) -> str:
        """
        Создает отпечаток задачи
        
        Args:
            parsed_task: Распарсенная задача
            
        Returns:
            Хэш-строка отпечатка
        """
        logger.info("Шаг 15: Создание отпечатка задачи")
        
        # Комбинируем ключевые характеристики
        fingerprint_data = (
            f"{parsed_task.task_type.value}"
            f"{parsed_task.goal}"
            f"{parsed_task.target}"
            f"{parsed_task.complexity.value}"
        )
        
        # Создаем хэш
        return hashlib.md5(fingerprint_data.encode()).hexdigest()


# ============================================================================
# ПОДРАЗДЕЛ 1.2: DECOMPOSITION STRATEGIES (Шаги 16-30)
# ============================================================================
# Будет реализовано в decomposition_strategies.py

# ============================================================================
# ПОДРАЗДЕЛ 1.3: SUBTASK CREATION (Шаги 31-40)
# ============================================================================

@dataclass
class Subtask:
    """
    Шаг 31: Create Subtask Objects
    
    Представляет одну подзадачу в плане выполнения.
    """
    id: str
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    constraints: Optional[TaskConstraint] = None
    
    # Шаги 32-33: Pre/Postconditions
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    
    # Шаг 36: Duration
    estimated_duration: float = 0.0
    
    # Шаг 37: Dependencies
    depends_on: List[str] = field(default_factory=list)
    enables: List[str] = field(default_factory=list)
    
    # Шаг 38: Priority
    priority: int = 5  # 1-10, где 10 - максимальный
    
    # Статус
    status: str = "pending"
    result: Optional[Any] = None
    
    created_at: datetime = field(default_factory=datetime.now)


class SubtaskCreator:
    """
    Создает объекты подзадач на основе разложения.
    """
    
    def create_subtasks(
        self,
        steps: List[str],
        task_id: str,
        base_priority: int = 5
    ) -> List[Subtask]:
        """
        Создает подзадачи из списка шагов
        
        Args:
            steps: Список шагов для выполнения
            task_id: ID родительской задачи
            base_priority: Базовый приоритет
            
        Returns:
            Список подзадач
        """
        logger.info(f"Шаг 31: Создание {len(steps)} подзадач")
        
        subtasks = []
        
        for i, step in enumerate(steps):
            subtask = Subtask(
                id=f"{task_id}_subtask_{i}",
                name=f"Шаг {i+1}",
                description=step,
                priority=base_priority,
                estimated_duration=10.0  # Базовая оценка
            )
            
            # Добавляем зависимость от предыдущего шага
            if i > 0:
                subtask.depends_on.append(f"{task_id}_subtask_{i-1}")
            
            subtasks.append(subtask)
        
        return subtasks


class PreconditionDefiner:
    """
    Шаг 32: Define Subtask Preconditions
    
    Определяет предусловия для выполнения подзадачи.
    """
    
    def define(self, subtask: Subtask, context: Dict) -> List[str]:
        """
        Определяет preconditions
        
        Args:
            subtask: Подзадача
            context: Контекст выполнения
            
        Returns:
            Список preconditions
        """
        logger.info(f"Шаг 32: Определение preconditions для {subtask.id}")
        
        preconditions = []
        
        # Зависимости - это preconditions
        for dep in subtask.depends_on:
            preconditions.append(f"Задача {dep} завершена")
        
        # Контекстные preconditions
        if 'required_resources' in context:
            for res in context['required_resources']:
                preconditions.append(f"Ресурс {res} доступен")
        
        return preconditions


class PostconditionDefiner:
    """
    Шаг 33: Define Subtask Postconditions
    
    Определяет постусловия после выполнения подзадачи.
    """
    
    def define(self, subtask: Subtask) -> List[str]:
        """
        Определяет postconditions
        
        Args:
            subtask: Подзадача
            
        Returns:
            Список postconditions
        """
        logger.info(f"Шаг 33: Определение postconditions для {subtask.id}")
        
        postconditions = [
            f"{subtask.name} выполнен успешно",
            "Результат сохранен",
        ]
        
        # Специфичные для типа
        if 'search' in subtask.name.lower():
            postconditions.append("Информация найдена")
        elif 'create' in subtask.name.lower():
            postconditions.append("Объект создан")
        
        return postconditions


class DependencyGraphBuilder:
    """
    Шаг 37: Calculate Subtask Dependencies
    
    Строит граф зависимостей (DAG) между подзадачами.
    """
    
    def build_dag(self, subtasks: List[Subtask]) -> Dict[str, List[str]]:
        """
        Строит направленный ациклический граф зависимостей
        
        Args:
            subtasks: Список подзадач
            
        Returns:
            DAG в виде adjacency list
        """
        logger.info("Шаг 37: Построение графа зависимостей (DAG)")
        
        dag = {}
        
        for subtask in subtasks:
            dag[subtask.id] = subtask.depends_on.copy()
        
        # Проверка на циклы
        if self._has_cycle(dag):
            logger.warning("Обнаружен цикл в графе зависимостей!")
        
        return dag
    
    def _has_cycle(self, graph: Dict[str, List[str]]) -> bool:
        """Проверяет наличие циклов в графе"""
        visited = set()
        rec_stack = set()
        
        def visit(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if visit(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if visit(node):
                return True
        
        return False


class PriorityAssigner:
    """
    Шаг 38: Assign Subtask Priority
    
    Назначает приоритет каждой подзадаче.
    """
    
    def assign(self, subtasks: List[Subtask], critical_path: List[str]) -> None:
        """
        Назначает приоритеты подзадачам
        
        Args:
            subtasks: Список подзадач
            critical_path: Критический путь (самые важные задачи)
        """
        logger.info("Шаг 38: Назначение приоритетов подзадачам")
        
        for subtask in subtasks:
            # Высокий приоритет для критического пути
            if subtask.id in critical_path:
                subtask.priority = 10
            # Приоритет зависит от количества зависимых задач
            else:
                dependent_count = sum(
                    1 for s in subtasks if subtask.id in s.depends_on
                )
                subtask.priority = min(5 + dependent_count, 9)


class SubtaskSetValidator:
    """
    Шаг 40: Validate Subtask Set
    
    Проверяет что набор подзадач полностью покрывает исходную задачу.
    """
    
    def validate(
        self,
        subtasks: List[Subtask],
        original_task: ParsedTask,
        success_criteria: List[str]
    ) -> Dict[str, Any]:
        """
        Валидирует набор подзадач
        
        Args:
            subtasks: Список подзадач
            original_task: Исходная задача
            success_criteria: Критерии успеха
            
        Returns:
            Результат валидации
        """
        logger.info("Шаг 40: Валидация набора подзадач")
        
        result = {
            'valid': True,
            'issues': [],
            'coverage': 0.0,
            'completeness': True
        }
        
        # Проверка полноты
        if len(subtasks) == 0:
            result['valid'] = False
            result['issues'].append("Нет подзадач")
            result['completeness'] = False
        
        # Проверка зависимостей
        all_ids = {s.id for s in subtasks}
        for subtask in subtasks:
            for dep in subtask.depends_on:
                if dep not in all_ids:
                    result['valid'] = False
                    result['issues'].append(
                        f"Зависимость {dep} не найдена для {subtask.id}"
                    )
        
        # Оценка покрытия
        if result['valid']:
            result['coverage'] = 1.0
        else:
            result['coverage'] = max(0.0, 1.0 - len(result['issues']) * 0.2)
        
        return result


# ============================================================================
# ФАСАД ДЛЯ ДЕКОМПОЗИЦИИ ЗАДАЧ
# ============================================================================

class TaskDecomposer:
    """
    Фасад для декомпозиции задач.
    Объединяет все компоненты анализа и разбиения задач.
    """
    
    def __init__(self):
        """Инициализация декомпозера"""
        self.parser = TaskParser()
        self.classifier = TaskTypeClassifier()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.resource_identifier = ResourceIdentifier()
        self.subtask_creator = SubtaskCreator()
        self.validator = SubtaskSetValidator()
        logger.info("✅ TaskDecomposer инициализирован")
    
    def decompose(self, task_description: str) -> Dict[str, Any]:
        """
        Разложить задачу на подзадачи.
        
        Args:
            task_description: Описание задачи
            
        Returns:
            Результат декомпозиции с подзадачами
        """
        logger.info(f"🔍 Декомпозиция задачи: {task_description}")
        
        # 1. Парсинг задачи
        parsed = self.parser.parse(task_description)
        
        # 2. Классификация
        task_type = self.classifier.classify(parsed)
        
        # 3. Анализ сложности
        complexity = self.complexity_analyzer.analyze(parsed)
        
        # 4. Идентификация ресурсов
        resources = self.resource_identifier.identify(parsed)
        
        # 5. Создание подзадач
        subtasks = self.subtask_creator.create(
            parsed,
            task_type,
            complexity
        )
        
        # 6. Валидация
        validation = self.validator.validate(
            subtasks,
            parsed,
            parsed.success_criteria
        )
        
        return {
            'task': parsed,
            'type': task_type,
            'complexity': complexity,
            'resources': resources,
            'subtasks': subtasks,
            'validation': validation,
            'success': validation['valid']
        }
