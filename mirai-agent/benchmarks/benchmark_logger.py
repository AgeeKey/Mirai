"""
Benchmark Logger Performance
Measures logging throughput and latency
"""
import sys
import time
import statistics
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logger import setup_logger

def benchmark_logging(num_logs=1000):
    """Benchmark logging performance"""
    
    # Create temporary log file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        log_path = f.name
    
    logger = setup_logger("benchmark_logger", log_path=log_path, console_output=False)
    
    log_times = []
    
    print(f"🏃 Writing {num_logs} log entries...")
    
    start_total = time.time()
    
    for i in range(num_logs):
        start_time = time.time()
        logger.info(f"Benchmark log message {i}", extra={"benchmark_id": i})
        elapsed = time.time() - start_time
        log_times.append(elapsed)
    
    total_time = time.time() - start_total
    
    print(f"\n📊 Logging Performance:")
    print(f"  Total:  {total_time:.3f}s")
    print(f"  Mean:   {statistics.mean(log_times)*1000:.3f}ms")
    print(f"  Median: {statistics.median(log_times)*1000:.3f}ms")
    print(f"  Min:    {min(log_times)*1000:.3f}ms")
    print(f"  Max:    {max(log_times)*1000:.3f}ms")
    
    if len(log_times) > 1:
        print(f"  StdDev: {statistics.stdev(log_times)*1000:.3f}ms")
    
    throughput = num_logs / total_time
    print(f"  Throughput: {throughput:.1f} logs/sec")
    
    # Check file size
    file_size = Path(log_path).stat().st_size
    print(f"  File size: {file_size / 1024:.1f} KB")
    print(f"  Avg size: {file_size / num_logs:.1f} bytes/log")
    
    # Cleanup
    Path(log_path).unlink()
    
    return {
        "total_time": total_time,
        "mean_ms": statistics.mean(log_times) * 1000,
        "median_ms": statistics.median(log_times) * 1000,
        "throughput": throughput,
        "file_size_kb": file_size / 1024,
        "samples": num_logs
    }

if __name__ == "__main__":
    print("🎯 Benchmarking Logger Performance\n" + "="*50)
    results = benchmark_logging(1000)
    
    print(f"\n✅ Benchmark complete!")
    print(f"📈 Logging throughput: {results['throughput']:.1f} logs/sec")
    print(f"📁 Average log size: {results['file_size_kb']*1024/results['samples']:.1f} bytes")
