#!/usr/bin/env python3
"""
🎯 РЕАЛЬНЫЕ Задачи для MIRAI
Замена "TODO" на конкретные действия с измеримым результатом
"""

import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class RealTaskExecutor:
    """Выполняет реальные задачи вместо TODO"""

    def __init__(self, base_dir: str = "/root/mirai"):
        self.base_dir = Path(base_dir)
        self.reports_dir = self.base_dir / "reports"
        self.metrics_dir = self.base_dir / "metrics"
        self.knowledge_dir = self.base_dir / "knowledge_base"

        # Создаём директории
        self.reports_dir.mkdir(exist_ok=True)
        self.metrics_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)

    def task1_analyze_logs_and_report(self) -> Dict:
        """
        ЗАДАЧА 1: Анализ Логов и Создание Отчёта

        Измеримый результат: Файл reports/daily_analysis_YYYY-MM-DD.md создан
        """
        print("🔍 Начинаю анализ логов...")

        # Читаем логи за последние 24 часа
        logs = self._read_journalctl_logs(since="24 hours ago")

        # Анализируем
        analysis = self._analyze_logs(logs)

        # Создаём отчёт
        report_date = datetime.now().strftime("%Y-%m-%d")
        report_content = self._generate_report(analysis, report_date)

        # Сохраняем отчёт
        report_file = self.reports_dir / f"daily_analysis_{report_date}.md"
        report_file.write_text(report_content, encoding="utf-8")

        # Сохраняем JSON со статистикой
        stats_file = self.reports_dir / f"daily_stats_{report_date}.json"
        stats_file.write_text(
            json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        result = {
            "task": "analyze_logs_and_report",
            "status": "COMPLETED",
            "timestamp": datetime.now().isoformat(),
            "report_file": str(report_file),
            "stats_file": str(stats_file),
            "summary": {
                "total_lines": analysis["total_lines"],
                "errors": analysis["error_count"],
                "warnings": analysis["warning_count"],
                "autonomous_cycles": analysis["autonomous_cycles"],
            },
        }

        print(f"✅ Отчёт создан: {report_file}")
        print(f"✅ Статистика: {stats_file}")

        return result

    def _read_journalctl_logs(self, since: str = "24 hours ago") -> List[str]:
        """Читает логи из journalctl"""
        try:
            cmd = ["sudo", "journalctl", "-u", "mirai", "--since", since, "--no-pager"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return result.stdout.split("\n")
            else:
                print(f"⚠️ Ошибка чтения логов: {result.stderr}")
                return []
        except Exception as e:
            print(f"❌ Не удалось прочитать логи: {e}")
            return []

    def _analyze_logs(self, logs: List[str]) -> Dict:
        """Анализирует логи и извлекает статистику"""

        analysis = {
            "total_lines": len(logs),
            "error_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "autonomous_cycles": 0,
            "todo_count": 0,
            "errors": [],
            "warnings": [],
            "top_messages": [],
            "cycle_numbers": [],
            "timestamp_first": None,
            "timestamp_last": None,
        }

        # Паттерны для поиска
        error_pattern = re.compile(
            r"(ERROR|error|ошибка|failed|failure)", re.IGNORECASE
        )
        warning_pattern = re.compile(r"(WARNING|warning|предупреждение)", re.IGNORECASE)
        cycle_pattern = re.compile(r"АВТОНОМНЫЙ ЦИКЛ #(\d+)")
        todo_pattern = re.compile(r"TODO:", re.IGNORECASE)

        message_counter = Counter()

        for line in logs:
            if not line.strip():
                continue

            # Считаем ошибки
            if error_pattern.search(line):
                analysis["error_count"] += 1
                # Сохраняем первые 10 уникальных ошибок
                if len(analysis["errors"]) < 10:
                    error_msg = line.split(":", 3)[-1].strip()[:200]
                    if error_msg and error_msg not in analysis["errors"]:
                        analysis["errors"].append(error_msg)

            # Считаем предупреждения
            if warning_pattern.search(line):
                analysis["warning_count"] += 1
                if len(analysis["warnings"]) < 10:
                    warn_msg = line.split(":", 3)[-1].strip()[:200]
                    if warn_msg and warn_msg not in analysis["warnings"]:
                        analysis["warnings"].append(warn_msg)

            # Считаем циклы
            cycle_match = cycle_pattern.search(line)
            if cycle_match:
                analysis["autonomous_cycles"] += 1
                cycle_num = int(cycle_match.group(1))
                analysis["cycle_numbers"].append(cycle_num)

            # Считаем TODO
            if todo_pattern.search(line):
                analysis["todo_count"] += 1

            # Считаем частые сообщения
            if any(
                keyword in line
                for keyword in ["🤖", "🌸", "✅", "❌", "КАЙДЗЕН", "MIRAI"]
            ):
                msg = line.split(":", 3)[-1].strip()[:100]
                if msg:
                    message_counter[msg] += 1

            # INFO сообщения
            if "INFO" in line or "info" in line:
                analysis["info_count"] += 1

        # Топ сообщений
        analysis["top_messages"] = [
            {"message": msg, "count": count}
            for msg, count in message_counter.most_common(10)
        ]

        # Временные метки
        if logs:
            for line in logs:
                if line.strip():
                    analysis["timestamp_first"] = line.split()[0:3]
                    break
            for line in reversed(logs):
                if line.strip():
                    analysis["timestamp_last"] = line.split()[0:3]
                    break

        return analysis

    def _generate_report(self, analysis: Dict, date: str) -> str:
        """Генерирует Markdown отчёт"""

        report = f"""# 📊 Ежедневный Анализ Логов MIRAI

**Дата:** {date}
**Период:** Последние 24 часа
**Сгенерировано:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 Общая Статистика

- **Всего строк логов:** {analysis['total_lines']:,}
- **Ошибки:** {analysis['error_count']:,}
- **Предупреждения:** {analysis['warning_count']:,}
- **Инфо сообщения:** {analysis['info_count']:,}
- **Автономных циклов:** {analysis['autonomous_cycles']:,}
- **TODO записей:** {analysis['todo_count']:,}

---

## 🔴 Топ Ошибок

"""

        if analysis["errors"]:
            for i, error in enumerate(analysis["errors"], 1):
                report += f"{i}. `{error}`\n"
        else:
            report += "*Ошибок не найдено* ✅\n"

        report += "\n---\n\n## ⚠️ Топ Предупреждений\n\n"

        if analysis["warnings"]:
            for i, warning in enumerate(analysis["warnings"], 1):
                report += f"{i}. `{warning}`\n"
        else:
            report += "*Предупреждений не найдено* ✅\n"

        report += "\n---\n\n## 💬 Топ Сообщений (Частота)\n\n"

        for item in analysis["top_messages"][:5]:
            report += f"- `{item['message']}` - **{item['count']}** раз\n"

        report += "\n---\n\n## 🔄 Автономные Циклы\n\n"

        if analysis["cycle_numbers"]:
            report += f"- **Минимальный цикл:** #{min(analysis['cycle_numbers'])}\n"
            report += f"- **Максимальный цикл:** #{max(analysis['cycle_numbers'])}\n"
            report += (
                f"- **Всего выполнено:** {len(analysis['cycle_numbers'])} циклов\n"
            )
        else:
            report += "*Циклы не найдены*\n"

        report += "\n---\n\n## 🚨 TODO Проблема\n\n"

        if analysis["todo_count"] > 0:
            report += (
                f"⚠️ **ВНИМАНИЕ:** Найдено {analysis['todo_count']} записей TODO!\n\n"
            )
            report += "Это значит что MIRAI логирует намерения, но не выполняет их.\n"
            report += "**Требуется:** Заменить TODO на реальную имплементацию.\n"
        else:
            report += "✅ TODO записей не найдено - MIRAI работает корректно!\n"

        report += "\n---\n\n## 📊 Оценка Здоровья\n\n"

        # Вычисляем оценку здоровья
        health_score = 100

        if analysis["error_count"] > 10:
            health_score -= 30
        elif analysis["error_count"] > 5:
            health_score -= 15

        if analysis["todo_count"] > 10:
            health_score -= 20
        elif analysis["todo_count"] > 5:
            health_score -= 10

        if analysis["warning_count"] > 20:
            health_score -= 10

        if analysis["autonomous_cycles"] == 0:
            health_score -= 40

        if health_score >= 90:
            grade = "🟢 ОТЛИЧНО"
        elif health_score >= 70:
            grade = "🟡 ХОРОШО"
        elif health_score >= 50:
            grade = "🟠 УДОВЛЕТВОРИТЕЛЬНО"
        else:
            grade = "🔴 ТРЕБУЕТ ВНИМАНИЯ"

        report += f"**Оценка:** {health_score}/100 - {grade}\n\n"

        report += "---\n\n*Отчёт сгенерирован автоматически MIRAI Real Task Executor*\n"

        return report

    def task2_monitor_cicd_and_create_issue(self, health_data: Dict) -> Dict:
        """
        ЗАДАЧА 2: Мониторинг CI/CD и Создание GitHub Issue

        Измеримый результат: Issue создан в GitHub или записан в файл
        """
        print("🔍 Мониторю CI/CD и создаю issue при проблемах...")

        status = health_data.get("status", "UNKNOWN")
        grade = health_data.get("grade", "N/A")

        # Проверяем счётчик проблем
        counter_file = self.metrics_dir / "cicd_unhealthy_counter.json"

        if counter_file.exists():
            counter_data = json.loads(counter_file.read_text())
            count = counter_data.get("count", 0)
            last_issue_date = counter_data.get("last_issue_date", None)
        else:
            count = 0
            last_issue_date = None

        # Увеличиваем счётчик если unhealthy
        if status == "UNHEALTHY":
            count += 1
        else:
            count = 0  # Сбрасываем если здоров

        # Сохраняем счётчик
        counter_data = {
            "count": count,
            "last_check": datetime.now().isoformat(),
            "last_issue_date": last_issue_date,
        }
        counter_file.write_text(json.dumps(counter_data, indent=2))

        # Создаём issue если 3+ раза unhealthy подряд
        if count >= 3 and (
            not last_issue_date
            or (datetime.now() - datetime.fromisoformat(last_issue_date)).days >= 1
        ):

            issue_data = self._create_cicd_issue_file(health_data, count)

            # Обновляем дату последнего issue
            counter_data["last_issue_date"] = datetime.now().isoformat()
            counter_data["count"] = 0  # Сбрасываем после создания issue
            counter_file.write_text(json.dumps(counter_data, indent=2))

            result = {
                "task": "monitor_cicd_and_create_issue",
                "status": "ISSUE_CREATED",
                "timestamp": datetime.now().isoformat(),
                "issue_file": issue_data["file"],
                "unhealthy_count": count,
                "action": "Issue created due to persistent problems",
            }
            print(f"✅ Issue создан: {issue_data['file']}")
        else:
            result = {
                "task": "monitor_cicd_and_create_issue",
                "status": "MONITORING",
                "timestamp": datetime.now().isoformat(),
                "unhealthy_count": count,
                "action": f"Monitoring (need {3-count} more to create issue)",
            }
            print(f"📊 Мониторинг: {count}/3 проблем")

        return result

    def _create_cicd_issue_file(self, health_data: Dict, count: int) -> Dict:
        """Создаёт файл с данными issue"""
        issues_dir = self.base_dir / "issues"
        issues_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        issue_file = issues_dir / f"cicd_problem_{timestamp}.json"

        issue_content = {
            "title": f"🔴 CI/CD Unhealthy: {health_data.get('grade', 'N/A')}",
            "body": f"""
## Problem Details

CI/CD pipeline has been unhealthy {count} times in a row.

**Status:** {health_data.get('status', 'UNKNOWN')}
**Grade:** {health_data.get('grade', 'N/A')}
**Success Rate:** {health_data.get('success_rate', 'N/A')}

## Recent Runs

{health_data.get('report', 'No report available')}

## Action Required

Please investigate and fix the failing tests or workflows.

---
*Auto-generated by MIRAI Real Task Executor*
""",
            "labels": ["bug", "ci-cd", "automated"],
            "created_at": datetime.now().isoformat(),
            "unhealthy_count": count,
        }

        issue_file.write_text(json.dumps(issue_content, indent=2, ensure_ascii=False))

        return {"file": str(issue_file), "content": issue_content}

    def task3_build_knowledge_base(self) -> Dict:
        """
        ЗАДАЧА 3: Построение Базы Знаний из Логов

        Измеримый результат: knowledge_base/errors.json обновлён
        """
        print("📚 Строю базу знаний из паттернов ошибок...")

        # Читаем логи за неделю
        logs = self._read_journalctl_logs(since="7 days ago")

        # Извлекаем ошибки
        error_patterns = self._extract_error_patterns(logs)

        # Загружаем существующую базу знаний
        kb_file = self.knowledge_dir / "errors.json"

        if kb_file.exists():
            kb = json.loads(kb_file.read_text())
        else:
            kb = {
                "error_patterns": {},
                "last_updated": None,
                "total_errors_analyzed": 0,
            }

        # Обновляем паттерны
        for pattern, data in error_patterns.items():
            if pattern in kb["error_patterns"]:
                # Обновляем существующий паттерн
                kb["error_patterns"][pattern]["count"] += data["count"]
                kb["error_patterns"][pattern]["last_seen"] = data["last_seen"]
            else:
                # Добавляем новый паттерн
                kb["error_patterns"][pattern] = data

        kb["last_updated"] = datetime.now().isoformat()
        kb["total_errors_analyzed"] = sum(
            p["count"] for p in kb["error_patterns"].values()
        )

        # Сохраняем обновлённую базу знаний
        kb_file.write_text(json.dumps(kb, indent=2, ensure_ascii=False))

        # Генерируем FAQ
        faq_file = self.knowledge_dir / "FAQ.md"
        faq_content = self._generate_faq_from_kb(kb)
        faq_file.write_text(faq_content)

        result = {
            "task": "build_knowledge_base",
            "status": "COMPLETED",
            "timestamp": datetime.now().isoformat(),
            "kb_file": str(kb_file),
            "faq_file": str(faq_file),
            "summary": {
                "unique_patterns": len(kb["error_patterns"]),
                "total_errors": kb["total_errors_analyzed"],
                "new_patterns": len(error_patterns),
            },
        }

        print(f"✅ База знаний обновлена: {len(kb['error_patterns'])} паттернов")
        print(f"✅ FAQ сгенерирован: {faq_file}")

        return result

    def _extract_error_patterns(self, logs: List[str]) -> Dict:
        """Извлекает паттерны ошибок из логов"""
        patterns = {}

        error_regex = re.compile(r"(ERROR|error|ошибка|failed|failure)", re.IGNORECASE)

        for line in logs:
            if error_regex.search(line):
                # Извлекаем суть ошибки (убираем временные метки и специфичные данные)
                error_msg = line.split(":", 3)[-1].strip()[:150]

                # Нормализуем (убираем числа, пути и т.д.)
                normalized = re.sub(r"\d+", "N", error_msg)
                normalized = re.sub(r"/[\w/]+", "/PATH", normalized)

                if normalized and len(normalized) > 20:
                    if normalized in patterns:
                        patterns[normalized]["count"] += 1
                    else:
                        patterns[normalized] = {
                            "count": 1,
                            "example": error_msg,
                            "first_seen": datetime.now().isoformat(),
                            "last_seen": datetime.now().isoformat(),
                        }

        return patterns

    def _generate_faq_from_kb(self, kb: Dict) -> str:
        """Генерирует FAQ из базы знаний"""
        faq = f"""# 🤔 FAQ - Частые Ошибки и Решения

**Обновлено:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Всего ошибок проанализировано:** {kb['total_errors_analyzed']:,}
**Уникальных паттернов:** {len(kb['error_patterns'])}

---

## Топ-10 Частых Ошибок

"""

        # Сортируем по частоте
        sorted_patterns = sorted(
            kb["error_patterns"].items(), key=lambda x: x[1]["count"], reverse=True
        )[:10]

        for i, (pattern, data) in enumerate(sorted_patterns, 1):
            faq += f"""
### {i}. Ошибка (встречалась {data['count']} раз)

**Паттерн:** `{pattern[:100]}`

**Пример:**
```
{data['example']}
```

**Последнее появление:** {data['last_seen']}

**Возможное решение:** 
- Проверьте логи для деталей
- Убедитесь что зависимости установлены
- Проверьте конфигурацию

---
"""

        faq += "\n*FAQ автоматически сгенерирован MIRAI Real Task Executor*\n"

        return faq

    def task4_update_metrics_dashboard(self) -> Dict:
        """
        ЗАДАЧА 4: Обновление Метрик и Dashboard

        Измеримый результат: metrics/latest.json и web/dashboard.html обновлены
        """
        print("📊 Обновляю метрики и генерирую dashboard...")

        # Собираем метрики
        metrics = self._collect_current_metrics()

        # Сохраняем метрики
        metrics_file = self.metrics_dir / "latest.json"
        metrics_file.write_text(json.dumps(metrics, indent=2, ensure_ascii=False))

        # Добавляем в историю
        history_file = self.metrics_dir / "history.jsonl"
        with open(history_file, "a") as f:
            f.write(json.dumps(metrics, ensure_ascii=False) + "\n")

        # Генерируем HTML dashboard
        web_dir = self.base_dir / "web"
        web_dir.mkdir(exist_ok=True)

        dashboard_file = web_dir / "dashboard.html"
        dashboard_html = self._generate_dashboard_html(metrics)
        dashboard_file.write_text(dashboard_html)

        result = {
            "task": "update_metrics_dashboard",
            "status": "COMPLETED",
            "timestamp": datetime.now().isoformat(),
            "metrics_file": str(metrics_file),
            "dashboard_file": str(dashboard_file),
            "summary": metrics,
        }

        print(f"✅ Метрики обновлены: {metrics_file}")
        print(f"✅ Dashboard создан: {dashboard_file}")

        return result

    def _collect_current_metrics(self) -> Dict:
        """Собирает текущие метрики системы"""

        # Получаем статистику из journalctl
        logs = self._read_journalctl_logs(since="1 hour ago")

        # Подсчитываем циклы
        cycles = len([l for l in logs if "АВТОНОМНЫЙ ЦИКЛ" in l])

        # Проверяем память БД
        db_file = self.base_dir / "mirai-agent" / "data" / "mirai_memory.db"
        db_size = db_file.stat().st_size if db_file.exists() else 0

        # Собираем метрики
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cycles_last_hour": cycles,
            "db_size_bytes": db_size,
            "db_size_human": self._human_readable_size(db_size),
            "log_lines_last_hour": len(logs),
            "errors_last_hour": len([l for l in logs if "ERROR" in l or "error" in l]),
            "warnings_last_hour": len(
                [l for l in logs if "WARNING" in l or "warning" in l]
            ),
        }

        return metrics

    def _human_readable_size(self, size_bytes: int) -> str:
        """Конвертирует байты в человеко-читаемый формат"""
        size = float(size_bytes)
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def _generate_dashboard_html(self, metrics: Dict) -> str:
        """Генерирует HTML dashboard"""

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIRAI Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .metric-label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .status {{
            padding: 10px 20px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
        }}
        .status-ok {{
            background: #4caf50;
            color: white;
        }}
        .status-warning {{
            background: #ff9800;
            color: white;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 MIRAI Dashboard</h1>
        <div class="timestamp">Обновлено: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Циклы (последний час)</div>
                <div class="metric-value">{metrics.get('cycles_last_hour', 0)}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Размер БД</div>
                <div class="metric-value">{metrics.get('db_size_human', 'N/A')}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Строк логов</div>
                <div class="metric-value">{metrics.get('log_lines_last_hour', 0):,}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Ошибки</div>
                <div class="metric-value">{metrics.get('errors_last_hour', 0)}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Предупреждения</div>
                <div class="metric-value">{metrics.get('warnings_last_hour', 0)}</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <span class="status {'status-ok' if metrics.get('errors_last_hour', 0) == 0 else 'status-warning'}">
                {'✅ Система работает нормально' if metrics.get('errors_last_hour', 0) == 0 else '⚠️ Обнаружены ошибки'}
            </span>
        </div>
        
        <div class="footer">
            Auto-generated by MIRAI Real Task Executor<br>
            Next update: {(datetime.now()).strftime("%H:%M")}
        </div>
    </div>
</body>
</html>
"""

        return html

    def task5_auto_fix_code(self, issue_description: str | None = None) -> Dict:
        """
        ЗАДАЧА 5: Автоматическое Исправление Кода

        Поток:
        1. AI анализирует проблему и генерирует исправление
        2. Создаёт новую ветку в GitHub
        3. Коммитит исправленный код
        4. Создаёт Pull Request с описанием

        Измеримый результат: PR создан в GitHub
        """
        print("🤖 Начинаю автоисправление кода...")

        try:
            from core.autonomous_agent import AutonomousAgent
            from core.github_integration import GitHubIntegration

            # Инициализация
            agent = AutonomousAgent()
            gh = GitHubIntegration()

            if not gh.is_authenticated():
                return {
                    "task": "task5_auto_fix_code",
                    "status": "❌ FAILED",
                    "error": "GitHub not authenticated",
                }

            # Если issue не указан, ищем в логах
            if not issue_description:
                logs = self._read_journalctl_logs(since="1 hour ago")
                analysis = self._analyze_logs(logs)

                if analysis["error_count"] == 0:
                    return {
                        "task": "task5_auto_fix_code",
                        "status": "✅ SKIP",
                        "reason": "No errors found in logs",
                    }

                # Берём самую частую ошибку
                issue_description = f"Fix error: {analysis['top_errors'][0]}"

            # AI генерирует исправление
            prompt = f"""
Анализируй эту проблему и предложи исправление:

Проблема: {issue_description}

Верни JSON:
{{
    "file_path": "путь к файлу который нужно исправить",
    "fixed_content": "исправленный код целиком",
    "explanation": "что именно исправлено"
}}
"""

            print(f"💭 Спрашиваю AI как исправить: {issue_description[:80]}...")
            ai_response = agent.think(prompt, max_iterations=1)

            # Парсим ответ AI
            try:
                # Извлекаем JSON из ответа
                import re

                json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
                if not json_match:
                    raise ValueError("No JSON in AI response")

                fix_data = json.loads(json_match.group())
                file_path = fix_data["file_path"]
                fixed_content = fix_data["fixed_content"]
                explanation = fix_data["explanation"]

            except Exception as e:
                return {
                    "task": "task5_auto_fix_code",
                    "status": "❌ FAILED",
                    "error": f"Failed to parse AI response: {e}",
                }

            # Создаём ветку
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            branch_name = f"autofix/{timestamp}"

            print(f"🌿 Создаю ветку: {branch_name}")
            branch_result = gh.create_branch(
                owner="AgeeKey",
                repo="Mirai",
                branch_name=branch_name,
                from_branch="main",
            )

            if "error" in branch_result:
                return {
                    "task": "task5_auto_fix_code",
                    "status": "❌ FAILED",
                    "error": f"Failed to create branch: {branch_result['error']}",
                }

            # Коммитим исправление
            print(f"💾 Коммичу исправление в {file_path}")
            commit_result = gh.create_or_update_file(
                owner="AgeeKey",
                repo="Mirai",
                path=file_path,
                content=fixed_content,
                message=f"🤖 Auto-fix: {issue_description[:50]}",
                branch=branch_name,
            )

            if "error" in commit_result:
                return {
                    "task": "task5_auto_fix_code",
                    "status": "❌ FAILED",
                    "error": f"Failed to commit: {commit_result['error']}",
                }

            # Создаём Pull Request
            pr_body = f"""
## 🤖 Автоматическое Исправление

**Проблема:**
{issue_description}

**Что исправлено:**
{explanation}

**Изменённый файл:**
- `{file_path}`

---
*Создано автономным агентом MIRAI*
"""

            print(f"📬 Создаю Pull Request...")
            pr_result = gh.create_pull_request(
                owner="AgeeKey",
                repo="Mirai",
                title=f"🤖 Auto-fix: {issue_description[:60]}",
                head=branch_name,
                base="main",
                body=pr_body,
            )

            if "error" in pr_result:
                return {
                    "task": "task5_auto_fix_code",
                    "status": "⚠️ PARTIAL",
                    "branch": branch_name,
                    "commit": commit_result.get("sha"),
                    "error": f"PR creation failed: {pr_result['error']}",
                }

            return {
                "task": "task5_auto_fix_code",
                "status": "✅ SUCCESS",
                "pr_number": pr_result["number"],
                "pr_url": pr_result["url"],
                "branch": branch_name,
                "file_fixed": file_path,
            }

        except Exception as e:
            return {
                "task": "task5_auto_fix_code",
                "status": "❌ FAILED",
                "error": str(e),
            }


def main():
    """Запуск всех задач для тестирования"""
    executor = RealTaskExecutor()

    print("🚀 Запускаю все РЕАЛЬНЫЕ задачи MIRAI\n")

    # Задача 1: Анализ логов
    result1 = executor.task1_analyze_logs_and_report()
    print(f"\n1️⃣ {result1['task']}: {result1['status']}")

    # Задача 2: Мониторинг CI/CD (для примера)
    mock_health = {
        "status": "UNHEALTHY",
        "grade": "D (50%)",
        "success_rate": "50%",
        "report": "2/4 workflows failed",
    }
    result2 = executor.task2_monitor_cicd_and_create_issue(mock_health)
    print(f"\n2️⃣ {result2['task']}: {result2['status']}")

    # Задача 3: База знаний
    result3 = executor.task3_build_knowledge_base()
    print(f"\n3️⃣ {result3['task']}: {result3['status']}")

    # Задача 4: Dashboard
    result4 = executor.task4_update_metrics_dashboard()
    print(f"\n4️⃣ {result4['task']}: {result4['status']}")

    print("\n" + "=" * 60)
    print("✅ ВСЕ 4 ЗАДАЧИ ВЫПОЛНЕНЫ!")
    print("=" * 60)

    summary = {"task1": result1, "task2": result2, "task3": result3, "task4": result4}

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
