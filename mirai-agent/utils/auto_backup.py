import os
import shutil
import datetime
def create_backup(source_dirs, backup_dir):
    # Получаем текущую дату и время для имени папки бэкапа
    now = datetime.datetime.now()
    backup_folder_name = now.strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, backup_folder_name)
    os.makedirs(backup_path, exist_ok=True)
    log_entries = []
    
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            # Копируем содержимое файловой директории в директорию бэкапа
            dest_dir = os.path.join(backup_path, os.path.basename(source_dir))
            shutil.copytree(source_dir, dest_dir)
            log_entry = f'Содержимое {source_dir} успешно скопировано в {dest_dir}'
            log_entries.append(log_entry)
        else:
            log_entry = f'Ошибка: {source_dir} не найден'
            log_entries.append(log_entry)
    
    # Записываем лог
    with open(os.path.join(backup_path, 'backup_log.txt'), 'w') as log_file:
        log_file.write('\n'.join(log_entries))
    print(f'Бэкап успешно создан в {backup_path}')

# Пример использования
source_directories = ['/путь/к/вашему/важному/директории1', '/путь/к/вашему/важному/директории2']
backup_directory = '/путь/к/директории/бэкапа'
create_backup(source_directories, backup_directory)