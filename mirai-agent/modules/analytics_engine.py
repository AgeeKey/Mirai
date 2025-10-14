"""
🧠 NASA-Level Analytics Engine
Advanced ML-powered analytics for learning optimization

Features:
- Learning trends analysis (temporal patterns)
- Technology recommendations (what to learn next)
- Proficiency predictions (success likelihood)
- Performance insights (statistical analysis)
"""

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class LearningTrend:
    """Trend data for a technology or metric"""

    period: str  # 'day', 'week', 'month'
    technology: Optional[str]
    metric: str  # 'proficiency', 'attempts', 'success_rate'
    values: List[float]
    timestamps: List[str]
    trend_direction: str  # 'up', 'down', 'stable'
    confidence: float  # 0.0-1.0


@dataclass
class TechnologyRecommendation:
    """Recommendation for next technology to learn"""

    technology: str
    score: float  # 0.0-1.0
    reason: str
    related_techs: List[str]
    estimated_difficulty: str  # 'easy', 'medium', 'hard'
    estimated_time_hours: float


@dataclass
class ProficiencyPrediction:
    """Prediction for learning outcome"""

    technology: str
    predicted_proficiency: float  # 0.0-1.0
    confidence: float  # 0.0-1.0
    estimated_attempts: int
    success_probability: float  # 0.0-1.0
    factors: Dict[str, float]  # Contributing factors


@dataclass
class PerformanceInsight:
    """Statistical insight about performance"""

    category: str  # 'strength', 'weakness', 'opportunity', 'pattern'
    title: str
    description: str
    metric_value: float
    recommendation: str
    priority: str  # 'high', 'medium', 'low'


class AnalyticsEngine:
    """Advanced analytics for NASA-Level Learning System"""

    def __init__(self, knowledge_db_path: str = "nasa_knowledge.json"):
        self.knowledge_db_path = Path(knowledge_db_path)
        self.knowledge_data = self._load_knowledge()

    def _load_knowledge(self) -> List[Dict]:
        """Load knowledge base"""
        if not self.knowledge_db_path.exists():
            return []

        with open(self.knowledge_db_path) as f:
            return json.load(f)

    def get_learning_trends(
        self, period: str = "week", technology: Optional[str] = None
    ) -> List[LearningTrend]:
        """
        Analyze learning trends over time

        Args:
            period: 'day', 'week', 'month'
            technology: Specific tech or None for overall

        Returns:
            List of trend objects
        """
        trends = []

        # Calculate time buckets
        now = datetime.now()
        if period == "day":
            days = 7
            bucket_size = timedelta(days=1)
        elif period == "week":
            days = 28
            bucket_size = timedelta(days=7)
        else:  # month
            days = 180
            bucket_size = timedelta(days=30)

        # Group data by time buckets
        proficiency_buckets = defaultdict(list)
        attempts_buckets = defaultdict(int)

        for entry in self.knowledge_data:
            learned_at = datetime.fromisoformat(
                entry["learned_at"].replace("Z", "+00:00")
            )

            # Skip if outside time window
            if (now - learned_at).days > days:
                continue

            # Skip if filtering by technology
            if technology and entry["technology"] != technology:
                continue

            # Calculate bucket index
            bucket_idx = int((now - learned_at) / bucket_size)

            proficiency_buckets[bucket_idx].append(entry["proficiency_score"])
            attempts_buckets[bucket_idx] += 1

        # Create proficiency trend
        if proficiency_buckets:
            sorted_buckets = sorted(proficiency_buckets.keys(), reverse=True)
            values = [np.mean(proficiency_buckets[b]) for b in sorted_buckets]
            timestamps = [
                (now - bucket_size * b).strftime("%Y-%m-%d") for b in sorted_buckets
            ]

            # Calculate trend direction
            if len(values) >= 2:
                slope = (values[-1] - values[0]) / len(values)
                if slope > 0.05:
                    direction = "up"
                    confidence = min(1.0, abs(slope) * 5)
                elif slope < -0.05:
                    direction = "down"
                    confidence = min(1.0, abs(slope) * 5)
                else:
                    direction = "stable"
                    confidence = 0.8
            else:
                direction = "stable"
                confidence = 0.5

            trends.append(
                LearningTrend(
                    period=period,
                    technology=technology,
                    metric="proficiency",
                    values=values,
                    timestamps=timestamps,
                    trend_direction=direction,
                    confidence=confidence,
                )
            )

        # Create attempts trend
        if attempts_buckets:
            sorted_buckets = sorted(attempts_buckets.keys(), reverse=True)
            values = [float(attempts_buckets[b]) for b in sorted_buckets]
            timestamps = [
                (now - bucket_size * b).strftime("%Y-%m-%d") for b in sorted_buckets
            ]

            # Calculate trend
            if len(values) >= 2:
                slope = (values[-1] - values[0]) / len(values)
                if slope > 0.5:
                    direction = "up"
                    confidence = 0.9
                elif slope < -0.5:
                    direction = "down"
                    confidence = 0.9
                else:
                    direction = "stable"
                    confidence = 0.7
            else:
                direction = "stable"
                confidence = 0.5

            trends.append(
                LearningTrend(
                    period=period,
                    technology=technology,
                    metric="attempts",
                    values=values,
                    timestamps=timestamps,
                    trend_direction=direction,
                    confidence=confidence,
                )
            )

        return trends

    def get_technology_recommendations(
        self, limit: int = 5, user_level: str = "intermediate"
    ) -> List[TechnologyRecommendation]:
        """
        Get AI-powered recommendations for what to learn next

        Args:
            limit: Max number of recommendations
            user_level: 'beginner', 'intermediate', 'advanced'

        Returns:
            List of recommendations sorted by score
        """
        # Get already learned technologies
        learned_techs = {entry["technology"] for entry in self.knowledge_data}

        # Technology clusters and relationships
        tech_clusters = {
            # Python ecosystem
            "pandas": ["numpy", "matplotlib", "seaborn", "scipy"],
            "numpy": ["pandas", "scipy", "tensorflow"],
            "fastapi": ["pydantic", "uvicorn", "sqlalchemy", "alembic"],
            "flask": ["jinja2", "sqlalchemy", "wtforms"],
            "django": ["celery", "drf", "channels"],
            # JS ecosystem
            "react": ["redux", "react-router", "next.js", "typescript"],
            "vue": ["vuex", "nuxt.js", "typescript"],
            "node.js": ["express", "nest.js", "typescript"],
            # DevOps
            "docker": ["kubernetes", "docker-compose", "helm"],
            "kubernetes": ["helm", "istio", "prometheus"],
            "terraform": ["ansible", "packer", "vault"],
            # Databases
            "postgresql": ["pgvector", "timescaledb", "postgis"],
            "mongodb": ["mongoose", "redis"],
            "redis": ["celery", "bull"],
        }

        # Recommended next steps
        recommendations = []

        # 1. Based on what user already knows
        for tech in learned_techs:
            if tech in tech_clusters:
                for related in tech_clusters[tech]:
                    if related not in learned_techs:
                        # Calculate score based on mastery of prerequisite
                        prereq_entries = [
                            e for e in self.knowledge_data if e["technology"] == tech
                        ]
                        if prereq_entries:
                            avg_proficiency = np.mean(
                                [e["proficiency_score"] for e in prereq_entries]
                            )
                            score = (
                                avg_proficiency * 0.9
                            )  # High score if mastered prereq

                            recommendations.append(
                                TechnologyRecommendation(
                                    technology=related,
                                    score=score,
                                    reason=f"Complements your {tech} knowledge",
                                    related_techs=[tech],
                                    estimated_difficulty="medium",
                                    estimated_time_hours=4.0,
                                )
                            )

        # 2. Popular technologies not yet learned
        popular_techs = [
            ("typescript", 0.9, "JavaScript superset with type safety", 8.0),
            ("graphql", 0.85, "Modern API query language", 6.0),
            ("redis", 0.88, "In-memory data store for caching", 4.0),
            ("postgresql", 0.92, "Advanced relational database", 10.0),
            ("docker", 0.95, "Container platform for deployment", 6.0),
            ("kubernetes", 0.85, "Container orchestration", 12.0),
            ("terraform", 0.82, "Infrastructure as code", 8.0),
            ("pytest", 0.87, "Python testing framework", 4.0),
            ("sqlalchemy", 0.84, "Python SQL toolkit and ORM", 6.0),
        ]

        for tech, base_score, reason, hours in popular_techs:
            if tech not in learned_techs and tech not in [
                r.technology for r in recommendations
            ]:
                # Adjust score based on user level
                if user_level == "beginner":
                    score = base_score * 0.7
                    difficulty = "medium" if hours > 6 else "easy"
                elif user_level == "advanced":
                    score = base_score * 1.1
                    difficulty = "easy" if hours < 8 else "medium"
                else:
                    score = base_score
                    difficulty = "medium" if hours > 8 else "easy"

                recommendations.append(
                    TechnologyRecommendation(
                        technology=tech,
                        score=min(1.0, score),
                        reason=reason,
                        related_techs=[],
                        estimated_difficulty=difficulty,
                        estimated_time_hours=hours,
                    )
                )

        # Sort by score and limit
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]

    def predict_proficiency(
        self, technology: str, context: Optional[Dict[str, Any]] = None
    ) -> ProficiencyPrediction:
        """
        Predict learning outcome using historical data

        Args:
            technology: Technology to predict
            context: Additional context (user_level, related_knowledge, etc.)

        Returns:
            Prediction object
        """
        context = context or {}

        # Get historical data
        all_attempts = [
            e["proficiency_score"]
            for e in self.knowledge_data
            if "proficiency_score" in e
        ]

        if not all_attempts:
            # No historical data - use defaults
            return ProficiencyPrediction(
                technology=technology,
                predicted_proficiency=0.7,
                confidence=0.3,
                estimated_attempts=1,
                success_probability=0.75,
                factors={
                    "historical_avg": 0.0,
                    "user_level": 0.7,
                    "related_knowledge": 0.0,
                },
            )

        # Calculate base prediction from historical average
        historical_avg = np.mean(all_attempts)
        historical_std = np.std(all_attempts) if len(all_attempts) > 1 else 0.15

        # Factors affecting prediction
        factors = {}

        # 1. Historical performance
        factors["historical_avg"] = historical_avg * 0.4

        # 2. User level
        user_level = context.get("user_level", "intermediate")
        level_bonus = {"beginner": -0.1, "intermediate": 0.0, "advanced": 0.15}.get(
            user_level, 0.0
        )
        factors["user_level"] = level_bonus * 0.3

        # 3. Related knowledge
        learned_techs = {entry["technology"] for entry in self.knowledge_data}
        related_count = len(learned_techs)
        factors["related_knowledge"] = min(0.2, related_count * 0.02) * 0.3

        # Combine factors
        predicted_proficiency = sum(factors.values()) + 0.5
        predicted_proficiency = max(0.0, min(1.0, predicted_proficiency))

        # Confidence based on data quantity
        confidence = min(0.95, 0.5 + len(all_attempts) * 0.05)

        # Estimate attempts needed
        if predicted_proficiency < 0.5:
            estimated_attempts = 3
            success_probability = 0.6
        elif predicted_proficiency < 0.75:
            estimated_attempts = 2
            success_probability = 0.85
        else:
            estimated_attempts = 1
            success_probability = 0.95

        return ProficiencyPrediction(
            technology=technology,
            predicted_proficiency=predicted_proficiency,
            confidence=confidence,
            estimated_attempts=estimated_attempts,
            success_probability=success_probability,
            factors=factors,
        )

    def get_performance_insights(self) -> List[PerformanceInsight]:
        """
        Generate insights about learning performance

        Returns:
            List of insights with recommendations
        """
        insights = []

        if not self.knowledge_data:
            return [
                PerformanceInsight(
                    category="opportunity",
                    title="Start Your Learning Journey",
                    description="No learning history yet",
                    metric_value=0.0,
                    recommendation="Try learning a popular technology like Python or JavaScript",
                    priority="high",
                )
            ]

        # 1. Overall proficiency analysis
        all_proficiencies = [
            e["proficiency_score"]
            for e in self.knowledge_data
            if "proficiency_score" in e
        ]
        if all_proficiencies:
            avg_proficiency = np.mean(all_proficiencies)

            if avg_proficiency >= 0.85:
                insights.append(
                    PerformanceInsight(
                        category="strength",
                        title="Excellent Learning Performance",
                        description=f"Your average proficiency is {avg_proficiency:.1%}",
                        metric_value=avg_proficiency,
                        recommendation="Consider learning advanced topics or becoming a mentor",
                        priority="low",
                    )
                )
            elif avg_proficiency < 0.6:
                insights.append(
                    PerformanceInsight(
                        category="weakness",
                        title="Room for Improvement",
                        description=f"Average proficiency is {avg_proficiency:.1%}",
                        metric_value=avg_proficiency,
                        recommendation="Try easier topics first, use more resources, practice more",
                        priority="high",
                    )
                )

        # 2. Learning consistency
        if len(self.knowledge_data) >= 3:
            dates = [
                datetime.fromisoformat(e["learned_at"].replace("Z", "+00:00"))
                for e in self.knowledge_data
            ]
            dates.sort()
            gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
            avg_gap = np.mean(gaps)

            if avg_gap <= 2:
                insights.append(
                    PerformanceInsight(
                        category="strength",
                        title="Consistent Learning Habit",
                        description=f"You learn new things every {avg_gap:.1f} days",
                        metric_value=1.0 / avg_gap,
                        recommendation="Maintain this excellent consistency!",
                        priority="low",
                    )
                )
            elif avg_gap > 7:
                insights.append(
                    PerformanceInsight(
                        category="pattern",
                        title="Irregular Learning Pattern",
                        description=f"Average gap between learning: {avg_gap:.1f} days",
                        metric_value=avg_gap,
                        recommendation="Try to learn more regularly for better retention",
                        priority="medium",
                    )
                )

        # 3. Diversity analysis
        unique_techs = len({e["technology"] for e in self.knowledge_data})
        if unique_techs >= 5:
            insights.append(
                PerformanceInsight(
                    category="strength",
                    title="Diverse Technology Stack",
                    description=f"You've learned {unique_techs} different technologies",
                    metric_value=float(unique_techs),
                    recommendation="Great breadth! Consider deepening knowledge in key areas",
                    priority="low",
                )
            )
        elif unique_techs <= 2 and len(self.knowledge_data) >= 5:
            insights.append(
                PerformanceInsight(
                    category="opportunity",
                    title="Limited Technology Diversity",
                    description=f"Only {unique_techs} technologies learned",
                    metric_value=float(unique_techs),
                    recommendation="Explore related technologies to broaden your skills",
                    priority="medium",
                )
            )

        # 4. Quality distribution
        grade_counts = defaultdict(int)
        for entry in self.knowledge_data:
            grade = entry.get("quality_grade", "C")
            grade_counts[grade] += 1

        total_entries = len(self.knowledge_data)
        a_grade_pct = grade_counts["A"] / total_entries if total_entries > 0 else 0

        if a_grade_pct >= 0.7:
            insights.append(
                PerformanceInsight(
                    category="strength",
                    title="High Quality Learning",
                    description=f"{a_grade_pct:.0%} of learnings are grade A",
                    metric_value=a_grade_pct,
                    recommendation="Excellent quality! Share your learning methods with others",
                    priority="low",
                )
            )
        elif a_grade_pct < 0.3:
            insights.append(
                PerformanceInsight(
                    category="weakness",
                    title="Quality Needs Improvement",
                    description=f"Only {a_grade_pct:.0%} are grade A",
                    metric_value=a_grade_pct,
                    recommendation="Focus on deeper understanding rather than speed",
                    priority="high",
                )
            )

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        insights.sort(key=lambda x: priority_order[x.priority])

        return insights


# Singleton instance
_analytics_engine: Optional[AnalyticsEngine] = None


def get_analytics_engine() -> AnalyticsEngine:
    """Get singleton analytics engine instance"""
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = AnalyticsEngine()
    return _analytics_engine
