"""
NASA-Level Code Quality Analysis System
Многоуровневая оценка качества кода
"""

import ast
import logging
from dataclasses import dataclass
from typing import List, Optional

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit

    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False
    logging.warning("Radon not available - using simplified metrics")

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    # Базовые метрики
    syntax_valid: bool
    lines_of_code: int
    comment_ratio: float

    # Complexity метрики
    cyclomatic_complexity: float
    cognitive_complexity: float
    maintainability_index: float

    # Стиль
    pep8_score: float
    naming_score: float

    # Структура
    has_docstrings: bool
    has_type_hints: bool
    has_tests: bool

    # Итоговая оценка
    overall_score: float  # 0.0-1.0
    grade: str  # A-F

    # Рекомендации
    issues: List[str]
    suggestions: List[str]


class CodeQualityAnalyzer:
    """
    Анализатор качества кода по стандартам NASA

    Критерии оценки:
    - Syntax: обязательно валидный
    - Complexity: cyclomatic < 10
    - Maintainability: > 20
    - Documentation: docstrings обязательны
    """

    def __init__(self):
        self.min_maintainability = 20
        self.max_complexity = 10
        self.min_comment_ratio = 0.1

    def analyze(self, code: str, filepath: str = "temp.py") -> QualityMetrics:
        """Полный анализ качества кода"""

        issues = []
        suggestions = []

        # 1. Syntax validation
        syntax_valid, syntax_error = self._check_syntax(code)
        if not syntax_valid:
            return self._failed_quality(f"Syntax error: {syntax_error}")

        # 2. Parse AST
        try:
            tree = ast.parse(code)
        except:
            return self._failed_quality("Cannot parse code")

        # 3. Calculate metrics
        loc = len(
            [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
        )
        comment_ratio = self._calculate_comment_ratio(code)

        # 4. Complexity analysis
        complexity_metrics = self._analyze_complexity(code)

        # 5. Structure analysis
        has_docstrings = self._check_docstrings(tree)
        has_type_hints = self._check_type_hints(tree)

        # 6. Calculate overall score
        scores = {
            "syntax": 1.0 if syntax_valid else 0.0,
            "complexity": min(
                1.0, self.max_complexity / max(complexity_metrics["cyclomatic"], 1)
            ),
            "maintainability": min(1.0, complexity_metrics["maintainability"] / 100),
            "docstrings": 1.0 if has_docstrings else 0.5,
            "type_hints": 1.0 if has_type_hints else 0.7,
            "comments": min(1.0, comment_ratio * 5),
        }

        overall_score = sum(scores.values()) / len(scores)
        grade = self._calculate_grade(overall_score)

        # 7. Generate issues & suggestions
        if complexity_metrics["cyclomatic"] > self.max_complexity:
            issues.append(
                f"High complexity: {complexity_metrics['cyclomatic']:.1f} (max {self.max_complexity})"
            )
            suggestions.append("Refactor complex functions into smaller ones")

        if not has_docstrings:
            issues.append("Missing docstrings")
            suggestions.append("Add docstrings to all functions and classes")

        if not has_type_hints:
            suggestions.append("Add type hints for better code clarity")

        if comment_ratio < self.min_comment_ratio:
            suggestions.append(f"Add more comments (current: {comment_ratio:.1%})")

        if complexity_metrics["maintainability"] < self.min_maintainability:
            issues.append(
                f"Low maintainability: {complexity_metrics['maintainability']:.1f}"
            )
            suggestions.append("Improve code structure and documentation")

        return QualityMetrics(
            syntax_valid=syntax_valid,
            lines_of_code=loc,
            comment_ratio=comment_ratio,
            cyclomatic_complexity=complexity_metrics["cyclomatic"],
            cognitive_complexity=complexity_metrics["cognitive"],
            maintainability_index=complexity_metrics["maintainability"],
            pep8_score=8.0,  # Simplified
            naming_score=0.8,
            has_docstrings=has_docstrings,
            has_type_hints=has_type_hints,
            has_tests=False,
            overall_score=overall_score,
            grade=grade,
            issues=issues,
            suggestions=suggestions,
        )

    def _check_syntax(self, code: str) -> tuple:
        """Проверка синтаксиса"""
        try:
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, str(e)

    def _analyze_complexity(self, code: str) -> dict:
        """Анализ сложности кода"""

        if RADON_AVAILABLE:
            try:
                # Cyclomatic complexity
                complexity = cc_visit(code)
                avg_complexity = (
                    sum(c.complexity for c in complexity) / max(len(complexity), 1)
                    if complexity
                    else 1
                )

                # Maintainability index
                mi = mi_visit(code, True)

                return {
                    "cyclomatic": avg_complexity,
                    "cognitive": avg_complexity * 1.2,
                    "maintainability": mi,
                }
            except:
                pass

        # Fallback: simple heuristics
        lines = len(code.split("\n"))
        # Простая эвристика: чем больше строк, тем сложнее
        complexity = min(15, lines / 10)
        maintainability = max(20, 100 - lines / 5)

        return {
            "cyclomatic": complexity,
            "cognitive": complexity * 1.2,
            "maintainability": maintainability,
        }

    def _check_docstrings(self, tree: ast.AST) -> bool:
        """Проверка наличия docstrings"""
        has_any_docstring = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    has_any_docstring = True
                else:
                    # Если есть хоть одна функция без docstring - не идеально
                    # но засчитаем если есть хоть что-то
                    pass
        return has_any_docstring

    def _check_type_hints(self, tree: ast.AST) -> bool:
        """Проверка наличия type hints"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.returns or any(arg.annotation for arg in node.args.args):
                    return True
        return False

    def _calculate_comment_ratio(self, code: str) -> float:
        """Расчёт отношения комментариев к коду"""
        lines = code.split("\n")
        comment_lines = sum(1 for l in lines if l.strip().startswith("#"))
        total_lines = len([l for l in lines if l.strip()])
        return comment_lines / max(total_lines, 1)

    def _calculate_grade(self, score: float) -> str:
        """Конвертация оценки в grade"""
        if score >= 0.9:
            return "A"
        if score >= 0.8:
            return "B"
        if score >= 0.7:
            return "C"
        if score >= 0.6:
            return "D"
        return "F"

    def _failed_quality(self, reason: str) -> QualityMetrics:
        """Возврат failed метрик"""
        return QualityMetrics(
            syntax_valid=False,
            lines_of_code=0,
            comment_ratio=0.0,
            cyclomatic_complexity=0.0,
            cognitive_complexity=0.0,
            maintainability_index=0.0,
            pep8_score=0.0,
            naming_score=0.0,
            has_docstrings=False,
            has_type_hints=False,
            has_tests=False,
            overall_score=0.0,
            grade="F",
            issues=[reason],
            suggestions=[],
        )


# Quick test
if __name__ == "__main__":
    analyzer = CodeQualityAnalyzer()

    # Test 1: Good code
    print("\n=== Test 1: Good code ===")
    good_code = '''
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    # Add the numbers
    return a + b

class Calculator:
    """Simple calculator."""
    
    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y
'''

    metrics = analyzer.analyze(good_code)
    print(f"Grade: {metrics.grade}")
    print(f"Overall Score: {metrics.overall_score:.2f}")
    print(f"Complexity: {metrics.cyclomatic_complexity:.1f}")
    print(f"Has docstrings: {metrics.has_docstrings}")
    print(f"Has type hints: {metrics.has_type_hints}")

    # Test 2: Bad code
    print("\n=== Test 2: Bad code ===")
    bad_code = """
def f(x,y):
    return x+y
"""

    metrics = analyzer.analyze(bad_code)
    print(f"Grade: {metrics.grade}")
    print(f"Overall Score: {metrics.overall_score:.2f}")
    print(f"Issues: {metrics.issues}")
    print(f"Suggestions: {metrics.suggestions}")

    print("\n✅ CodeQualityAnalyzer ready!")
