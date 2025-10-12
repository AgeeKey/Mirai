import json
import os

# Определение путей к файлам состояния агента
state_file_path = os.path.join('data', 'state', 'agent_state.json')

# Функция для сбора и записи статуса агента
def report_agent_status():
    try:
        # Чтение состояния из JSON файла
        with open(state_file_path, 'r') as f:
            agent_state = json.load(f)
        
        # Формирование отчета
        report = {
            'agent_status': agent_state.get('status'),
            'tasks': agent_state.get('tasks')
        }
        
        # Запись отчета в файл
        report_file_path = os.path.join('data', 'status_report.json')
        with open(report_file_path, 'w') as report_file:
            json.dump(report, report_file, indent=4)
        
        print("Отчет о состоянии агента успешно записан в ", report_file_path)
    except Exception as e:
        print("Ошибка при создании отчета: ", e)

# Выполнение функции
if __name__ == '__main__':
    report_agent_status()