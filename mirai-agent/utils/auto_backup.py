import os
import shutil
import logging
import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s %(message)s')

def backup_files(source_dirs, backup_dir):
    # Создаем бэкап директорию, если она не существует
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создана директория для бэкапа: {backup_dir}')

    # Проходим по всем исходным директориям
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            # Создаем имя для бэкапного каталога
            dir_name = os.path.basename(os.path.normpath(source_dir))
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'{dir_name}_{timestamp}')
            # Копируем содержимое
            shutil.copytree(source_dir, backup_path)
            logging.info(f'Бэкап выполнен для: {source_dir} в {backup_path}')
        else:
            logging.warning(f'Исходная директория не найдена: {source_dir}')

if __name__ == '__main__':
    # Примеры директорий для бэкапа
    source_directories = ['/путь/к/вашему/важному/каталогу1', '/путь/к/вашему/важному/каталогу2']
    backup_directory = '/путь/к/директории/бэкапа'
    backup_files(source_directories, backup_directory)