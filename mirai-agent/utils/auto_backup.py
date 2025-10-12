import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='backup.log',
                    format='%(asctime)s:%(levelname)s:%(message)s')

def backup_files(source_dirs, backup_dir):
    try:
        # Проверка, существует ли директория для бэкапа
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Создана директория для бэкапа: {backup_dir}')

        for source_dir in source_dirs:
            # Проверка, существует ли источник
            if os.path.exists(source_dir):
                # Формируем путь бэкапа
                dir_name = os.path.basename(os.path.normpath(source_dir))
                target_dir = os.path.join(backup_dir, dir_name + '-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
                # Копирование файлов
                shutil.copytree(source_dir, target_dir)
                logging.info(f'Бэкап директорий {source_dir} в {target_dir}')
            else:
                logging.warning(f'Источник не найден: {source_dir}')

    except Exception as e:
        logging.error(f'Ошибка во время бэкапа: {str(e)}')

if __name__ == '__main__':
    # Примеры директорий для бэкапа
    source_dirs = ['/path/to/important/files', '/another/path/to/backup']
    backup_dir = '/path/to/backup/directory'
    backup_files(source_dirs, backup_dir)
