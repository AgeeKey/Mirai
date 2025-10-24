#!/usr/bin/env python3
"""
Vision System Validation Script
Validates code structure and completeness without requiring all dependencies.
"""

import ast
import sys
from pathlib import Path


def validate_python_file(filepath: str) -> tuple[bool, list[str]]:
    """
    Validate Python file syntax and structure.
    
    Returns:
        Tuple of (is_valid, list of issues)
    """
    issues = []
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content, filename=filepath)
        
        # Count classes and functions
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        print(f"✅ {filepath}:")
        print(f"   • Classes: {len(classes)}")
        print(f"   • Functions: {len(functions)}")
        print(f"   • Lines: {len(content.splitlines())}")
        
        # Check for docstrings
        if tree.body and isinstance(tree.body[0], ast.Expr):
            if isinstance(tree.body[0].value, ast.Constant):
                print(f"   • Module docstring: ✅")
            else:
                issues.append("Missing module docstring")
        
        # Check main classes exist (for vision_complete.py)
        if "vision_complete" in filepath:
            expected_classes = [
                'VisionConfig', 'VisionLogger', 'VisionCache', 'VisionDatabase',
                'VisionInitializer', 'ScreenCaptureManager', 'GPT4VisionAnalyzer',
                'ScreenAnalyzer', 'ElementDetector', 'ProblemDetector', 'VisionOrchestrator'
            ]
            
            class_names = [cls.name for cls in classes]
            
            for expected in expected_classes:
                if expected in class_names:
                    print(f"   • {expected}: ✅")
                else:
                    issues.append(f"Missing class: {expected}")
        
        return len(issues) == 0, issues
    
    except SyntaxError as e:
        return False, [f"Syntax error: {e}"]
    except Exception as e:
        return False, [f"Error: {e}"]


def validate_documentation(filepath: str) -> tuple[bool, list[str]]:
    """Validate markdown documentation."""
    issues = []
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        print(f"✅ {filepath}:")
        print(f"   • Size: {len(content)} bytes")
        print(f"   • Lines: {len(content.splitlines())}")
        
        # Check for key sections
        required_sections = [
            '# PHASE 1',
            'Installation',
            'Quick Start',
            'Examples'
        ]
        
        for section in required_sections:
            if section in content:
                print(f"   • Section '{section}': ✅")
            else:
                issues.append(f"Missing section: {section}")
        
        return len(issues) == 0, issues
    
    except Exception as e:
        return False, [f"Error: {e}"]


def main():
    """Main validation routine."""
    print("=" * 70)
    print("🔍 PHASE 1 VISION SYSTEM VALIDATION")
    print("=" * 70)
    print()
    
    base_dir = Path(__file__).parent
    
    files_to_validate = [
        ('vision_complete.py', validate_python_file),
        ('vision_tests.py', validate_python_file),
        ('README_PHASE_1.md', validate_documentation),
        ('PHASE_1_VISION_SYSTEM_DETAILED.md', validate_documentation),
    ]
    
    all_valid = True
    
    for filename, validator in files_to_validate:
        filepath = base_dir / filename
        
        if not filepath.exists():
            print(f"❌ {filename}: FILE NOT FOUND")
            all_valid = False
            continue
        
        is_valid, issues = validator(str(filepath))
        
        if not is_valid:
            print(f"❌ {filename}: VALIDATION FAILED")
            for issue in issues:
                print(f"   • {issue}")
            all_valid = False
        
        print()
    
    # Summary
    print("=" * 70)
    if all_valid:
        print("✅ ALL VALIDATIONS PASSED")
        print("=" * 70)
        print()
        print("📦 Required Dependencies:")
        print("   pip install openai pillow pyautogui opencv-python numpy")
        print()
        print("🧪 Run Tests:")
        print("   python vision_tests.py")
        print()
        print("🚀 Run System:")
        print("   python vision_complete.py")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
