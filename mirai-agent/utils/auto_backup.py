import os
import shutil
import datetime
import logging

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def backup_files(source_dirs, backup_dir):
    """Создает резервные копии файлов из указанных директорий."""
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_subdir = os.path.join(backup_dir, f'backup_{current_time}')
    
    try:
        os.makedirs(backup_subdir)
        logging.info(f'Создана директория для бэкапа: {backup_subdir}')
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                # Копируем директорию
                shutil.copytree(source_dir, os.path.join(backup_subdir, os.path.basename(source_dir)))
                logging.info(f'Бэкап директории {source_dir} успешно завершен.')
            else:
                logging.warning(f'Директория источника не найдена: {source_dir}')
    except Exception as e:
        logging.error(f'Ошибка при выполнении бэкапа: {e}')

if __name__ == '__main__':
    # Пример использования
    source_directories = ['/path/to/important/files1', '/path/to/important/files2']
    backup_directory = '/path/to/backup'
    backup_files(source_directories, backup_directory)