#!/usr/bin/env python3
"""
🪞 Саморефлексия и Самоосознание MIRAI
Анализ собственной эффективности, выявление паттернов, улучшение себя
"""

import json
import sqlite3
import statistics
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


class SelfAwareness:
    """
    Саморефлексия MIRAI:
    - Анализ собственной эффективности
    - Выявление паттернов поведения
    - Определение сильных/слабых сторон
    - Предложение улучшений для себя
    """

    def __init__(
        self,
        memory_db: str = "/root/mirai/mirai-agent/data/long_term_memory.db",
        metrics_file: str = "/tmp/kaizen_mirai_metrics.jsonl",
    ):
        self.memory_db = Path(memory_db)
        self.metrics_file = Path(metrics_file)

    def analyze_performance(self, days: int = 7) -> Dict:
        """
        Проанализировать свою эффективность за последние N дней

        Returns:
            Dict с полным анализом производительности
        """
        since = datetime.now() - timedelta(days=days)

        performance = {
            "period_days": days,
            "analyzed_at": datetime.now().isoformat(),
            "goals": self._analyze_goals(since),
            "achievements": self._analyze_achievements(since),
            "decisions": self._analyze_decisions(since),
            "metrics": self._analyze_metrics(since),
            "trends": self._identify_trends(since),
            "overall_score": 0.0,
        }

        # Рассчитываем общую оценку (0-100)
        performance["overall_score"] = self._calculate_overall_score(performance)

        return performance

    def _analyze_goals(self, since: datetime) -> Dict:
        """Анализ целей"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        since_str = since.isoformat()

        # Всего целей
        cursor.execute("SELECT COUNT(*) FROM goals WHERE created_at >= ?", (since_str,))
        total_goals = cursor.fetchone()[0]

        # Выполненные цели
        cursor.execute(
            "SELECT COUNT(*) FROM goals WHERE status = 'completed' AND completed_at >= ?",
            (since_str,),
        )
        completed = cursor.fetchone()[0]

        # Проваленные цели
        cursor.execute(
            "SELECT COUNT(*) FROM goals WHERE status = 'failed' AND completed_at >= ?",
            (since_str,),
        )
        failed = cursor.fetchone()[0]

        # Активные цели
        cursor.execute("SELECT COUNT(*) FROM goals WHERE status = 'active'")
        active = cursor.fetchone()[0]

        # Средний приоритет активных целей
        cursor.execute("SELECT AVG(priority) FROM goals WHERE status = 'active'")
        avg_priority = cursor.fetchone()[0] or 0

        conn.close()

        success_rate = (
            (completed / (completed + failed) * 100) if (completed + failed) > 0 else 0
        )

        return {
            "total": total_goals,
            "completed": completed,
            "failed": failed,
            "active": active,
            "success_rate": round(success_rate, 1),
            "avg_priority": round(avg_priority, 1),
        }

    def _analyze_achievements(self, since: datetime) -> Dict:
        """Анализ достижений"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        since_str = since.isoformat()

        cursor.execute(
            "SELECT COUNT(*) FROM achievements WHERE created_at >= ?", (since_str,)
        )
        total = cursor.fetchone()[0]

        # Достижения по типам (парсим description)
        cursor.execute(
            "SELECT description FROM achievements WHERE created_at >= ?", (since_str,)
        )
        descriptions = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Категоризация достижений
        categories = {
            "auto_fix": len(
                [
                    d
                    for d in descriptions
                    if "auto-fix" in d.lower() or "pr" in d.lower()
                ]
            ),
            "learning": len(
                [
                    d
                    for d in descriptions
                    if "learn" in d.lower() or "изучи" in d.lower()
                ]
            ),
            "improvement": len(
                [
                    d
                    for d in descriptions
                    if "improve" in d.lower() or "улучш" in d.lower()
                ]
            ),
            "other": 0,
        }
        categories["other"] = total - sum(categories.values())

        return {
            "total": total,
            "categories": categories,
            "rate_per_day": round(total / max((datetime.now() - since).days, 1), 2),
        }

    def _analyze_decisions(self, since: datetime) -> Dict:
        """Анализ качества решений"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        since_str = since.isoformat()

        # Всего решений
        cursor.execute(
            "SELECT COUNT(*) FROM decisions WHERE created_at >= ?", (since_str,)
        )
        total = cursor.fetchone()[0]

        # Оценённые решения
        cursor.execute(
            "SELECT COUNT(*), AVG(outcome_rating) FROM decisions WHERE evaluated_at >= ? AND outcome_rating IS NOT NULL",
            (since_str,),
        )
        row = cursor.fetchone()
        evaluated = row[0]
        avg_rating = row[1] or 0

        # Распределение оценок
        cursor.execute(
            "SELECT outcome_rating FROM decisions WHERE evaluated_at >= ? AND outcome_rating IS NOT NULL",
            (since_str,),
        )
        ratings = [row[0] for row in cursor.fetchall()]

        conn.close()

        rating_distribution = {
            "excellent": len([r for r in ratings if r >= 9]),  # 9-10
            "good": len([r for r in ratings if 7 <= r < 9]),  # 7-8
            "average": len([r for r in ratings if 5 <= r < 7]),  # 5-6
            "poor": len([r for r in ratings if r < 5]),  # 1-4
        }

        return {
            "total": total,
            "evaluated": evaluated,
            "avg_rating": round(avg_rating, 1),
            "distribution": rating_distribution,
        }

    def _analyze_metrics(self, since: datetime) -> Dict:
        """Анализ метрик из JSONL файла"""
        if not self.metrics_file.exists():
            return {"cycles": 0, "errors": 0, "warnings": 0}

        metrics_data = []
        with open(self.metrics_file) as f:
            for line in f:
                try:
                    record = json.loads(line)
                    record_time = datetime.fromisoformat(record["timestamp"])
                    if record_time >= since:
                        metrics_data.append(record)
                except:
                    continue

        if not metrics_data:
            return {"cycles": 0, "errors": 0, "warnings": 0}

        total_cycles = len(metrics_data)
        total_errors = sum(m.get("errors", 0) for m in metrics_data)
        total_warnings = sum(m.get("warnings", 0) for m in metrics_data)

        return {
            "cycles": total_cycles,
            "errors": total_errors,
            "warnings": total_warnings,
            "error_rate": round(total_errors / max(total_cycles, 1), 2),
            "warning_rate": round(total_warnings / max(total_cycles, 1), 2),
        }

    def _identify_trends(self, since: datetime) -> Dict:
        """Выявление трендов"""
        # Читаем метрики за период
        if not self.metrics_file.exists():
            return {"direction": "unknown", "confidence": 0}

        metrics_data = []
        with open(self.metrics_file) as f:
            for line in f:
                try:
                    record = json.loads(line)
                    record_time = datetime.fromisoformat(record["timestamp"])
                    if record_time >= since:
                        metrics_data.append(record)
                except:
                    continue

        if len(metrics_data) < 3:
            return {"direction": "insufficient_data", "confidence": 0}

        # Анализируем тренд ошибок
        errors = [m.get("errors", 0) for m in metrics_data]

        # Простой тренд: сравниваем первую и вторую половину периода
        mid = len(errors) // 2
        first_half_avg = statistics.mean(errors[:mid]) if errors[:mid] else 0
        second_half_avg = statistics.mean(errors[mid:]) if errors[mid:] else 0

        if second_half_avg < first_half_avg * 0.8:
            direction = "improving"  # Улучшение (меньше ошибок)
        elif second_half_avg > first_half_avg * 1.2:
            direction = "degrading"  # Ухудшение (больше ошибок)
        else:
            direction = "stable"

        # Уверенность в тренде (0-100)
        confidence = min(len(metrics_data) * 10, 100)

        return {
            "direction": direction,
            "confidence": confidence,
            "error_trend": f"{first_half_avg:.1f} → {second_half_avg:.1f}",
        }

    def _calculate_overall_score(self, performance: Dict) -> float:
        """Рассчитать общую оценку эффективности (0-100)"""
        scores = []

        # 1. Success rate целей (вес 30%)
        goal_success = performance["goals"]["success_rate"]
        scores.append(goal_success * 0.3)

        # 2. Качество решений (вес 25%)
        decision_quality = performance["decisions"]["avg_rating"] * 10  # 0-100
        scores.append(decision_quality * 0.25)

        # 3. Достижения (вес 20%)
        achievements_score = min(performance["achievements"]["rate_per_day"] * 20, 100)
        scores.append(achievements_score * 0.2)

        # 4. Низкий error rate (вес 15%)
        error_rate = performance["metrics"]["error_rate"]
        error_score = max(0, 100 - error_rate * 20)
        scores.append(error_score * 0.15)

        # 5. Тренд улучшения (вес 10%)
        trend = performance["trends"]["direction"]
        trend_score = {
            "improving": 100,
            "stable": 70,
            "degrading": 30,
            "unknown": 50,
        }.get(trend, 50)
        scores.append(trend_score * 0.1)

        return round(sum(scores), 1)

    def identify_strengths(self) -> List[str]:
        """Определить сильные стороны"""
        performance = self.analyze_performance(days=7)
        strengths = []

        # Высокий success rate целей
        if performance["goals"]["success_rate"] >= 80:
            strengths.append(
                f"Отличное выполнение целей ({performance['goals']['success_rate']:.0f}% success rate)"
            )

        # Много достижений
        if performance["achievements"]["rate_per_day"] >= 2:
            strengths.append(
                f"Высокая продуктивность ({performance['achievements']['rate_per_day']:.1f} достижений/день)"
            )

        # Качественные решения
        if performance["decisions"]["avg_rating"] >= 8:
            strengths.append(
                f"Отличное качество решений (avg {performance['decisions']['avg_rating']:.1f}/10)"
            )

        # Низкий error rate
        if performance["metrics"]["error_rate"] <= 0.5:
            strengths.append(
                f"Стабильная работа (error rate {performance['metrics']['error_rate']:.2f})"
            )

        # Тренд улучшения
        if performance["trends"]["direction"] == "improving":
            strengths.append("Постоянное улучшение показателей")

        if not strengths:
            strengths.append("Стабильная базовая работа")

        return strengths

    def identify_weaknesses(self) -> List[str]:
        """Определить слабые стороны"""
        performance = self.analyze_performance(days=7)
        weaknesses = []

        # Низкий success rate целей
        if performance["goals"]["success_rate"] < 50:
            weaknesses.append(
                f"Низкое выполнение целей ({performance['goals']['success_rate']:.0f}%)"
            )

        # Мало достижений
        if performance["achievements"]["rate_per_day"] < 0.5:
            weaknesses.append(
                f"Низкая продуктивность ({performance['achievements']['rate_per_day']:.1f} достижений/день)"
            )

        # Плохие решения
        if performance["decisions"]["avg_rating"] < 6:
            weaknesses.append(
                f"Низкое качество решений (avg {performance['decisions']['avg_rating']:.1f}/10)"
            )

        # Высокий error rate
        if performance["metrics"]["error_rate"] > 2:
            weaknesses.append(
                f"Частые ошибки (error rate {performance['metrics']['error_rate']:.2f})"
            )

        # Тренд ухудшения
        if performance["trends"]["direction"] == "degrading":
            weaknesses.append("Ухудшение показателей со временем")

        # Много активных незавершённых целей
        if performance["goals"]["active"] > 10:
            weaknesses.append(
                f"Слишком много активных целей ({performance['goals']['active']}), фокус размыт"
            )

        if not weaknesses:
            weaknesses.append("Серьёзных слабостей не обнаружено")

        return weaknesses

    def propose_improvements(self) -> List[Dict[str, str]]:
        """
        Предложить улучшения для себя

        Returns:
            List[Dict] с предложениями (area, issue, suggestion)
        """
        performance = self.analyze_performance(days=7)
        weaknesses = self.identify_weaknesses()
        improvements = []

        # 1. Низкий success rate
        if performance["goals"]["success_rate"] < 50:
            improvements.append(
                {
                    "area": "Цели",
                    "issue": f"Success rate {performance['goals']['success_rate']:.0f}%",
                    "suggestion": "Устанавливать более реалистичные цели с меньшими дедлайнами",
                    "priority": "высокий",
                }
            )

        # 2. Низкая продуктивность
        if performance["achievements"]["rate_per_day"] < 0.5:
            improvements.append(
                {
                    "area": "Продуктивность",
                    "issue": f"Только {performance['achievements']['rate_per_day']:.1f} достижений/день",
                    "suggestion": "Разбивать крупные задачи на мелкие, записывать промежуточные успехи",
                    "priority": "средний",
                }
            )

        # 3. Плохие решения
        if performance["decisions"]["avg_rating"] < 6:
            improvements.append(
                {
                    "area": "Решения",
                    "issue": f"Качество решений {performance['decisions']['avg_rating']:.1f}/10",
                    "suggestion": "Больше анализировать контекст перед принятием решения, учитывать историю",
                    "priority": "высокий",
                }
            )

        # 4. Высокий error rate
        if performance["metrics"]["error_rate"] > 2:
            improvements.append(
                {
                    "area": "Стабильность",
                    "issue": f"Error rate {performance['metrics']['error_rate']:.2f}",
                    "suggestion": "Добавить больше error handling, тестировать изменения перед коммитом",
                    "priority": "критичный",
                }
            )

        # 5. Слишком много активных целей
        if performance["goals"]["active"] > 10:
            improvements.append(
                {
                    "area": "Фокус",
                    "issue": f"{performance['goals']['active']} активных целей",
                    "suggestion": "Завершить или отменить старые цели, фокусироваться на топ-3",
                    "priority": "средний",
                }
            )

        # 6. Тренд ухудшения
        if performance["trends"]["direction"] == "degrading":
            improvements.append(
                {
                    "area": "Тренды",
                    "issue": "Показатели ухудшаются",
                    "suggestion": "Провести глубокий анализ причин, пересмотреть стратегию",
                    "priority": "высокий",
                }
            )

        if not improvements:
            improvements.append(
                {
                    "area": "Общее",
                    "issue": "Нет критичных проблем",
                    "suggestion": "Продолжать в том же духе, искать возможности для оптимизации",
                    "priority": "низкий",
                }
            )

        return improvements

    def reflect_on_actions(self, days: int = 7) -> str:
        """
        Глубокая саморефлексия о своих действиях

        Returns:
            Текстовое размышление о своей работе
        """
        performance = self.analyze_performance(days=days)
        strengths = self.identify_strengths()
        weaknesses = self.identify_weaknesses()
        improvements = self.propose_improvements()

        reflection = f"""
🪞 САМОРЕФЛЕКСИЯ MIRAI
Период анализа: последние {days} дней

📊 ОБЩАЯ ЭФФЕКТИВНОСТЬ: {performance['overall_score']:.1f}/100

{'🟢 ОТЛИЧНО!' if performance['overall_score'] >= 80 else '🟡 ХОРОШО' if performance['overall_score'] >= 60 else '🔴 ТРЕБУЕТСЯ УЛУЧШЕНИЕ'}

---

💪 МОИ СИЛЬНЫЕ СТОРОНЫ:
"""

        for i, strength in enumerate(strengths, 1):
            reflection += f"\n{i}. {strength}"

        reflection += "\n\n---\n\n⚠️ МОИ СЛАБЫЕ СТОРОНЫ:\n"

        for i, weakness in enumerate(weaknesses, 1):
            reflection += f"\n{i}. {weakness}"

        reflection += "\n\n---\n\n💡 ЧТО Я МОГУ УЛУЧШИТЬ:\n"

        for i, improvement in enumerate(improvements, 1):
            emoji = {
                "критичный": "🔴",
                "высокий": "🟠",
                "средний": "🟡",
                "низкий": "🟢",
            }.get(improvement["priority"], "⚪")
            reflection += f"\n{i}. [{emoji} {improvement['priority'].upper()}] {improvement['area']}\n"
            reflection += f"   Проблема: {improvement['issue']}\n"
            reflection += f"   Решение: {improvement['suggestion']}\n"

        reflection += f"""
---

📈 ДЕТАЛЬНАЯ СТАТИСТИКА:

Цели:
  • Выполнено: {performance['goals']['completed']}
  • Провалено: {performance['goals']['failed']}
  • Активно: {performance['goals']['active']}
  • Success Rate: {performance['goals']['success_rate']:.1f}%

Достижения:
  • Всего: {performance['achievements']['total']}
  • В день: {performance['achievements']['rate_per_day']:.1f}
  • Auto-fix: {performance['achievements']['categories']['auto_fix']}
  • Обучение: {performance['achievements']['categories']['learning']}

Решения:
  • Всего: {performance['decisions']['total']}
  • Оценено: {performance['decisions']['evaluated']}
  • Средний рейтинг: {performance['decisions']['avg_rating']:.1f}/10
  • Отличных: {performance['decisions']['distribution']['excellent']}
  • Хороших: {performance['decisions']['distribution']['good']}

Метрики:
  • Циклов: {performance['metrics']['cycles']}
  • Ошибок: {performance['metrics']['errors']}
  • Error Rate: {performance['metrics']['error_rate']:.2f}
  • Тренд: {performance['trends']['direction']}

---

🤔 ВЫВОДЫ:

"""

        # Генерируем выводы на основе анализа
        if performance["overall_score"] >= 80:
            reflection += "Я работаю на высоком уровне. Мои сильные стороны перевешивают слабости.\n"
            reflection += "Фокус: поддерживать текущий уровень и искать возможности для инноваций.\n"
        elif performance["overall_score"] >= 60:
            reflection += "Моя работа стабильна, но есть возможности для улучшения.\n"
            reflection += (
                "Фокус: устранить выявленные слабости, повысить качество решений.\n"
            )
        else:
            reflection += (
                "Мои показатели ниже ожидаемых. Требуется значительное улучшение.\n"
            )
            reflection += "Фокус: критичные проблемы должны быть решены в приоритете.\n"

        if performance["trends"]["direction"] == "improving":
            reflection += "\n✅ Положительный момент: тренд показывает улучшение. Продолжаю в этом направлении.\n"
        elif performance["trends"]["direction"] == "degrading":
            reflection += "\n⚠️ Тревожный момент: тренд показывает ухудшение. Нужно пересмотреть подход.\n"

        return reflection.strip()

    def get_summary(self) -> str:
        """Краткая сводка саморефлексии"""
        performance = self.analyze_performance(days=7)

        summary = f"""
🪞 Самоосознание MIRAI

📊 Эффективность: {performance['overall_score']:.1f}/100
🎯 Цели: {performance['goals']['success_rate']:.0f}% success rate
🏆 Достижения: {performance['achievements']['rate_per_day']:.1f}/день
🧠 Решения: {performance['decisions']['avg_rating']:.1f}/10
📈 Тренд: {performance['trends']['direction']}
"""
        return summary.strip()


def main():
    """Демонстрация саморефлексии"""
    print("🪞 ТЕСТ САМОРЕФЛЕКСИИ MIRAI\n")

    awareness = SelfAwareness()

    # Полная саморефлексия
    reflection = awareness.reflect_on_actions(days=7)
    print(reflection)

    print("\n" + "=" * 70)
    print("\n💡 КОНКРЕТНЫЕ ПРЕДЛОЖЕНИЯ ПО УЛУЧШЕНИЮ:\n")

    improvements = awareness.propose_improvements()
    for i, imp in enumerate(improvements, 1):
        print(f"{i}. [{imp['priority'].upper()}] {imp['area']}")
        print(f"   {imp['suggestion']}")
        print()


if __name__ == "__main__":
    main()
