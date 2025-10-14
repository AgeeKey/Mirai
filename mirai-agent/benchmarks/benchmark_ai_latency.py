"""
Benchmark AI Response Latency
Measures time to get responses from OpenAI API
"""
import sys
import time
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.autonomous_agent import AutonomousAgent

def benchmark_ai_latency(num_runs=5):
    """Benchmark AI response time"""
    
    agent = AutonomousAgent(user_id="benchmark_user")
    latencies = []
    
    test_queries = [
        "What is 2+2?",
        "Explain Python in one sentence.",
        "List 3 programming languages.",
        "What is AI?",
        "Define function."
    ]
    
    print(f"🏃 Running {num_runs} AI queries...")
    
    for i, query in enumerate(test_queries[:num_runs], 1):
        start_time = time.time()
        
        try:
            response = agent.think(query, max_iterations=1)
            elapsed = time.time() - start_time
            latencies.append(elapsed)
            
            print(f"  Query {i}: {elapsed:.2f}s - {len(response)} chars")
        except Exception as e:
            print(f"  Query {i}: ❌ Failed - {e}")
    
    if latencies:
        print(f"\n📊 AI Latency Stats:")
        print(f"  Min:    {min(latencies):.2f}s")
        print(f"  Max:    {max(latencies):.2f}s")
        print(f"  Mean:   {statistics.mean(latencies):.2f}s")
        print(f"  Median: {statistics.median(latencies):.2f}s")
        
        if len(latencies) > 1:
            print(f"  StdDev: {statistics.stdev(latencies):.2f}s")
        
        return {
            "min": min(latencies),
            "max": max(latencies),
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "samples": len(latencies)
        }
    else:
        print("❌ No successful queries")
        return None

if __name__ == "__main__":
    print("🎯 Benchmarking AI Latency\n" + "="*50)
    results = benchmark_ai_latency()
    
    if results:
        print(f"\n✅ Benchmark complete: {results['samples']} samples")
        print(f"📈 Average response time: {results['mean']:.2f}s")
