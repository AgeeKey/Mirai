"""
Integration test for memory persistence
Tests that memory survives agent restarts
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.memory_manager import MemoryManager
from core.autonomous_agent import AutonomousAgent

def test_memory_persistence():
    """Test that memory persists across agent instances"""
    
    # Create first agent and session
    user_id = "persistence_test_user"
    agent1 = AutonomousAgent(user_id=user_id)
    session1_id = agent1.session_id
    
    print(f"✅ Created agent 1 with session: {session1_id}")
    
    # Send a message
    test_message = "Remember this: the answer is 42"
    agent1.think(test_message, max_iterations=1)
    
    print(f"✅ Sent message through agent 1")
    
    # Delete first agent
    del agent1
    
    # Create new agent with same user_id
    agent2 = AutonomousAgent(user_id=user_id)
    session2_id = agent2.session_id
    
    print(f"✅ Created agent 2 with session: {session2_id}")
    
    # Check database for messages from first session
    memory = MemoryManager()
    messages = memory.get_recent_messages(session1_id, limit=100)
    
    print(f"✅ Retrieved {len(messages)} messages from session 1")
    
    # Verify message was stored
    found_message = False
    for msg in messages:
        if test_message in msg.content:
            found_message = True
            break
    
    assert found_message, "Test message not found in database!"
    print(f"✅ Message persisted in database")
    
    # Check stats
    stats = memory.get_stats()
    print(f"✅ Database stats: {stats['total_sessions']} sessions, {stats['total_messages']} messages")
    
    assert stats['total_sessions'] >= 2, "Should have at least 2 sessions"
    assert stats['total_messages'] >= 2, "Should have at least 2 messages"

if __name__ == "__main__":
    print("🧪 Testing Memory Persistence...")
    test_memory_persistence()
    print("🎉 Memory persistence test passed!")
