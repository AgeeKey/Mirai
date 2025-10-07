# 🧪 Тест автоматизации GitHub Copilot

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def test_copilot_automation():
    """
    Эта функция проверяет работу автоматизации Copilot.
    Начните печатать код ниже - Copilot должен предлагать автодополнения.
    """
    pass
    
    
# Начните писать функцию для сортировки списка  
def sort_list(data):
    return sorted(data)


# Начните писать класс для работы с данными
class DataProcessor:
    def __init__(self):
        self.data = []
    
    def add_data(self, item):
        self.data.append(item)
    
    def process(self):
        return sorted(self.data)


if __name__ == "__main__":
    print("🤖 Тест автоматизации GitHub Copilot запущен!")
    print("💡 Начните писать код выше и наблюдайте за автодополнениями")
    
    # Тестируем функции
    test = DataProcessor()
    test.add_data(3)
    test.add_data(1) 
    test.add_data(2)
    print(f"Результат: {test.process()}")
    print(f"Факториал 5: {factorial(5)}")