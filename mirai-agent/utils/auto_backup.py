import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к важным файлам и папке бэкапа
important_files = ['/path/to/important/file1.txt', '/path/to/important/file2.txt']
backup_folder = '/path/to/backup'

def create_backup():
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        logging.info('Создана папка для бэкапа: {}'.format(backup_folder))

    for file in important_files:
        try:
            if os.path.exists(file):
                shutil.copy(file, backup_folder)
                logging.info('Файл {} успешно скопирован в {}'.format(file, backup_folder))
            else:
                logging.warning('Файл {} не найден'.format(file))
        except Exception as e:
            logging.error('Ошибка при копировании {}: {}'.format(file, e))

if __name__ == '__main__':
    logging.info('Начинаем процесс бэкапа')
    create_backup()
    logging.info('Процесс бэкапа завершен')