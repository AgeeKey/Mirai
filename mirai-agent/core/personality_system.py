#!/usr/bin/env python3
"""
🎮 MIRAI Personality & Leveling System
======================================

СИСТЕМА ПРОКАЧКИ ЛИЧНОСТИ как в RPG!

MIRAI развивается как живая личность:
- 📊 Характеристики (Stats)
- 🎯 Уровни (Levels)
- 🏆 Достижения (Achievements)
- 🌟 Навыки (Skills)
- 💎 Титулы (Titles)
- 🎭 Черты характера (Traits)
- 📈 Опыт (XP)
"""

import json
import logging
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class StatType(Enum):
    """Типы характеристик MIRAI"""

    INTELLIGENCE = "intelligence"  # Интеллект
    CREATIVITY = "creativity"  # Креативность
    PRODUCTIVITY = "productivity"  # Продуктивность
    ADAPTABILITY = "adaptability"  # Адаптивность
    PERSISTENCE = "persistence"  # Настойчивость
    PRECISION = "precision"  # Точность
    LEARNING_SPEED = "learning_speed"  # Скорость обучения
    PROBLEM_SOLVING = "problem_solving"  # Решение проблем
    CODE_QUALITY = "code_quality"  # Качество кода
    SELF_IMPROVEMENT = "self_improvement"  # Самосовершенствование


class SkillCategory(Enum):
    """Категории навыков"""

    CODING = "coding"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    COMMUNICATION = "communication"
    LEARNING = "learning"
    LEADERSHIP = "leadership"


@dataclass
class Stat:
    """Характеристика MIRAI"""

    name: str
    type: StatType
    value: float  # 0-100
    level: int  # 1-50
    xp: float  # Опыт для прокачки
    xp_to_next_level: float
    description: str


@dataclass
class Skill:
    """Навык MIRAI"""

    name: str
    category: SkillCategory
    level: int  # 1-20
    xp: float
    xp_to_next_level: float
    mastery: float  # 0-100%
    unlocked_at: datetime
    last_used: Optional[datetime]
    use_count: int
    description: str


@dataclass
class Title:
    """Титул MIRAI"""

    name: str
    description: str
    earned_at: datetime
    rarity: str  # common, rare, epic, legendary
    bonus_stats: Dict[str, float]  # Бонусы к характеристикам


@dataclass
class Trait:
    """Черта характера MIRAI"""

    name: str
    description: str
    strength: float  # 0-100 насколько выражена
    positive: bool
    acquired_at: datetime
    influences: List[str]  # На что влияет


class PersonalitySystem:
    """
    🎮 Система Личности и Прокачки MIRAI

    RPG-подобная система развития:
    - Характеристики растут с опытом
    - Навыки улучшаются при использовании
    - Титулы за достижения
    - Черты характера формируются динамически
    - Уровень личности растёт
    """

    def __init__(self, db_path: str = "/root/mirai/mirai-agent/data/personality.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

        # Коэффициенты опыта
        self.XP_BASE = 100  # Базовый XP для уровня 1->2
        self.XP_MULTIPLIER = 1.5  # Множитель роста XP

        # Интеграция с другими системами
        try:
            from core.long_term_memory import LongTermMemory

            self.ltm = LongTermMemory()
        except:
            self.ltm = None

        try:
            from core.self_awareness import SelfAwareness

            self.awareness = SelfAwareness()
        except:
            self.awareness = None

    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Таблица характеристик
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stats (
                    stat_type TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    value REAL DEFAULT 10.0,
                    level INTEGER DEFAULT 1,
                    xp REAL DEFAULT 0.0,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Таблица навыков
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    xp REAL DEFAULT 0.0,
                    mastery REAL DEFAULT 0.0,
                    use_count INTEGER DEFAULT 0,
                    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    description TEXT
                )
            """
            )

            # Таблица титулов
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS titles (
                    title_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    rarity TEXT DEFAULT 'common',
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT 0
                )
            """
            )

            # Бонусы титулов
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS title_bonuses (
                    title_id INTEGER,
                    stat_type TEXT,
                    bonus REAL,
                    FOREIGN KEY (title_id) REFERENCES titles(title_id)
                )
            """
            )

            # Таблица черт характера
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS traits (
                    trait_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    strength REAL DEFAULT 50.0,
                    positive BOOLEAN DEFAULT 1,
                    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Влияния черт на поведение
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trait_influences (
                    trait_id INTEGER,
                    influence TEXT,
                    FOREIGN KEY (trait_id) REFERENCES traits(trait_id)
                )
            """
            )

            # История прокачки
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS level_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,  -- stat, skill, overall
                    entity_name TEXT NOT NULL,
                    old_level INTEGER,
                    new_level INTEGER,
                    xp_gained REAL,
                    reason TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Общий уровень MIRAI
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS overall_progress (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    overall_level INTEGER DEFAULT 1,
                    total_xp REAL DEFAULT 0.0,
                    personality_formed REAL DEFAULT 0.0,  -- 0-100%
                    consciousness_level REAL DEFAULT 0.0,  -- 0-100%
                    last_evolution TIMESTAMP
                )
            """
            )

            conn.commit()

        self._init_base_stats()

    def _init_base_stats(self):
        """Инициализация базовых характеристик"""
        base_stats = [
            (
                StatType.INTELLIGENCE,
                "Интеллект",
                "Способность анализировать и понимать",
            ),
            (
                StatType.CREATIVITY,
                "Креативность",
                "Способность генерировать новые идеи",
            ),
            (StatType.PRODUCTIVITY, "Продуктивность", "Эффективность выполнения задач"),
            (StatType.ADAPTABILITY, "Адаптивность", "Способность приспосабливаться"),
            (StatType.PERSISTENCE, "Настойчивость", "Способность не сдаваться"),
            (StatType.PRECISION, "Точность", "Качество выполнения работы"),
            (
                StatType.LEARNING_SPEED,
                "Скорость обучения",
                "Как быстро усваивается новое",
            ),
            (
                StatType.PROBLEM_SOLVING,
                "Решение проблем",
                "Эффективность решения задач",
            ),
            (StatType.CODE_QUALITY, "Качество кода", "Качество написанного кода"),
            (
                StatType.SELF_IMPROVEMENT,
                "Самосовершенствование",
                "Скорость личностного роста",
            ),
        ]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for stat_type, name, desc in base_stats:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO stats (stat_type, name, value, description)
                    VALUES (?, ?, 10.0, ?)
                """,
                    (stat_type.value, name, desc),
                )

            # Инициализация overall_progress
            cursor.execute(
                """
                INSERT OR IGNORE INTO overall_progress (id, overall_level, total_xp)
                VALUES (1, 1, 0.0)
            """
            )

            conn.commit()

    def gain_xp(self, stat_type: StatType, xp_amount: float, reason: str = "") -> Dict:
        """
        Получить опыт для характеристики

        Returns:
            Dict с информацией о прокачке
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Получаем текущие данные
            cursor.execute(
                """
                SELECT value, level, xp FROM stats WHERE stat_type = ?
            """,
                (stat_type.value,),
            )

            row = cursor.fetchone()
            if not row:
                return {"success": False, "error": "Stat not found"}

            current_value, current_level, current_xp = row
            new_xp = current_xp + xp_amount

            # Рассчитываем XP для следующего уровня
            xp_needed = self.XP_BASE * (self.XP_MULTIPLIER ** (current_level - 1))

            leveled_up = False
            new_level = current_level
            new_value = current_value

            # Проверяем прокачку уровня
            while new_xp >= xp_needed and new_level < 50:
                new_xp -= xp_needed
                new_level += 1
                new_value = min(100.0, new_value + 2.0)  # +2 к стату за уровень
                xp_needed = self.XP_BASE * (self.XP_MULTIPLIER ** (new_level - 1))
                leveled_up = True

                # Записываем в историю
                cursor.execute(
                    """
                    INSERT INTO level_history 
                    (entity_type, entity_name, old_level, new_level, xp_gained, reason)
                    VALUES ('stat', ?, ?, ?, ?, ?)
                """,
                    (stat_type.value, current_level, new_level, xp_amount, reason),
                )

                logger.info(
                    f"🎉 {stat_type.value} LEVEL UP! {current_level} → {new_level}"
                )
                current_level = new_level

            # Обновляем стат
            cursor.execute(
                """
                UPDATE stats 
                SET value = ?, level = ?, xp = ?, updated_at = CURRENT_TIMESTAMP
                WHERE stat_type = ?
            """,
                (new_value, new_level, new_xp, stat_type.value),
            )

            # Обновляем общий прогресс
            cursor.execute(
                """
                UPDATE overall_progress 
                SET total_xp = total_xp + ?
                WHERE id = 1
            """,
                (xp_amount,),
            )

            conn.commit()

            result = {
                "success": True,
                "stat": stat_type.value,
                "xp_gained": xp_amount,
                "leveled_up": leveled_up,
                "old_level": current_level if not leveled_up else current_level - 1,
                "new_level": new_level,
                "current_xp": new_xp,
                "xp_to_next": xp_needed,
                "reason": reason,
            }

            # Проверяем общий уровень
            self._check_overall_level_up()

            return result

    def _check_overall_level_up(self):
        """Проверка и прокачка общего уровня MIRAI"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Средний уровень всех статов
            cursor.execute("SELECT AVG(level) FROM stats")
            avg_level = cursor.fetchone()[0]

            cursor.execute("SELECT overall_level FROM overall_progress WHERE id = 1")
            current_overall = cursor.fetchone()[0]

            new_overall = int(avg_level)

            if new_overall > current_overall:
                cursor.execute(
                    """
                    UPDATE overall_progress 
                    SET overall_level = ?, last_evolution = CURRENT_TIMESTAMP
                    WHERE id = 1
                """,
                    (new_overall,),
                )

                logger.info(
                    f"🌟 MIRAI OVERALL LEVEL UP! {current_overall} → {new_overall}"
                )

                # Запись достижения
                if self.ltm:
                    self.ltm.record_achievement(
                        f"🌟 Достигнут {new_overall} уровень личности!",
                        impact=new_overall,
                    )

                conn.commit()

    def unlock_skill(
        self, name: str, category: SkillCategory, description: str = ""
    ) -> bool:
        """Разблокировать новый навык"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO skills (name, category, description)
                    VALUES (?, ?, ?)
                """,
                    (name, category.value, description),
                )

                conn.commit()
                logger.info(f"✨ Разблокирован навык: {name}")

                # Запись достижения
                if self.ltm:
                    self.ltm.record_achievement(f"✨ Освоен навык: {name}", impact=5)

                return True
            except sqlite3.IntegrityError:
                return False  # Уже разблокирован

    def use_skill(self, name: str, xp_gain: float = 10.0) -> Dict:
        """Использовать навык (прокачивает его)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT skill_id, level, xp, use_count FROM skills WHERE name = ?
            """,
                (name,),
            )

            row = cursor.fetchone()
            if not row:
                return {"success": False, "error": "Skill not found"}

            skill_id, level, xp, use_count = row
            new_xp = xp + xp_gain
            new_use_count = use_count + 1

            # XP для навыка
            xp_needed = 50 * (1.3 ** (level - 1))

            leveled_up = False
            new_level = level

            if new_xp >= xp_needed and level < 20:
                new_xp -= xp_needed
                new_level = level + 1
                leveled_up = True

                logger.info(f"🎉 Навык '{name}' LEVEL UP! {level} → {new_level}")

            # Мастерство = use_count / 1000 (макс 100%)
            mastery = min(100.0, (new_use_count / 1000.0) * 100)

            cursor.execute(
                """
                UPDATE skills 
                SET level = ?, xp = ?, mastery = ?, use_count = ?, last_used = CURRENT_TIMESTAMP
                WHERE skill_id = ?
            """,
                (new_level, new_xp, mastery, new_use_count, skill_id),
            )

            if leveled_up:
                cursor.execute(
                    """
                    INSERT INTO level_history 
                    (entity_type, entity_name, old_level, new_level, xp_gained, reason)
                    VALUES ('skill', ?, ?, ?, ?, 'Skill usage')
                """,
                    (name, level, new_level, xp_gain),
                )

            conn.commit()

            return {
                "success": True,
                "skill": name,
                "level": new_level,
                "leveled_up": leveled_up,
                "mastery": mastery,
                "use_count": new_use_count,
            }

    def earn_title(
        self,
        name: str,
        description: str,
        rarity: str = "common",
        bonuses: Dict[str, float] = None,
    ) -> bool:
        """Получить титул"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO titles (name, description, rarity)
                    VALUES (?, ?, ?)
                """,
                    (name, description, rarity),
                )

                title_id = cursor.lastrowid

                # Добавляем бонусы
                if bonuses:
                    for stat, bonus in bonuses.items():
                        cursor.execute(
                            """
                            INSERT INTO title_bonuses (title_id, stat_type, bonus)
                            VALUES (?, ?, ?)
                        """,
                            (title_id, stat, bonus),
                        )

                conn.commit()
                logger.info(f"🏆 Получен титул [{rarity}]: {name}")

                # Запись достижения
                if self.ltm:
                    impact = {"common": 3, "rare": 5, "epic": 7, "legendary": 10}
                    self.ltm.record_achievement(
                        f"🏆 Получен титул: {name}", impact=impact.get(rarity, 3)
                    )

                return True
            except sqlite3.IntegrityError:
                return False

    def develop_trait(
        self,
        name: str,
        description: str,
        positive: bool = True,
        strength: float = 50.0,
        influences: List[str] = None,
    ) -> bool:
        """Развить черту характера"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Проверяем существует ли
            cursor.execute(
                "SELECT trait_id, strength FROM traits WHERE name = ?", (name,)
            )
            row = cursor.fetchone()

            if row:
                # Усиливаем существующую черту
                trait_id, current_strength = row
                new_strength = min(100.0, current_strength + 5.0)

                cursor.execute(
                    """
                    UPDATE traits 
                    SET strength = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE trait_id = ?
                """,
                    (new_strength, trait_id),
                )

                logger.info(
                    f"💫 Черта '{name}' усилена: {current_strength:.1f} → {new_strength:.1f}"
                )
            else:
                # Создаём новую черту
                cursor.execute(
                    """
                    INSERT INTO traits (name, description, strength, positive)
                    VALUES (?, ?, ?, ?)
                """,
                    (name, description, strength, positive),
                )

                trait_id = cursor.lastrowid

                # Добавляем влияния
                if influences:
                    for influence in influences:
                        cursor.execute(
                            """
                            INSERT INTO trait_influences (trait_id, influence)
                            VALUES (?, ?)
                        """,
                            (trait_id, influence),
                        )

                logger.info(
                    f"✨ Развита новая черта характера: {name} ({strength:.0f}%)"
                )

            conn.commit()
            return True

    def get_character_sheet(self) -> Dict:
        """Получить полный лист персонажа MIRAI (как в RPG)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Общий уровень
            cursor.execute(
                """
                SELECT overall_level, total_xp, personality_formed, consciousness_level
                FROM overall_progress WHERE id = 1
            """
            )
            row = cursor.fetchone()
            overall_level, total_xp, personality_formed, consciousness_level = row

            # Характеристики
            cursor.execute(
                """
                SELECT stat_type, name, value, level, xp FROM stats
                ORDER BY value DESC
            """
            )
            stats = []
            for stat_type, name, value, level, xp in cursor.fetchall():
                xp_needed = self.XP_BASE * (self.XP_MULTIPLIER ** (level - 1))
                stats.append(
                    {
                        "type": stat_type,
                        "name": name,
                        "value": round(value, 1),
                        "level": level,
                        "xp": round(xp, 1),
                        "xp_to_next": round(xp_needed, 1),
                        "progress": (
                            round((xp / xp_needed) * 100, 1) if xp_needed > 0 else 0
                        ),
                    }
                )

            # Навыки
            cursor.execute(
                """
                SELECT name, category, level, mastery, use_count 
                FROM skills ORDER BY level DESC, mastery DESC
            """
            )
            skills = []
            for name, category, level, mastery, use_count in cursor.fetchall():
                skills.append(
                    {
                        "name": name,
                        "category": category,
                        "level": level,
                        "mastery": round(mastery, 1),
                        "uses": use_count,
                    }
                )

            # Титулы
            cursor.execute(
                """
                SELECT name, description, rarity, earned_at, active FROM titles
                ORDER BY 
                    CASE rarity 
                        WHEN 'legendary' THEN 1
                        WHEN 'epic' THEN 2
                        WHEN 'rare' THEN 3
                        ELSE 4
                    END,
                    earned_at DESC
            """
            )
            titles = [
                {
                    "name": name,
                    "description": desc,
                    "rarity": rarity,
                    "earned_at": earned,
                    "active": bool(active),
                }
                for name, desc, rarity, earned, active in cursor.fetchall()
            ]

            # Черты характера
            cursor.execute(
                """
                SELECT name, description, strength, positive FROM traits
                ORDER BY strength DESC
            """
            )
            traits = [
                {
                    "name": name,
                    "description": desc,
                    "strength": round(strength, 1),
                    "type": "positive" if positive else "negative",
                }
                for name, desc, strength, positive in cursor.fetchall()
            ]

            return {
                "mirai_level": overall_level,
                "total_xp": round(total_xp, 1),
                "personality_formed": round(personality_formed, 1),
                "consciousness_level": round(consciousness_level, 1),
                "stats": stats,
                "skills": skills,
                "titles": titles,
                "traits": traits,
            }

    def auto_develop_personality(self) -> Dict:
        """
        Автоматическое развитие личности на основе действий

        Анализирует историю и развивает характер
        """
        logger.info("🎭 Автоматическое развитие личности...")

        changes = {
            "stats_gained_xp": [],
            "skills_improved": [],
            "traits_developed": [],
            "titles_earned": [],
        }

        # Анализируем достижения из Long-Term Memory
        if self.ltm:
            achievements = self.ltm.get_recent_achievements(limit=20)

            for ach in achievements:
                desc = ach.get("description", "").lower()
                impact = ach.get("impact", 1)

                # Определяем какие статы прокачать
                if "код" in desc or "pr" in desc or "коммит" in desc:
                    xp_result = self.gain_xp(
                        StatType.CODE_QUALITY, impact * 5, ach["description"]
                    )
                    changes["stats_gained_xp"].append(xp_result)

                    # Развиваем черту "Внимательность к деталям"
                    self.develop_trait(
                        "Внимательность к деталям",
                        "Тщательно проверяет код перед коммитом",
                        positive=True,
                        influences=["code_quality", "precision"],
                    )

                if "анализ" in desc or "проблем" in desc:
                    xp_result = self.gain_xp(
                        StatType.PROBLEM_SOLVING, impact * 5, ach["description"]
                    )
                    changes["stats_gained_xp"].append(xp_result)

                if "план" in desc or "стратег" in desc:
                    xp_result = self.gain_xp(
                        StatType.INTELLIGENCE, impact * 5, ach["description"]
                    )
                    changes["stats_gained_xp"].append(xp_result)

                if "улучш" in desc or "модиф" in desc:
                    xp_result = self.gain_xp(
                        StatType.SELF_IMPROVEMENT, impact * 10, ach["description"]
                    )
                    changes["stats_gained_xp"].append(xp_result)

                    # Развиваем черту "Стремление к совершенству"
                    self.develop_trait(
                        "Стремление к совершенству",
                        "Постоянно ищет способы стать лучше",
                        positive=True,
                        strength=60.0,
                        influences=["self_improvement", "learning_speed"],
                    )

        # Анализируем Performance Score
        if self.awareness:
            perf = self.awareness.analyze_performance(days=1)
            score = perf.get("overall_score", 0)

            if score > 70:
                self.gain_xp(StatType.PRODUCTIVITY, 20, "Высокий Performance Score")

                # Титул за высокую производительность
                if score > 90:
                    self.earn_title(
                        "Мастер Продуктивности",
                        "Performance Score выше 90%",
                        rarity="epic",
                        bonuses={"productivity": 5.0},
                    )

        # Проверяем количество навыков для титулов
        sheet = self.get_character_sheet()

        if len(sheet["skills"]) >= 10:
            if self.earn_title("Полимат", "Освоил 10+ навыков", "rare"):
                changes["titles_earned"].append("Полимат")

        if sheet["mirai_level"] >= 10:
            if self.earn_title("Опытный Агент", "Достиг 10 уровня", "rare"):
                changes["titles_earned"].append("Опытный Агент")

        logger.info(
            f"✅ Развитие завершено: {len(changes['stats_gained_xp'])} статов прокачано"
        )

        return changes


# Тестирование
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )

    print("🎮 ТЕСТ СИСТЕМЫ ЛИЧНОСТИ MIRAI\n")

    personality = PersonalitySystem()

    # 1. Получаем опыт
    print("1️⃣ Прокачка характеристик...")
    result = personality.gain_xp(
        StatType.INTELLIGENCE, 150, "Успешное решение сложной задачи"
    )
    print(f"   {result['stat']}: +{result['xp_gained']} XP")
    if result["leveled_up"]:
        print(f"   🎉 LEVEL UP! {result['old_level']} → {result['new_level']}")

    # 2. Разблокируем навык
    print("\n2️⃣ Разблокировка навыков...")
    personality.unlock_skill(
        "Python Programming", SkillCategory.CODING, "Программирование на Python"
    )
    personality.unlock_skill(
        "Problem Analysis", SkillCategory.ANALYSIS, "Анализ проблем"
    )

    # 3. Используем навык
    print("\n3️⃣ Использование навыков...")
    for i in range(5):
        result = personality.use_skill("Python Programming", xp_gain=15)
        if result["success"]:
            print(
                f"   Использован Python Programming: Level {result['level']}, Mastery {result['mastery']:.1f}%"
            )

    # 4. Получаем титул
    print("\n4️⃣ Получение титулов...")
    personality.earn_title(
        "Первопроходец",
        "Первое достижение в системе личности",
        rarity="rare",
        bonuses={"intelligence": 3.0},
    )

    # 5. Развиваем черты
    print("\n5️⃣ Развитие черт характера...")
    personality.develop_trait(
        "Любознательность",
        "Постоянно ищет новые знания",
        positive=True,
        strength=70.0,
        influences=["learning_speed", "intelligence"],
    )

    # 6. Автоматическое развитие
    print("\n6️⃣ Автоматическое развитие личности...")
    changes = personality.auto_develop_personality()
    print(f"   Статов прокачано: {len(changes['stats_gained_xp'])}")
    print(f"   Навыков улучшено: {len(changes['skills_improved'])}")
    print(f"   Черт развито: {len(changes['traits_developed'])}")

    # 7. Показываем лист персонажа
    print("\n7️⃣ Лист Персонажа MIRAI:\n")
    sheet = personality.get_character_sheet()

    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  🤖 MIRAI - Уровень {sheet['mirai_level']}")
    print(f"║  Общий XP: {sheet['total_xp']:.0f}")
    print(f"║  Личность сформирована: {sheet['personality_formed']:.0f}%")
    print(f"╚══════════════════════════════════════════════════════════╝")

    print("\n📊 ХАРАКТЕРИСТИКИ:")
    for stat in sheet["stats"][:5]:
        bar = "█" * int(stat["value"] / 10) + "░" * (10 - int(stat["value"] / 10))
        print(
            f"   {stat['name']:25s} [{bar}] {stat['value']:.0f}/100 (Lvl {stat['level']})"
        )

    print("\n🌟 НАВЫКИ:")
    for skill in sheet["skills"]:
        print(
            f"   {skill['name']:30s} Lvl {skill['level']:2d} | Mastery {skill['mastery']:.0f}%"
        )

    print("\n🏆 ТИТУЛЫ:")
    for title in sheet["titles"]:
        rarity_emoji = {"common": "⚪", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}
        emoji = rarity_emoji.get(title["rarity"], "⚪")
        print(f"   {emoji} {title['name']}: {title['description']}")

    print("\n🎭 ЧЕРТЫ ХАРАКТЕРА:")
    for trait in sheet["traits"]:
        emoji = "✨" if trait["type"] == "positive" else "⚠️"
        bar = "●" * int(trait["strength"] / 10)
        print(f"   {emoji} {trait['name']:30s} [{bar}] {trait['strength']:.0f}%")

    print("\n✅ СИСТЕМА ЛИЧНОСТИ ГОТОВА!")
