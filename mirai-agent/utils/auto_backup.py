import os
import shutil
import datetime
import logging

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def backup_files(source_dir, backup_dir):
    try:
        # Создаем имя папки для бэкапа с текущей датой
        date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = os.path.join(backup_dir, f'backup_{date_str}')

        # Копируем файлы
def main():
            os.makedirs(backup_path, exist_ok=True)
        files = os.listdir(source_dir)
        for file_name in files:
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, backup_path)
                logging.info(f'Файл {file_name} был успешно скопирован в {backup_path}')

        logging.info('Бэкап завершен успешно.')
    except Exception as e:
        logging.error(f'Произошла ошибка: {e}')

if __name__ == '__main__':
    source_directory = 'path/to/your/important/files'
    backup_directory = 'path/to/your/backup/directory'
    backup_files(source_directory, backup_directory)