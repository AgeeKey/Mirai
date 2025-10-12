import os
import shutil
import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='backup.log', format='%(asctime)s - %(levelname)s - %(message)s')

# Настройки бэкапа
SOURCE_DIR = 'важные_файлы/'  # Папка с важными файлами
BACKUP_DIR = 'бэкапы/'  # Папка для бэкапов

def create_backup():
    try:
        # Получаем текущее время для уникальности имени папки бэкапа
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(BACKUP_DIR, f'backup_{timestamp}')

        # Копируем файлы
        shutil.copytree(SOURCE_DIR, backup_path)
        logging.info(f'Успешный бэкап в {backup_path}')
    except Exception as e:
        logging.error(f'Ошибка во время бэкапа: {e}')

if __name__ == '__main__':
    create_backup()