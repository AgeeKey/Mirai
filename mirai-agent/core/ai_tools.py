"""
AI TOOLS - Дополнительные возможности для AI агента
"""

import asyncio
import subprocess
import os
from typing import Optional, List, Dict
import requests
from bs4 import BeautifulSoup


class AITools:
    """Инструменты для расширения возможностей AI"""
    
    def __init__(self):
        self.web_dir = "/root/mirai/mirai-agent/web"
        
    async def search_internet(self, query: str, max_results: int = 5) -> str:
        """
        Поиск информации в интернете
        Использует DuckDuckGo HTML (не требует API ключа)
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._search_sync, query, max_results)
        except Exception as e:
            return f"❌ Ошибка поиска: {e}"
    
    def _search_sync(self, query: str, max_results: int) -> str:
        """Синхронный поиск (вызывается через executor)"""
        try:
            # DuckDuckGo HTML поиск (простой, без API)
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Парсим результаты
            for result in soup.find_all('div', class_='result', limit=max_results):
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append(f"📌 {title}\n   {snippet}\n   🔗 {link}")
            
            if results:
                return f"🔍 Результаты поиска по запросу '{query}':\n\n" + "\n\n".join(results)
            else:
                return f"❌ Ничего не найдено по запросу '{query}'"
                
        except Exception as e:
            return f"❌ Ошибка при поиске: {e}"
    
    async def create_python_file(self, filename: str, code: str, description: str = "") -> str:
        """Создать Python файл"""
        try:
            filepath = os.path.join("/root/mirai/mirai-agent", filename)
            
            # Создаём директорию если нужно
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Пишем код
            with open(filepath, 'w', encoding='utf-8') as f:
                if description:
                    f.write(f'"""\n{description}\n"""\n\n')
                f.write(code)
            
            return f"✅ Python файл создан: {filepath}"
        except Exception as e:
            return f"❌ Ошибка создания Python файла: {e}"
    
    async def create_web_file(self, filename: str, content: str, file_type: str = "html") -> str:
        """
        Создать веб файл (HTML/CSS/JS)
        
        Args:
            filename: имя файла (например, "dashboard.html")
            content: содержимое файла
            file_type: тип файла (html, css, js)
        """
        try:
            filepath = os.path.join(self.web_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✅ Веб файл создан: {filepath}\n🌐 Доступен по: http://localhost:8000/static/{filename}"
        except Exception as e:
            return f"❌ Ошибка создания веб файла: {e}"
    
    async def run_python_code(self, code: str, timeout: int = 30) -> str:
        """
        Выполнить Python код (безопасно, с таймаутом)
        
        Args:
            code: Python код для выполнения
            timeout: максимальное время выполнения (секунды)
        """
        try:
            # Создаём временный файл
            temp_file = "/tmp/mirai_temp_code.py"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Выполняем через subprocess с таймаутом
            process = await asyncio.create_subprocess_exec(
                'python3', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8')
                errors = stderr.decode('utf-8')
                
                result = ""
                if output:
                    result += f"📤 Вывод:\n{output}\n"
                if errors:
                    result += f"⚠️ Ошибки:\n{errors}"
                
                return result or "✅ Код выполнен без вывода"
                
            except asyncio.TimeoutError:
                process.kill()
                return f"⏱️ Превышен таймаут ({timeout}с)"
                
        except Exception as e:
            return f"❌ Ошибка выполнения кода: {e}"
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    async def install_python_package(self, package: str) -> str:
        """Установить Python пакет через pip"""
        try:
            venv_pip = "/root/mirai/mirai-agent/venv/bin/pip"
            
            process = await asyncio.create_subprocess_exec(
                venv_pip, 'install', package,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return f"✅ Пакет {package} успешно установлен"
            else:
                return f"❌ Ошибка установки {package}:\n{stderr.decode('utf-8')}"
                
        except Exception as e:
            return f"❌ Ошибка установки пакета: {e}"
    
    async def read_file(self, filepath: str) -> str:
        """Прочитать файл"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"📄 Содержимое {filepath}:\n\n{content}"
        except Exception as e:
            return f"❌ Ошибка чтения файла: {e}"
    
    async def list_files(self, directory: str = ".") -> str:
        """Список файлов в директории"""
        try:
            files = os.listdir(directory)
            return f"📁 Файлы в {directory}:\n" + "\n".join(f"  • {f}" for f in files)
        except Exception as e:
            return f"❌ Ошибка чтения директории: {e}"


# Глобальный экземпляр
ai_tools = AITools()
