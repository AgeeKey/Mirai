#!/usr/bin/env python3
"""
🤖 KAIZEN × 🌸 MIRAI - Autonomous Background Service
Работают автономно в фоне, результаты в логи + web dashboard
"""

import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent
from core.cicd_monitor import CICDMonitor
from core.nasa_level.orchestrator import NASALearningOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("/tmp/kaizen_mirai.log"), logging.StreamHandler()],
)

logger = logging.getLogger("KAIZEN_MIRAI")


class AutonomousService:
    """Автономный сервис KAIZEN + MIRAI"""

    def __init__(self):
        logger.info("🤖 Инициализация KAIZEN...")
        self.kaizen = AutonomousAgent()

        logger.info("🌸 Инициализация MIRAI...")
        self.mirai = AutonomousAgent()

        # Load GitHub config
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        logger.info("📊 Инициализация CI/CD Monitor...")
        self.monitor = CICDMonitor(
            github_token=config["GITHUB_TOKEN"],
            repo_owner="AgeeKey",
            repo_name="mirai-showcase",
        )

        logger.info("🚀 Инициализация NASA-Level Learning System...")
        self.nasa_learning = NASALearningOrchestrator()
        logger.info("✅ NASA-Level Learning System готова!")

        logger.info("🧠 Инициализация Long-Term Memory...")
        from core.long_term_memory import LongTermMemory

        self.memory = LongTermMemory()
        logger.info("✅ Long-Term Memory готова!")

        logger.info("🪞 Инициализация Self-Awareness...")
        from core.self_awareness import SelfAwareness

        self.awareness = SelfAwareness()
        logger.info("✅ Self-Awareness готова!")

        logger.info("📋 Инициализация Auto-Planner...")
        from core.auto_planner import AutoPlanner

        self.planner = AutoPlanner()
        logger.info("✅ Auto-Planner готов!")

        logger.info("🔧 Инициализация Self-Modification...")
        from core.self_modification import SelfModification

        self.self_mod = SelfModification()
        logger.info("✅ Self-Modification готова!")
        logger.info("⚠️ ПОЛНЫЕ ПРАВА НА МОДИФИКАЦИЮ ПОЛУЧЕНЫ!")

        logger.info("🎮 Инициализация Personality System...")
        from core.personality_system import PersonalitySystem

        self.personality = PersonalitySystem()
        logger.info("✅ Personality System готова!")
        logger.info("🎭 MIRAI развивается как личность!")

        self.running = True
        self.cycle_count = 0

        # Handle signals
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        """Graceful shutdown"""
        logger.info("🛑 Получен сигнал остановки...")
        self.running = False

    def _init_initial_goals(self):
        """Инициализация начальных целей при первом запуске"""
        from datetime import timedelta

        # Проверяем есть ли уже активные цели
        active_goals = self.memory.get_active_goals()
        if len(active_goals) > 0:
            logger.info(f"🎯 Найдено {len(active_goals)} активных целей")
            return

        logger.info("🎯 Инициализация начальных целей...")

        # Цель 1: Автономность
        self.memory.set_goal(
            title="Достичь полной автономности",
            description="Автоматически создавать PR, исправлять код, обучаться новым технологиям",
            priority=10,
            deadline=(datetime.now() + timedelta(days=30)).isoformat(),
        )

        # Цель 2: Качество кода
        self.memory.set_goal(
            title="Поддерживать CI/CD success rate > 90%",
            description="Мониторить GitHub Actions, автоматически исправлять падающие тесты",
            priority=9,
        )

        # Цель 3: Обучение
        self.memory.set_goal(
            title="Изучить 10+ новых технологий",
            description="Через NASA-Level Learning System изучать современные технологии",
            priority=7,
            deadline=(datetime.now() + timedelta(days=60)).isoformat(),
        )

        # Цель 4: База знаний
        self.memory.set_goal(
            title="Построить исчерпывающую базу знаний",
            description="Каталогизировать все ошибки, решения, паттерны",
            priority=6,
        )

        logger.info("✅ Начальные цели установлены!")

    def log_separator(self):
        """Красивый разделитель в логах"""
        logger.info("=" * 70)

    def consult_mirai(self, question: str) -> str:
        """KAIZEN консультируется с MIRAI"""
        logger.info("🤖 КАЙДЗЕН спрашивает МИРАЙ...")
        response = self.mirai.think(question, max_iterations=1)
        logger.info(f"🌸 МИРАЙ отвечает: {response[:100]}...")
        return response

    def autonomous_learning(self):
        """Автономное обучение через NASA-Level систему"""
        logger.info("🎓 Запуск автономного обучения...")

        # Получаем рекомендации от MIRAI о том, что изучить
        question = """
        Ты МИРАЙ. Выбери 1-2 Python библиотеки, которые стоит изучить сейчас.
        Выбирай полезные для автоматизации, мониторинга или AI.
        
        Формат ответа: просто названия библиотек через запятую.
        Например: prometheus-client, aiohttp
        """

        mirai_recommendation = self.consult_mirai(question)
        logger.info(f"📚 МИРАЙ рекомендует изучить: {mirai_recommendation}")

        # Парсим рекомендации
        technologies = [t.strip() for t in mirai_recommendation.split(",")[:2]]

        # KAIZEN изучает каждую технологию
        for tech in technologies:
            # Очищаем название от лишних символов
            tech = tech.strip().strip("'\"").strip()
            if not tech or len(tech) > 50:
                continue

            logger.info(f"🚀 КАЙДЗЕН начинает изучение: {tech}")

            try:
                result = self.nasa_learning.learn_technology(tech, depth="basic")

                if result.success:
                    logger.info(f"✅ Успешно изучил {tech}!")
                    logger.info(f"   📊 Профессиональность: {result.proficiency:.1f}%")
                    logger.info(f"   🎯 Качество кода: {result.quality_grade}")
                    logger.info(f"   ⏱️  Время: {result.execution_time:.1f}s")
                else:
                    error_msg = result.errors[0] if result.errors else "Unknown error"
                    logger.warning(f"⚠️  Не удалось изучить {tech}: {error_msg}")

            except Exception as e:
                logger.error(f"❌ Ошибка при изучении {tech}: {e}")

        # Показываем статистику обучения
        status = self.nasa_learning.get_status()
        kb_stats = status.get("knowledge", {})
        metrics_summary = status.get("metrics", {})

        logger.info(f"📊 Статистика обучения:")
        logger.info(
            f"   • Всего изучено: {kb_stats.get('total_entries', 0)} технологий"
        )
        logger.info(f"   • Success rate: {metrics_summary.get('success_rate', 0):.1f}%")
        logger.info(
            f"   • Средняя профессиональность: {kb_stats.get('average_proficiency', 0):.1f}%"
        )

    def autonomous_cycle(self):
        """Один цикл автономной работы"""
        self.cycle_count += 1

        self.log_separator()
        logger.info(f"🔄 АВТОНОМНЫЙ ЦИКЛ #{self.cycle_count}")
        logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_separator()

        try:
            # 1. Проверяем здоровье CI/CD
            logger.info("📊 Проверяю здоровье CI/CD...")
            health = self.monitor.check_health()

            logger.info(f"🏥 Статус: {health['status']} | Оценка: {health['grade']}")
            logger.info(f"✅ Success Rate: {health['metrics']['success_rate']}%")

            # 2. Если есть проблемы - советуемся с MIRAI
            if not health["is_healthy"]:
                logger.warning("⚠️  CI/CD НЕ ЗДОРОВ! Консультируюсь с МИРАЙ...")

                # Получаем список упавших тестов
                failures = self.monitor.get_failing_workflows()
                failures_text = "\n".join(
                    f"   • {f['name']} #{f['run_number']}" for f in failures[:5]
                )

                question = f"""
🚨 СРОЧНО МИРАЙ! CI/CD проблемы уже {self.cycle_count} циклов!

📊 Текущий статус:
• Статус: {health['status']}
• Оценка: {health['grade']}
• Success Rate: {health['metrics']['success_rate']}%
• Провалов: {health['metrics']['failed']}

❌ Упавшие тесты:
{failures_text}

💡 Ты уже несколько раз выбирала "2. Анализировать логи", но проблема НЕ РЕШЕНА!
Пора переходить к КОНКРЕТНЫМ ДЕЙСТВИЯМ!

🎯 НОВЫЕ ВАРИАНТЫ (ВЫБЕРИ ОДНО):
1. ИСПРАВИТЬ ТЕСТЫ - я создам PR с фиксами
2. ОТКЛЮЧИТЬ ПРОБЛЕМНЫЕ ТЕСТЫ - временно skip
3. ОБНОВИТЬ ЗАВИСИМОСТИ - возможно устаревшие пакеты
4. УПРОСТИТЬ CI/CD - убрать лишние проверки
5. СОЗДАТЬ GITHUB ISSUE - задокументировать проблему
6. ПЕРЕЗАПУСТИТЬ ТЕСТЫ - может глюк

Формат ответа: "Выбираю [номер]. [Почему именно это действие сейчас эффективно]"
"""

                mirai_decision = self.consult_mirai(question)
                logger.info(f"💡 Решение МИРАЙ: {mirai_decision}")

                # KAIZEN выполняет решение MIRAI - РЕАЛЬНЫЕ ДЕЙСТВИЯ!
                from core.real_tasks import RealTaskExecutor

                executor = RealTaskExecutor()

                if "1" in mirai_decision or "исправить" in mirai_decision.lower():
                    logger.info("🔧 КАЙДЗЕН: Создаю issue для исправлений...")
                    result = executor.task2_monitor_cicd_and_create_issue(health)
                    logger.info(
                        f"   ✅ {result['status']}: {result.get('action', 'N/A')}"
                    )

                elif "5" in mirai_decision or "issue" in mirai_decision.lower():
                    logger.info("📋 КАЙДЗЕН: Создаю GitHub Issue...")
                    result = executor.task2_monitor_cicd_and_create_issue(health)
                    logger.info(
                        f"   ✅ {result['status']}: {result.get('issue_file', 'monitoring')}"
                    )

                else:
                    # По умолчанию - анализ логов и обновление базы знаний
                    logger.info("🔍 КАЙДЗЕН: Анализирую логи и обновляю базу знаний...")
                    result1 = executor.task3_build_knowledge_base()
                    logger.info(
                        f"   ✅ База знаний: {result1['summary']['unique_patterns']} паттернов"
                    )

                    for fail in failures[:3]:
                        logger.warning(f"   ❌ {fail['name']} #{fail['run_number']}")
            else:
                logger.info("✨ Всё отлично! CI/CD здоров.")

            # 3. Каждые 3 цикла - автономное обучение через NASA-Level
            if self.cycle_count % 3 == 0:
                logger.info("🎓 Время для автономного обучения...")
                self.autonomous_learning()

            # 4. Каждые 5 циклов - спрашиваем MIRAI что улучшить
            if self.cycle_count % 5 == 0:
                logger.info("💭 Время для планирования улучшений...")

                question = """
                Ты МИРАЙ. Прошло 5 циклов мониторинга.
                
                Что улучшить дальше?
                1. Добавить новые метрики в dashboard
                2. Оптимизировать скорость тестов
                3. Создать новые примеры кода
                4. Интегрировать новый сервис
                
                Выбери ОДНО и скажи почему кратко.
                """

                improvement = self.consult_mirai(question)
                logger.info(f"🎯 План улучшений от МИРАЙ: {improvement}")

            # 5. Регулярные задачи каждый цикл
            from core.real_tasks import RealTaskExecutor

            executor = RealTaskExecutor()

            # Каждый цикл - обновляем метрики и dashboard
            logger.info("📊 Обновляю метрики и dashboard...")
            metrics_result = executor.task4_update_metrics_dashboard()

            # Каждые 12 циклов (~1 час) - создаём отчёт по логам
            if self.cycle_count % 12 == 0:
                logger.info("📝 Создаю ежечасный отчёт...")
                report_result = executor.task1_analyze_logs_and_report()
                logger.info(f"   ✅ Отчёт создан: {report_result['report_file']}")

            # Каждые 6 циклов (~30 минут) - автоисправление кода
            if self.cycle_count % 6 == 0:
                logger.info("🤖 Проверяю нужно ли исправить код...")
                autofix_result = executor.task5_auto_fix_code()
                if autofix_result["status"] == "✅ SUCCESS":
                    logger.info(
                        f"   ✅ PR создан: {autofix_result['pr_url']} (#{autofix_result['pr_number']})"
                    )
                    # Записываем достижение в долгосрочную память
                    self.memory.record_achievement(
                        description=f"Auto-fix PR #{autofix_result['pr_number']}",
                        result=f"Fixed: {autofix_result.get('file_fixed', 'unknown file')}",
                    )
                elif autofix_result["status"] == "✅ SKIP":
                    logger.info(f"   ⏭️ Пропущено: {autofix_result['reason']}")
                else:
                    logger.warning(
                        f"   ⚠️ Не удалось: {autofix_result.get('error', 'Unknown')}"
                    )

            # Каждые 24 цикла (~2 часа) - показываем сводку памяти
            if self.cycle_count % 24 == 0:
                logger.info("🧠 Долгосрочная память:")
                summary = self.memory.get_summary()
                for line in summary.split("\n"):
                    logger.info(f"   {line}")

            # Каждые 48 циклов (~4 часа) - саморефлексия
            if self.cycle_count % 48 == 0:
                logger.info("🪞 Провожу саморефлексию...")

                # Краткая сводка
                awareness_summary = self.awareness.get_summary()
                for line in awareness_summary.split("\n"):
                    logger.info(f"   {line}")

                # Предложения по улучшению
                improvements = self.awareness.propose_improvements()
                if improvements:
                    logger.info("   💡 Топ-3 предложения по улучшению:")
                    for i, imp in enumerate(improvements[:3], 1):
                        logger.info(
                            f"      {i}. [{imp['priority']}] {imp['area']}: {imp['suggestion']}"
                        )

                # Записываем решение о самоулучшении
                if improvements and improvements[0]["priority"] in [
                    "критичный",
                    "высокий",
                ]:
                    decision_id = self.memory.record_decision(
                        context=f"Саморефлексия выявила: {improvements[0]['issue']}",
                        decision=f"Применить: {improvements[0]['suggestion']}",
                        reasoning=f"Критичность: {improvements[0]['priority']}",
                    )
                    logger.info(
                        f"   📝 Решение о самоулучшении записано (ID: {decision_id})"
                    )

            # Каждое утро (первый цикл дня) - создаём план на день
            current_hour = datetime.now().hour
            if current_hour >= 6 and current_hour < 7:  # Между 6 и 7 утра
                if self.cycle_count % 12 == 0:  # Раз в час проверяем
                    logger.info("📋 Создаю план на день...")
                    daily_plan = self.planner.create_daily_plan()
                    logger.info(f"   Фокус дня: {daily_plan['focus_area']}")
                    logger.info(f"   Задач: {daily_plan['total_tasks']}")
                    logger.info(f"   Часов: {daily_plan['estimated_hours']:.1f}")

            # Каждое воскресенье - создаём план на неделю
            if datetime.now().weekday() == 6:  # Воскресенье
                if self.cycle_count % 24 == 0:  # Раз в 2 часа проверяем
                    logger.info("📆 Создаю план на неделю...")
                    weekly_plan = self.planner.create_weekly_plan()
                    logger.info(f"   Стратегия: {weekly_plan['strategy']}")
                    logger.info(f"   Целей: {weekly_plan['total_goals']}")

            # Каждый вечер (около 22:00) - ревью выполнения плана
            if current_hour >= 22 and current_hour < 23:
                if self.cycle_count % 12 == 0:
                    logger.info("📊 Анализирую выполнение плана...")
                    review = self.planner.review_plan_execution()
                    if review.get("status") != "no_plan":
                        logger.info(
                            f"   Completion Rate: {review['completion_rate']:.1f}%"
                        )
                        logger.info(f"   Статус: {review['status']}")
                        logger.info(
                            f"   Достижений сегодня: {review['achievements_today']}"
                        )

                        # Адаптируем план на завтра
                        adaptation = self.planner.adapt_plan()
                        logger.info(f"   💡 Адаптация: {adaptation['message']}")

                # 7. 🔧 Самомодификация (раз в 7 дней = каждые 2016 циклов по 5 минут)
                # ИЛИ раз в неделю в воскресенье вечером
                if datetime.now().weekday() == 6:  # Воскресенье
                    if current_hour >= 23 and current_hour < 24:  # 23:00-24:00
                        if self.cycle_count % 12 == 0:  # Раз в час в это время
                            logger.info(
                                "🔧 ЗАПУСК САМОМОДИФИКАЦИИ (раз в неделю, воскресенье вечером)"
                            )
                            try:
                                summary = self.self_mod.run_self_improvement_cycle()
                                logger.info(
                                    f"   ✅ Цикл завершён за {summary['duration_seconds']:.1f}с"
                                )
                                logger.info(
                                    f"   📊 Проанализировано: {summary['analysis']['files_analyzed']} файлов"
                                )
                                logger.info(
                                    f"   ⚠️ Проблем: {summary['analysis']['total_issues']} ({summary['analysis']['high_priority_issues']} критичных)"
                                )
                                logger.info(
                                    f"   💡 Предложено: {summary['improvements_proposed']} улучшений"
                                )
                                logger.info(
                                    f"   🔧 Применено: {summary['improvements_applied']} улучшений"
                                )

                                if summary["improvements_applied"] > 0:
                                    for mod in summary["applied"]:
                                        logger.info(
                                            f"   ✅ PR #{mod['pr_number']}: {mod['improvement']['solution'][:50]}..."
                                        )
                            except Exception as e:
                                logger.error(
                                    f"❌ Ошибка самомодификации: {e}", exc_info=True
                                )

                # 8. 🎭 Развитие Личности (каждые 6 часов = каждые 72 цикла)
                if self.cycle_count % 72 == 0:
                    logger.info("🎭 РАЗВИТИЕ ЛИЧНОСТИ (каждые 6 часов)")
                    try:
                        changes = self.personality.auto_develop_personality()

                        if changes["stats_gained_xp"]:
                            logger.info(
                                f"   📊 Прокачано {len(changes['stats_gained_xp'])} характеристик"
                            )
                            # Показываем level ups
                            for xp_result in changes["stats_gained_xp"]:
                                if xp_result.get("leveled_up"):
                                    logger.info(
                                        f"   🎉 {xp_result['stat']} LEVEL UP! {xp_result['old_level']} → {xp_result['new_level']}"
                                    )

                        if changes["titles_earned"]:
                            logger.info(
                                f"   🏆 Получено титулов: {len(changes['titles_earned'])}"
                            )
                            for title in changes["titles_earned"]:
                                logger.info(f"   🏆 {title}")

                        # Показываем лист персонажа раз в день
                        if self.cycle_count % 288 == 0:  # Раз в сутки
                            sheet = self.personality.get_character_sheet()
                            logger.info(
                                f"   🤖 MIRAI Level {sheet['mirai_level']} | XP: {sheet['total_xp']:.0f}"
                            )
                            logger.info(
                                f"   🎭 Личность: {sheet['personality_formed']:.0f}% | Сознание: {sheet['consciousness_level']:.0f}%"
                            )
                            logger.info(f"   🌟 Навыков: {len(sheet['skills'])}")
                            logger.info(f"   🏆 Титулов: {len(sheet['titles'])}")
                            logger.info(f"   🎭 Черт характера: {len(sheet['traits'])}")

                    except Exception as e:
                        logger.error(f"❌ Ошибка развития личности: {e}", exc_info=True)

            # 6. Логируем метрики для истории
            self.save_metrics(health["metrics"])

            logger.info("✅ Цикл завершён успешно")

        except Exception as e:
            logger.error(f"❌ Ошибка в цикле: {e}", exc_info=True)

    def save_metrics(self, metrics):
        """Сохраняем метрики для истории"""
        metrics_file = Path("/tmp/kaizen_mirai_metrics.jsonl")

        record = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            **metrics,
        }

        with open(metrics_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def run(self, interval_seconds=300):
        """Главный цикл - работаем автономно в фоне"""
        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  🤖 KAIZEN × 🌸 MIRAI - Autonomous Service Started                  ║
╚══════════════════════════════════════════════════════════════════════╝

🌸 РЕШЕНИЕ МИРАЙ: Работаем автономно в фоне
   
   "Такой режим позволяет AI-агентам работать без постоянного
   взаимодействия с пользователями, что увеличивает эффективность
   выполнения задач и автоматизацию процессов."

🤖 КАЙДЗЕН: Реализую решение МИРАЙ!

📋 РЕЖИМ РАБОТЫ:
   • Автономные циклы каждые {interval} секунд
   • Мониторинг CI/CD GitHub Actions
   • Консультации между KAIZEN ↔ MIRAI
   • Логи в /tmp/kaizen_mirai.log
   • Метрики в /tmp/kaizen_mirai_metrics.jsonl
   • Dashboard на http://localhost:5000

🎯 ЧТО ДЕЛАЕМ:
   1. Проверяем здоровье CI/CD
   2. При проблемах - MIRAI принимает решения
   3. Каждые 5 циклов - планируем улучшения
   4. Сохраняем метрики для анализа

🚀 ЗАПУСК АВТОНОМНОГО РЕЖИМА...
        """.format(
                interval=interval_seconds
            )
        )

        # Инициализируем начальные цели при первом запуске
        self._init_initial_goals()

        while self.running:
            try:
                self.autonomous_cycle()

                if self.running:
                    logger.info(
                        f"😴 Сплю {interval_seconds} секунд до следующего цикла..."
                    )
                    time.sleep(interval_seconds)

            except KeyboardInterrupt:
                logger.info("⌨️  Прервано пользователем")
                break
            except Exception as e:
                logger.error(f"💥 Критическая ошибка: {e}", exc_info=True)
                time.sleep(60)  # Wait before retry

        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  👋 KAIZEN × MIRAI - Autonomous Service Stopped                     ║
╚══════════════════════════════════════════════════════════════════════╝

🤖 КАЙДЗЕН: Останавливаем автономный режим.
🌸 МИРАЙ: До встречи, ониичан!

📊 Статистика сессии:
   • Циклов выполнено: {cycles}
   • Логи: /tmp/kaizen_mirai.log
   • Метрики: /tmp/kaizen_mirai_metrics.jsonl

改善 (Kaizen) - Continuous Improvement
未来 (Mirai) - Future
        """.format(
                cycles=self.cycle_count
            )
        )


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="KAIZEN × MIRAI Autonomous Service")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Интервал между циклами в секундах (default: 300)",
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Запустить как daemon в фоне"
    )

    args = parser.parse_args()

    if args.daemon:
        # Fork process to background
        pid = os.fork()
        if pid > 0:
            print(f"🚀 Daemon запущен с PID: {pid}")
            print(f"📋 Логи: /tmp/kaizen_mirai.log")
            print(f"🛑 Остановка: kill {pid}")
            sys.exit(0)

    service = AutonomousService()
    service.run(interval_seconds=args.interval)


if __name__ == "__main__":
    main()
