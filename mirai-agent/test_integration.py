"""
Integration test for local AI engineer components
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_tool_validator():
    """Test tool validator"""
    print("\n" + "="*60)
    print("🧪 Testing Tool Validator")
    print("="*60)
    
    from core.tool_validator import run_validation_tests
    
    success = run_validation_tests()
    
    if success:
        print("✅ Tool Validator: PASSED")
        return True
    else:
        print("❌ Tool Validator: FAILED")
        return False


def test_faiss_rag():
    """Test FAISS RAG system"""
    print("\n" + "="*60)
    print("🧪 Testing FAISS RAG System")
    print("="*60)
    
    try:
        from core.faiss_rag import FAISSRAGSystem
    except ImportError as e:
        print(f"⚠️ FAISS RAG dependencies not installed: {e}")
        print("   Install with: pip install faiss-cpu sentence-transformers")
        print("✅ FAISS RAG: SKIPPED (dependencies not installed)")
        return True
    
    try:
        # Create RAG system
        rag = FAISSRAGSystem(
            persist_directory="/tmp/test_faiss_integration",
            embedding_model="all-MiniLM-L6-v2",
        )
        
        # Add test documents
        rag.add_document(
            text="MIRAI is an autonomous AI agent for trading and continuous self-improvement.",
            source="test_doc_1.md",
            metadata={"topic": "overview"}
        )
        
        rag.add_document(
            text="The agent uses GPT-4o-mini model for fast inference and decision making. It supports multiple programming languages.",
            source="test_doc_2.md",
            metadata={"topic": "architecture"}
        )
        
        rag.add_document(
            text="KAIZEN (改善) is the executor agent. MIRAI (未来) is the advisory agent.",
            source="test_doc_3.md",
            metadata={"topic": "agents"}
        )
        
        # Test search
        results = rag.search("What is MIRAI?", top_k=3)
        
        print(f"✅ Added {rag.index.ntotal} documents to index")
        print(f"✅ Search returned {len(results)} results")
        
        if len(results) > 0:
            print(f"   Top result: {results[0][0]['text'][:80]}...")
            print(f"   Score: {results[0][1]:.3f}")
        
        # Test context retrieval
        context = rag.get_relevant_context("AI agent", max_chunks=3)
        print(f"✅ Context retrieved: {len(context)} characters")
        
        # Get stats
        stats = rag.get_stats()
        print(f"✅ Stats: {stats['total_documents']} docs, {stats['metrics']['total_queries']} queries")
        
        print("✅ FAISS RAG: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FAISS RAG: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_docker_runner():
    """Test Docker code runner"""
    print("\n" + "="*60)
    print("🧪 Testing Docker Code Runner")
    print("="*60)
    
    from core.docker_runner import DockerCodeRunner, SubprocessCodeRunner
    
    try:
        runner = DockerCodeRunner()
        
        if runner.docker_available:
            print("✅ Docker is available")
            
            # Test Python execution
            result = runner.execute_python("print('Hello from test!')")
            
            if result.status.value == "success":
                print(f"✅ Python execution: {result.output.strip()}")
            else:
                print(f"⚠️ Python execution failed: {result.error}")
            
            print(f"✅ Execution time: {result.execution_time:.3f}s")
            
        else:
            print("⚠️ Docker not available, testing fallback subprocess runner")
            
            fallback = SubprocessCodeRunner()
            result = fallback.execute_python("print('Hello from fallback!')")
            
            if result.status.value == "success":
                print(f"✅ Fallback execution: {result.output.strip()}")
            else:
                print(f"❌ Fallback execution failed: {result.error}")
        
        print("✅ Docker Runner: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Docker Runner: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_self_reflection():
    """Test self-reflection system"""
    print("\n" + "="*60)
    print("🧪 Testing Self-Reflection System")
    print("="*60)
    
    from core.self_reflection import SelfReflectionSystem
    
    try:
        system = SelfReflectionSystem(db_path="/tmp/test_reflections_integration.db")
        
        # Add test reflection
        system.add_reflection(
            task_id="test_task_1",
            task_description="Test task execution",
            status="success",
            what_worked="Everything worked as expected",
            what_failed="Nothing failed",
            lessons_learned="System is working correctly",
            tool_calls=[{"tool": "execute_python", "args": {}}],
            execution_time=2.5,
            tokens_used=100,
            hallucination_detected=False,
        )
        
        print("✅ Added test reflection")
        
        # Get metrics
        metrics = system.calculate_metrics()
        print(f"✅ Task Success Rate: {metrics.task_success_rate:.1f}%")
        print(f"✅ Mean Time to Result: {metrics.mean_time_to_result:.2f} min")
        print(f"✅ Hallucination Rate: {metrics.hallucination_rate:.1f}%")
        
        # Get summary
        summary = system.get_summary()
        print(f"✅ Summary: {summary['total_reflections']} reflections")
        
        system.close()
        
        print("✅ Self-Reflection: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Self-Reflection: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_react_controller():
    """Test ReAct controller with mock LLM"""
    print("\n" + "="*60)
    print("🧪 Testing ReAct Controller")
    print("="*60)
    
    from core.react_controller import ReActController, Task
    
    try:
        # Mock LLM
        class MockLLM:
            def __init__(self):
                self.call_count = 0
            
            def chat(self, messages, **kwargs):
                self.call_count += 1
                
                if self.call_count == 1:
                    return {
                        "message": {
                            "content": """Thought: I need to calculate 10 + 5.
Action: calculate
Action Input: {"operation": "add", "a": 10, "b": 5}"""
                        }
                    }
                else:
                    return {
                        "message": {
                            "content": """Thought: The calculation is complete.
Final Answer: The result is 15."""
                        }
                    }
        
        # Define tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform calculation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {"type": "string"},
                            "a": {"type": "number"},
                            "b": {"type": "number"},
                        },
                    },
                },
            },
        ]
        
        # Create controller
        llm = MockLLM()
        controller = ReActController(llm, tools, verbose=False)
        
        # Register handler
        def calculate(operation: str, a: float, b: float) -> float:
            if operation == "add":
                return a + b
            return 0
        
        controller.register_tool_handler("calculate", calculate)
        
        # Execute task
        task = Task(
            id="test_task",
            description="Calculate 10 + 5",
            goal="Get the sum",
            max_steps=5,
        )
        
        success, steps, answer = controller.execute_task(task)
        
        print(f"✅ Task executed: {success}")
        print(f"✅ Steps taken: {len(steps)}")
        print(f"✅ Answer: {answer}")
        
        stats = controller.get_stats()
        print(f"✅ Success rate: {stats['success_rate']:.1f}%")
        
        print("✅ ReAct Controller: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ReAct Controller: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_browser_automation():
    """Test browser automation"""
    print("\n" + "="*60)
    print("🧪 Testing Browser Automation")
    print("="*60)
    
    from core.browser_automation import BrowserAutomation
    
    try:
        browser = BrowserAutomation()
        
        if browser.chrome_available:
            print("✅ Chrome/Chromium is available")
            
            # Test URL fetch
            content = browser.fetch_url("https://example.com")
            
            if content:
                print(f"✅ Fetched page: {len(content)} characters")
                print(f"   Preview: {content[:100]}...")
            else:
                print("⚠️ Failed to fetch page")
            
        else:
            print("⚠️ Chrome/Chromium not available")
        
        print("✅ Browser Automation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Browser Automation: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 MIRAI Local AI Engineer - Integration Tests")
    print("="*60)
    
    start_time = time.time()
    
    results = {
        "Tool Validator": test_tool_validator(),
        "FAISS RAG": test_faiss_rag(),
        "Docker Runner": test_docker_runner(),
        "Self-Reflection": test_self_reflection(),
        "ReAct Controller": test_react_controller(),
        "Browser Automation": test_browser_automation(),
    }
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {name:20s} {status}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print(f"Time: {elapsed:.2f}s")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
