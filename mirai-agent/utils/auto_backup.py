import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('backup.log'),
                              logging.StreamHandler()])

def backup_files(source_folder, backup_folder):
    try:
        # Проверка существования папки назначения
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            logging.info(f'Создана папка для бэкапа: {backup_folder}')

        # Получение текущего времени для уникальности бэкапа
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_subfolder = os.path.join(backup_folder, f'backup_{timestamp}')
        os.makedirs(backup_subfolder)

        # Копирование файлов
        for filename in os.listdir(source_folder):
            full_file_name = os.path.join(source_folder, filename)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, backup_subfolder)
                logging.info(f'Файл {filename} успешно скопирован в {backup_subfolder}')  
        logging.info('Бэкап завершен успешно.')
    except Exception as e:
        logging.error(f'Произошла ошибка: {e}') 

if __name__ == '__main__':
    source = 'important_files/'  # Папка с важными файлами
    backup = 'backups/'  # Папка для сохранения бэкапов
    backup_files(source, backup)