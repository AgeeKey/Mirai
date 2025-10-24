from core.multi_language_executor import MultiLanguageExecutor
import asyncio


if __name__ == '__main__':
    executor = MultiLanguageExecutor()
    # Вызов асинхронного метода для детального вывода ошибок
    res = asyncio.run(executor.execute_code('print("hello from async execute")', 'python'))
    print('ASYNC RESULT:', res)
    # Также проверим синхронную оболочку
    sync_res = executor.execute('python', 'print("hello from sync execute")')
    print('SYNC RESULT:', sync_res)
