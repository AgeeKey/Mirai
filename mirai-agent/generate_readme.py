import os

# Функция для генерации структуры README файла

def generate_readme(path):
    content = f'# Структура проекта\n\n## {path}\n\n'
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            content += f'### {item}\nСодержимое:\n'
            content += generate_readme(item_path)  # Рекурсивный вызов для подпапок
        else:
            content += f'- {item}\n'
    return content

# Запись результата в файл
if __name__ == '__main__':
    root_path = '/root/mirai/mirai-agent'  # Путь к корневой директории проекта
    readme_content = generate_readme(root_path)
    # Сохранение в файл README
    with open('project_structure_readme.md', 'w') as readme_file:
        readme_file.write(readme_content)