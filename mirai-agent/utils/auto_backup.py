import os
import shutil
import logging
import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    try:
        # Создание директории бэкапа, если ее нет
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Создана директория для бэкапа: {backup_dir}')

        # Копирование файлов
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(backup_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
                logging.info(f'Скопирована директория: {s} в {d}')
            else:
                shutil.copy2(s, d)
                logging.info(f'Скопирован файл: {s} в {d}')

        logging.info('Бэкап завершен успешно')
    except Exception as e:
        logging.error(f'Ошибка при создании бэкапа: {e}')

if __name__ == '__main__':
    source_directory = '/path/to/your/important/files'
    backup_directory = '/path/to/your/backup/location'
    backup_files(source_directory, backup_directory)
