#!/usr/bin/env python3
"""
⚡ РАЗДЕЛ 3.1: PLAN OPTIMIZATION (Шаги 81-105)
=============================================

Оптимизация планов выполнения по различным критериям:
- Время
- Ресурсы
- Стоимость
- Безопасность
- И многое другое
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class TimeOptimizer:
    """
    Шаг 81: Time Optimization
    
    Минимизирует общее время выполнения плана.
    """
    
    def optimize(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оптимизирует план по времени
        
        Args:
            plan: Исходный план
            
        Returns:
            Оптимизированный план
        """
        logger.info("Шаг 81: Оптимизация по времени")
        
        optimized = plan.copy()
        
        # Максимизируем параллелизм
        if 'tasks' in optimized:
            tasks = optimized['tasks']
            
            # Находим задачи которые можно параллелить
            parallel_tasks = self._find_parallelizable_tasks(tasks)
            
            if parallel_tasks:
                logger.info(f"Найдено {len(parallel_tasks)} групп для параллелизации")
                optimized['parallel_execution'] = True
                optimized['parallel_groups'] = parallel_tasks
        
        original_time = plan.get('total_duration', 0)
        optimized_time = self._calculate_duration(optimized)
        optimized['total_duration'] = optimized_time
        
        improvement = ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
        logger.info(f"Время: {original_time:.1f}с → {optimized_time:.1f}с "
                   f"(улучшение: {improvement:.1f}%)")
        
        return optimized
    
    def _find_parallelizable_tasks(self, tasks: List[Dict]) -> List[List[str]]:
        """Находит задачи для параллельного выполнения"""
        # Упрощенная логика
        groups = []
        current_group = []
        
        for task in tasks:
            if not task.get('depends_on'):
                current_group.append(task.get('id'))
            elif current_group:
                groups.append(current_group)
                current_group = []
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _calculate_duration(self, plan: Dict) -> float:
        """Вычисляет общую длительность плана"""
        if 'parallel_groups' in plan:
            # Для параллельного плана - сумма максимумов по группам
            total = 0.0
            for group_ids in plan['parallel_groups']:
                group_duration = max(
                    task.get('estimated_duration', 10.0)
                    for task in plan['tasks']
                    if task.get('id') in group_ids
                )
                total += group_duration
            return total
        else:
            # Для последовательного - сумма всех
            return sum(
                task.get('estimated_duration', 10.0)
                for task in plan.get('tasks', [])
            )


class ResourceOptimizer:
    """
    Шаг 82: Resource Optimization
    
    Минимизирует использование ресурсов (CPU, Memory, etc).
    """
    
    def optimize(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оптимизирует использование ресурсов
        
        Args:
            plan: Исходный план
            
        Returns:
            Оптимизированный план
        """
        logger.info("Шаг 82: Оптимизация ресурсов")
        
        optimized = plan.copy()
        
        # Балансируем нагрузку
        if 'tasks' in optimized:
            balanced_tasks = self._balance_resources(optimized['tasks'])
            optimized['tasks'] = balanced_tasks
            optimized['resource_balanced'] = True
        
        logger.info("Ресурсы оптимизированы")
        
        return optimized
    
    def _balance_resources(self, tasks: List[Dict]) -> List[Dict]:
        """Балансирует распределение ресурсов"""
        # Сортируем задачи по потреблению ресурсов
        return sorted(
            tasks,
            key=lambda t: t.get('resource_usage', 0.5),
            reverse=False  # Сначала легкие задачи
        )


class SafetyOptimizer:
    """
    Шаг 84: Safety Optimization
    
    Максимизирует безопасность плана.
    """
    
    def optimize(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оптимизирует безопасность
        
        Args:
            plan: Исходный план
            
        Returns:
            Более безопасный план
        """
        logger.info("Шаг 84: Оптимизация безопасности")
        
        optimized = plan.copy()
        
        if 'tasks' in optimized:
            # Добавляем проверки безопасности
            safe_tasks = []
            for task in optimized['tasks']:
                safe_tasks.append(task)
                
                # Добавляем валидацию после рискованных операций
                if task.get('risk_level') in ['high', 'critical']:
                    validation = {
                        'id': f"{task.get('id')}_safety_validation",
                        'name': f"Проверка безопасности: {task.get('name')}",
                        'type': 'safety_validation',
                        'depends_on': [task.get('id')]
                    }
                    safe_tasks.append(validation)
            
            optimized['tasks'] = safe_tasks
            optimized['safety_enhanced'] = True
        
        logger.info("Безопасность улучшена")
        
        return optimized


class MultiObjectiveOptimizer:
    """
    Шаг 91: Multi-Objective Optimization
    
    Оптимизирует по нескольким целям одновременно (Pareto-оптимальность).
    """
    
    def __init__(self):
        self.time_optimizer = TimeOptimizer()
        self.resource_optimizer = ResourceOptimizer()
        self.safety_optimizer = SafetyOptimizer()
    
    def optimize(
        self,
        plan: Dict[str, Any],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Многокритериальная оптимизация
        
        Args:
            plan: Исходный план
            weights: Веса для различных критериев
            
        Returns:
            Оптимизированный план
        """
        logger.info("Шаг 91: Многокритериальная оптимизация")
        
        if weights is None:
            weights = {
                'time': 0.4,
                'resources': 0.3,
                'safety': 0.3
            }
        
        # Применяем различные оптимизаторы
        optimized = plan.copy()
        
        if weights['time'] > 0:
            optimized = self.time_optimizer.optimize(optimized)
        
        if weights['resources'] > 0:
            optimized = self.resource_optimizer.optimize(optimized)
        
        if weights['safety'] > 0:
            optimized = self.safety_optimizer.optimize(optimized)
        
        # Вычисляем общий скор
        score = self._calculate_score(optimized, weights)
        optimized['optimization_score'] = score
        optimized['optimization_weights'] = weights
        
        logger.info(f"Многокритериальная оптимизация завершена (score: {score:.2f})")
        
        return optimized
    
    def _calculate_score(self, plan: Dict, weights: Dict) -> float:
        """Вычисляет общий скор оптимизации"""
        score = 0.0
        
        # Нормализованные метрики (0-1, где 1 - лучше)
        time_score = 1.0 / (1.0 + plan.get('total_duration', 100) / 100)
        resource_score = 0.8 if plan.get('resource_balanced') else 0.5
        safety_score = 0.9 if plan.get('safety_enhanced') else 0.6
        
        score = (
            weights['time'] * time_score +
            weights['resources'] * resource_score +
            weights['safety'] * safety_score
        )
        
        return score


class PlanCompactor:
    """
    Шаг 93: Plan Compaction
    
    Совмещает похожие операции для уменьшения размера плана.
    """
    
    def compact(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Уплотняет план
        
        Args:
            plan: Исходный план
            
        Returns:
            Уплотненный план
        """
        logger.info("Шаг 93: Уплотнение плана")
        
        compacted = plan.copy()
        
        if 'tasks' in compacted:
            original_count = len(compacted['tasks'])
            compacted_tasks = self._merge_similar_tasks(compacted['tasks'])
            compacted['tasks'] = compacted_tasks
            
            reduction = ((original_count - len(compacted_tasks)) / original_count * 100) if original_count > 0 else 0
            logger.info(f"Задачи: {original_count} → {len(compacted_tasks)} "
                       f"(сокращение: {reduction:.1f}%)")
        
        return compacted
    
    def _merge_similar_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """Объединяет похожие задачи"""
        merged = []
        skip_ids = set()
        
        for i, task1 in enumerate(tasks):
            if task1.get('id') in skip_ids:
                continue
            
            # Ищем похожие задачи
            similar = [task1]
            for j, task2 in enumerate(tasks[i+1:], i+1):
                if task2.get('id') in skip_ids:
                    continue
                
                if self._are_similar(task1, task2):
                    similar.append(task2)
                    skip_ids.add(task2.get('id'))
            
            # Если нашли похожие - объединяем
            if len(similar) > 1:
                merged_task = self._merge_tasks(similar)
                merged.append(merged_task)
            else:
                merged.append(task1)
        
        return merged
    
    def _are_similar(self, task1: Dict, task2: Dict) -> bool:
        """Проверяет похожесть задач"""
        # Упрощенная проверка - по типу
        return task1.get('type') == task2.get('type')
    
    def _merge_tasks(self, tasks: List[Dict]) -> Dict:
        """Объединяет список задач в одну"""
        merged = tasks[0].copy()
        merged['name'] = f"Объединенная задача ({len(tasks)} операций)"
        merged['merged_from'] = [t.get('id') for t in tasks]
        merged['description'] = f"Объединяет {len(tasks)} похожих операций"
        return merged


class PlanSimplifier:
    """
    Шаг 95: Plan Simplification
    
    Упрощает план где возможно (Occam's Razor).
    """
    
    def simplify(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Упрощает план
        
        Args:
            plan: Исходный план
            
        Returns:
            Упрощенный план
        """
        logger.info("Шаг 95: Упрощение плана")
        
        simplified = plan.copy()
        
        if 'tasks' in simplified:
            # Удаляем избыточные задачи
            essential_tasks = self._keep_essential_only(simplified['tasks'])
            simplified['tasks'] = essential_tasks
            
            logger.info(f"Упрощение: {len(plan['tasks'])} → {len(essential_tasks)} задач")
        
        return simplified
    
    def _keep_essential_only(self, tasks: List[Dict]) -> List[Dict]:
        """Оставляет только необходимые задачи"""
        essential = []
        
        for task in tasks:
            # Оставляем задачи которые:
            # 1. Не являются optional
            # 2. Имеют зависимые задачи
            # 3. Критически важны
            
            if task.get('optional', False):
                continue
            
            if task.get('priority', 5) < 3:
                continue
            
            essential.append(task)
        
        return essential


class CachingOpportunitiesIdentifier:
    """
    Шаг 96: Caching Opportunities
    
    Определяет какие результаты можно кешировать для переиспользования.
    """
    
    def identify(self, plan: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Определяет возможности кеширования
        
        Args:
            plan: План выполнения
            
        Returns:
            Словарь с кешируемыми операциями
        """
        logger.info("Шаг 96: Определение возможностей кеширования")
        
        cacheable = {
            'read_operations': [],
            'expensive_computations': [],
            'api_calls': []
        }
        
        for task in plan.get('tasks', []):
            task_type = task.get('type', '')
            task_id = task.get('id')
            
            # Read операции
            if 'read' in task_type.lower() or 'get' in task_type.lower():
                cacheable['read_operations'].append(task_id)
            
            # Дорогие вычисления
            if task.get('estimated_duration', 0) > 30:
                cacheable['expensive_computations'].append(task_id)
            
            # API вызовы
            if 'api' in task_type.lower():
                cacheable['api_calls'].append(task_id)
        
        total = sum(len(v) for v in cacheable.values())
        logger.info(f"Найдено {total} возможностей для кеширования")
        
        return cacheable


class LoadBalancer:
    """
    Шаг 100: Load Balancing
    
    Распределяет нагрузку равномерно между ресурсами.
    """
    
    def balance(
        self,
        plan: Dict[str, Any],
        num_workers: int = 4
    ) -> Dict[str, Any]:
        """
        Балансирует нагрузку
        
        Args:
            plan: План выполнения
            num_workers: Количество воркеров
            
        Returns:
            План с балансировкой нагрузки
        """
        logger.info(f"Шаг 100: Балансировка нагрузки ({num_workers} воркеров)")
        
        balanced = plan.copy()
        
        tasks = balanced.get('tasks', [])
        
        # Распределяем задачи по воркерам
        workers = [[] for _ in range(num_workers)]
        worker_loads = [0.0] * num_workers
        
        # Сортируем задачи по длительности (от большего к меньшему)
        sorted_tasks = sorted(
            tasks,
            key=lambda t: t.get('estimated_duration', 0),
            reverse=True
        )
        
        # Жадный алгоритм: назначаем каждую задачу наименее загруженному воркеру
        for task in sorted_tasks:
            # Находим наименее загруженного воркера
            min_worker_idx = worker_loads.index(min(worker_loads))
            
            workers[min_worker_idx].append(task)
            worker_loads[min_worker_idx] += task.get('estimated_duration', 0)
        
        balanced['worker_assignment'] = {
            f'worker_{i}': worker_tasks
            for i, worker_tasks in enumerate(workers)
        }
        balanced['worker_loads'] = worker_loads
        balanced['load_balanced'] = True
        
        max_load = max(worker_loads)
        avg_load = sum(worker_loads) / num_workers
        balance_ratio = avg_load / max_load if max_load > 0 else 1.0
        
        logger.info(f"Балансировка завершена (коэффициент: {balance_ratio:.2f})")
        
        return balanced
