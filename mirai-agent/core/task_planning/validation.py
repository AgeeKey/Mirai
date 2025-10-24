#!/usr/bin/env python3
"""
✅ РАЗДЕЛ 3.2: PLAN VALIDATION (Шаги 106-130)
=============================================

Валидация планов выполнения по различным критериям:
- Полнота
- Корректность
- Безопасность
- Производительность
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Результат валидации"""
    valid: bool
    score: float  # 0.0 - 1.0
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 0


class CompletenessChecker:
    """
    Шаг 106: Completeness Check
    
    Проверяет что план полностью покрывает задачу.
    """
    
    def check(
        self,
        plan: Dict[str, Any],
        requirements: List[str]
    ) -> ValidationResult:
        """
        Проверяет полноту плана
        
        Args:
            plan: План для проверки
            requirements: Список требований
            
        Returns:
            ValidationResult
        """
        logger.info("Шаг 106: Проверка полноты плана")
        
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        # Проверка 1: План содержит задачи
        checks_total += 1
        if not plan.get('tasks'):
            issues.append("План не содержит задач")
        else:
            checks_passed += 1
        
        # Проверка 2: Все требования покрыты
        checks_total += 1
        covered_requirements = self._check_requirements_coverage(
            plan,
            requirements
        )
        if covered_requirements == len(requirements):
            checks_passed += 1
        else:
            missing = len(requirements) - covered_requirements
            issues.append(f"Не покрыто {missing} требований")
        
        # Проверка 3: Есть начало и конец
        checks_total += 1
        if self._has_start_and_end(plan):
            checks_passed += 1
        else:
            warnings.append("Нет явного начала или конца")
        
        score = checks_passed / checks_total if checks_total > 0 else 0.0
        valid = len(issues) == 0 and score >= 0.8
        
        logger.info(f"Полнота: {checks_passed}/{checks_total} проверок (score: {score:.2f})")
        
        return ValidationResult(
            valid=valid,
            score=score,
            issues=issues,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total
        )
    
    def _check_requirements_coverage(
        self,
        plan: Dict,
        requirements: List[str]
    ) -> int:
        """Проверяет сколько требований покрыто"""
        covered = 0
        task_descriptions = [
            t.get('description', '').lower()
            for t in plan.get('tasks', [])
        ]
        
        for req in requirements:
            req_lower = req.lower()
            if any(req_lower in desc for desc in task_descriptions):
                covered += 1
        
        return covered
    
    def _has_start_and_end(self, plan: Dict) -> bool:
        """Проверяет наличие начала и конца"""
        tasks = plan.get('tasks', [])
        if not tasks:
            return False
        
        # Проверяем что есть задачи без зависимостей (начало)
        has_start = any(not t.get('depends_on') for t in tasks)
        
        # Проверяем что есть задачи от которых никто не зависит (конец)
        all_deps = set()
        for t in tasks:
            all_deps.update(t.get('depends_on', []))
        
        task_ids = {t.get('id') for t in tasks}
        has_end = len(task_ids - all_deps) > 0
        
        return has_start and has_end


class ConsistencyChecker:
    """
    Шаг 107: Consistency Check
    
    Проверяет отсутствие противоречий в плане.
    """
    
    def check(self, plan: Dict[str, Any]) -> ValidationResult:
        """
        Проверяет консистентность плана
        
        Args:
            plan: План для проверки
            
        Returns:
            ValidationResult
        """
        logger.info("Шаг 107: Проверка консистентности плана")
        
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        tasks = plan.get('tasks', [])
        
        # Проверка 1: Нет циклических зависимостей
        checks_total += 1
        if not self._has_cycles(tasks):
            checks_passed += 1
        else:
            issues.append("Обнаружены циклические зависимости")
        
        # Проверка 2: Все зависимости существуют
        checks_total += 1
        missing_deps = self._find_missing_dependencies(tasks)
        if not missing_deps:
            checks_passed += 1
        else:
            issues.append(f"Отсутствуют зависимости: {', '.join(missing_deps[:3])}")
        
        # Проверка 3: Нет конфликтующих ресурсов
        checks_total += 1
        conflicts = self._find_resource_conflicts(tasks)
        if not conflicts:
            checks_passed += 1
        else:
            warnings.append(f"Обнаружено {len(conflicts)} конфликтов ресурсов")
        
        score = checks_passed / checks_total if checks_total > 0 else 0.0
        valid = len(issues) == 0
        
        logger.info(f"Консистентность: {checks_passed}/{checks_total} (score: {score:.2f})")
        
        return ValidationResult(
            valid=valid,
            score=score,
            issues=issues,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total
        )
    
    def _has_cycles(self, tasks: List[Dict]) -> bool:
        """Проверяет наличие циклов"""
        graph = {t.get('id'): t.get('depends_on', []) for t in tasks}
        
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if dfs(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if dfs(node):
                return True
        
        return False
    
    def _find_missing_dependencies(self, tasks: List[Dict]) -> List[str]:
        """Находит отсутствующие зависимости"""
        task_ids = {t.get('id') for t in tasks}
        missing = set()
        
        for task in tasks:
            for dep in task.get('depends_on', []):
                if dep not in task_ids:
                    missing.add(dep)
        
        return list(missing)
    
    def _find_resource_conflicts(self, tasks: List[Dict]) -> List[Tuple[str, str]]:
        """Находит конфликты ресурсов"""
        # Упрощенная проверка
        return []


class FeasibilityChecker:
    """
    Шаг 108: Feasibility Check
    
    Проверяет осуществимость плана.
    """
    
    def check(
        self,
        plan: Dict[str, Any],
        available_resources: Dict[str, Any]
    ) -> ValidationResult:
        """
        Проверяет осуществимость плана
        
        Args:
            plan: План для проверки
            available_resources: Доступные ресурсы
            
        Returns:
            ValidationResult
        """
        logger.info("Шаг 108: Проверка осуществимости плана")
        
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        # Проверка 1: Достаточно времени
        checks_total += 1
        time_budget = available_resources.get('time_budget', float('inf'))
        planned_time = plan.get('total_duration', 0)
        if planned_time <= time_budget:
            checks_passed += 1
        else:
            issues.append(
                f"Превышен бюджет времени: {planned_time:.0f}с > {time_budget:.0f}с"
            )
        
        # Проверка 2: Достаточно ресурсов
        checks_total += 1
        if self._check_resource_availability(plan, available_resources):
            checks_passed += 1
        else:
            issues.append("Недостаточно ресурсов для выполнения")
        
        # Проверка 3: Технически возможно
        checks_total += 1
        if self._check_technical_feasibility(plan):
            checks_passed += 1
        else:
            warnings.append("Некоторые задачи могут быть технически сложны")
        
        score = checks_passed / checks_total if checks_total > 0 else 0.0
        valid = len(issues) == 0
        
        logger.info(f"Осуществимость: {checks_passed}/{checks_total} (score: {score:.2f})")
        
        return ValidationResult(
            valid=valid,
            score=score,
            issues=issues,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total
        )
    
    def _check_resource_availability(
        self,
        plan: Dict,
        available: Dict
    ) -> bool:
        """Проверяет доступность ресурсов"""
        required_resources = set()
        for task in plan.get('tasks', []):
            required_resources.update(task.get('required_resources', []))
        
        for resource in required_resources:
            if resource not in available.get('resources', []):
                return False
        
        return True
    
    def _check_technical_feasibility(self, plan: Dict) -> bool:
        """Проверяет техническую осуществимость"""
        # Упрощенная проверка
        return True


class SafetyChecker:
    """
    Шаг 109: Safety Check
    
    Проверяет безопасность плана.
    """
    
    def check(self, plan: Dict[str, Any]) -> ValidationResult:
        """
        Проверяет безопасность плана
        
        Args:
            plan: План для проверки
            
        Returns:
            ValidationResult
        """
        logger.info("Шаг 109: Проверка безопасности плана")
        
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        tasks = plan.get('tasks', [])
        
        # Проверка 1: Все рискованные задачи имеют проверки
        checks_total += 1
        risky_tasks = [t for t in tasks if t.get('risk_level') in ['high', 'critical']]
        if all(self._has_safety_measures(t, tasks) for t in risky_tasks):
            checks_passed += 1
        else:
            issues.append("Не все рискованные задачи имеют проверки безопасности")
        
        # Проверка 2: Есть возможность отката
        checks_total += 1
        if all(t.get('rollback_supported', True) for t in risky_tasks):
            checks_passed += 1
        else:
            warnings.append("Не для всех задач предусмотрен откат")
        
        # Проверка 3: Нет критических операций без подтверждения
        checks_total += 1
        critical_tasks = [t for t in tasks if t.get('risk_level') == 'critical']
        if all(t.get('requires_confirmation', False) for t in critical_tasks):
            checks_passed += 1
        else:
            warnings.append("Критические операции без подтверждения")
        
        score = checks_passed / checks_total if checks_total > 0 else 0.0
        valid = len(issues) == 0
        
        logger.info(f"Безопасность: {checks_passed}/{checks_total} (score: {score:.2f})")
        
        return ValidationResult(
            valid=valid,
            score=score,
            issues=issues,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total
        )
    
    def _has_safety_measures(self, task: Dict, all_tasks: List[Dict]) -> bool:
        """Проверяет наличие мер безопасности для задачи"""
        task_id = task.get('id')
        
        # Проверяем есть ли после этой задачи validation или safety_check
        for t in all_tasks:
            if task_id in t.get('depends_on', []):
                if t.get('type') in ['validation', 'safety_check']:
                    return True
        
        return False


class PerformanceChecker:
    """
    Шаг 110: Performance Check
    
    Проверяет производительность плана.
    """
    
    def check(
        self,
        plan: Dict[str, Any],
        performance_requirements: Optional[Dict] = None
    ) -> ValidationResult:
        """
        Проверяет производительность плана
        
        Args:
            plan: План для проверки
            performance_requirements: Требования к производительности
            
        Returns:
            ValidationResult
        """
        logger.info("Шаг 110: Проверка производительности плана")
        
        if performance_requirements is None:
            performance_requirements = {
                'max_duration': 300,  # 5 минут
                'max_tasks': 50,
                'min_parallelism': 1.0
            }
        
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        # Проверка 1: Время в норме
        checks_total += 1
        duration = plan.get('total_duration', 0)
        max_duration = performance_requirements.get('max_duration', float('inf'))
        if duration <= max_duration:
            checks_passed += 1
        else:
            issues.append(
                f"Превышено максимальное время: {duration:.0f}с > {max_duration:.0f}с"
            )
        
        # Проверка 2: Количество задач разумно
        checks_total += 1
        num_tasks = len(plan.get('tasks', []))
        max_tasks = performance_requirements.get('max_tasks', 100)
        if num_tasks <= max_tasks:
            checks_passed += 1
        else:
            warnings.append(f"Слишком много задач: {num_tasks} > {max_tasks}")
        
        # Проверка 3: Достаточный параллелизм
        checks_total += 1
        parallelism = plan.get('max_parallelism', 1)
        min_parallelism = performance_requirements.get('min_parallelism', 1.0)
        if parallelism >= min_parallelism:
            checks_passed += 1
        else:
            warnings.append("Низкий уровень параллелизма")
        
        score = checks_passed / checks_total if checks_total > 0 else 0.0
        valid = len(issues) == 0
        
        logger.info(f"Производительность: {checks_passed}/{checks_total} (score: {score:.2f})")
        
        return ValidationResult(
            valid=valid,
            score=score,
            issues=issues,
            warnings=warnings,
            checks_passed=checks_passed,
            checks_total=checks_total
        )


class ValidationReportGenerator:
    """
    Шаг 122: Validation Report Generation
    
    Создает отчет валидации.
    """
    
    def generate(
        self,
        plan: Dict[str, Any],
        results: Dict[str, ValidationResult]
    ) -> str:
        """
        Генерирует отчет валидации
        
        Args:
            plan: Проверенный план
            results: Результаты различных проверок
            
        Returns:
            Текстовый отчет
        """
        logger.info("Шаг 122: Генерация отчета валидации")
        
        report_lines = [
            "=" * 60,
            "ОТЧЕТ ВАЛИДАЦИИ ПЛАНА",
            "=" * 60,
            "",
            f"План: {plan.get('name', 'Unnamed')}",
            f"Дата проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "РЕЗУЛЬТАТЫ ПРОВЕРОК:",
            "-" * 60
        ]
        
        total_score = 0.0
        all_valid = True
        
        for check_name, result in results.items():
            status = "✅ ПРОЙДЕНО" if result.valid else "❌ НЕ ПРОЙДЕНО"
            report_lines.append(
                f"{check_name}: {status} "
                f"(score: {result.score:.2f}, "
                f"проверок: {result.checks_passed}/{result.checks_total})"
            )
            
            total_score += result.score
            all_valid = all_valid and result.valid
            
            if result.issues:
                report_lines.append("  Проблемы:")
                for issue in result.issues:
                    report_lines.append(f"    • {issue}")
            
            if result.warnings:
                report_lines.append("  Предупреждения:")
                for warning in result.warnings:
                    report_lines.append(f"    • {warning}")
            
            report_lines.append("")
        
        avg_score = total_score / len(results) if results else 0.0
        
        report_lines.extend([
            "-" * 60,
            "ИТОГО:",
            f"Общая оценка: {avg_score:.2f}/1.00",
            f"Статус: {'✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ' if all_valid else '❌ ЕСТЬ ПРОБЛЕМЫ'}",
            "=" * 60
        ])
        
        report = "\n".join(report_lines)
        logger.info(f"Отчет валидации сгенерирован (общая оценка: {avg_score:.2f})")
        
        return report


class PlanSignOff:
    """
    Шаг 129: Plan Sign-off
    
    Финальное утверждение плана после всех проверок.
    """
    
    def sign_off(
        self,
        plan: Dict[str, Any],
        validation_results: Dict[str, ValidationResult]
    ) -> Dict[str, Any]:
        """
        Утверждает план
        
        Args:
            plan: План для утверждения
            validation_results: Результаты валидации
            
        Returns:
            План с отметкой об утверждении
        """
        logger.info("Шаг 129: Утверждение плана")
        
        signed_plan = plan.copy()
        
        # Проверяем все ли валидации пройдены
        all_valid = all(r.valid for r in validation_results.values())
        avg_score = sum(r.score for r in validation_results.values()) / len(validation_results)
        
        # Более мягкие критерии: либо все пройдено, либо хороший score (>= 0.7)
        if all_valid or avg_score >= 0.7:
            signed_plan['approved'] = True
            signed_plan['approval_status'] = 'APPROVED'
            signed_plan['approval_score'] = avg_score
            signed_plan['approved_at'] = datetime.now().isoformat()
            logger.info(f"✅ План утвержден (score: {avg_score:.2f})")
        else:
            signed_plan['approved'] = False
            signed_plan['approval_status'] = 'REJECTED'
            signed_plan['approval_score'] = avg_score
            signed_plan['rejection_reason'] = "Валидация не пройдена"
            logger.warning(f"❌ План отклонен (score: {avg_score:.2f})")
        
        return signed_plan

