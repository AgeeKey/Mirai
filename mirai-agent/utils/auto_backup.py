import os
import shutil
import logging
import time

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def backup_files(source_dir, target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            logging.info(f'Создана директория для бэкапа: {target_dir}')

        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(target_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
                logging.info(f'Бэкап директории {s} в {d}')
            else:
                shutil.copy2(s, d)
                logging.info(f'Бэкап файла {s} в {d}')

    except Exception as e:
        logging.error(f'Ошибка при бэкапе: {str(e)}')

if __name__ == '__main__':
    source_directory = 'важные_файлы'  # Укажите ваш источник
    target_directory = f'бэкапы/backup_{time.strftime('%Y%m%d_%H%M%S')}'
    backup_files(source_directory, target_directory)
    logging.info('Бэкап завершён успешно.')