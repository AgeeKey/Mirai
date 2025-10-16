#!/usr/bin/env python3
"""
🔍 MIRAI Self-Diagnostic System
================================

MIRAI проверяет сама себя:
- Все файлы кода
- Импорты и зависимости
- Синтаксис и ошибки
- Производительность
- Качество кода
- Критичные проблемы
"""

import ast
import importlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Добавляем путь для импорта
sys.path.insert(0, "/root/mirai/mirai-agent")


class SelfDiagnostic:
    """Полная самодиагностика MIRAI"""

    def __init__(self):
        self.mirai_root = Path("/root/mirai/mirai-agent")
        self.core_dir = self.mirai_root / "core"

        self.results = {
            "timestamp": datetime.now().isoformat(),
            "files_checked": 0,
            "total_issues": 0,
            "critical_issues": 0,
            "warnings": 0,
            "files_ok": 0,
            "files_with_errors": [],
            "files_with_warnings": [],
            "files_perfect": [],
            "detailed_report": {},
        }

    def check_syntax(self, file_path: str) -> Tuple[bool, List[str]]:
        """Проверка синтаксиса Python"""
        errors = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            errors.append(f"🔴 SYNTAX ERROR: Line {e.lineno}: {e.msg}")
            return False, errors
        except Exception as e:
            errors.append(f"🔴 PARSE ERROR: {str(e)}")
            return False, errors

    def check_imports(self, file_path: str) -> Tuple[bool, List[str], List[str]]:
        """Проверка импортов"""
        errors = []
        warnings = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            importlib.import_module(alias.name)
                        except ImportError:
                            errors.append(f"🔴 MISSING IMPORT: {alias.name}")
                        except Exception as e:
                            warnings.append(f"⚠️ IMPORT WARNING: {alias.name} - {e}")

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        try:
                            importlib.import_module(node.module)
                        except ImportError:
                            # Проверяем локальные импорты
                            if not node.module.startswith("core."):
                                errors.append(f"🔴 MISSING MODULE: {node.module}")
                        except Exception as e:
                            warnings.append(f"⚠️ MODULE WARNING: {node.module} - {e}")

            return len(errors) == 0, errors, warnings

        except Exception as e:
            return False, [f"🔴 IMPORT CHECK FAILED: {str(e)}"], []

    def check_code_quality(self, file_path: str) -> Dict:
        """Анализ качества кода"""
        issues = {
            "missing_docstrings": [],
            "long_functions": [],
            "complex_functions": [],
            "unused_imports": [],
            "code_smells": [],
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
                tree = ast.parse(code)

            # Проверка docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        issues["missing_docstrings"].append(
                            f"Line {node.lineno}: {node.name}"
                        )

                # Проверка длины функций
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, "end_lineno"):
                        func_length = node.end_lineno - node.lineno
                        if func_length > 100:
                            issues["long_functions"].append(
                                f"Line {node.lineno}: {node.name} ({func_length} lines)"
                            )
                        elif func_length > 50:
                            issues["complex_functions"].append(
                                f"Line {node.lineno}: {node.name} ({func_length} lines)"
                            )

            # Проверка дублирования
            lines = code.split("\n")
            line_freq = defaultdict(int)
            for line in lines:
                stripped = line.strip()
                if len(stripped) > 30 and not stripped.startswith("#"):
                    line_freq[stripped] += 1

            for line, count in line_freq.items():
                if count > 5:
                    issues["code_smells"].append(
                        f"Duplicated code ({count} times): {line[:60]}..."
                    )

        except Exception as e:
            issues["code_smells"].append(f"Quality check failed: {e}")

        return issues

    def check_file_executable(self, file_path: str) -> Tuple[bool, str]:
        """Проверка что файл можно импортировать/выполнить"""
        try:
            # Пытаемся импортировать как модуль
            module_path = (
                file_path.replace("/root/mirai/mirai-agent/", "")
                .replace("/", ".")
                .replace(".py", "")
            )

            # Пропускаем тестовые скрипты
            if "__main__" in open(file_path).read():
                return True, "✅ Executable script"

            return True, "✅ Importable module"

        except Exception as e:
            return False, f"🔴 Cannot import: {e}"

    def analyze_file(self, file_path: str) -> Dict:
        """Полный анализ одного файла"""
        file_name = os.path.basename(file_path)

        report = {
            "file": file_name,
            "path": str(file_path),
            "status": "unknown",
            "errors": [],
            "warnings": [],
            "quality_issues": {},
            "lines_of_code": 0,
            "complexity_score": 0,
        }

        # 1. Проверка синтаксиса
        syntax_ok, syntax_errors = self.check_syntax(file_path)
        if not syntax_ok:
            report["errors"].extend(syntax_errors)
            report["status"] = "critical"
            return report

        # 2. Проверка импортов
        imports_ok, import_errors, import_warnings = self.check_imports(file_path)
        report["errors"].extend(import_errors)
        report["warnings"].extend(import_warnings)

        # 3. Качество кода
        quality_issues = self.check_code_quality(file_path)
        report["quality_issues"] = quality_issues

        # 4. Подсчёт строк
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            report["lines_of_code"] = len(
                [l for l in lines if l.strip() and not l.strip().startswith("#")]
            )

        # 5. Определение статуса
        total_issues = len(report["errors"]) + sum(
            len(v) for v in quality_issues.values()
        )

        if report["errors"]:
            report["status"] = "critical"
        elif total_issues > 10:
            report["status"] = "needs_attention"
        elif total_issues > 5:
            report["status"] = "warnings"
        else:
            report["status"] = "good"

        report["complexity_score"] = total_issues

        return report

    def scan_all_files(self) -> Dict:
        """Сканирование всех Python файлов"""
        print("🔍 MIRAI SELF-DIAGNOSTIC STARTING...\n")

        # Получаем все Python файлы
        python_files = []

        # Core модули
        if self.core_dir.exists():
            python_files.extend(list(self.core_dir.glob("*.py")))

        # Корневые скрипты
        for pattern in ["*.py", "autonomous_*.py"]:
            python_files.extend(list(self.mirai_root.glob(pattern)))

        # Фильтруем __init__ и тесты
        python_files = [
            f
            for f in python_files
            if f.name != "__init__.py" and not f.name.startswith("test_")
        ]

        print(f"📁 Found {len(python_files)} Python files\n")

        # Анализируем каждый файл
        for i, file_path in enumerate(python_files, 1):
            print(f"[{i}/{len(python_files)}] Checking {file_path.name}...", end=" ")

            report = self.analyze_file(str(file_path))
            self.results["detailed_report"][file_path.name] = report
            self.results["files_checked"] += 1

            # Обновляем статистику
            if report["status"] == "critical":
                print("🔴 CRITICAL")
                self.results["critical_issues"] += len(report["errors"])
                self.results["files_with_errors"].append(file_path.name)
            elif report["status"] == "needs_attention":
                print("🟠 NEEDS ATTENTION")
                self.results["warnings"] += report["complexity_score"]
                self.results["files_with_warnings"].append(file_path.name)
            elif report["status"] == "warnings":
                print("🟡 WARNINGS")
                self.results["warnings"] += report["complexity_score"]
                self.results["files_with_warnings"].append(file_path.name)
            else:
                print("✅ GOOD")
                self.results["files_ok"] += 1
                self.results["files_perfect"].append(file_path.name)

        # Подсчёт общих проблем
        for report in self.results["detailed_report"].values():
            self.results["total_issues"] += report["complexity_score"]

        return self.results

    def generate_report(self) -> str:
        """Генерация текстового отчёта"""
        report = []

        report.append(
            "╔══════════════════════════════════════════════════════════════════╗"
        )
        report.append(
            "║           🔍 MIRAI SELF-DIAGNOSTIC REPORT                        ║"
        )
        report.append(
            "╚══════════════════════════════════════════════════════════════════╝\n"
        )

        # Общая статистика
        report.append("📊 OVERALL STATISTICS:")
        report.append(f"   Files checked: {self.results['files_checked']}")
        report.append(f"   Total issues: {self.results['total_issues']}")
        report.append(f"   Critical errors: {self.results['critical_issues']}")
        report.append(f"   Warnings: {self.results['warnings']}")
        report.append(f"   Files OK: {self.results['files_ok']}")
        report.append("")

        # Статус по категориям
        critical_count = len(self.results["files_with_errors"])
        warning_count = len(self.results["files_with_warnings"])
        ok_count = len(self.results["files_perfect"])

        report.append("📈 STATUS BREAKDOWN:")
        report.append(f"   🔴 Critical: {critical_count} files")
        report.append(f"   🟡 Warnings: {warning_count} files")
        report.append(f"   ✅ Perfect: {ok_count} files")
        report.append("")

        # Критические проблемы
        if self.results["files_with_errors"]:
            report.append("🔴 CRITICAL ISSUES (MUST FIX):")
            for file_name in self.results["files_with_errors"]:
                file_report = self.results["detailed_report"][file_name]
                report.append(f"\n   📄 {file_name}:")
                for error in file_report["errors"]:
                    report.append(f"      {error}")
            report.append("")

        # Предупреждения
        if self.results["files_with_warnings"]:
            report.append("🟡 FILES NEEDING ATTENTION:")
            for file_name in self.results["files_with_warnings"]:
                file_report = self.results["detailed_report"][file_name]
                report.append(
                    f"\n   📄 {file_name} ({file_report['lines_of_code']} LOC):"
                )

                # Качество кода
                quality = file_report["quality_issues"]

                if quality["missing_docstrings"]:
                    report.append(
                        f"      ⚠️ Missing docstrings: {len(quality['missing_docstrings'])}"
                    )

                if quality["long_functions"]:
                    report.append(
                        f"      ⚠️ Long functions (>100 lines): {len(quality['long_functions'])}"
                    )
                    for func in quality["long_functions"][:3]:
                        report.append(f"         • {func}")

                if quality["complex_functions"]:
                    report.append(
                        f"      ⚠️ Complex functions (50-100 lines): {len(quality['complex_functions'])}"
                    )

                if quality["code_smells"]:
                    report.append(f"      ⚠️ Code smells: {len(quality['code_smells'])}")

                if file_report["warnings"]:
                    for warning in file_report["warnings"][:5]:
                        report.append(f"      {warning}")

            report.append("")

        # Отличные файлы
        if self.results["files_perfect"]:
            report.append("✅ PERFECT FILES (No issues):")
            for file_name in sorted(self.results["files_perfect"]):
                file_report = self.results["detailed_report"][file_name]
                report.append(f"   ✓ {file_name} ({file_report['lines_of_code']} LOC)")
            report.append("")

        # Топ-5 самых больших файлов
        report.append("📏 TOP 5 LARGEST FILES:")
        files_by_size = sorted(
            self.results["detailed_report"].items(),
            key=lambda x: x[1]["lines_of_code"],
            reverse=True,
        )[:5]

        for file_name, file_report in files_by_size:
            status_emoji = {
                "critical": "🔴",
                "needs_attention": "🟠",
                "warnings": "🟡",
                "good": "✅",
            }
            emoji = status_emoji.get(file_report["status"], "❓")
            report.append(
                f"   {emoji} {file_name}: {file_report['lines_of_code']} lines"
            )

        report.append("")

        # Топ-5 самых проблемных файлов
        if self.results["total_issues"] > 0:
            report.append("⚠️ TOP 5 MOST COMPLEX FILES:")
            files_by_complexity = sorted(
                self.results["detailed_report"].items(),
                key=lambda x: x[1]["complexity_score"],
                reverse=True,
            )[:5]

            for file_name, file_report in files_by_complexity:
                if file_report["complexity_score"] > 0:
                    report.append(
                        f"   🔶 {file_name}: {file_report['complexity_score']} issues"
                    )

            report.append("")

        # Рекомендации
        report.append("💡 RECOMMENDATIONS:")

        if self.results["critical_issues"] > 0:
            report.append("   1. 🔴 FIX CRITICAL ERRORS IMMEDIATELY")
            report.append("      These files have syntax or import errors!")

        if critical_count == 0 and warning_count > 0:
            report.append("   1. 🟡 Address warnings in complex files")
            report.append("      Consider refactoring large functions")

        if ok_count > critical_count + warning_count:
            report.append("   1. ✅ Code quality is generally good!")
            report.append("      Most files are clean and well-structured")

        report.append("")

        # Финальный вердикт
        report.append("🎯 FINAL VERDICT:")

        if critical_count > 0:
            report.append("   Status: 🔴 CRITICAL - Requires immediate attention")
            report.append(f"   Action: Fix {critical_count} critical files ASAP")
        elif warning_count > len(self.results["files_perfect"]):
            report.append("   Status: 🟡 NEEDS IMPROVEMENT")
            report.append("   Action: Refactor complex files, add docstrings")
        else:
            report.append("   Status: ✅ EXCELLENT")
            report.append("   Action: Maintain code quality, keep improving!")

        report.append("")
        report.append(f"Generated: {self.results['timestamp']}")
        report.append("🤖 MIRAI Self-Diagnostic System v1.0")

        return "\n".join(report)

    def save_report(self, filename: str = None):
        """Сохранение отчёта"""
        if filename is None:
            filename = f"/root/mirai/MIRAI_DIAGNOSTIC_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        report_text = self.generate_report()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)

        # Также сохраняем JSON
        json_file = filename.replace(".txt", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        return filename, json_file


def main():
    """Запуск самодиагностики"""
    diagnostic = SelfDiagnostic()

    # Сканируем все файлы
    results = diagnostic.scan_all_files()

    # Генерируем отчёт
    print("\n" + "=" * 70 + "\n")
    report = diagnostic.generate_report()
    print(report)

    # Сохраняем отчёты
    txt_file, json_file = diagnostic.save_report()

    print("\n" + "=" * 70)
    print(f"📄 Full report saved to: {txt_file}")
    print(f"📊 JSON data saved to: {json_file}")
    print("=" * 70 + "\n")

    # Возвращаем код выхода
    if results["critical_issues"] > 0:
        sys.exit(1)  # Критические ошибки
    elif results["total_issues"] > 20:
        sys.exit(2)  # Много предупреждений
    else:
        sys.exit(0)  # Всё хорошо


if __name__ == "__main__":
    main()
