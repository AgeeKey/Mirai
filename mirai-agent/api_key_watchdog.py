#!/usr/bin/env python3
"""
🛡️ API KEY WATCHDOG - Автоматический мониторинг здоровья API ключей
Защищает MIRAI от поломок связанных с API ключами
"""

import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/tmp/api_watchdog.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class APIKeyWatchdog:
    """Watchdog для мониторинга здоровья API ключей"""
    
    def __init__(self):
        self.config_path = Path(__file__).parent / "configs" / "api_keys.json"
        self.check_interval = 300  # 5 минут
        self.consecutive_failures = 0
        self.max_failures = 3
        
    def load_api_key(self):
        """Загрузить API ключ из конфига"""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            return config.get('openai')
        except Exception as e:
            logger.error(f"❌ Не могу загрузить конфиг: {e}")
            return None
    
    def test_api_key(self, api_key):
        """Проверить работает ли API ключ"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=5,
                timeout=10
            )
            
            return True, "OK"
            
        except Exception as e:
            return False, str(e)
    
    def kill_old_processes(self):
        """Убить старые процессы MIRAI (старше 1 дня)"""
        try:
            # Найти старые процессы
            cmd = """ps aux | grep -E "mirai.*autonomous|mirai_autonomous" | grep -v "grep\\|vscode\\|watchdog" | awk '$10 ~ /[0-9]+-[0-9]+/ || $11 ~ /[0-9]+-[0-9]+/ {print $2}'"""
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            old_pids = result.stdout.strip().split('\n')
            old_pids = [pid for pid in old_pids if pid.strip()]
            
            if old_pids:
                logger.warning(f"🔪 Найдены старые процессы: {old_pids}")
                for pid in old_pids:
                    try:
                        subprocess.run(['kill', '-9', pid], check=False)
                        logger.info(f"   ✅ Убит процесс {pid}")
                    except Exception as e:
                        logger.error(f"   ❌ Не могу убить {pid}: {e}")
                return len(old_pids)
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Ошибка при убийстве процессов: {e}")
            return 0
    
    def restart_service(self):
        """Перезапустить autonomous service"""
        try:
            logger.info("🔄 Перезапускаю autonomous service...")
            
            # Убить все процессы autonomous
            subprocess.run(['killall', '-9', 'python'], check=False)
            time.sleep(2)
            
            # Запустить новый
            service_path = Path(__file__).parent / "autonomous_service.py"
            log_path = "/tmp/mirai_autonomous.log"
            
            cmd = f"nohup python3 {service_path} > {log_path} 2>&1 &"
            subprocess.run(cmd, shell=True, cwd=Path(__file__).parent)
            
            time.sleep(5)
            
            # Проверить что запустилось
            result = subprocess.run(
                ['pgrep', '-f', 'autonomous_service.py'],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                logger.info(f"   ✅ Сервис перезапущен (PID: {result.stdout.strip()})")
                return True
            else:
                logger.error("   ❌ Не могу перезапустить сервис")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка при перезапуске: {e}")
            return False
    
    def send_alert(self, message):
        """Отправить алерт в Telegram"""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            
            bot_token = config.get('TELEGRAM_BOT_TOKEN')
            chat_id = config.get('TELEGRAM_CHAT_ID_ADMIN')
            
            if bot_token and chat_id:
                import requests
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': f"🚨 API WATCHDOG ALERT\n\n{message}",
                    'parse_mode': 'Markdown'
                }
                requests.post(url, json=data, timeout=10)
                logger.info("   📱 Алерт отправлен в Telegram")
                
        except Exception as e:
            logger.error(f"❌ Не могу отправить алерт: {e}")
    
    def check_health(self):
        """Проверить здоровье системы"""
        logger.info("🏥 Проверка здоровья API...")
        
        # 1. Загрузить ключ
        api_key = self.load_api_key()
        if not api_key:
            logger.error("❌ API ключ не найден в конфиге!")
            self.consecutive_failures += 1
            return False
        
        # 2. Проверить ключ
        is_valid, error = self.test_api_key(api_key)
        
        if is_valid:
            logger.info("✅ API ключ работает идеально!")
            self.consecutive_failures = 0
            
            # Убить старые процессы для профилактики
            killed = self.kill_old_processes()
            if killed > 0:
                logger.info(f"🧹 Убито {killed} старых процессов")
            
            return True
        else:
            logger.error(f"❌ API ключ НЕ работает: {error}")
            self.consecutive_failures += 1
            
            # Если много ошибок подряд - принять меры
            if self.consecutive_failures >= self.max_failures:
                logger.error(f"🚨 КРИТИЧНО: {self.consecutive_failures} ошибок подряд!")
                
                # Убить старые процессы
                self.kill_old_processes()
                
                # Перезапустить сервис
                if self.restart_service():
                    logger.info("✅ Сервис перезапущен, проверяю снова...")
                    time.sleep(10)
                    
                    # Проверить снова
                    is_valid_retry, _ = self.test_api_key(api_key)
                    if is_valid_retry:
                        logger.info("✅ После перезапуска всё работает!")
                        self.consecutive_failures = 0
                        return True
                
                # Отправить алерт
                alert_msg = f"""
❌ API ключ не работает {self.consecutive_failures} раз подряд!

Ошибка: {error}

Действия:
- Убиты старые процессы
- Перезапущен сервис
- Требуется проверка!

Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                self.send_alert(alert_msg)
            
            return False
    
    def run(self):
        """Запустить watchdog"""
        logger.info("🛡️ API KEY WATCHDOG ЗАПУЩЕН")
        logger.info(f"   Интервал проверки: {self.check_interval}s")
        logger.info(f"   Максимум ошибок: {self.max_failures}")
        logger.info("")
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                logger.info(f"{'='*60}")
                logger.info(f"🔄 ЦИКЛ #{cycle}")
                logger.info(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*60}")
                
                health = self.check_health()
                
                if health:
                    logger.info(f"✅ Цикл #{cycle} завершён успешно")
                else:
                    logger.warning(f"⚠️  Цикл #{cycle} завершён с ошибками")
                
                logger.info(f"😴 Сплю {self.check_interval}s...")
                logger.info("")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Watchdog остановлен пользователем")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
            self.send_alert(f"Watchdog crashed: {e}")


if __name__ == '__main__':
    watchdog = APIKeyWatchdog()
    watchdog.run()
