import os
import shutil
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к важным файлам и директории для бэкапа
important_files = ['/path/to/important/file1', '/path/to/important/file2']
destination_folder = '/path/to/backup/folder/'

# Функция для создания бэкапа
def backup_files(files, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
        logging.info(f'Создана директория для бэкапа: {destination}')
    for file in files:
        if os.path.exists(file):
            shutil.copy(file, destination)
            logging.info(f'Файл {file} скопирован в {destination}')
        else:
            logging.warning(f'Файл {file} не найден')

# Основная функция
if __name__ == '__main__':
    while True:
        logging.info('Запуск бэкапа...')
        backup_files(important_files, destination_folder)
        logging.info('Бэкап завершен. Ожидание перед следующим запуском...')
        time.sleep(86400)  # Ожидание 24 часа
