import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Функция для создания бэкапа
def backup_files(source_dirs, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создан каталог бэкапа: {backup_dir}')

    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            try:
                shutil.copytree(source_dir, os.path.join(backup_dir, os.path.basename(source_dir)), dirs_exist_ok=True)
                logging.info(f'Успешный бэкап {source_dir} в {backup_dir}')
            except Exception as e:
                logging.error(f'Ошибка при бэкапе {source_dir}: {e}')
        else:
            logging.warning(f'Исходный каталог не найден: {source_dir}')

if __name__ == '__main__':
    source_directories = ['/path/to/important/files1', '/path/to/important/files2']  # Указать важные файлы
    backup_directory = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'  # Уникальный каталог бэкапа по времени
    backup_files(source_directories, backup_directory)