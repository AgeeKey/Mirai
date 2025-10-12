import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Создана директория бэкапа: {backup_dir}')
        
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            backup_path = os.path.join(backup_dir, item)
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, backup_path)
                logging.info(f'Файл {source_path} скопирован в {backup_path}')
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, backup_path)
                logging.info(f'Директория {source_path} скопирована в {backup_path}')
        
        logging.info('Бэкап завершен успешно')
    except Exception as e:
        logging.error(f'Ошибка при выполнении бэкапа: {e}')

if __name__ == '__main__':
    # Укажите директории для бэкапа
    source_directory = 'path/to/source'
    backup_directory = 'path/to/backup'
    backup_files(source_directory, backup_directory)