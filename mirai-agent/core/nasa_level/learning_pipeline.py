"""
NASA-Level Learning Pipeline
Manages learning queue with priorities, dependencies, and retry logic
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set
from queue import PriorityQueue

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Learning task priority levels"""
    CRITICAL = 1  # Must learn immediately (security fixes, critical bugs)
    HIGH = 2      # Important features
    NORMAL = 3    # Regular learning
    LOW = 4       # Nice to have


class TaskStatus(Enum):
    """Task lifecycle states"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class LearningTask:
    """A technology to learn with metadata"""
    technology: str
    depth: str = "basic"
    priority: Priority = Priority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    max_retries: int = 3
    retry_count: int = 0
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None
    result: Optional[Dict] = None
    
    def __lt__(self, other):
        """Priority queue comparison"""
        return self.priority.value < other.priority.value


class DependencyResolver:
    """Resolves learning dependencies"""
    
    def __init__(self):
        self.learned: Set[str] = set()
        self.in_progress: Set[str] = set()
    
    def can_learn(self, task: LearningTask) -> bool:
        """Check if all dependencies are satisfied"""
        for dep in task.dependencies:
            if dep not in self.learned and dep not in self.in_progress:
                return False
        return True
    
    def mark_started(self, technology: str):
        """Mark technology as being learned"""
        self.in_progress.add(technology)
    
    def mark_completed(self, technology: str):
        """Mark technology as learned"""
        self.in_progress.discard(technology)
        self.learned.add(technology)
    
    def mark_failed(self, technology: str):
        """Mark technology learning as failed"""
        self.in_progress.discard(technology)


class LearningPipeline:
    """
    CI/CD-style learning pipeline with:
    - Priority queue
    - Dependency resolution
    - Automatic retries
    - Concurrent learning
    - Progress tracking
    """
    
    def __init__(
        self,
        learning_engine,
        knowledge_manager=None,
        metrics=None,
        max_concurrent: int = 2,
        state_file: str = "/tmp/learning_pipeline_state.json"
    ):
        self.learning_engine = learning_engine
        self.knowledge_manager = knowledge_manager
        self.metrics = metrics
        self.max_concurrent = max_concurrent
        self.state_file = Path(state_file)
        
        self.queue: PriorityQueue = PriorityQueue()
        self.tasks: Dict[str, LearningTask] = {}
        self.resolver = DependencyResolver()
        self.running = False
        
        # Stats
        self.total_completed = 0
        self.total_failed = 0
        self.total_retries = 0
        
        # Load previous state if exists
        self._load_state()
    
    def add_task(
        self,
        technology: str,
        depth: str = "basic",
        priority: Priority = Priority.NORMAL,
        dependencies: List[str] = None
    ) -> LearningTask:
        """Add a new learning task to the queue"""
        
        if technology in self.tasks:
            logger.info(f"📝 Task {technology} already exists, updating priority")
            task = self.tasks[technology]
            if priority.value < task.priority.value:
                task.priority = priority
            return task
        
        task = LearningTask(
            technology=technology,
            depth=depth,
            priority=priority,
            dependencies=dependencies or []
        )
        
        self.tasks[technology] = task
        self.queue.put(task)
        
        logger.info(f"➕ Added task: {technology} (priority: {priority.name})")
        self._save_state()
        
        return task
    
    def add_batch(self, technologies: List[str], priority: Priority = Priority.NORMAL):
        """Add multiple technologies at once"""
        for tech in technologies:
            self.add_task(tech, priority=priority)
        logger.info(f"➕ Added {len(technologies)} tasks to queue")
    
    async def process_queue(self):
        """Main processing loop - handle tasks with concurrency"""
        self.running = True
        logger.info(f"🚀 Starting pipeline with max_concurrent={self.max_concurrent}")
        
        active_tasks = set()
        
        try:
            while self.running or not self.queue.empty() or active_tasks:
                # Start new tasks if we have capacity
                while len(active_tasks) < self.max_concurrent and not self.queue.empty():
                    task = self.queue.get_nowait()
                    
                    # Check dependencies
                    if not self.resolver.can_learn(task):
                        logger.info(f"⏳ {task.technology} waiting for dependencies")
                        self.queue.put(task)  # Put back in queue
                        await asyncio.sleep(1)
                        continue
                    
                    # Start learning
                    task_future = asyncio.create_task(self._process_task(task))
                    active_tasks.add(task_future)
                
                # Wait for any task to complete
                if active_tasks:
                    done, active_tasks = await asyncio.wait(
                        active_tasks,
                        timeout=1.0,
                        return_when=asyncio.FIRST_COMPLETED
                    )
                else:
                    await asyncio.sleep(1)
                
                # Save state periodically
                self._save_state()
        
        except KeyboardInterrupt:
            logger.info("⚠️  Pipeline interrupted by user")
        finally:
            self.running = False
            self._save_state()
            logger.info("🛑 Pipeline stopped")
    
    async def _process_task(self, task: LearningTask):
        """Process a single learning task"""
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = time.time()
        self.resolver.mark_started(task.technology)
        
        logger.info(f"🎯 Learning: {task.technology} (depth: {task.depth})")
        
        try:
            # Run learning in thread pool (blocking operation)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self.learning_engine.learn_technology,
                task.technology,
                task.depth
            )
            
            if result.success:
                task.status = TaskStatus.COMPLETED
                task.completed_at = time.time()
                task.result = {
                    'proficiency': result.proficiency,
                    'quality_grade': result.quality_grade,
                    'tests_passed': result.tests_passed,
                    'execution_time': result.execution_time
                }
                
                self.resolver.mark_completed(task.technology)
                self.total_completed += 1
                
                duration = task.completed_at - task.started_at
                logger.info(
                    f"✅ {task.technology} learned successfully! "
                    f"(proficiency: {result.proficiency:.1%}, "
                    f"grade: {result.quality_grade}, "
                    f"time: {duration:.1f}s)"
                )
                
                # Record metrics
                if self.metrics:
                    self.metrics.record_learning(
                        technology=task.technology,
                        success=True,
                        duration=duration,
                        proficiency=result.proficiency,
                        quality_grade=result.quality_grade
                    )
            
            else:
                # Learning failed, retry if possible
                await self._handle_failure(task, result.errors)
        
        except Exception as e:
            logger.error(f"❌ Error learning {task.technology}: {e}", exc_info=True)
            await self._handle_failure(task, [str(e)])
    
    async def _handle_failure(self, task: LearningTask, errors: List[str]):
        """Handle task failure with retry logic"""
        task.error = "; ".join(errors)
        
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            task.status = TaskStatus.RETRYING
            self.total_retries += 1
            
            # Exponential backoff
            delay = 2 ** task.retry_count
            logger.warning(
                f"⚠️  {task.technology} failed, retry {task.retry_count}/{task.max_retries} "
                f"in {delay}s"
            )
            
            await asyncio.sleep(delay)
            self.queue.put(task)
        
        else:
            task.status = TaskStatus.FAILED
            task.completed_at = time.time()
            self.resolver.mark_failed(task.technology)
            self.total_failed += 1
            
            logger.error(
                f"❌ {task.technology} failed after {task.max_retries} retries. "
                f"Errors: {task.error}"
            )
            
            # Record failure
            if self.metrics:
                self.metrics.record_learning(
                    technology=task.technology,
                    success=False,
                    errors=task.error
                )
    
    def get_status(self) -> Dict:
        """Get pipeline status"""
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        
        return {
            'running': self.running,
            'queue_size': self.queue.qsize(),
            'tasks': {
                'total': len(self.tasks),
                'pending': pending,
                'in_progress': in_progress,
                'completed': completed,
                'failed': failed
            },
            'stats': {
                'total_completed': self.total_completed,
                'total_failed': self.total_failed,
                'total_retries': self.total_retries
            }
        }
    
    def _save_state(self):
        """Save pipeline state to disk"""
        try:
            state = {
                'tasks': {
                    tech: {
                        'technology': t.technology,
                        'depth': t.depth,
                        'priority': t.priority.name,
                        'status': t.status.value,
                        'retry_count': t.retry_count,
                        'error': t.error,
                        'result': t.result
                    }
                    for tech, t in self.tasks.items()
                },
                'stats': {
                    'total_completed': self.total_completed,
                    'total_failed': self.total_failed,
                    'total_retries': self.total_retries
                },
                'saved_at': datetime.now().isoformat()
            }
            
            self.state_file.write_text(json.dumps(state, indent=2))
        
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def _load_state(self):
        """Load pipeline state from disk"""
        try:
            if self.state_file.exists():
                state = json.loads(self.state_file.read_text())
                
                # Restore stats
                stats = state.get('stats', {})
                self.total_completed = stats.get('total_completed', 0)
                self.total_failed = stats.get('total_failed', 0)
                self.total_retries = stats.get('total_retries', 0)
                
                logger.info(f"📂 Loaded state from {self.state_file}")
        
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
    
    def stop(self):
        """Stop the pipeline gracefully"""
        logger.info("🛑 Stopping pipeline...")
        self.running = False


# Demo/Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*80)
    print("🧪 NASA-Level Learning Pipeline Test")
    print("="*80)
    
    # Mock learning engine for testing
    class MockLearningEngine:
        def learn_technology(self, tech, depth):
            import random
            time.sleep(random.uniform(1, 3))  # Simulate learning
            
            from core.nasa_level.advanced_learning import LearningResult
            return LearningResult(
                technology=tech,
                success=random.random() > 0.2,  # 80% success rate
                proficiency=random.uniform(0.7, 0.95),
                quality_grade="A",
                tests_passed=1,
                tests_total=1,
                execution_time=2.0,
                errors=[],
                suggestions=[],
                artifacts=[]
            )
    
    # Create pipeline
    engine = MockLearningEngine()
    pipeline = LearningPipeline(
        learning_engine=engine,
        max_concurrent=2
    )
    
    # Add tasks
    pipeline.add_task("requests", priority=Priority.HIGH)
    pipeline.add_task("pandas", priority=Priority.NORMAL, dependencies=["numpy"])
    pipeline.add_task("numpy", priority=Priority.HIGH)
    pipeline.add_task("flask", priority=Priority.LOW)
    
    print(f"\n📊 Initial status:")
    print(json.dumps(pipeline.get_status(), indent=2))
    
    # Run pipeline
    print(f"\n🚀 Starting pipeline...\n")
    
    async def run():
        await asyncio.wait_for(pipeline.process_queue(), timeout=30)
    
    try:
        asyncio.run(run())
    except asyncio.TimeoutError:
        print("\n⏱️  Test completed (timeout)")
    
    print(f"\n📊 Final status:")
    print(json.dumps(pipeline.get_status(), indent=2))
    
    print("\n✅ Pipeline test complete!")
