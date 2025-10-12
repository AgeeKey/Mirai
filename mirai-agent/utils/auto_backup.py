import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    filename='backup_log.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создан каталог для бэкапа: {backup_dir}')
    
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(backup_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
            logging.info(f'Бэкап каталога: {s} в {d}')
        else:
            shutil.copy2(s, d)
            logging.info(f'Бэкап файла: {s} в {d}')

if __name__ == '__main__':
    source_directory = 'path/to/important/files'
    backup_directory = f'path/to/backup/directory/backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    backup_files(source_directory, backup_directory)
    logging.info('Бэкап завершен!')