"""
MULTI-LANGUAGE EXECUTOR - Выполнение кода на разных языках
Поддержка: Python, JavaScript, C/C++, Go, Rust, Bash
"""

import subprocess
import tempfile
import os
import asyncio
from typing import Dict, Tuple, Optional
import shutil


class MultiLanguageExecutor:
    """Выполнение кода на множестве языков программирования"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.working_dir = "/root/mirai/mirai-agent/temp_execution"
        os.makedirs(self.working_dir, exist_ok=True)

    async def execute_code(self, code: str, language: str) -> Dict[str, str]:
        """
        Выполнить код на указанном языке

        Args:
            code: Код для выполнения
            language: Язык (python, javascript, cpp, c, go, rust, bash, shell)

        Returns:
            Dict с ключами: success, output, error, execution_time
        """
        language = language.lower()

        executors = {
            "python": self._execute_python,
            "python3": self._execute_python,
            "py": self._execute_python,
            "javascript": self._execute_javascript,
            "js": self._execute_javascript,
            "node": self._execute_javascript,
            "typescript": self._execute_typescript,
            "ts": self._execute_typescript,
            "c": self._execute_c,
            "cpp": self._execute_cpp,
            "c++": self._execute_cpp,
            "go": self._execute_go,
            "golang": self._execute_go,
            "rust": self._execute_rust,
            "rs": self._execute_rust,
            "bash": self._execute_bash,
            "shell": self._execute_bash,
            "sh": self._execute_bash,
        }

        executor = executors.get(language)
        if not executor:
            return {
                "success": False,
                "output": "",
                "error": f'❌ Язык "{language}" не поддерживается. Доступны: {", ".join(executors.keys())}',
                "execution_time": 0,
            }

        try:
            return await executor(code)
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"❌ Ошибка выполнения: {str(e)}",
                "execution_time": 0,
            }

    async def _execute_python(self, code: str) -> Dict[str, str]:
        """Выполнить Python код"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            filepath = f.name

        try:
            result = await self._run_command(["python3", filepath])
            return result
        finally:
            os.unlink(filepath)

    async def _execute_javascript(self, code: str) -> Dict[str, str]:
        """Выполнить JavaScript код (Node.js)"""
        # Проверяем наличие Node.js
        if not shutil.which("node"):
            return {
                "success": False,
                "output": "",
                "error": "❌ Node.js не установлен. Установите: apt-get install nodejs",
                "execution_time": 0,
            }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".js", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            filepath = f.name

        try:
            result = await self._run_command(["node", filepath])
            return result
        finally:
            os.unlink(filepath)

    async def _execute_typescript(self, code: str) -> Dict[str, str]:
        """Выполнить TypeScript код (через ts-node)"""
        # Проверяем ts-node
        if not shutil.which("ts-node"):
            # Пробуем через npx
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".ts", delete=False, dir=self.working_dir
            ) as f:
                f.write(code)
                filepath = f.name

            try:
                result = await self._run_command(["npx", "-y", "ts-node", filepath])
                return result
            finally:
                os.unlink(filepath)
        else:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".ts", delete=False, dir=self.working_dir
            ) as f:
                f.write(code)
                filepath = f.name

            try:
                result = await self._run_command(["ts-node", filepath])
                return result
            finally:
                os.unlink(filepath)

    async def _execute_c(self, code: str) -> Dict[str, str]:
        """Компилировать и выполнить C код"""
        if not shutil.which("gcc"):
            return {
                "success": False,
                "output": "",
                "error": "❌ GCC не установлен. Установите: apt-get install gcc",
                "execution_time": 0,
            }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".c", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            source_file = f.name

        executable = source_file.replace(".c", ".out")

        try:
            # Компиляция
            compile_result = await self._run_command(
                ["gcc", source_file, "-o", executable]
            )
            if not compile_result["success"]:
                return {
                    "success": False,
                    "output": compile_result["output"],
                    "error": f"❌ Ошибка компиляции:\n{compile_result['error']}",
                    "execution_time": compile_result["execution_time"],
                }

            # Выполнение
            run_result = await self._run_command([executable])
            return run_result
        finally:
            if os.path.exists(source_file):
                os.unlink(source_file)
            if os.path.exists(executable):
                os.unlink(executable)

    async def _execute_cpp(self, code: str) -> Dict[str, str]:
        """Компилировать и выполнить C++ код"""
        if not shutil.which("g++"):
            return {
                "success": False,
                "output": "",
                "error": "❌ G++ не установлен. Установите: apt-get install g++",
                "execution_time": 0,
            }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".cpp", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            source_file = f.name

        executable = source_file.replace(".cpp", ".out")

        try:
            # Компиляция
            compile_result = await self._run_command(
                ["g++", source_file, "-o", executable, "-std=c++17"]
            )
            if not compile_result["success"]:
                return {
                    "success": False,
                    "output": compile_result["output"],
                    "error": f"❌ Ошибка компиляции:\n{compile_result['error']}",
                    "execution_time": compile_result["execution_time"],
                }

            # Выполнение
            run_result = await self._run_command([executable])
            return run_result
        finally:
            if os.path.exists(source_file):
                os.unlink(source_file)
            if os.path.exists(executable):
                os.unlink(executable)

    async def _execute_go(self, code: str) -> Dict[str, str]:
        """Выполнить Go код"""
        if not shutil.which("go"):
            return {
                "success": False,
                "output": "",
                "error": "❌ Go не установлен. Установите: apt-get install golang",
                "execution_time": 0,
            }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".go", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            filepath = f.name

        try:
            result = await self._run_command(["go", "run", filepath])
            return result
        finally:
            os.unlink(filepath)

    async def _execute_rust(self, code: str) -> Dict[str, str]:
        """Компилировать и выполнить Rust код"""
        if not shutil.which("rustc"):
            return {
                "success": False,
                "output": "",
                "error": "❌ Rust не установлен. Установите: curl --proto =https --tlsv1.2 -sSf https://sh.rustup.rs | sh",
                "execution_time": 0,
            }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".rs", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            source_file = f.name

        executable = source_file.replace(".rs", "")

        try:
            # Компиляция
            compile_result = await self._run_command(
                ["rustc", source_file, "-o", executable]
            )
            if not compile_result["success"]:
                return {
                    "success": False,
                    "output": compile_result["output"],
                    "error": f"❌ Ошибка компиляции:\n{compile_result['error']}",
                    "execution_time": compile_result["execution_time"],
                }

            # Выполнение
            run_result = await self._run_command([executable])
            return run_result
        finally:
            if os.path.exists(source_file):
                os.unlink(source_file)
            if os.path.exists(executable):
                os.unlink(executable)

    async def _execute_bash(self, code: str) -> Dict[str, str]:
        """Выполнить Bash скрипт"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".sh", delete=False, dir=self.working_dir
        ) as f:
            f.write(code)
            filepath = f.name

        try:
            # Делаем исполняемым
            os.chmod(filepath, 0o755)
            result = await self._run_command(["bash", filepath])
            return result
        finally:
            os.unlink(filepath)

    async def _run_command(self, cmd: list) -> Dict[str, str]:
        """Выполнить команду с таймаутом"""
        import time

        start_time = time.time()

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.working_dir,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=self.timeout
                )

                execution_time = time.time() - start_time

                return {
                    "success": process.returncode == 0,
                    "output": stdout.decode("utf-8", errors="replace"),
                    "error": stderr.decode("utf-8", errors="replace"),
                    "execution_time": round(execution_time, 3),
                }
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return {
                    "success": False,
                    "output": "",
                    "error": f"❌ Превышен таймаут {self.timeout} секунд",
                    "execution_time": self.timeout,
                }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"❌ Ошибка запуска команды: {str(e)}",
                "execution_time": time.time() - start_time,
            }

    def get_supported_languages(self) -> list:
        """Получить список поддерживаемых языков"""
        return [
            "Python",
            "JavaScript/Node.js",
            "TypeScript",
            "C",
            "C++",
            "Go",
            "Rust",
            "Bash/Shell",
        ]

    def cleanup(self):
        """Очистить временные файлы"""
        try:
            for file in os.listdir(self.working_dir):
                filepath = os.path.join(self.working_dir, file)
                try:
                    os.unlink(filepath)
                except:
                    pass
        except:
            pass


# Пример использования
if __name__ == "__main__":

    async def test():
        executor = MultiLanguageExecutor()

        # Python
        print("🐍 Python:")
        result = await executor.execute_code('print("Hello from Python!")', "python")
        print(f"   {result}")

        # JavaScript
        print("\n📜 JavaScript:")
        result = await executor.execute_code(
            'console.log("Hello from Node.js!")', "javascript"
        )
        print(f"   {result}")

        # C++
        print("\n⚙️ C++:")
        cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello from C++!" << std::endl;
    return 0;
}
"""
        result = await executor.execute_code(cpp_code, "cpp")
        print(f"   {result}")

        print(f"\n✅ Поддерживаемые языки: {executor.get_supported_languages()}")

    asyncio.run(test())
