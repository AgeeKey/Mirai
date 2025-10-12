logger.info("🛑 Полу... shutting down")
sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def signal_handler(signum, frame):
    """Обработчик сигнала завершения программы"""
    logger.info("🚨 Программа завершена")
    sys.exit(0)

async def main():
    """Главная асинхронная функция, запускающая агента"""
    logger.info("🚀 Запуск MIRAI автономного агента")
    # добавить реализацию основного цикла события

if __name__ == '__main__':
    # Запускаем основную функцию
    asyncio.run(main())
