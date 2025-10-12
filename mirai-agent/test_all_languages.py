#!/usr/bin/env python3
"""
ПОЛНЫЙ ТЕСТ ВСЕХ 8 ЯЗЫКОВ ПРОГРАММИРОВАНИЯ
"""

import asyncio
import sys
import os

sys.path.insert(0, "/root/mirai/mirai-agent")

# Добавляем Rust в PATH
os.environ["PATH"] = f"{os.path.expanduser('~')}/.cargo/bin:" + os.environ["PATH"]

from core.multi_language_executor import MultiLanguageExecutor


async def test_all_languages():
    """Тест всех 8 языков"""
    print("=" * 80)
    print("🌍 ТЕСТ ВСЕХ 8 ЯЗЫКОВ ПРОГРАММИРОВАНИЯ MIRAI")
    print("=" * 80)

    executor = MultiLanguageExecutor()

    tests = [
        {
            "name": "🐍 Python",
            "code": """print("✅ Python работает!")
import math
print(f"π = {math.pi:.2f}")""",
            "language": "python",
        },
        {
            "name": "📜 JavaScript",
            "code": """console.log("✅ JavaScript работает!");
const pi = Math.PI;
console.log(`π = ${pi.toFixed(2)}`);""",
            "language": "javascript",
        },
        {
            "name": "📘 TypeScript",
            "code": """const message: string = "✅ TypeScript работает!";
console.log(message);
const pi: number = Math.PI;
console.log(`π = ${pi.toFixed(2)}`);""",
            "language": "typescript",
        },
        {
            "name": "🔧 C",
            "code": """#include <stdio.h>
#include <math.h>
int main() {
    printf("✅ C работает!\\n");
    printf("π = %.2f\\n", M_PI);
    return 0;
}""",
            "language": "c",
        },
        {
            "name": "⚙️ C++",
            "code": """#include <iostream>
#include <cmath>
using namespace std;
int main() {
    cout << "✅ C++ работает!" << endl;
    cout << "π = " << M_PI << endl;
    return 0;
}""",
            "language": "cpp",
        },
        {
            "name": "🔵 Go",
            "code": """package main
import (
    "fmt"
    "math"
)
func main() {
    fmt.Println("✅ Go работает!")
    fmt.Printf("π = %.2f\\n", math.Pi)
}""",
            "language": "go",
        },
        {
            "name": "🦀 Rust",
            "code": """fn main() {
    println!("✅ Rust работает!");
    let pi = std::f64::consts::PI;
    println!("π = {:.2}", pi);
}""",
            "language": "rust",
        },
        {
            "name": "🐚 Bash",
            "code": '''#!/bin/bash
echo "✅ Bash работает!"
echo "Hostname: $(hostname)"
echo "Date: $(date +%Y-%m-%d)"''',
            "language": "bash",
        },
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n{'='*80}")
        print(f"{test['name']}")
        print(f"{'='*80}")

        result = await executor.execute_code(test["code"], test["language"])

        if result["success"]:
            print(f"✅ УСПЕХ ({result['execution_time']}s)")
            print(f"Вывод:")
            print(result["output"])
            passed += 1
        else:
            print(f"❌ ОШИБКА:")
            print(result["error"])
            failed += 1

    print(f"\n{'='*80}")
    print(f"📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"{'='*80}")
    print(f"✅ Успешно: {passed}/8")
    print(f"❌ Ошибок: {failed}/8")
    print(f"{'='*80}")

    if passed == 8:
        print("🎉 ВСЕ 8 ЯЗЫКОВ РАБОТАЮТ ИДЕАЛЬНО!")
    else:
        print(f"⚠️ {failed} языков требуют настройки")

    print(f"\n🚀 MIRAI поддерживает: {', '.join(executor.get_supported_languages())}")


if __name__ == "__main__":
    asyncio.run(test_all_languages())
