import os
import shutil
import logging
import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Создан каталог для бэкапа: {backup_dir}')

        # Копирование файлов
        for filename in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, filename)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, backup_dir)
                logging.info(f'Копирован файл: {full_file_name} в {backup_dir}')
        logging.info('Бэкап завершён успешно.')
    except Exception as e:
        logging.error(f'Ошибка при выполнении бэкапа: {str(e)}')

if __name__ == '__main__':
    source_directory = 'path/to/your/important/files'
    backup_directory = 'path/to/your/backup'
    backup_files(source_directory, backup_directory)
