import os
import shutil
import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='backup.log', format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создан_backup_каталог: {backup_dir}')
    
    try:
        # Получаем текущее время для создания уникальной папки
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_subdir = os.path.join(backup_dir, f'backup_{timestamp}')
        os.makedirs(backup_subdir)
        logging.info(f'Создан_каталог_резервной_копии: {backup_subdir}')
        
        # Копирование файлов
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            destination_item = os.path.join(backup_subdir, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, destination_item)
                logging.info(f'Скопирован файл: {source_item} -> {destination_item}')
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
                logging.info(f'Скопирована папка: {source_item} -> {destination_item}')
        
        logging.info('Резервное копирование завершено успешно.')
    except Exception as e:
        logging.error(f'Ошибка при резервном копировании: {e}')

# Пример использования
if __name__ == '__main__':
    source_directory = '/path/to/important/files'
    backup_directory = '/path/to/backup/location'
    backup_files(source_directory, backup_directory)