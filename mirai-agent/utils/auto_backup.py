import os
import datetime
import shutil
import logging

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def backup_files(source_dirs, backup_dir):
    try:
        # Создаем резервную папку для сегодняшней даты
        today = datetime.date.today().isoformat()
        daily_backup_dir = os.path.join(backup_dir, today)
        os.makedirs(daily_backup_dir, exist_ok=True)
        logging.info(f'Создана папка для резервного копирования: {daily_backup_dir}')

        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                # Копируем файлы
                destination = os.path.join(daily_backup_dir, os.path.basename(source_dir))
                shutil.copytree(source_dir, destination)
                logging.info(f'Резервная копия папки {source_dir} сохранена в {destination}')
            else:
                logging.warning(f'Исходная папка не найдена: {source_dir}')

    except Exception as e:
        logging.error(f'Ошибка при выполнении резервного копирования: {e}')

if __name__ == '__main__':
    # Пример использования
    source_directories = ['/path/to/important/files1', '/path/to/important/files2']  # Замените на свои пути
    backup_directory = '/path/to/backup/location'  # Путь для хранения резервных копий
    backup_files(source_directories, backup_directory)