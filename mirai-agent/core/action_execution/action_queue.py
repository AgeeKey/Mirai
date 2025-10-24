#!/usr/bin/env python3
"""
📋 Action Queue - Очередь действий
Шаг 3 из 150: Initialize Action Queue

FIFO queue для выполнения действий
"""

import asyncio
import logging
from typing import Optional, List
from queue import Queue, Empty
from datetime import datetime
from .action_executor import Action, ActionStatus

logger = logging.getLogger(__name__)


class ActionQueue:
    """
    Очередь действий FIFO
    
    Функции:
    - Добавление действий в очередь
    - Извлечение действий для выполнения
    - Приоритизация действий
    - Управление очередью
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Инициализация очереди
        
        Args:
            max_size: Максимальный размер очереди
        """
        self.queue: Queue = Queue(maxsize=max_size)
        self.max_size = max_size
        self.total_enqueued = 0
        self.total_dequeued = 0
        self.priority_queue: List[Action] = []
        
        logger.info(f"📋 ActionQueue создана (max_size={max_size})")
    
    def enqueue(self, action: Action, priority: bool = False) -> bool:
        """
        Добавить действие в очередь
        
        Args:
            action: Действие для добавления
            priority: Добавить в начало очереди (высокий приоритет)
            
        Returns:
            bool: True если добавлено успешно
        """
        try:
            if priority:
                self.priority_queue.insert(0, action)
                logger.info(f"⭐ Действие добавлено с приоритетом: {action.description}")
            else:
                self.queue.put_nowait(action)
                logger.debug(f"➕ Действие добавлено в очередь: {action.description}")
            
            self.total_enqueued += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка добавления в очередь: {e}")
            return False
    
    def dequeue(self, timeout: float = 1.0) -> Optional[Action]:
        """
        Извлечь следующее действие из очереди
        
        Args:
            timeout: Таймаут ожидания (секунды)
            
        Returns:
            Action или None
        """
        try:
            # Сначала проверяем приоритетную очередь
            if self.priority_queue:
                action = self.priority_queue.pop(0)
                self.total_dequeued += 1
                logger.debug(f"⭐ Извлечено приоритетное действие: {action.description}")
                return action
            
            # Затем основную очередь
            action = self.queue.get(timeout=timeout)
            self.total_dequeued += 1
            logger.debug(f"➖ Извлечено действие из очереди: {action.description}")
            return action
            
        except Empty:
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения из очереди: {e}")
            return None
    
    def peek(self) -> Optional[Action]:
        """
        Посмотреть следующее действие без извлечения
        
        Returns:
            Action или None
        """
        if self.priority_queue:
            return self.priority_queue[0]
        
        if not self.queue.empty():
            # Peek не поддерживается напрямую в Queue
            # Возвращаем None, используйте dequeue
            return None
        
        return None
    
    def size(self) -> int:
        """Текущий размер очереди"""
        return self.queue.qsize() + len(self.priority_queue)
    
    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.queue.empty() and len(self.priority_queue) == 0
    
    def is_full(self) -> bool:
        """Проверка на заполненность"""
        return self.queue.full()
    
    def clear(self):
        """Очистить очередь"""
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except Empty:
                break
        
        self.priority_queue.clear()
        logger.info("🗑️ Очередь очищена")
    
    def get_stats(self) -> dict:
        """Получить статистику очереди"""
        return {
            'current_size': self.size(),
            'priority_size': len(self.priority_queue),
            'regular_size': self.queue.qsize(),
            'max_size': self.max_size,
            'total_enqueued': self.total_enqueued,
            'total_dequeued': self.total_dequeued,
            'is_empty': self.is_empty(),
            'is_full': self.is_full()
        }


# Тесты
if __name__ == "__main__":
    from .action_executor import ActionType
    
    # Создаем очередь
    queue = ActionQueue(max_size=10)
    
    # Добавляем действия
    action1 = Action(
        id="1",
        type=ActionType.MOUSE_CLICK,
        parameters={},
        description="Действие 1"
    )
    
    action2 = Action(
        id="2",
        type=ActionType.KEYBOARD_TYPE,
        parameters={},
        description="Действие 2 (приоритет)"
    )
    
    action3 = Action(
        id="3",
        type=ActionType.WINDOW_FOCUS,
        parameters={},
        description="Действие 3"
    )
    
    # Тестируем
    queue.enqueue(action1)
    queue.enqueue(action3)
    queue.enqueue(action2, priority=True)  # Добавляем с приоритетом
    
    print("\n" + "="*60)
    print("📊 СТАТИСТИКА ОЧЕРЕДИ")
    print("="*60)
    stats = queue.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*60)
    print("📋 ИЗВЛЕЧЕНИЕ ИЗ ОЧЕРЕДИ")
    print("="*60)
    while not queue.is_empty():
        action = queue.dequeue()
        if action:
            print(f"✓ {action.description}")
    
    print("\n✅ Тест очереди завершен")
