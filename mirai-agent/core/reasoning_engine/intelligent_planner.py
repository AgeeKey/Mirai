#!/usr/bin/env python3
"""
🧠 Intelligent Planner - Steps 91-140
РАЗДЕЛ 3: INTELLIGENT PLANNING

Подсистемы:
3.1: Task Decomposition (Steps 91-110)
3.2: Execution Planning (Steps 111-130)
3.3: Adaptive Optimization (Steps 131-140)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
import json

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Individual task in the plan"""
    id: str
    name: str
    description: str
    task_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)
    enables: List[str] = field(default_factory=list)
    
    # Estimates
    estimated_time: float = 0.0  # seconds
    estimated_complexity: float = 0.0  # 0-1 scale
    
    # Execution
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.task_type,
            "parameters": self.parameters,
            "depends_on": self.depends_on,
            "enables": self.enables,
            "estimated_time": self.estimated_time,
            "estimated_complexity": self.estimated_complexity,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class ExecutionPlan:
    """Complete execution plan for a goal"""
    goal: str
    tasks: List[Task] = field(default_factory=list)
    critical_path: List[str] = field(default_factory=list)
    parallel_groups: List[List[str]] = field(default_factory=list)
    estimated_total_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


class IntelligentPlanner:
    """
    🧠 Intelligent Planning System
    
    Implements Steps 91-140: Task decomposition and execution planning
    """
    
    def __init__(self):
        self.task_registry: Dict[str, Task] = {}
        self.execution_history: List[Dict] = []
        self.current_plan: Optional[ExecutionPlan] = None
        
        logger.info("✅ Intelligent Planner initialized")
    
    # ═══════════════════════════════════════════════════════════════
    # Subsection 3.1: Task Decomposition (Steps 91-110)
    # ═══════════════════════════════════════════════════════════════
    
    def hierarchical_task_breakdown(self, goal: str) -> List[Task]:
        """
        Step 91: Hierarchical Task Breakdown
        - Break down high-level task into subtasks
        - Tree of Tasks
        - Each node is a subtask
        """
        logger.info(f"🌳 Breaking down goal: {goal}")
        
        tasks = []
        
        # Analyze goal and create task hierarchy
        # This is a simplified version - can be enhanced with GPT-4
        if "search" in goal.lower():
            tasks.extend(self._create_search_tasks(goal))
        elif "open" in goal.lower():
            tasks.extend(self._create_open_app_tasks(goal))
        elif "write" in goal.lower() or "create" in goal.lower():
            tasks.extend(self._create_write_tasks(goal))
        else:
            # Generic task breakdown
            tasks.append(Task(
                id=f"task_0",
                name="Execute goal",
                description=goal,
                task_type="generic"
            ))
        
        return tasks
    
    def _create_search_tasks(self, goal: str) -> List[Task]:
        """Create tasks for web search"""
        tasks = [
            Task(
                id="search_1",
                name="Open browser",
                description="Launch web browser",
                task_type="open_application",
                parameters={"application": "chrome"},
                estimated_time=3.0
            ),
            Task(
                id="search_2",
                name="Navigate to search engine",
                description="Go to Google or preferred search engine",
                task_type="navigate",
                parameters={"url": "https://www.google.com"},
                depends_on=["search_1"],
                estimated_time=2.0
            ),
            Task(
                id="search_3",
                name="Enter search query",
                description="Type search query",
                task_type="type",
                parameters={"text": goal},
                depends_on=["search_2"],
                estimated_time=2.0
            ),
            Task(
                id="search_4",
                name="Submit search",
                description="Press Enter or click Search",
                task_type="submit",
                depends_on=["search_3"],
                estimated_time=1.0
            )
        ]
        return tasks
    
    def _create_open_app_tasks(self, goal: str) -> List[Task]:
        """Create tasks for opening application"""
        # Extract app name from goal
        app_name = "unknown"
        for word in ["chrome", "firefox", "vscode", "notepad"]:
            if word in goal.lower():
                app_name = word
                break
        
        tasks = [
            Task(
                id="open_1",
                name=f"Locate {app_name}",
                description=f"Find {app_name} in start menu or desktop",
                task_type="locate",
                parameters={"application": app_name},
                estimated_time=1.0
            ),
            Task(
                id="open_2",
                name=f"Launch {app_name}",
                description=f"Click to launch {app_name}",
                task_type="click",
                depends_on=["open_1"],
                estimated_time=0.5
            ),
            Task(
                id="open_3",
                name="Wait for ready",
                description="Wait for application to be ready",
                task_type="wait",
                depends_on=["open_2"],
                estimated_time=5.0
            )
        ]
        return tasks
    
    def _create_write_tasks(self, goal: str) -> List[Task]:
        """Create tasks for writing/creating content"""
        tasks = [
            Task(
                id="write_1",
                name="Open editor",
                description="Open text editor or IDE",
                task_type="open_application",
                parameters={"application": "notepad"},
                estimated_time=2.0
            ),
            Task(
                id="write_2",
                name="Create new file",
                description="Create new document",
                task_type="click",
                depends_on=["write_1"],
                estimated_time=1.0
            ),
            Task(
                id="write_3",
                name="Write content",
                description="Type the content",
                task_type="type",
                depends_on=["write_2"],
                parameters={"text": goal},
                estimated_time=10.0
            ),
            Task(
                id="write_4",
                name="Save file",
                description="Save the document",
                task_type="save",
                depends_on=["write_3"],
                estimated_time=2.0
            )
        ]
        return tasks
    
    def identify_leaf_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Step 92: Leaf Task Identification
        - Leaves of tree are executable actions
        - For Chrome: click, type, navigate, select profile
        """
        leaf_tasks = []
        
        task_ids_that_are_depended_on = set()
        for task in tasks:
            task_ids_that_are_depended_on.update(task.depends_on)
        
        # Leaf tasks are those that no other task depends on
        for task in tasks:
            if task.id not in task_ids_that_are_depended_on:
                leaf_tasks.append(task)
        
        logger.info(f"🍃 Identified {len(leaf_tasks)} leaf tasks")
        return leaf_tasks
    
    def map_dependencies(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """
        Step 93: Dependency Mapping
        - Which tasks depend on others?
        - DAG (Directed Acyclic Graph)
        - Topological sorting
        """
        dependency_graph = {}
        
        for task in tasks:
            dependency_graph[task.id] = task.depends_on
        
        # Check for circular dependencies
        if self._has_circular_dependencies(dependency_graph):
            logger.warning("⚠️ Circular dependencies detected!")
        
        return dependency_graph
    
    def _has_circular_dependencies(self, graph: Dict[str, List[str]]) -> bool:
        """Check for circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        
        def visit(node):
            if node in rec_stack:
                return True  # Cycle detected
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
    
    def topological_sort(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks in dependency order"""
        # Build adjacency list
        graph = {}
        in_degree = {}
        
        for task in tasks:
            graph[task.id] = task.depends_on
            in_degree[task.id] = len(task.depends_on)
        
        # Find tasks with no dependencies
        queue = [task for task in tasks if in_degree[task.id] == 0]
        sorted_tasks = []
        
        while queue:
            current = queue.pop(0)
            sorted_tasks.append(current)
            
            # Reduce in-degree of dependent tasks
            for task in tasks:
                if current.id in task.depends_on:
                    in_degree[task.id] -= 1
                    if in_degree[task.id] == 0:
                        queue.append(task)
        
        return sorted_tasks
    
    def find_critical_path(self, tasks: List[Task]) -> List[str]:
        """
        Step 94: Critical Path Analysis
        - Find critical path in graph
        - Which tasks determine total time?
        - Optimize critical path
        """
        # Build graph with task durations
        task_dict = {task.id: task for task in tasks}
        
        # Calculate earliest start times
        earliest_start = {}
        for task in self.topological_sort(tasks):
            if not task.depends_on:
                earliest_start[task.id] = 0
            else:
                earliest_start[task.id] = max(
                    earliest_start.get(dep, 0) + task_dict[dep].estimated_time
                    for dep in task.depends_on
                )
        
        # Find task with latest finish time
        latest_finish = max(
            earliest_start[task.id] + task.estimated_time
            for task in tasks
        )
        
        # Trace back critical path
        critical_path = []
        current_time = latest_finish
        
        for task in reversed(self.topological_sort(tasks)):
            task_finish = earliest_start[task.id] + task.estimated_time
            if abs(task_finish - current_time) < 0.001:  # On critical path
                critical_path.insert(0, task.id)
                current_time = earliest_start[task.id]
        
        logger.info(f"🎯 Critical path: {len(critical_path)} tasks, {latest_finish:.1f}s total")
        return critical_path
    
    def identify_parallelization(self, tasks: List[Task]) -> List[List[str]]:
        """
        Step 95: Parallelization Opportunities
        - Which tasks can be done in parallel?
        - If no dependencies - parallel
        - But with resource constraints
        """
        parallel_groups = []
        task_dict = {task.id: task for task in tasks}
        completed = set()
        
        while len(completed) < len(tasks):
            # Find tasks whose dependencies are all completed
            ready_tasks = [
                task.id for task in tasks
                if task.id not in completed and
                all(dep in completed for dep in task.depends_on)
            ]
            
            if ready_tasks:
                parallel_groups.append(ready_tasks)
                completed.update(ready_tasks)
            else:
                break  # No more tasks can be executed
        
        logger.info(f"⚡ Found {len(parallel_groups)} parallel execution groups")
        return parallel_groups
    
    def adjust_task_granularity(self, tasks: List[Task]) -> List[Task]:
        """
        Step 96: Task Granularity Adjustment
        - Too large tasks - break down further
        - Too small tasks - combine
        - Optimal granularity
        """
        adjusted = []
        
        for task in tasks:
            # If task is too large (>30 seconds), suggest breaking down
            if task.estimated_time > 30:
                logger.warning(f"⚠️ Task {task.name} may be too large ({task.estimated_time}s)")
                # In real implementation, would break down further
                adjusted.append(task)
            
            # If task is too small (<0.5 seconds), might combine with others
            elif task.estimated_time < 0.5:
                logger.debug(f"Task {task.name} is very quick ({task.estimated_time}s)")
                adjusted.append(task)
            
            else:
                adjusted.append(task)
        
        return adjusted
    
    def estimate_tasks(self, tasks: List[Task], historical_data: Optional[List[Dict]] = None) -> List[Task]:
        """
        Step 97: Task Estimation
        - For each task estimate time
        - Complexity, dependencies, resources needed
        - Use historical data
        """
        for task in tasks:
            # Base estimates by task type
            base_estimates = {
                "click": 0.5,
                "type": 2.0,
                "navigate": 3.0,
                "wait": 2.0,
                "open_application": 5.0,
                "search": 10.0,
                "save": 2.0
            }
            
            base_time = base_estimates.get(task.task_type, 5.0)
            
            # Adjust based on complexity
            complexity_factor = 1.0 + (task.estimated_complexity * 0.5)
            
            # Adjust based on dependencies
            dependency_factor = 1.0 + (len(task.depends_on) * 0.1)
            
            task.estimated_time = base_time * complexity_factor * dependency_factor
            
            # Use historical data if available
            if historical_data:
                similar = [
                    h for h in historical_data
                    if h.get("task_type") == task.task_type
                ]
                if similar:
                    avg_time = sum(h.get("actual_time", 0) for h in similar) / len(similar)
                    # Blend estimate with historical average
                    task.estimated_time = (task.estimated_time + avg_time) / 2
        
        return tasks
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Step 98: Task Prioritization
        - Rank subtasks by priority
        - Which need to be executed first?
        """
        # Priority factors:
        # 1. Tasks with no dependencies (can start immediately)
        # 2. Tasks on critical path
        # 3. Tasks that enable many other tasks
        
        critical_path = set(self.find_critical_path(tasks))
        
        def priority_score(task: Task) -> float:
            score = 0.0
            
            # No dependencies = higher priority
            if not task.depends_on:
                score += 10.0
            
            # On critical path = higher priority
            if task.id in critical_path:
                score += 20.0
            
            # Enables many tasks = higher priority
            score += len(task.enables) * 5.0
            
            # Shorter tasks slightly higher priority
            score += (60 - min(task.estimated_time, 60)) / 10
            
            return score
        
        prioritized = sorted(tasks, key=priority_score, reverse=True)
        logger.info(f"📊 Tasks prioritized")
        return prioritized
    
    # ═══════════════════════════════════════════════════════════════
    # Main Planning Methods
    # ═══════════════════════════════════════════════════════════════
    
    def create_execution_plan(self, goal: str, constraints: Optional[Dict] = None) -> ExecutionPlan:
        """
        Create complete execution plan for a goal
        
        Steps:
        1. Hierarchical breakdown (91)
        2. Identify leaf tasks (92)
        3. Map dependencies (93)
        4. Find critical path (94)
        5. Identify parallelization (95)
        6. Adjust granularity (96)
        7. Estimate tasks (97)
        8. Prioritize tasks (98)
        """
        logger.info(f"📋 Creating execution plan for: {goal}")
        
        # Step 91: Break down into tasks
        tasks = self.hierarchical_task_breakdown(goal)
        
        # Step 92: Identify leaf tasks
        leaf_tasks = self.identify_leaf_tasks(tasks)
        
        # Step 93: Map dependencies
        dependencies = self.map_dependencies(tasks)
        
        # Step 94: Find critical path
        critical_path = self.find_critical_path(tasks)
        
        # Step 95: Identify parallelization opportunities
        parallel_groups = self.identify_parallelization(tasks)
        
        # Step 96: Adjust granularity
        tasks = self.adjust_task_granularity(tasks)
        
        # Step 97: Estimate tasks
        tasks = self.estimate_tasks(tasks, self.execution_history)
        
        # Step 98: Prioritize tasks
        tasks = self.prioritize_tasks(tasks)
        
        # Calculate total estimated time (sum of critical path)
        total_time = sum(
            task.estimated_time for task in tasks
            if task.id in critical_path
        )
        
        # Create execution plan
        plan = ExecutionPlan(
            goal=goal,
            tasks=tasks,
            critical_path=critical_path,
            parallel_groups=parallel_groups,
            estimated_total_time=total_time
        )
        
        self.current_plan = plan
        
        logger.info(f"✅ Plan created: {len(tasks)} tasks, ~{total_time:.1f}s estimated")
        return plan
    
    def get_next_tasks(self, completed_task_ids: Set[str]) -> List[Task]:
        """
        Get next tasks that can be executed
        Based on completed tasks and dependencies
        """
        if not self.current_plan:
            return []
        
        ready_tasks = []
        for task in self.current_plan.tasks:
            if (task.status == TaskStatus.PENDING and
                all(dep in completed_task_ids for dep in task.depends_on)):
                ready_tasks.append(task)
        
        return ready_tasks
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[Dict] = None, error: Optional[str] = None):
        """Update task execution status"""
        if not self.current_plan:
            return
        
        for task in self.current_plan.tasks:
            if task.id == task_id:
                task.status = status
                task.result = result
                task.error = error
                
                if status == TaskStatus.IN_PROGRESS and not task.started_at:
                    task.started_at = datetime.now()
                
                if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED]:
                    task.completed_at = datetime.now()
                    
                    # Record in history
                    if task.started_at and task.completed_at:
                        actual_time = (task.completed_at - task.started_at).total_seconds()
                        self.execution_history.append({
                            "task_id": task_id,
                            "task_type": task.task_type,
                            "estimated_time": task.estimated_time,
                            "actual_time": actual_time,
                            "success": status == TaskStatus.COMPLETED,
                            "timestamp": datetime.now().isoformat()
                        })
                
                logger.info(f"📝 Task {task_id} status updated: {status.value}")
                break
    
    def get_plan_progress(self) -> Dict:
        """Get current plan execution progress"""
        if not self.current_plan:
            return {"status": "no_plan"}
        
        total = len(self.current_plan.tasks)
        completed = sum(1 for t in self.current_plan.tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.current_plan.tasks if t.status == TaskStatus.FAILED)
        in_progress = sum(1 for t in self.current_plan.tasks if t.status == TaskStatus.IN_PROGRESS)
        
        progress = {
            "goal": self.current_plan.goal,
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "pending": total - completed - failed - in_progress,
            "progress_percent": (completed / total * 100) if total > 0 else 0,
            "estimated_total_time": self.current_plan.estimated_total_time,
            "timestamp": datetime.now().isoformat()
        }
        
        return progress
    
    def export_plan(self) -> Dict:
        """Export current plan to dict"""
        if not self.current_plan:
            return {}
        
        return {
            "goal": self.current_plan.goal,
            "tasks": [task.to_dict() for task in self.current_plan.tasks],
            "critical_path": self.current_plan.critical_path,
            "parallel_groups": self.current_plan.parallel_groups,
            "estimated_total_time": self.current_plan.estimated_total_time,
            "created_at": self.current_plan.created_at.isoformat(),
            "progress": self.get_plan_progress()
        }
