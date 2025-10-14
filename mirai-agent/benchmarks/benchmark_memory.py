"""
Benchmark Memory (Database) Performance
Measures speed of database operations
"""
import sys
import time
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.memory_manager import MemoryManager
from core.memory_manager import Message

def benchmark_write_performance(num_writes=100):
    """Benchmark database write speed"""
    
    memory = MemoryManager()
    session = memory.create_session("benchmark_user")
    
    write_times = []
    
    print(f"🏃 Writing {num_writes} messages...")
    
    for i in range(num_writes):
        start_time = time.time()
        
        message = Message(
            role="user",
            content=f"Benchmark message {i}",
            tokens=10
        )
        
        memory.add_message(session.id, message)
        
        elapsed = time.time() - start_time
        write_times.append(elapsed)
    
    print(f"\n📊 Write Performance:")
    print(f"  Total:  {sum(write_times):.3f}s")
    print(f"  Mean:   {statistics.mean(write_times)*1000:.2f}ms")
    print(f"  Median: {statistics.median(write_times)*1000:.2f}ms")
    print(f"  Min:    {min(write_times)*1000:.2f}ms")
    print(f"  Max:    {max(write_times)*1000:.2f}ms")
    
    if len(write_times) > 1:
        print(f"  StdDev: {statistics.stdev(write_times)*1000:.2f}ms")
    
    throughput = num_writes / sum(write_times)
    print(f"  Throughput: {throughput:.1f} writes/sec")
    
    return {
        "total_time": sum(write_times),
        "mean_ms": statistics.mean(write_times) * 1000,
        "median_ms": statistics.median(write_times) * 1000,
        "throughput": throughput,
        "samples": num_writes
    }

def benchmark_read_performance(num_reads=100):
    """Benchmark database read speed"""
    
    memory = MemoryManager()
    
    # Get a session with messages
    stats = memory.get_stats()
    if stats['total_sessions'] == 0:
        print("⚠️ No sessions in database, skipping read benchmark")
        return None
    
    # Get all sessions
    from core.memory_manager import Session
    with memory._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM sessions LIMIT 1")
        row = cursor.fetchone()
        if not row:
            print("⚠️ No sessions found")
            return None
        session_id = row[0]
    
    read_times = []
    
    print(f"\n🏃 Reading messages {num_reads} times...")
    
    for i in range(num_reads):
        start_time = time.time()
        messages = memory.get_session_messages(session_id)
        elapsed = time.time() - start_time
        read_times.append(elapsed)
    
    print(f"\n📊 Read Performance:")
    print(f"  Total:  {sum(read_times):.3f}s")
    print(f"  Mean:   {statistics.mean(read_times)*1000:.2f}ms")
    print(f"  Median: {statistics.median(read_times)*1000:.2f}ms")
    print(f"  Min:    {min(read_times)*1000:.2f}ms")
    print(f"  Max:    {max(read_times)*1000:.2f}ms")
    
    if len(read_times) > 1:
        print(f"  StdDev: {statistics.stdev(read_times)*1000:.2f}ms")
    
    throughput = num_reads / sum(read_times)
    print(f"  Throughput: {throughput:.1f} reads/sec")
    
    return {
        "total_time": sum(read_times),
        "mean_ms": statistics.mean(read_times) * 1000,
        "median_ms": statistics.median(read_times) * 1000,
        "throughput": throughput,
        "samples": num_reads
    }

if __name__ == "__main__":
    print("🎯 Benchmarking Memory Performance\n" + "="*50)
    
    write_results = benchmark_write_performance(100)
    read_results = benchmark_read_performance(100)
    
    print(f"\n✅ Benchmark complete!")
    print(f"📈 Write throughput: {write_results['throughput']:.1f} writes/sec")
    if read_results:
        print(f"📈 Read throughput: {read_results['throughput']:.1f} reads/sec")
