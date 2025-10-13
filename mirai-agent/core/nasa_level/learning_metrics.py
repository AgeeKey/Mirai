"""
NASA-Level Learning Metrics
Prometheus integration and performance monitoring
"""

import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest, REGISTRY

logger = logging.getLogger(__name__)


# Prometheus metrics
LEARNING_ATTEMPTS = Counter(
    'nasa_learning_attempts_total',
    'Total number of learning attempts',
    ['technology', 'depth']
)

LEARNING_SUCCESS = Counter(
    'nasa_learning_success_total',
    'Total number of successful learning',
    ['technology', 'grade']
)

LEARNING_FAILURES = Counter(
    'nasa_learning_failures_total',
    'Total number of failed learning attempts',
    ['technology', 'reason']
)

LEARNING_DURATION = Histogram(
    'nasa_learning_duration_seconds',
    'Time spent learning a technology',
    ['technology', 'depth'],
    buckets=[10, 30, 60, 120, 300, 600, 1200, 3600]
)

PROFICIENCY_SCORE = Gauge(
    'nasa_proficiency_score',
    'Current proficiency score for technology',
    ['technology']
)

QUALITY_SCORE = Gauge(
    'nasa_quality_score',
    'Current quality score for technology',
    ['technology']
)

CODE_QUALITY_METRICS = Histogram(
    'nasa_code_quality_metrics',
    'Distribution of code quality metrics',
    ['metric_type'],  # complexity, maintainability, etc.
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

ACTIVE_LEARNING_TASKS = Gauge(
    'nasa_active_learning_tasks',
    'Number of currently active learning tasks'
)

KNOWLEDGE_BASE_SIZE = Gauge(
    'nasa_knowledge_base_size',
    'Total number of learned technologies'
)


@dataclass
class LearningEvent:
    """A single learning event"""
    technology: str
    success: bool
    duration: float
    proficiency: float
    quality_grade: str
    timestamp: float = field(default_factory=time.time)
    errors: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class LearningMetrics:
    """
    Collects and tracks learning metrics:
    - Prometheus integration for real-time monitoring
    - Historical performance tracking
    - Trend analysis
    - Success/failure rates
    """
    
    def __init__(self, metrics_file: str = "/tmp/nasa_metrics.jsonl"):
        self.metrics_file = Path(metrics_file)
        self.events: List[LearningEvent] = []
        
        # In-memory stats
        self.stats = {
            'total_attempts': 0,
            'total_success': 0,
            'total_failures': 0,
            'by_technology': defaultdict(lambda: {
                'attempts': 0,
                'success': 0,
                'failures': 0,
                'total_duration': 0.0,
                'best_proficiency': 0.0
            })
        }
        
        # Load historical data
        self._load_metrics()
    
    def record_learning(
        self,
        technology: str,
        success: bool,
        duration: float = 0.0,
        proficiency: float = 0.0,
        quality_grade: str = 'F',
        depth: str = 'basic',
        errors: List[str] = None,
        metadata: Dict = None
    ):
        """Record a learning event"""
        
        event = LearningEvent(
            technology=technology,
            success=success,
            duration=duration,
            proficiency=proficiency,
            quality_grade=quality_grade,
            errors=errors or [],
            metadata=metadata or {'depth': depth}
        )
        
        self.events.append(event)
        
        # Update Prometheus metrics
        LEARNING_ATTEMPTS.labels(
            technology=technology,
            depth=depth
        ).inc()
        
        if success:
            LEARNING_SUCCESS.labels(
                technology=technology,
                grade=quality_grade
            ).inc()
            
            LEARNING_DURATION.labels(
                technology=technology,
                depth=depth
            ).observe(duration)
            
            PROFICIENCY_SCORE.labels(
                technology=technology
            ).set(proficiency)
            
            # Map grade to score
            grade_map = {'A': 1.0, 'B': 0.85, 'C': 0.7, 'D': 0.55, 'F': 0.4}
            quality_score = grade_map.get(quality_grade, 0.4)
            
            QUALITY_SCORE.labels(
                technology=technology
            ).set(quality_score)
        
        else:
            reason = errors[0] if errors else 'unknown'
            LEARNING_FAILURES.labels(
                technology=technology,
                reason=reason[:50]  # Limit label length
            ).inc()
        
        # Update internal stats
        self.stats['total_attempts'] += 1
        if success:
            self.stats['total_success'] += 1
        else:
            self.stats['total_failures'] += 1
        
        tech_stats = self.stats['by_technology'][technology]
        tech_stats['attempts'] += 1
        if success:
            tech_stats['success'] += 1
            tech_stats['total_duration'] += duration
            tech_stats['best_proficiency'] = max(
                tech_stats['best_proficiency'],
                proficiency
            )
        else:
            tech_stats['failures'] += 1
        
        # Save to disk
        self._save_event(event)
        
        logger.info(
            f"📊 Metrics recorded: {technology} - "
            f"{'✅ SUCCESS' if success else '❌ FAILED'} "
            f"({duration:.1f}s, {proficiency:.1%})"
        )
    
    def get_success_rate(self, technology: str = None) -> float:
        """Get success rate (overall or for specific technology)"""
        if technology:
            stats = self.stats['by_technology'].get(technology)
            if not stats or stats['attempts'] == 0:
                return 0.0
            return stats['success'] / stats['attempts']
        else:
            if self.stats['total_attempts'] == 0:
                return 0.0
            return self.stats['total_success'] / self.stats['total_attempts']
    
    def get_average_duration(self, technology: str = None) -> float:
        """Get average learning duration"""
        if technology:
            stats = self.stats['by_technology'].get(technology)
            if not stats or stats['success'] == 0:
                return 0.0
            return stats['total_duration'] / stats['success']
        else:
            total_duration = sum(
                e.duration for e in self.events if e.success
            )
            success_count = sum(1 for e in self.events if e.success)
            return total_duration / success_count if success_count > 0 else 0.0
    
    def get_proficiency_trend(self, technology: str) -> List[float]:
        """Get proficiency trend over time"""
        return [
            e.proficiency
            for e in self.events
            if e.technology == technology and e.success
        ]
    
    def get_top_technologies(self, limit: int = 10) -> List[Dict]:
        """Get top performing technologies"""
        tech_list = []
        
        for tech, stats in self.stats['by_technology'].items():
            if stats['success'] > 0:
                tech_list.append({
                    'technology': tech,
                    'proficiency': stats['best_proficiency'],
                    'attempts': stats['attempts'],
                    'success_rate': stats['success'] / stats['attempts'],
                    'avg_duration': stats['total_duration'] / stats['success']
                })
        
        # Sort by proficiency, then success rate
        tech_list.sort(
            key=lambda x: (x['proficiency'], x['success_rate']),
            reverse=True
        )
        
        return tech_list[:limit]
    
    def get_summary(self) -> Dict:
        """Get overall metrics summary"""
        recent_events = self.events[-100:] if len(self.events) > 100 else self.events
        
        recent_success_rate = (
            sum(1 for e in recent_events if e.success) / len(recent_events)
            if recent_events else 0.0
        )
        
        avg_proficiency = (
            sum(e.proficiency for e in recent_events if e.success) /
            sum(1 for e in recent_events if e.success)
            if any(e.success for e in recent_events) else 0.0
        )
        
        return {
            'total_attempts': self.stats['total_attempts'],
            'total_success': self.stats['total_success'],
            'total_failures': self.stats['total_failures'],
            'overall_success_rate': self.get_success_rate(),
            'recent_success_rate': recent_success_rate,
            'average_duration': self.get_average_duration(),
            'average_proficiency': avg_proficiency,
            'unique_technologies': len(self.stats['by_technology']),
            'total_events': len(self.events)
        }
    
    def generate_report(self) -> str:
        """Generate human-readable metrics report"""
        summary = self.get_summary()
        top_techs = self.get_top_technologies(5)
        
        report = []
        report.append("="*80)
        report.append("📊 NASA-LEVEL LEARNING METRICS REPORT")
        report.append("="*80)
        
        report.append("\n📈 OVERALL STATISTICS")
        report.append(f"  Total Attempts: {summary['total_attempts']}")
        report.append(f"  Success: {summary['total_success']} ({summary['overall_success_rate']:.1%})")
        report.append(f"  Failures: {summary['total_failures']}")
        report.append(f"  Avg Duration: {summary['average_duration']:.1f}s")
        report.append(f"  Avg Proficiency: {summary['average_proficiency']:.1%}")
        report.append(f"  Technologies Learned: {summary['unique_technologies']}")
        
        if top_techs:
            report.append("\n🏆 TOP TECHNOLOGIES")
            for i, tech in enumerate(top_techs, 1):
                report.append(
                    f"  {i}. {tech['technology']}: "
                    f"{tech['proficiency']:.1%} proficiency, "
                    f"{tech['success_rate']:.1%} success rate, "
                    f"{tech['avg_duration']:.1f}s avg"
                )
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)
    
    def export_prometheus(self) -> bytes:
        """Export metrics in Prometheus format"""
        return generate_latest(REGISTRY)
    
    def _save_event(self, event: LearningEvent):
        """Append event to metrics file"""
        try:
            with open(self.metrics_file, 'a') as f:
                f.write(json.dumps({
                    'technology': event.technology,
                    'success': event.success,
                    'duration': event.duration,
                    'proficiency': event.proficiency,
                    'quality_grade': event.quality_grade,
                    'timestamp': event.timestamp,
                    'errors': event.errors,
                    'metadata': event.metadata
                }) + '\n')
        except Exception as e:
            logger.error(f"Failed to save event: {e}")
    
    def _load_metrics(self):
        """Load historical metrics from file"""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            event = LearningEvent(**data)
                            self.events.append(event)
                            
                            # Rebuild stats
                            self.stats['total_attempts'] += 1
                            if event.success:
                                self.stats['total_success'] += 1
                            else:
                                self.stats['total_failures'] += 1
                            
                            tech_stats = self.stats['by_technology'][event.technology]
                            tech_stats['attempts'] += 1
                            if event.success:
                                tech_stats['success'] += 1
                                tech_stats['total_duration'] += event.duration
                                tech_stats['best_proficiency'] = max(
                                    tech_stats['best_proficiency'],
                                    event.proficiency
                                )
                            else:
                                tech_stats['failures'] += 1
                
                logger.info(f"📂 Loaded {len(self.events)} historical events")
        except Exception as e:
            logger.error(f"Failed to load metrics: {e}")


# Demo/Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*80)
    print("🧪 NASA-Level Learning Metrics Test")
    print("="*80)
    
    metrics = LearningMetrics("/tmp/test_metrics.jsonl")
    
    # Simulate some learning events
    print("\n➕ Recording test events...")
    
    metrics.record_learning(
        technology="requests",
        success=True,
        duration=25.3,
        proficiency=0.92,
        quality_grade="A",
        depth="basic"
    )
    
    metrics.record_learning(
        technology="pandas",
        success=True,
        duration=45.7,
        proficiency=0.85,
        quality_grade="B",
        depth="intermediate"
    )
    
    metrics.record_learning(
        technology="flask",
        success=False,
        duration=0.0,
        proficiency=0.0,
        quality_grade="F",
        errors=["Timeout", "Quality too low"]
    )
    
    metrics.record_learning(
        technology="requests",
        success=True,
        duration=22.1,
        proficiency=0.95,
        quality_grade="A",
        depth="advanced"
    )
    
    # Show summary
    print("\n" + metrics.generate_report())
    
    # Show top technologies
    print("\n🏆 Top Technologies:")
    for tech in metrics.get_top_technologies(3):
        print(f"  - {tech['technology']}: {tech['proficiency']:.1%}")
    
    # Show Prometheus metrics
    print("\n📊 Prometheus metrics (sample):")
    prom_data = metrics.export_prometheus().decode('utf-8')
    for line in prom_data.split('\n')[:20]:
        if line and not line.startswith('#'):
            print(f"  {line}")
    
    print("\n✅ Metrics test complete!")
