import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)  # Создать каталог, если он не существует
        
        # Копирование файлов
        for filename in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, filename)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, backup_dir)
                logging.info(f'Файл {filename} успешно сохранен в {backup_dir}')

        logging.info('Бэкап завершен успешно.')
    except Exception as e:
        logging.error(f'Ошибка во время бэкапа: {e}')

if __name__ == '__main__':
    # Задайте свои каталоги
    source_directory = 'важные_файлы'
    backup_directory = 'бэкапы'
    # Запуск бэкапа
    backup_files(source_directory, backup_directory)