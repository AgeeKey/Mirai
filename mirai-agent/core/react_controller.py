"""
ReAct Controller
Reason + Act pattern for autonomous tool selection and execution
"""

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class Step:
    """Single ReAct step"""
    step_num: int
    thought: str
    action: Optional[str]
    action_input: Optional[Dict]
    observation: Optional[str]
    timestamp: float


@dataclass
class Task:
    """Task to be executed"""
    id: str
    description: str
    goal: str
    max_steps: int = 10
    timeout: float = 600.0  # 10 minutes


class ReActController:
    """
    ReAct (Reason + Act) controller for autonomous task execution
    
    Flow:
    1. Thought: Reason about what to do next
    2. Action: Choose tool to use
    3. Observation: Get result from tool
    4. Repeat until task is complete
    
    Features:
    - Autonomous tool selection
    - Multi-step reasoning
    - Error recovery
    - Progress tracking
    """

    def __init__(
        self,
        llm_client: Any,
        tools: List[Dict],
        max_steps: int = 10,
        verbose: bool = True,
    ):
        """
        Initialize ReAct controller

        Args:
            llm_client: LLM client (OpenAI or Ollama)
            tools: List of available tools
            max_steps: Maximum steps per task
            verbose: Print progress
        """
        self.llm_client = llm_client
        self.tools = {tool["function"]["name"]: tool["function"] for tool in tools}
        self.tool_handlers = {}  # Map tool names to handler functions
        self.max_steps = max_steps
        self.verbose = verbose
        
        # Statistics
        self.stats = {
            "tasks_executed": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_steps": 0,
            "avg_steps_per_task": 0.0,
        }

    def register_tool_handler(self, tool_name: str, handler: Callable):
        """
        Register a handler function for a tool

        Args:
            tool_name: Name of the tool
            handler: Function to call when tool is used
        """
        self.tool_handlers[tool_name] = handler
        logger.info(f"🔧 Registered handler for tool: {tool_name}")

    def execute_task(self, task: Task) -> Tuple[bool, List[Step], Optional[str]]:
        """
        Execute a task using ReAct pattern

        Args:
            task: Task to execute

        Returns:
            Tuple of (success, steps, final_answer)
        """
        self.stats["tasks_executed"] += 1
        start_time = time.time()
        
        steps = []
        context = []
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🎯 Task: {task.description}")
            print(f"   Goal: {task.goal}")
            print(f"{'='*60}\n")
        
        # Build initial prompt
        system_prompt = self._build_system_prompt()
        context.append({
            "role": "system",
            "content": system_prompt
        })
        
        context.append({
            "role": "user",
            "content": f"Task: {task.description}\nGoal: {task.goal}"
        })
        
        for step_num in range(task.max_steps):
            if time.time() - start_time > task.timeout:
                logger.warning(f"Task timeout after {task.timeout}s")
                self.stats["tasks_failed"] += 1
                return False, steps, None
            
            # Step 1: Thought (Reasoning)
            thought = self._get_thought(context)
            
            if self.verbose:
                print(f"💭 Step {step_num + 1} - Thought:")
                print(f"   {thought}\n")
            
            # Check if task is complete
            if self._is_task_complete(thought):
                final_answer = self._extract_final_answer(thought)
                
                if self.verbose:
                    print(f"✅ Task completed!")
                    print(f"   Answer: {final_answer}\n")
                
                steps.append(Step(
                    step_num=step_num + 1,
                    thought=thought,
                    action=None,
                    action_input=None,
                    observation="Task completed",
                    timestamp=time.time(),
                ))
                
                self.stats["tasks_completed"] += 1
                self.stats["total_steps"] += len(steps)
                self.stats["avg_steps_per_task"] = (
                    self.stats["total_steps"] / self.stats["tasks_executed"]
                )
                
                return True, steps, final_answer
            
            # Step 2: Action (Tool selection)
            action, action_input = self._parse_action(thought)
            
            if not action:
                # No action parsed, ask for clarification
                context.append({
                    "role": "assistant",
                    "content": thought
                })
                context.append({
                    "role": "user",
                    "content": "Please specify an action to take using the format: Action: <tool_name> with input: <input>"
                })
                continue
            
            if self.verbose:
                print(f"🔧 Action: {action}")
                print(f"   Input: {action_input}\n")
            
            # Step 3: Observation (Execute tool)
            observation = self._execute_tool(action, action_input)
            
            if self.verbose:
                print(f"👁️ Observation:")
                print(f"   {observation[:200]}{'...' if len(observation) > 200 else ''}\n")
            
            # Record step
            step = Step(
                step_num=step_num + 1,
                thought=thought,
                action=action,
                action_input=action_input,
                observation=observation,
                timestamp=time.time(),
            )
            steps.append(step)
            
            # Update context
            context.append({
                "role": "assistant",
                "content": f"Thought: {thought}\nAction: {action}\nAction Input: {json.dumps(action_input)}"
            })
            context.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })
        
        # Max steps reached
        logger.warning(f"Max steps ({task.max_steps}) reached without completion")
        self.stats["tasks_failed"] += 1
        return False, steps, None

    def _build_system_prompt(self) -> str:
        """Build system prompt with available tools"""
        prompt = """You are an autonomous AI agent that can use tools to complete tasks.

Follow the ReAct (Reason + Act) pattern:
1. Think about what to do next
2. Choose a tool and provide input
3. Observe the result
4. Repeat until the task is complete

When you're done, respond with: "Final Answer: <your answer>"

Available tools:
"""
        
        for tool_name, tool_def in self.tools.items():
            desc = tool_def.get("description", "")
            params = tool_def.get("parameters", {}).get("properties", {})
            
            prompt += f"\n{tool_name}: {desc}\n"
            if params:
                prompt += "  Parameters:\n"
                for param_name, param_info in params.items():
                    param_type = param_info.get("type", "string")
                    param_desc = param_info.get("description", "")
                    prompt += f"    - {param_name} ({param_type}): {param_desc}\n"
        
        prompt += """
Format your responses as:
Thought: <your reasoning>
Action: <tool_name>
Action Input: <json input>

Or when done:
Thought: <final reasoning>
Final Answer: <answer>
"""
        
        return prompt

    def _get_thought(self, context: List[Dict]) -> str:
        """Get next thought from LLM"""
        try:
            # Check if using OpenAI or Ollama client
            if hasattr(self.llm_client, "chat"):
                if hasattr(self.llm_client.chat, "completions"):
                    # OpenAI client
                    response = self.llm_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=context,
                        temperature=0.3,
                        max_tokens=500,
                    )
                    return response.choices[0].message.content
                else:
                    # Ollama client
                    response = self.llm_client.chat(
                        messages=context,
                        temperature=0.3,
                        max_tokens=500,
                    )
                    return response["message"]["content"]
            else:
                return "Error: Invalid LLM client"
        except Exception as e:
            logger.error(f"Error getting thought: {e}")
            return f"Error: {e}"

    def _is_task_complete(self, thought: str) -> bool:
        """Check if task is complete"""
        return "Final Answer:" in thought or "Task completed" in thought

    def _extract_final_answer(self, thought: str) -> str:
        """Extract final answer from thought"""
        if "Final Answer:" in thought:
            return thought.split("Final Answer:")[1].strip()
        return thought

    def _parse_action(self, thought: str) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Parse action and input from thought

        Returns:
            Tuple of (action_name, action_input)
        """
        lines = thought.split("\n")
        
        action = None
        action_input = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith("Action:"):
                action = line.replace("Action:", "").strip()
            
            if line.startswith("Action Input:"):
                input_str = line.replace("Action Input:", "").strip()
                try:
                    action_input = json.loads(input_str)
                except json.JSONDecodeError:
                    # Try to extract from next line
                    if i + 1 < len(lines):
                        try:
                            action_input = json.loads(lines[i + 1].strip())
                        except:
                            pass
        
        return action, action_input if action_input else None

    def _execute_tool(self, tool_name: str, tool_input: Optional[Dict]) -> str:
        """
        Execute a tool

        Args:
            tool_name: Name of tool to execute
            tool_input: Input parameters

        Returns:
            Tool output as string
        """
        if tool_name not in self.tool_handlers:
            return f"Error: Tool '{tool_name}' not found or not registered"
        
        handler = self.tool_handlers[tool_name]
        
        try:
            if tool_input:
                result = handler(**tool_input)
            else:
                result = handler()
            
            return str(result)
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"Error executing {tool_name}: {e}"

    def get_stats(self) -> Dict:
        """Get controller statistics"""
        return {
            **self.stats,
            "success_rate": (
                (self.stats["tasks_completed"] / self.stats["tasks_executed"] * 100)
                if self.stats["tasks_executed"] > 0
                else 0.0
            ),
        }


if __name__ == "__main__":
    # Test ReAct controller
    print("🧪 Testing ReAct Controller...")
    
    # Mock LLM client
    class MockLLM:
        def __init__(self):
            self.call_count = 0
        
        def chat(self, messages, **kwargs):
            self.call_count += 1
            
            if self.call_count == 1:
                return {
                    "message": {
                        "content": """Thought: I need to add two numbers.
Action: add_numbers
Action Input: {"a": 5, "b": 3}"""
                    }
                }
            else:
                return {
                    "message": {
                        "content": """Thought: The numbers have been added successfully.
Final Answer: The sum of 5 and 3 is 8."""
                    }
                }
    
    # Define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_numbers",
                "description": "Add two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                    "required": ["a", "b"],
                },
            },
        },
    ]
    
    # Create controller
    llm = MockLLM()
    controller = ReActController(llm, tools, verbose=True)
    
    # Register tool handler
    def add_numbers(a: float, b: float) -> float:
        return a + b
    
    controller.register_tool_handler("add_numbers", add_numbers)
    
    # Execute task
    task = Task(
        id="test_1",
        description="Add 5 and 3",
        goal="Calculate the sum",
        max_steps=5,
    )
    
    success, steps, answer = controller.execute_task(task)
    
    print(f"\n✅ Task {'succeeded' if success else 'failed'}")
    print(f"   Steps taken: {len(steps)}")
    print(f"   Final answer: {answer}")
    print(f"\n📊 Stats: {controller.get_stats()}")
