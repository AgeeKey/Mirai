import os
import shutil
import logging
import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Функция для выполнения бэкапа

def backup_files(source_dirs, backup_dir):
    for src in source_dirs:
        if os.path.exists(src):
            try:
                # Получение имени директории
                dir_name = os.path.basename(src)
                destination = os.path.join(backup_dir, f"{dir_name}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                shutil.copytree(src, destination)
                logging.info(f"Бэкап для {src} выполнен успешно в {destination}")
            except Exception as e:
                logging.error(f"Ошибка при бэкапе {src}: {e}")
        else:
            logging.warning(f"Исходная директория {src} не существует")


# Пример использования
if __name__ == "__main__":
    source_directories = ['/path/to/important/files', '/another/path/to/important/data']  # Измените на ваши директории
    backup_directory = '/path/to/backup/location'  # Измените на место для хранения бэкапов
    backup_files(source_directories, backup_directory)
