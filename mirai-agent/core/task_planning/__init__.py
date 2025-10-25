#!/usr/bin/env python3
"""
🎯 ФАЗА 3: TASK PLANNING - Планирование задач КАК ЧЕЛОВЕК
=========================================================

Полная система планирования из 150 шагов для разбиения сложных задач.

Разделы:
1. TASK DECOMPOSITION (Шаги 1-40) - Разложение задач
2. SEQUENTIAL PLANNING (Шаги 41-80) - Последовательное планирование
3. OPTIMIZATION & VALIDATION (Шаги 81-130) - Оптимизация и валидация
4. INTEGRATION & FINALIZATION (Шаги 131-150) - Интеграция и финализация
"""

from .task_decomposition import (
    TaskParser,
    ConstraintExtractor,
    TaskTypeClassifier,
    ComplexityAnalyzer,
    ResourceIdentifier,
    TaskDecomposer,
)

from .decomposition_strategies import (
    LinearDecomposer,
    HierarchicalDecomposer,
    ModularDecomposer,
    AdaptiveDecomposer,
)

from .sequential_planning import (
    ExecutionOrderDeterminer,
    CriticalPathFinder,
    ParallelizationAnalyzer,
    SequentialPlanCreator,
)

from .optimization import (
    TimeOptimizer,
    ResourceOptimizer,
    SafetyOptimizer,
    MultiObjectiveOptimizer,
)

from .validation import (
    CompletenessChecker,
    ConsistencyChecker,
    FeasibilityChecker,
    SafetyChecker,
)

from .main_planner import TaskPlanningSystem

__all__ = [
    'TaskPlanningSystem',
    'TaskParser',
    'ConstraintExtractor',
    'TaskTypeClassifier',
    'ComplexityAnalyzer',
    'TaskDecomposer',
    'LinearDecomposer',
    'HierarchicalDecomposer',
    'ExecutionOrderDeterminer',
    'TimeOptimizer',
    'CompletenessChecker',
]

__version__ = '3.0.0'
__author__ = 'MIRAI Team'
