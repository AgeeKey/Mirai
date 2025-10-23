"""
Self-Reflection System
Tracks successes, failures, and learnings for future LoRA training
"""

import json
import logging
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Reflection:
    """Single reflection entry"""
    id: Optional[int]
    timestamp: str
    task_id: str
    task_description: str
    status: str  # success, failure, partial
    what_worked: str
    what_failed: str
    lessons_learned: str
    tool_calls: str  # JSON of tool calls made
    execution_time: float
    tokens_used: int
    hallucination_detected: bool
    error_message: Optional[str] = None


@dataclass
class PerformanceMetrics:
    """Performance metrics for tracking"""
    task_success_rate: float  # Target: ≥70%
    mean_time_to_result: float  # Target: <10 min
    tool_use_accuracy: float  # Target: ≥90%
    hallucination_rate: float  # Target: →0%
    rag_hit_rate: float  # Target: >80%


class SelfReflectionSystem:
    """
    System for tracking and learning from task execution
    
    Features:
    - Store reflections in SQLite
    - Track success/failure patterns
    - Calculate KPIs
    - Export training data for LoRA
    """

    def __init__(self, db_path: str = "data/reflections.db"):
        """
        Initialize reflection system

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        
        self._create_tables()
        
        logger.info(f"📝 Reflection system initialized: {self.db_path}")

    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Reflections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_description TEXT NOT NULL,
                status TEXT NOT NULL,
                what_worked TEXT,
                what_failed TEXT,
                lessons_learned TEXT,
                tool_calls TEXT,
                execution_time REAL,
                tokens_used INTEGER,
                hallucination_detected INTEGER,
                error_message TEXT
            )
        """)
        
        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metadata TEXT
            )
        """)
        
        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_reflections_timestamp ON reflections(timestamp)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_reflections_status ON reflections(status)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)"
        )
        
        self.conn.commit()

    def add_reflection(
        self,
        task_id: str,
        task_description: str,
        status: str,
        what_worked: str,
        what_failed: str,
        lessons_learned: str,
        tool_calls: List[Dict],
        execution_time: float,
        tokens_used: int,
        hallucination_detected: bool = False,
        error_message: Optional[str] = None,
    ) -> int:
        """
        Add a reflection entry

        Args:
            task_id: Unique task identifier
            task_description: Description of the task
            status: success, failure, or partial
            what_worked: What went well
            what_failed: What didn't work
            lessons_learned: Key learnings
            tool_calls: List of tool calls made
            execution_time: Time taken in seconds
            tokens_used: Number of tokens used
            hallucination_detected: Whether hallucination was detected
            error_message: Optional error message

        Returns:
            Reflection ID
        """
        cursor = self.conn.cursor()
        
        reflection = Reflection(
            id=None,
            timestamp=datetime.utcnow().isoformat(),
            task_id=task_id,
            task_description=task_description,
            status=status,
            what_worked=what_worked,
            what_failed=what_failed,
            lessons_learned=lessons_learned,
            tool_calls=json.dumps(tool_calls),
            execution_time=execution_time,
            tokens_used=tokens_used,
            hallucination_detected=hallucination_detected,
            error_message=error_message,
        )
        
        cursor.execute("""
            INSERT INTO reflections (
                timestamp, task_id, task_description, status,
                what_worked, what_failed, lessons_learned,
                tool_calls, execution_time, tokens_used,
                hallucination_detected, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reflection.timestamp,
            reflection.task_id,
            reflection.task_description,
            reflection.status,
            reflection.what_worked,
            reflection.what_failed,
            reflection.lessons_learned,
            reflection.tool_calls,
            reflection.execution_time,
            reflection.tokens_used,
            1 if reflection.hallucination_detected else 0,
            reflection.error_message,
        ))
        
        self.conn.commit()
        
        reflection_id = cursor.lastrowid
        logger.info(f"📝 Reflection added: {task_id} ({status})")
        
        return reflection_id

    def get_reflections(
        self,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Reflection]:
        """
        Get reflections

        Args:
            status: Filter by status (success, failure, partial)
            limit: Maximum number to return

        Returns:
            List of reflections
        """
        cursor = self.conn.cursor()
        
        if status:
            cursor.execute(
                "SELECT * FROM reflections WHERE status = ? ORDER BY timestamp DESC LIMIT ?",
                (status, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM reflections ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
        
        reflections = []
        for row in cursor.fetchall():
            reflection = Reflection(
                id=row["id"],
                timestamp=row["timestamp"],
                task_id=row["task_id"],
                task_description=row["task_description"],
                status=row["status"],
                what_worked=row["what_worked"],
                what_failed=row["what_failed"],
                lessons_learned=row["lessons_learned"],
                tool_calls=row["tool_calls"],
                execution_time=row["execution_time"],
                tokens_used=row["tokens_used"],
                hallucination_detected=bool(row["hallucination_detected"]),
                error_message=row["error_message"],
            )
            reflections.append(reflection)
        
        return reflections

    def calculate_metrics(self) -> PerformanceMetrics:
        """
        Calculate performance metrics

        Returns:
            Performance metrics
        """
        cursor = self.conn.cursor()
        
        # Task success rate
        cursor.execute("SELECT COUNT(*) as total FROM reflections")
        total = cursor.fetchone()["total"]
        
        if total == 0:
            return PerformanceMetrics(
                task_success_rate=0.0,
                mean_time_to_result=0.0,
                tool_use_accuracy=0.0,
                hallucination_rate=0.0,
                rag_hit_rate=0.0,
            )
        
        cursor.execute(
            "SELECT COUNT(*) as successful FROM reflections WHERE status = 'success'"
        )
        successful = cursor.fetchone()["successful"]
        task_success_rate = (successful / total) * 100.0
        
        # Mean time to result
        cursor.execute("SELECT AVG(execution_time) as avg_time FROM reflections")
        avg_time = cursor.fetchone()["avg_time"] or 0.0
        mean_time_to_result = avg_time / 60.0  # Convert to minutes
        
        # Hallucination rate
        cursor.execute(
            "SELECT COUNT(*) as hallucinations FROM reflections WHERE hallucination_detected = 1"
        )
        hallucinations = cursor.fetchone()["hallucinations"]
        hallucination_rate = (hallucinations / total) * 100.0
        
        # Tool use accuracy (placeholder - would need tool validator integration)
        tool_use_accuracy = 0.0
        
        # RAG hit rate (placeholder - would need RAG integration)
        rag_hit_rate = 0.0
        
        metrics = PerformanceMetrics(
            task_success_rate=task_success_rate,
            mean_time_to_result=mean_time_to_result,
            tool_use_accuracy=tool_use_accuracy,
            hallucination_rate=hallucination_rate,
            rag_hit_rate=rag_hit_rate,
        )
        
        # Store metrics
        self._store_metric("task_success_rate", metrics.task_success_rate)
        self._store_metric("mean_time_to_result", metrics.mean_time_to_result)
        self._store_metric("hallucination_rate", metrics.hallucination_rate)
        
        return metrics

    def _store_metric(self, name: str, value: float, metadata: Optional[Dict] = None):
        """Store a metric value"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO metrics (timestamp, metric_name, metric_value, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            name,
            value,
            json.dumps(metadata) if metadata else None,
        ))
        
        self.conn.commit()

    def get_metric_history(self, metric_name: str, limit: int = 100) -> List[Dict]:
        """
        Get historical values for a metric

        Args:
            metric_name: Name of the metric
            limit: Number of recent values to return

        Returns:
            List of metric entries
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, metric_value, metadata
            FROM metrics
            WHERE metric_name = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (metric_name, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "timestamp": row["timestamp"],
                "value": row["metric_value"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else None,
            })
        
        return history

    def export_training_data(self, output_path: str, status: Optional[str] = None):
        """
        Export reflections as training data for LoRA

        Args:
            output_path: Path to save JSONL file
            status: Filter by status (optional)
        """
        reflections = self.get_reflections(status=status, limit=10000)
        
        with open(output_path, "w") as f:
            for reflection in reflections:
                # Format as instruction-following data
                training_example = {
                    "instruction": reflection.task_description,
                    "tool_calls": json.loads(reflection.tool_calls),
                    "status": reflection.status,
                    "execution_time": reflection.execution_time,
                    "lessons_learned": reflection.lessons_learned,
                }
                f.write(json.dumps(training_example) + "\n")
        
        logger.info(f"📦 Exported {len(reflections)} reflections to {output_path}")

    def get_summary(self) -> Dict:
        """Get summary of reflections and metrics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM reflections")
        total = cursor.fetchone()["total"]
        
        cursor.execute(
            "SELECT COUNT(*) as successful FROM reflections WHERE status = 'success'"
        )
        successful = cursor.fetchone()["successful"]
        
        cursor.execute(
            "SELECT COUNT(*) as failed FROM reflections WHERE status = 'failure'"
        )
        failed = cursor.fetchone()["failed"]
        
        metrics = self.calculate_metrics()
        
        return {
            "total_reflections": total,
            "successful": successful,
            "failed": failed,
            "metrics": asdict(metrics),
        }

    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Test reflection system
    print("🧪 Testing Self-Reflection System...")
    
    system = SelfReflectionSystem(db_path="/tmp/test_reflections.db")
    
    # Add test reflections
    system.add_reflection(
        task_id="task_1",
        task_description="Write Python script to calculate fibonacci",
        status="success",
        what_worked="Used recursive approach, tested with small numbers",
        what_failed="",
        lessons_learned="Recursion works well for small numbers",
        tool_calls=[{"tool": "execute_python", "args": {"code": "..."}}],
        execution_time=5.2,
        tokens_used=150,
        hallucination_detected=False,
    )
    
    system.add_reflection(
        task_id="task_2",
        task_description="Search for Python best practices",
        status="failure",
        what_worked="",
        what_failed="Network timeout",
        lessons_learned="Need to increase timeout for web searches",
        tool_calls=[{"tool": "search_web", "args": {"query": "python best practices"}}],
        execution_time=30.5,
        tokens_used=80,
        hallucination_detected=False,
        error_message="Connection timeout after 30s",
    )
    
    # Get metrics
    metrics = system.calculate_metrics()
    print(f"\n✅ Metrics:")
    print(f"   Task Success Rate: {metrics.task_success_rate:.1f}% (target ≥70%)")
    print(f"   Mean Time to Result: {metrics.mean_time_to_result:.2f} min (target <10 min)")
    print(f"   Hallucination Rate: {metrics.hallucination_rate:.1f}% (target →0%)")
    
    # Get summary
    summary = system.get_summary()
    print(f"\n✅ Summary: {summary}")
    
    system.close()
