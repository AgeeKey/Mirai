"""
NASA-Level Learning Orchestrator
Master coordinator for the entire learning system
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.autonomous_agent import AutonomousAgent
from core.nasa_level.sandbox_executor import SandboxExecutor
from core.nasa_level.quality_analyzer import CodeQualityAnalyzer
from core.nasa_level.advanced_learning import AdvancedLearningEngine
from core.nasa_level.knowledge_manager import KnowledgeManager
from core.nasa_level.learning_metrics import LearningMetrics
from core.nasa_level.learning_pipeline import LearningPipeline, Priority

logger = logging.getLogger(__name__)


class NASALearningOrchestrator:
    """
    Master orchestrator that ties everything together:
    - Advanced Learning Engine
    - Learning Pipeline with priorities
    - Knowledge Manager with search
    - Metrics and monitoring
    """
    
    def __init__(self):
        logger.info("🚀 Initializing NASA-Level Learning System...")
        
        # Core components
        self.ai_agent = AutonomousAgent()
        self.sandbox = SandboxExecutor()
        self.quality_analyzer = CodeQualityAnalyzer()
        
        # Learning engine
        self.learning_engine = AdvancedLearningEngine(
            self.ai_agent,
            self.sandbox,
            self.quality_analyzer
        )
        
        # Knowledge management
        self.knowledge_manager = KnowledgeManager()
        
        # Metrics
        self.metrics = LearningMetrics()
        
        # Pipeline
        self.pipeline = LearningPipeline(
            learning_engine=self.learning_engine,
            knowledge_manager=self.knowledge_manager,
            metrics=self.metrics,
            max_concurrent=2
        )
        
        logger.info("✅ NASA-Level Learning System initialized!")
    
    def learn_technology(self, technology: str, depth: str = "basic", priority: Priority = Priority.NORMAL):
        """Learn a single technology synchronously"""
        logger.info(f"🎯 Learning {technology} ({depth})...")
        
        result = self.learning_engine.learn_technology(technology, depth)
        
        if result.success:
            # Save to knowledge base
            self.knowledge_manager.save_knowledge(
                technology=technology,
                research=result.artifacts[0].content if result.artifacts else "",
                code=result.artifacts[1].content if len(result.artifacts) > 1 else "",
                quality_grade=result.quality_grade,
                proficiency=result.proficiency,
                tests_passed=result.tests_passed,
                tests_total=result.tests_total,
                metadata={'depth': depth}
            )
            
            # Record metrics
            self.metrics.record_learning(
                technology=technology,
                success=True,
                duration=result.execution_time,
                proficiency=result.proficiency,
                quality_grade=result.quality_grade,
                depth=depth
            )
        else:
            self.metrics.record_learning(
                technology=technology,
                success=False,
                errors=result.errors
            )
        
        return result
    
    def queue_learning(self, technology: str, depth: str = "basic", priority: Priority = Priority.NORMAL):
        """Add technology to learning queue"""
        self.pipeline.add_task(technology, depth, priority)
        logger.info(f"➕ Queued: {technology} with priority {priority.name}")
    
    async def start_pipeline(self):
        """Start the learning pipeline"""
        logger.info("🚀 Starting NASA learning pipeline...")
        await self.pipeline.process_queue()
    
    def get_status(self):
        """Get system status"""
        return {
            'pipeline': self.pipeline.get_status(),
            'knowledge': self.knowledge_manager.get_stats(),
            'metrics': self.metrics.get_summary()
        }
    
    def search_knowledge(self, query: str):
        """Search in knowledge base"""
        return self.knowledge_manager.search(query)
    
    def get_learned_technologies(self):
        """Get all learned technologies"""
        return self.knowledge_manager.get_all_technologies()
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = []
        report.append("="*80)
        report.append("🚀 NASA-LEVEL LEARNING SYSTEM REPORT")
        report.append("="*80)
        
        # Metrics
        report.append("\n" + self.metrics.generate_report())
        
        # Knowledge stats
        kb_stats = self.knowledge_manager.get_stats()
        report.append("\n📚 KNOWLEDGE BASE")
        report.append(f"  Unique Technologies: {kb_stats['unique_technologies']}")
        report.append(f"  Total Entries: {kb_stats['total_entries']}")
        report.append(f"  Avg Proficiency: {kb_stats['average_proficiency']:.1%}")
        report.append(f"  Learned Last 7 Days: {kb_stats['learned_last_7_days']}")
        
        # Pipeline status
        pipeline_status = self.pipeline.get_status()
        report.append("\n⚙️  PIPELINE STATUS")
        report.append(f"  Running: {pipeline_status['running']}")
        report.append(f"  Queue Size: {pipeline_status['queue_size']}")
        report.append(f"  Completed: {pipeline_status['tasks']['completed']}")
        report.append(f"  Failed: {pipeline_status['tasks']['failed']}")
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description="NASA-Level Learning System")
    parser.add_argument('command', choices=['learn', 'queue', 'status', 'report', 'search'],
                       help='Command to execute')
    parser.add_argument('--tech', help='Technology to learn')
    parser.add_argument('--depth', default='basic', choices=['basic', 'intermediate', 'advanced'])
    parser.add_argument('--priority', default='normal', choices=['critical', 'high', 'normal', 'low'])
    parser.add_argument('--query', help='Search query')
    
    args = parser.parse_args()
    
    orchestrator = NASALearningOrchestrator()
    
    if args.command == 'learn':
        if not args.tech:
            print("❌ --tech is required for learn command")
            sys.exit(1)
        
        result = orchestrator.learn_technology(args.tech, args.depth)
        if result.success:
            print(f"✅ Successfully learned {args.tech}!")
            print(f"   Proficiency: {result.proficiency:.1%}")
            print(f"   Grade: {result.quality_grade}")
        else:
            print(f"❌ Failed to learn {args.tech}")
            for error in result.errors:
                print(f"   - {error}")
    
    elif args.command == 'queue':
        if not args.tech:
            print("❌ --tech is required for queue command")
            sys.exit(1)
        
        priority_map = {
            'critical': Priority.CRITICAL,
            'high': Priority.HIGH,
            'normal': Priority.NORMAL,
            'low': Priority.LOW
        }
        orchestrator.queue_learning(args.tech, args.depth, priority_map[args.priority])
        print(f"✅ Queued {args.tech} for learning")
    
    elif args.command == 'status':
        status = orchestrator.get_status()
        print("\n📊 SYSTEM STATUS\n")
        print("Pipeline:", status['pipeline'])
        print("\nKnowledge:", status['knowledge'])
        print("\nMetrics:", status['metrics'])
    
    elif args.command == 'report':
        print(orchestrator.generate_report())
    
    elif args.command == 'search':
        if not args.query:
            print("❌ --query is required for search command")
            sys.exit(1)
        
        results = orchestrator.search_knowledge(args.query)
        print(f"\n🔍 Found {len(results)} results for '{args.query}':\n")
        for r in results:
            print(f"  - {r.technology} v{r.version} (grade: {r.quality_grade}, {r.proficiency:.1%})")
