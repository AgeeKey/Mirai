#!/usr/bin/env python3
"""
Complete NASA-Level System Integration Test
Tests all components working together
"""

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/mirai/mirai-agent")

from core.nasa_level import NASALearningOrchestrator, Priority


async def main():
    print("="*80)
    print("🚀 NASA-LEVEL COMPLETE SYSTEM TEST")
    print("="*80)
    
    # Initialize system
    print("\n📦 Initializing NASA-Level Learning System...")
    orchestrator = NASALearningOrchestrator()
    print("✅ System initialized!\n")
    
    # Test 1: Learn a single technology
    print("="*80)
    print("TEST 1: Single Technology Learning")
    print("="*80)
    
    print("\n🎯 Learning 'requests' library...")
    start = time.time()
    result = orchestrator.learn_technology("requests", depth="basic")
    duration = time.time() - start
    
    if result.success:
        print(f"✅ SUCCESS! Learned in {duration:.1f}s")
        print(f"   Proficiency: {result.proficiency:.1%}")
        print(f"   Quality Grade: {result.quality_grade}")
        print(f"   Tests Passed: {result.tests_passed}/{result.tests_total}")
    else:
        print(f"❌ FAILED: {result.errors}")
        return 1
    
    # Test 2: Queue multiple technologies
    print("\n" + "="*80)
    print("TEST 2: Pipeline with Multiple Technologies")
    print("="*80)
    
    print("\n➕ Adding technologies to queue...")
    orchestrator.queue_learning("json", depth="basic", priority=Priority.HIGH)
    orchestrator.queue_learning("datetime", depth="basic", priority=Priority.NORMAL)
    orchestrator.queue_learning("pathlib", depth="basic", priority=Priority.LOW)
    
    print("🚀 Starting pipeline (30s timeout)...")
    
    try:
        await asyncio.wait_for(orchestrator.start_pipeline(), timeout=120)
    except asyncio.TimeoutError:
        print("⏱️  Pipeline timeout - stopping...")
        orchestrator.pipeline.stop()
    
    # Test 3: Knowledge base
    print("\n" + "="*80)
    print("TEST 3: Knowledge Base Operations")
    print("="*80)
    
    print("\n📚 Listing learned technologies...")
    technologies = orchestrator.get_learned_technologies()
    print(f"Found {len(technologies)} technologies:")
    for tech in technologies:
        print(f"  - {tech}")
    
    print("\n🔍 Searching for 'HTTP'...")
    search_results = orchestrator.search_knowledge("HTTP")
    print(f"Found {len(search_results)} results:")
    for r in search_results:
        print(f"  - {r.technology} v{r.version} (grade: {r.quality_grade})")
    
    # Test 4: Metrics and reporting
    print("\n" + "="*80)
    print("TEST 4: Metrics and Reporting")
    print("="*80)
    
    print("\n📊 System status:")
    status = orchestrator.get_status()
    print(f"  Pipeline completed: {status['pipeline']['tasks']['completed']}")
    print(f"  Pipeline failed: {status['pipeline']['tasks']['failed']}")
    print(f"  Knowledge entries: {status['knowledge']['total_entries']}")
    print(f"  Unique technologies: {status['knowledge']['unique_technologies']}")
    print(f"  Success rate: {status['metrics']['overall_success_rate']:.1%}")
    print(f"  Avg proficiency: {status['metrics']['average_proficiency']:.1%}")
    
    # Full report
    print("\n" + "="*80)
    print("FINAL REPORT")
    print("="*80)
    print(orchestrator.generate_report())
    
    print("\n" + "="*80)
    print("🎉 ALL TESTS COMPLETE!")
    print("="*80)
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
