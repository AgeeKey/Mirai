"""
Tool Call Validator
Validates JSON tool calls from LLM responses
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ToolValidator:
    """Validates tool calls against defined schemas"""

    def __init__(self, tools: List[Dict]):
        """
        Initialize validator with tool definitions

        Args:
            tools: List of tool definitions (OpenAI format)
        """
        self.tools = {tool["function"]["name"]: tool["function"] for tool in tools}
        self.validation_stats = {
            "total_calls": 0,
            "valid_calls": 0,
            "invalid_calls": 0,
            "errors": [],
        }

    def validate_tool_call(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a single tool call

        Args:
            tool_name: Name of the tool being called
            arguments: Arguments passed to the tool

        Returns:
            Tuple of (is_valid, error_message)
        """
        self.validation_stats["total_calls"] += 1

        # Check if tool exists
        if tool_name not in self.tools:
            error = f"Unknown tool: {tool_name}"
            self.validation_stats["invalid_calls"] += 1
            self.validation_stats["errors"].append(error)
            logger.warning(error)
            return False, error

        tool_def = self.tools[tool_name]
        params_schema = tool_def.get("parameters", {})
        required_params = params_schema.get("required", [])
        properties = params_schema.get("properties", {})

        # Check required parameters
        for param in required_params:
            if param not in arguments:
                error = f"Missing required parameter: {param}"
                self.validation_stats["invalid_calls"] += 1
                self.validation_stats["errors"].append(error)
                logger.warning(f"Tool {tool_name}: {error}")
                return False, error

        # Validate parameter types
        for param_name, param_value in arguments.items():
            if param_name not in properties:
                logger.warning(
                    f"Tool {tool_name}: Unexpected parameter: {param_name}"
                )
                continue

            param_schema = properties[param_name]
            expected_type = param_schema.get("type")

            if not self._validate_type(param_value, expected_type):
                error = (
                    f"Parameter {param_name} type mismatch: "
                    f"expected {expected_type}, got {type(param_value).__name__}"
                )
                self.validation_stats["invalid_calls"] += 1
                self.validation_stats["errors"].append(error)
                logger.warning(f"Tool {tool_name}: {error}")
                return False, error

        self.validation_stats["valid_calls"] += 1
        return True, None

    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value matches expected JSON schema type"""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            return True  # Unknown type, accept it

        return isinstance(value, expected_python_type)

    def validate_tool_calls_batch(
        self, tool_calls: List[Dict]
    ) -> Tuple[bool, List[str]]:
        """
        Validate multiple tool calls

        Args:
            tool_calls: List of tool call dicts

        Returns:
            Tuple of (all_valid, error_messages)
        """
        errors = []
        all_valid = True

        for tool_call in tool_calls:
            try:
                func = tool_call.get("function", {})
                tool_name = func.get("name")
                arguments_str = func.get("arguments", "{}")

                # Parse arguments if string
                if isinstance(arguments_str, str):
                    arguments = json.loads(arguments_str)
                else:
                    arguments = arguments_str

                is_valid, error = self.validate_tool_call(tool_name, arguments)
                if not is_valid:
                    all_valid = False
                    errors.append(error)

            except json.JSONDecodeError as e:
                error = f"Invalid JSON in arguments: {e}"
                errors.append(error)
                all_valid = False
                self.validation_stats["invalid_calls"] += 1

            except Exception as e:
                error = f"Validation error: {e}"
                errors.append(error)
                all_valid = False
                self.validation_stats["invalid_calls"] += 1

        return all_valid, errors

    def get_accuracy(self) -> float:
        """
        Get tool-use accuracy percentage

        Returns:
            Accuracy as percentage (0.0 - 100.0)
        """
        total = self.validation_stats["total_calls"]
        if total == 0:
            return 100.0

        valid = self.validation_stats["valid_calls"]
        return (valid / total) * 100.0

    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            **self.validation_stats,
            "accuracy": self.get_accuracy(),
        }

    def reset_stats(self):
        """Reset validation statistics"""
        self.validation_stats = {
            "total_calls": 0,
            "valid_calls": 0,
            "invalid_calls": 0,
            "errors": [],
        }


def create_test_validator() -> ToolValidator:
    """Create a validator with test tools for validation"""
    test_tools = [
        {
            "type": "function",
            "function": {
                "name": "execute_python",
                "description": "Execute Python code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read file contents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to file",
                        }
                    },
                    "required": ["filepath"],
                },
            },
        },
    ]

    return ToolValidator(test_tools)


# Validation test cases
def run_validation_tests() -> bool:
    """Run validation test suite"""
    validator = create_test_validator()

    test_cases = [
        # Valid calls
        (
            "execute_python",
            {"code": "print('hello')"},
            True,
            "Valid execute_python call",
        ),
        ("read_file", {"filepath": "/tmp/test.txt"}, True, "Valid read_file call"),
        # Invalid calls
        ("execute_python", {}, False, "Missing required parameter"),
        ("unknown_tool", {"param": "value"}, False, "Unknown tool"),
        (
            "read_file",
            {"code": "wrong param"},
            False,
            "Missing required parameter",
        ),
    ]

    passed = 0
    failed = 0

    print("\n🧪 Running Tool Validator Tests...")
    print("=" * 50)

    for tool_name, arguments, expected_valid, description in test_cases:
        is_valid, error = validator.validate_tool_call(tool_name, arguments)

        if is_valid == expected_valid:
            print(f"✅ PASS: {description}")
            passed += 1
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Expected: {expected_valid}, Got: {is_valid}")
            if error:
                print(f"   Error: {error}")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Validation Accuracy: {validator.get_accuracy():.1f}%")
    print()

    return failed == 0


if __name__ == "__main__":
    success = run_validation_tests()
    exit(0 if success else 1)
