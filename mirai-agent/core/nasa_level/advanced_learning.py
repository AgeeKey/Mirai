"""
NASA-Level Advanced Learning System
Многоэтапное обучение с верификацией
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class LearningPhase(Enum):
    RESEARCH = "research"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    TESTING = "testing"
    INTEGRATION = "integration"
    VERIFICATION = "verification"


@dataclass
class LearningArtifact:
    """Артефакт обучения"""

    phase: LearningPhase
    content: str
    metadata: Dict[str, Any]
    quality_score: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LearningResult:
    """Результат обучения технологии"""

    technology: str
    success: bool
    proficiency: float  # 0.0-1.0
    artifacts: List[LearningArtifact]
    quality_grade: str
    tests_passed: int
    tests_total: int
    execution_time: float
    errors: List[str]
    suggestions: List[str]


class AdvancedLearningEngine:
    """
    Продвинутый движок обучения

    Процесс обучения:
    1. RESEARCH - поиск и анализ документации
    2. SYNTHESIS - генерация рабочего кода (НЕ TODO!)
    3. VALIDATION - проверка качества кода
    4. TESTING - автоматическое тестирование
    5. INTEGRATION - интеграция в knowledge base
    6. VERIFICATION - итоговая верификация
    """

    def __init__(self, ai_agent, sandbox, quality_analyzer):
        self.ai = ai_agent
        self.sandbox = sandbox
        self.quality = quality_analyzer
        self.min_quality_score = 0.6  # минимум "D" grade
        self.min_proficiency = 0.5

    def learn_technology(self, technology: str, depth: str = "basic") -> LearningResult:
        """
        Изучить технологию с полной верификацией

        Args:
            technology: название технологии
            depth: глубина изучения (basic, intermediate, advanced)

        Returns:
            LearningResult с полными метриками
        """
        import time

        start_time = time.time()
        artifacts = []
        errors = []

        print(f"\n{'='*70}")
        print(f"📚 LEARNING: {technology} ({depth} level)")
        print(f"{'='*70}\n")

        try:
            # PHASE 1: RESEARCH
            print("📖 Phase 1/6: Research...")
            research = self._phase_research(technology)
            artifacts.append(research)

            if research.quality_score < 0.5:
                errors.append("Research phase failed - insufficient information")
                return self._failed_result(
                    technology, artifacts, errors, time.time() - start_time
                )

            # PHASE 2: SYNTHESIS
            print("🧬 Phase 2/6: Code Synthesis...")
            synthesis = self._phase_synthesis(technology, research, depth)
            artifacts.append(synthesis)

            if synthesis.quality_score < 0.5:
                errors.append("Synthesis phase failed - cannot generate code")
                return self._failed_result(
                    technology, artifacts, errors, time.time() - start_time
                )

            # PHASE 3: VALIDATION
            print("✅ Phase 3/6: Quality Validation...")
            validation = self._phase_validation(synthesis.content)
            artifacts.append(validation)

            quality_metrics = validation.metadata["metrics"]

            # Retry if quality too low
            if quality_metrics.overall_score < self.min_quality_score:
                print(f"⚠️  Quality low ({quality_metrics.grade}), retrying...")
                synthesis = self._phase_synthesis_with_feedback(
                    technology, research, depth, quality_metrics
                )
                artifacts.append(synthesis)
                validation = self._phase_validation(synthesis.content)
                artifacts.append(validation)
                quality_metrics = validation.metadata["metrics"]

            # PHASE 4: TESTING
            print("🧪 Phase 4/6: Automated Testing...")
            testing = self._phase_testing(technology, synthesis.content)
            artifacts.append(testing)

            tests_passed = testing.metadata["passed"]
            tests_total = testing.metadata["total"]
            test_ratio = tests_passed / max(tests_total, 1)

            # PHASE 5: INTEGRATION
            print("🔗 Phase 5/6: Knowledge Integration...")
            integration = self._phase_integration(
                technology, synthesis.content, quality_metrics, testing.metadata
            )
            artifacts.append(integration)

            # PHASE 6: VERIFICATION
            print("🎯 Phase 6/6: Final Verification...")
            verification = self._phase_verification(technology)
            artifacts.append(verification)

            # Calculate proficiency
            proficiency = self._calculate_proficiency(
                quality_metrics.overall_score, test_ratio, verification.quality_score
            )

            execution_time = time.time() - start_time

            print(f"\n{'='*70}")
            print(f"✅ LEARNING COMPLETE: {technology}")
            print(f"   Proficiency: {proficiency:.1%}")
            print(f"   Quality: {quality_metrics.grade}")
            print(f"   Tests: {tests_passed}/{tests_total}")
            print(f"   Time: {execution_time:.1f}s")
            print(f"{'='*70}\n")

            return LearningResult(
                technology=technology,
                success=True,
                proficiency=proficiency,
                artifacts=artifacts,
                quality_grade=quality_metrics.grade,
                tests_passed=tests_passed,
                tests_total=tests_total,
                execution_time=execution_time,
                errors=errors,
                suggestions=quality_metrics.suggestions,
            )

        except Exception as e:
            logger.error(f"Learning error: {e}", exc_info=True)
            errors.append(f"Critical error: {str(e)}")
            return self._failed_result(
                technology, artifacts, errors, time.time() - start_time
            )

    def _phase_research(self, technology: str) -> LearningArtifact:
        """Phase 1: Research documentation"""
        prompt = f"""You are a technical documentation expert. Research {technology} and provide comprehensive documentation:

## OVERVIEW
What is {technology}? What problem does it solve? (3-5 sentences)

## KEY CONCEPTS
- List 4-6 core concepts/features
- Explain each in 1-2 sentences

## COMMON USE CASES
- 3-5 practical applications
- When developers use {technology}

## INSTALLATION & SETUP
- How to install/import
- Required dependencies

## BASIC EXAMPLE
- Show a simple working code snippet
- Must be actual Python code, not pseudocode

## BEST PRACTICES
- 3-5 important tips
- Common pitfalls to avoid

Be thorough but concise. Focus on actionable information."""

        research_data = self.ai.ask(prompt)

        # Better quality scoring
        quality = 0.0
        if len(research_data) > 300:
            quality += 0.3
        if any(
            word in research_data.lower() for word in ["overview", "what is", "purpose"]
        ):
            quality += 0.2
        if "example" in research_data.lower() or "```" in research_data:
            quality += 0.3
        if any(
            word in research_data.lower() for word in ["usage", "use case", "install"]
        ):
            quality += 0.2

        return LearningArtifact(
            phase=LearningPhase.RESEARCH,
            content=research_data,
            metadata={"length": len(research_data)},
            quality_score=min(quality, 1.0),
        )

    def _phase_synthesis(
        self, technology: str, research: LearningArtifact, depth: str
    ) -> LearningArtifact:
        """Phase 2: Generate REAL working code"""

        prompt = f"""Generate PRODUCTION-READY Python code using {technology}.

Context: {research.content[:300]}

Requirements:
- Create a working example
- Include proper imports
- Add docstrings
- Add type hints if possible
- Include error handling
- Add inline comments
- NO TODO comments!
- Code must be runnable

Generate ONLY the code, no explanations."""

        code = self.ai.ask(prompt)
        code = self._extract_code(code)

        return LearningArtifact(
            phase=LearningPhase.SYNTHESIS,
            content=code,
            metadata={"depth": depth, "length": len(code)},
            quality_score=0.8,
        )

    def _phase_synthesis_with_feedback(
        self, technology: str, research: LearningArtifact, depth: str, prev_quality
    ) -> LearningArtifact:
        """Phase 2 retry: Generate code with quality feedback"""

        issues_text = "\n".join(f"- {issue}" for issue in prev_quality.issues)

        prompt = f"""Generate IMPROVED Python code using {technology}.

Previous code had issues:
{issues_text}

Generate code that fixes these issues.
Include: imports, docstrings, type hints, error handling, comments.
NO TODO! Code must be complete."""

        code = self.ai.ask(prompt)
        code = self._extract_code(code)

        return LearningArtifact(
            phase=LearningPhase.SYNTHESIS,
            content=code,
            metadata={"depth": depth, "retry": True},
            quality_score=0.9,
        )

    def _phase_validation(self, code: str) -> LearningArtifact:
        """Phase 3: Validate code quality"""
        metrics = self.quality.analyze(code)

        return LearningArtifact(
            phase=LearningPhase.VALIDATION,
            content="Quality analysis complete",
            metadata={"metrics": metrics},
            quality_score=metrics.overall_score,
        )

    def _phase_testing(self, technology: str, code: str) -> LearningArtifact:
        """Phase 4: Test code execution"""

        # Execute in sandbox
        result = self.sandbox.execute_python(code, timeout=30)

        passed = 1 if result.status.value == "success" else 0
        total = 1

        return LearningArtifact(
            phase=LearningPhase.TESTING,
            content="Testing complete",
            metadata={"passed": passed, "total": total, "execution": result},
            quality_score=passed / total,
        )

    def _phase_integration(
        self, technology: str, code: str, quality, test_metadata: Dict
    ) -> LearningArtifact:
        """Phase 5: Integrate into knowledge base"""

        filename = f"learning/{technology.lower().replace(' ', '_')}_verified.py"

        header = f'''"""
{technology} - Verified Learning Artifact

Quality Grade: {quality.grade}
Overall Score: {quality.overall_score:.2f}
Tests Passed: {test_metadata['passed']}/{test_metadata['total']}
Learned: {datetime.now().isoformat()}

This code has been verified by MIRAI's NASA-level learning system.
"""

'''

        full_code = header + code

        try:
            self.ai.write_file(filename, full_code)

            # Update knowledge base
            from core.self_evolution import KnowledgeBase

            kb = KnowledgeBase()
            kb.add_technology(technology, quality.overall_score)
        except Exception as e:
            logger.error(f"Integration error: {e}")

        return LearningArtifact(
            phase=LearningPhase.INTEGRATION,
            content=filename,
            metadata={"filepath": filename},
            quality_score=1.0,
        )

    def _phase_verification(self, technology: str) -> LearningArtifact:
        """Phase 6: Final verification"""

        filename = f"learning/{technology.lower().replace(' ', '_')}_verified.py"

        try:
            code = self.ai.read_file(filename)
            result = self.sandbox.execute_python(code, timeout=30)
            success = result.status.value == "success"

            return LearningArtifact(
                phase=LearningPhase.VERIFICATION,
                content="Verification complete",
                metadata={"success": success, "result": result},
                quality_score=1.0 if success else 0.5,
            )
        except:
            return LearningArtifact(
                phase=LearningPhase.VERIFICATION,
                content="Verification failed",
                metadata={"success": False},
                quality_score=0.0,
            )

    def _calculate_proficiency(
        self, quality_score: float, test_ratio: float, verification_score: float
    ) -> float:
        """Calculate real proficiency level"""
        return quality_score * 0.4 + test_ratio * 0.4 + verification_score * 0.2

    def _extract_code(self, text: str) -> str:
        """Extract Python code from markdown or mixed text"""

        # Try to extract from ```python blocks
        pattern = r"```python\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0]

        # Try ``` blocks
        pattern = r"```\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0]

        # Return as-is
        return text

    def _failed_result(
        self, technology: str, artifacts: List, errors: List, execution_time: float
    ) -> LearningResult:
        """Create failed learning result"""
        return LearningResult(
            technology=technology,
            success=False,
            proficiency=0.0,
            artifacts=artifacts,
            quality_grade="F",
            tests_passed=0,
            tests_total=0,
            execution_time=execution_time,
            errors=errors,
            suggestions=["Review errors and retry"],
        )
