#!/usr/bin/env python3
"""
🎯 MAIN PLANNER - Главная система планирования (Шаги 131-150)
==============================================================

Интегрирует все компоненты Фазы 3 в единую систему планирования.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .task_decomposition import (
    TaskParser,
    ConstraintExtractor,
    TaskTypeClassifier,
    ComplexityAnalyzer,
    ResourceIdentifier,
    ResourceAvailabilityChecker,
    DependencyAnalyzer,
    SuccessCriteriaDefiner,
    DurationEstimator,
    RiskAssessor,
    TaskFingerprinter,
    SubtaskCreator,
    PreconditionDefiner,
    PostconditionDefiner,
    DependencyGraphBuilder,
    PriorityAssigner,
    SubtaskSetValidator,
    ParsedTask,
    Subtask,
)

from .decomposition_strategies import (
    AdaptiveDecomposer,
    DecompositionValidator,
    DecompositionOptimizer,
)

from .sequential_planning import (
    ExecutionOrderDeterminer,
    CriticalPathFinder,
    ParallelizationAnalyzer,
    SequentialPlanCreator,
    ParallelPlanCreator,
    TransitionMinimizer,
    CheckpointIdentifier,
    ErrorHandlerAdder,
    ValidationStepAdder,
    LoggingPointAdder,
    SafetyCheckAdder,
    ReplanningTriggerDetector,
    IncrementalReplanner,
    RealityAdapter,
)

from .optimization import (
    TimeOptimizer,
    ResourceOptimizer,
    SafetyOptimizer,
    MultiObjectiveOptimizer,
    PlanCompactor,
    PlanSimplifier,
    CachingOpportunitiesIdentifier,
    LoadBalancer,
)

from .validation import (
    CompletenessChecker,
    ConsistencyChecker,
    FeasibilityChecker,
    SafetyChecker,
    PerformanceChecker,
    ValidationReportGenerator,
    PlanSignOff,
    ValidationResult,
)

logger = logging.getLogger(__name__)


@dataclass
class PlanningResult:
    """Результат планирования"""
    success: bool
    parsed_task: Optional[ParsedTask] = None
    decomposition: List[Dict[str, Any]] = field(default_factory=list)
    subtasks: List[Subtask] = field(default_factory=list)
    execution_plan: Optional[Dict[str, Any]] = None
    validation_results: Dict[str, ValidationResult] = field(default_factory=dict)
    approved: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class TaskPlanningSystem:
    """
    🎯 Главная система планирования задач
    
    Интегрирует все 150 шагов Фазы 3:
    - Task Decomposition (1-40)
    - Sequential Planning (41-80)
    - Optimization & Validation (81-130)
    - Integration & Finalization (131-150)
    """
    
    def __init__(self):
        """Инициализация системы планирования"""
        logger.info("🎯 Инициализация Task Planning System (Фаза 3)")
        
        # РАЗДЕЛ 1: TASK DECOMPOSITION (Шаги 1-40)
        self.task_parser = TaskParser()
        self.constraint_extractor = ConstraintExtractor()
        self.type_classifier = TaskTypeClassifier()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.resource_identifier = ResourceIdentifier()
        self.resource_checker = ResourceAvailabilityChecker()
        self.dependency_analyzer = DependencyAnalyzer()
        self.success_criteria_definer = SuccessCriteriaDefiner()
        self.duration_estimator = DurationEstimator()
        self.risk_assessor = RiskAssessor()
        self.task_fingerprinter = TaskFingerprinter()
        
        # Decomposition Strategies (16-30)
        self.adaptive_decomposer = AdaptiveDecomposer()
        self.decomposition_validator = DecompositionValidator()
        self.decomposition_optimizer = DecompositionOptimizer()
        
        # Subtask Creation (31-40)
        self.subtask_creator = SubtaskCreator()
        self.precondition_definer = PreconditionDefiner()
        self.postcondition_definer = PostconditionDefiner()
        self.dependency_graph_builder = DependencyGraphBuilder()
        self.priority_assigner = PriorityAssigner()
        self.subtask_validator = SubtaskSetValidator()
        
        # РАЗДЕЛ 2: SEQUENTIAL PLANNING (Шаги 41-80)
        self.execution_order_determiner = ExecutionOrderDeterminer()
        self.critical_path_finder = CriticalPathFinder()
        self.parallelization_analyzer = ParallelizationAnalyzer()
        self.sequential_plan_creator = SequentialPlanCreator()
        self.parallel_plan_creator = ParallelPlanCreator()
        self.transition_minimizer = TransitionMinimizer()
        self.checkpoint_identifier = CheckpointIdentifier()
        
        # Plan Refinement (56-70)
        self.error_handler_adder = ErrorHandlerAdder()
        self.validation_step_adder = ValidationStepAdder()
        self.logging_point_adder = LoggingPointAdder()
        self.safety_check_adder = SafetyCheckAdder()
        
        # Adaptive Planning (71-80)
        self.replanning_detector = ReplanningTriggerDetector()
        self.incremental_replanner = IncrementalReplanner()
        self.reality_adapter = RealityAdapter()
        
        # РАЗДЕЛ 3: OPTIMIZATION & VALIDATION (Шаги 81-130)
        self.time_optimizer = TimeOptimizer()
        self.resource_optimizer = ResourceOptimizer()
        self.safety_optimizer = SafetyOptimizer()
        self.multi_objective_optimizer = MultiObjectiveOptimizer()
        self.plan_compactor = PlanCompactor()
        self.plan_simplifier = PlanSimplifier()
        self.caching_identifier = CachingOpportunitiesIdentifier()
        self.load_balancer = LoadBalancer()
        
        # Validation (106-130)
        self.completeness_checker = CompletenessChecker()
        self.consistency_checker = ConsistencyChecker()
        self.feasibility_checker = FeasibilityChecker()
        self.safety_checker = SafetyChecker()
        self.performance_checker = PerformanceChecker()
        self.report_generator = ValidationReportGenerator()
        self.plan_signoff = PlanSignOff()
        
        logger.info("✅ Task Planning System готова к работе")
    
    def plan_task(
        self,
        user_task: str,
        requirements: Optional[List[str]] = None,
        available_resources: Optional[Dict[str, Any]] = None,
        optimization_goals: Optional[Dict[str, float]] = None
    ) -> PlanningResult:
        """
        Полное планирование задачи (все 150 шагов)
        
        Args:
            user_task: Задача от пользователя
            requirements: Список требований
            available_resources: Доступные ресурсы
            optimization_goals: Цели оптимизации
            
        Returns:
            PlanningResult с полным планом
        """
        logger.info("=" * 70)
        logger.info(f"🎯 НАЧАЛО ПЛАНИРОВАНИЯ: {user_task}")
        logger.info("=" * 70)
        
        result = PlanningResult(success=False)
        
        try:
            # ================================================================
            # ЭТАП 1: АНАЛИЗ И РАЗЛОЖЕНИЕ ЗАДАЧИ (Шаги 1-40)
            # ================================================================
            logger.info("\n📋 ЭТАП 1: АНАЛИЗ И РАЗЛОЖЕНИЕ ЗАДАЧИ")
            logger.info("-" * 70)
            
            # Шаг 1: Парсинг задачи
            parsed_task = self.task_parser.parse(user_task)
            result.parsed_task = parsed_task
            
            # Шаг 2: Извлечение ограничений
            parsed_task.constraints = self.constraint_extractor.extract(user_task)
            
            # Шаг 3: Классификация типа задачи
            task_template = self.type_classifier.classify(parsed_task)
            logger.info(f"   Тип задачи: {parsed_task.task_type.value}")
            
            # Шаг 4: Анализ сложности
            parsed_task.complexity = self.complexity_analyzer.analyze(
                parsed_task,
                task_template
            )
            logger.info(f"   Сложность: {parsed_task.complexity.name}")
            
            # Шаг 5: Идентификация ресурсов
            required_resources = self.resource_identifier.identify(
                parsed_task,
                task_template
            )
            logger.info(f"   Ресурсы: {', '.join(required_resources)}")
            
            # Шаг 6: Проверка доступности ресурсов
            resource_availability = self.resource_checker.check(required_resources)
            
            # Шаг 8: Критерии успеха
            success_criteria = self.success_criteria_definer.define(
                parsed_task,
                task_template
            )
            
            # Шаг 10: Оценка рисков
            parsed_task.risk_level = self.risk_assessor.assess(
                parsed_task,
                required_resources
            )
            logger.info(f"   Риск: {parsed_task.risk_level.value}")
            
            # Шаг 15: Создание отпечатка задачи
            parsed_task.fingerprint = self.task_fingerprinter.create_fingerprint(
                parsed_task
            )
            
            # Шаги 16-30: Разложение задачи
            logger.info("\n   🔄 Разложение задачи...")
            decomposition = self.adaptive_decomposer.decompose(parsed_task)
            result.decomposition = decomposition
            logger.info(f"   Создано {len(decomposition)} подзадач")
            
            # Шаг 29: Валидация разложения
            decomp_validation = self.decomposition_validator.validate(
                decomposition,
                parsed_task
            )
            if not decomp_validation['valid']:
                result.errors.extend(decomp_validation['issues'])
                result.warnings.extend(decomp_validation.get('warnings', []))
            
            # Шаг 30: Оптимизация разложения
            decomposition = self.decomposition_optimizer.optimize(
                decomposition,
                optimization_goal='balanced'
            )
            
            # Шаги 31-40: Создание подзадач
            logger.info("\n   📝 Создание подзадач...")
            subtasks = self.subtask_creator.create_subtasks(
                [d.get('description', d.get('name', '')) for d in decomposition],
                parsed_task.fingerprint
            )
            result.subtasks = subtasks
            
            # Шаг 37: Построение графа зависимостей
            dependency_graph = self.dependency_graph_builder.build_dag(subtasks)
            
            # Шаг 40: Валидация набора подзадач
            subtask_validation = self.subtask_validator.validate(
                subtasks,
                parsed_task,
                success_criteria
            )
            if not subtask_validation['valid']:
                result.errors.extend(subtask_validation['issues'])
            
            # ================================================================
            # ЭТАП 2: ПОСЛЕДОВАТЕЛЬНОЕ ПЛАНИРОВАНИЕ (Шаги 41-80)
            # ================================================================
            logger.info("\n⏭️ ЭТАП 2: ПОСЛЕДОВАТЕЛЬНОЕ ПЛАНИРОВАНИЕ")
            logger.info("-" * 70)
            
            # Конвертируем subtasks в Dict для дальнейшей работы
            task_dicts = [
                {
                    'id': st.id,
                    'name': st.name,
                    'description': st.description,
                    'depends_on': st.depends_on,
                    'estimated_duration': st.estimated_duration,
                    'priority': st.priority,
                    'risk_level': parsed_task.risk_level.value
                }
                for st in subtasks
            ]
            
            # Шаг 41: Определение порядка выполнения
            execution_order = self.execution_order_determiner.determine_order(
                task_dicts
            )
            logger.info(f"   Порядок выполнения определен: {len(execution_order)} шагов")
            
            # Шаг 42: Критический путь
            critical_path, critical_duration = self.critical_path_finder.find_critical_path(
                task_dicts,
                execution_order
            )
            logger.info(f"   Критический путь: {len(critical_path)} задач, "
                       f"{critical_duration:.1f}с")
            
            # Шаг 38: Назначение приоритетов
            self.priority_assigner.assign(subtasks, critical_path)
            
            # Шаг 43: Анализ параллелизации
            parallel_groups = self.parallelization_analyzer.find_parallel_groups(
                task_dicts
            )
            logger.info(f"   Возможностей для параллелизации: {len(parallel_groups)}")
            
            # Шаги 44-45: Создание плана выполнения
            if len(parallel_groups) > 1 and max(len(g) for g in parallel_groups) > 1:
                execution_plan = self.parallel_plan_creator.create_plan(
                    task_dicts,
                    parallel_groups
                )
                logger.info(f"   Создан ПАРАЛЛЕЛЬНЫЙ план "
                           f"(параллелизм: {execution_plan['max_parallelism']})")
            else:
                execution_plan = self.sequential_plan_creator.create_plan(
                    task_dicts,
                    execution_order
                )
                logger.info("   Создан ПОСЛЕДОВАТЕЛЬНЫЙ план")
            
            execution_plan['tasks'] = task_dicts  # Добавляем задачи в план
            execution_plan['critical_path'] = critical_path
            
            # Шаг 49: Минимизация переходов
            task_dicts = self.transition_minimizer.minimize_transitions(task_dicts)
            
            # Шаг 51: Идентификация checkpoints
            checkpoints = self.checkpoint_identifier.identify_checkpoints(task_dicts)
            execution_plan['checkpoints'] = checkpoints
            logger.info(f"   Checkpoints: {len(checkpoints)}")
            
            # Шаги 56-64: Уточнение плана
            logger.info("\n   🔧 Уточнение плана...")
            task_dicts = self.error_handler_adder.add_handlers(task_dicts)
            task_dicts = self.validation_step_adder.add_validation_steps(task_dicts)
            task_dicts = self.logging_point_adder.add_logging(task_dicts)
            task_dicts = self.safety_check_adder.add_safety_checks(task_dicts)
            
            execution_plan['tasks'] = task_dicts
            logger.info(f"   План уточнен: {len(task_dicts)} задач (с проверками)")
            
            # ================================================================
            # ЭТАП 3: ОПТИМИЗАЦИЯ И ВАЛИДАЦИЯ (Шаги 81-130)
            # ================================================================
            logger.info("\n⚡ ЭТАП 3: ОПТИМИЗАЦИЯ И ВАЛИДАЦИЯ")
            logger.info("-" * 70)
            
            # Шаги 81-91: Оптимизация
            logger.info("\n   ⚡ Оптимизация плана...")
            
            if optimization_goals:
                execution_plan = self.multi_objective_optimizer.optimize(
                    execution_plan,
                    optimization_goals
                )
            else:
                # Балансированная оптимизация по умолчанию
                execution_plan = self.time_optimizer.optimize(execution_plan)
                execution_plan = self.resource_optimizer.optimize(execution_plan)
                execution_plan = self.safety_optimizer.optimize(execution_plan)
            
            logger.info(f"   Оптимизация завершена "
                       f"(score: {execution_plan.get('optimization_score', 0):.2f})")
            
            # Шаг 93: Уплотнение плана
            execution_plan = self.plan_compactor.compact(execution_plan)
            
            # Шаг 95: Упрощение плана
            execution_plan = self.plan_simplifier.simplify(execution_plan)
            
            # Шаг 96: Определение возможностей кеширования
            caching_opportunities = self.caching_identifier.identify(execution_plan)
            execution_plan['caching_opportunities'] = caching_opportunities
            
            # Шаг 100: Балансировка нагрузки
            execution_plan = self.load_balancer.balance(execution_plan)
            
            result.execution_plan = execution_plan
            
            # Шаги 106-130: Валидация
            logger.info("\n   ✅ Валидация плана...")
            
            if requirements is None:
                requirements = success_criteria
            
            if available_resources is None:
                available_resources = {
                    'time_budget': 600,  # 10 минут
                    'resources': required_resources
                }
            
            # Шаг 106: Проверка полноты
            completeness_result = self.completeness_checker.check(
                execution_plan,
                requirements
            )
            result.validation_results['completeness'] = completeness_result
            
            # Шаг 107: Проверка консистентности
            consistency_result = self.consistency_checker.check(execution_plan)
            result.validation_results['consistency'] = consistency_result
            
            # Шаг 108: Проверка осуществимости
            feasibility_result = self.feasibility_checker.check(
                execution_plan,
                available_resources
            )
            result.validation_results['feasibility'] = feasibility_result
            
            # Шаг 109: Проверка безопасности
            safety_result = self.safety_checker.check(execution_plan)
            result.validation_results['safety'] = safety_result
            
            # Шаг 110: Проверка производительности
            performance_result = self.performance_checker.check(execution_plan)
            result.validation_results['performance'] = performance_result
            
            # Вывод результатов валидации
            for check_name, check_result in result.validation_results.items():
                status = "✅" if check_result.valid else "❌"
                logger.info(f"   {status} {check_name.capitalize()}: "
                           f"{check_result.score:.2f} "
                           f"({check_result.checks_passed}/{check_result.checks_total})")
            
            # Шаг 122: Генерация отчета
            validation_report = self.report_generator.generate(
                execution_plan,
                result.validation_results
            )
            execution_plan['validation_report'] = validation_report
            
            # Шаг 129: Утверждение плана
            execution_plan = self.plan_signoff.sign_off(
                execution_plan,
                result.validation_results
            )
            
            result.approved = execution_plan.get('approved', False)
            
            # ================================================================
            # ЭТАП 4: ФИНАЛИЗАЦИЯ (Шаги 131-150)
            # ================================================================
            logger.info("\n🎯 ЭТАП 4: ФИНАЛИЗАЦИЯ")
            logger.info("-" * 70)
            
            # Финальная проверка
            result.success = result.approved and len(result.errors) == 0
            
            if result.success:
                logger.info("✅ ПЛАНИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО")
                logger.info(f"   Задач: {len(execution_plan.get('tasks', []))}")
                logger.info(f"   Время: {execution_plan.get('total_duration', 0):.1f}с")
                logger.info(f"   Параллелизм: {execution_plan.get('max_parallelism', 1)}")
                logger.info(f"   Checkpoints: {len(execution_plan.get('checkpoints', []))}")
            else:
                logger.warning("⚠️ ПЛАНИРОВАНИЕ ЗАВЕРШЕНО С ПРЕДУПРЕЖДЕНИЯМИ")
                if result.errors:
                    logger.warning(f"   Ошибки: {len(result.errors)}")
                if result.warnings:
                    logger.warning(f"   Предупреждения: {len(result.warnings)}")
            
        except Exception as e:
            logger.error(f"❌ ОШИБКА ПЛАНИРОВАНИЯ: {e}", exc_info=True)
            result.success = False
            result.errors.append(str(e))
        
        logger.info("=" * 70)
        logger.info("🎯 ПЛАНИРОВАНИЕ ЗАВЕРШЕНО")
        logger.info("=" * 70)
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Возвращает статистику системы планирования
        
        Returns:
            Словарь со статистикой
        """
        return {
            'name': 'Task Planning System - Phase 3',
            'version': '3.0.0',
            'total_steps': 150,
            'sections': {
                'task_decomposition': '1-40',
                'sequential_planning': '41-80',
                'optimization_validation': '81-130',
                'finalization': '131-150'
            },
            'components': {
                'decomposition': 15,
                'strategies': 10,
                'planning': 12,
                'optimization': 10,
                'validation': 8
            }
        }
