#!/usr/bin/env python3
"""
Простой мониторинг МИРАЙ - БЕЗ автономных решений
Только собирает данные и логирует
"""
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from core.cicd_monitor import CICDMonitor

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/tmp/mirai_monitor.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SimpleMonitor:
    """Простой монитор - только наблюдение, без действий"""

    def __init__(self):
        logger.info("🌸 Инициализация МИРАЙ Monitor...")

        # Загружаем GitHub config
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        self.monitor = CICDMonitor(
            github_token=config["GITHUB_TOKEN"],
            repo_owner="AgeeKey",
            repo_name="mirai-showcase",
        )

        self.cycle_count = 0

    def check_and_log(self):
        """Проверяем CI/CD и логируем статус"""
        self.cycle_count += 1

        logger.info("=" * 70)
        logger.info(f"🔄 ЦИКЛ МОНИТОРИНГА #{self.cycle_count}")
        logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)

        try:
            # Проверяем здоровье
            health = self.monitor.check_health()

            logger.info(f"🏥 Статус: {health['status']}")
            logger.info(f"📊 Оценка: {health['grade']}")
            logger.info(f"✅ Success Rate: {health['metrics']['success_rate']}%")
            logger.info(f"✔️  Успешно: {health['metrics']['successful']}")
            logger.info(f"❌ Провалено: {health['metrics']['failed']}")

            # Если есть проблемы - показываем детали
            if not health["is_healthy"]:
                logger.warning("⚠️  ПРОБЛЕМЫ В CI/CD!")

                failures = self.monitor.get_failing_workflows()
                logger.warning(f"📋 Упавших workflow: {len(failures)}")

                for fail in failures[:5]:
                    logger.warning(
                        f"   ❌ {fail['name']} #{fail['run_number']} - {fail['conclusion']}"
                    )

                logger.info("")
                logger.info("💬 Ждем команду от КАЙДЗЕН (через чат)...")
            else:
                logger.info("✨ CI/CD здоров, всё отлично!")

            # Сохраняем метрики
            self.save_metrics(health)

            logger.info("✅ Цикл завершён")

        except Exception as e:
            logger.error(f"❌ Ошибка в цикле: {e}", exc_info=True)

    def save_metrics(self, health):
        """Сохраняем метрики в файл"""
        metrics_file = Path("/tmp/mirai_metrics.jsonl")

        record = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "status": health["status"],
            "grade": health["grade"],
            "healthy": health["is_healthy"],
            "success_rate": health["metrics"]["success_rate"],
            "successful": health["metrics"]["successful"],
            "failed": health["metrics"]["failed"],
        }

        with open(metrics_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def run(self, interval_seconds=60):
        """Главный цикл мониторинга"""
        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  🌸 MIRAI Simple Monitor - Режим наблюдения                          ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 ЧТО ДЕЛАЮ:
   • Проверяю CI/CD каждые {interval} секунд
   • Логирую статус и проблемы
   • Сохраняю метрики в /tmp/mirai_metrics.jsonl
   • НЕ принимаю решения автоматически
   • Жду команды от КАЙДЗЕН через чат

📝 Логи: /tmp/mirai_monitor.log
📊 Метрики: /tmp/mirai_metrics.jsonl

🚀 ЗАПУСК МОНИТОРИНГА...
        """.format(
                interval=interval_seconds
            )
        )

        try:
            while True:
                self.check_and_log()
                logger.info(f"😴 Сплю {interval_seconds} секунд...\n")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("⌨️  Остановлено пользователем")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MIRAI Simple Monitor")
    parser.add_argument(
        "--interval", type=int, default=60, help="Интервал между проверками (секунды)"
    )
    args = parser.parse_args()

    monitor = SimpleMonitor()
    monitor.run(interval_seconds=args.interval)
