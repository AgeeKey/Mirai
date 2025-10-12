"""
DATABASE MANAGER - Работа с разными базами данных
Поддержка: SQLite, PostgreSQL, MongoDB, Redis
"""

import sqlite3
import json
from typing import Any, Dict, List, Optional, Union
import asyncio
from datetime import datetime


class DatabaseManager:
    """Универсальный менеджер баз данных"""
    
    def __init__(self):
        self.connections = {}
        self.db_configs = {
            'sqlite': {'path': '/root/mirai/mirai-agent/data/mirai.db'},
            'postgres': {'host': 'localhost', 'port': 5432, 'database': 'mirai', 'user': 'mirai', 'password': ''},
            'mongodb': {'host': 'localhost', 'port': 27017, 'database': 'mirai'},
            'redis': {'host': 'localhost', 'port': 6379, 'db': 0}
        }
    
    # ============ SQLITE ============
    
    async def sqlite_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнить SQL запрос к SQLite"""
        try:
            conn = sqlite3.connect(self.db_configs['sqlite']['path'])
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                results = [{'affected_rows': cursor.rowcount}]
            
            conn.close()
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    # ============ POSTGRESQL ============
    
    async def postgres_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнить SQL запрос к PostgreSQL"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            config = self.db_configs['postgres']
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                results = [{'affected_rows': cursor.rowcount}]
            
            cursor.close()
            conn.close()
            return results
        except ImportError:
            return [{'error': 'PostgreSQL драйвер не установлен. Установите: pip install psycopg2-binary'}]
        except Exception as e:
            return [{'error': str(e)}]
    
    # ============ MONGODB ============
    
    async def mongodb_find(self, collection: str, query: Dict = None, limit: int = 100) -> List[Dict]:
        """Найти документы в MongoDB"""
        try:
            from pymongo import MongoClient
            
            config = self.db_configs['mongodb']
            client = MongoClient(config['host'], config['port'])
            db = client[config['database']]
            
            query = query or {}
            results = list(db[collection].find(query).limit(limit))
            
            # Конвертируем ObjectId в строки
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            client.close()
            return results
        except ImportError:
            return [{'error': 'MongoDB драйвер не установлен. Установите: pip install pymongo'}]
        except Exception as e:
            return [{'error': str(e)}]
    
    async def mongodb_insert(self, collection: str, document: Dict) -> Dict:
        """Вставить документ в MongoDB"""
        try:
            from pymongo import MongoClient
            
            config = self.db_configs['mongodb']
            client = MongoClient(config['host'], config['port'])
            db = client[config['database']]
            
            result = db[collection].insert_one(document)
            
            client.close()
            return {'inserted_id': str(result.inserted_id), 'success': True}
        except ImportError:
            return {'error': 'MongoDB драйвер не установлен. Установите: pip install pymongo'}
        except Exception as e:
            return {'error': str(e)}
    
    async def mongodb_update(self, collection: str, query: Dict, update: Dict) -> Dict:
        """Обновить документы в MongoDB"""
        try:
            from pymongo import MongoClient
            
            config = self.db_configs['mongodb']
            client = MongoClient(config['host'], config['port'])
            db = client[config['database']]
            
            result = db[collection].update_many(query, {'$set': update})
            
            client.close()
            return {'matched_count': result.matched_count, 'modified_count': result.modified_count, 'success': True}
        except ImportError:
            return {'error': 'MongoDB драйвер не установлен. Установите: pip install pymongo'}
        except Exception as e:
            return {'error': str(e)}
    
    # ============ REDIS ============
    
    async def redis_get(self, key: str) -> Optional[str]:
        """Получить значение из Redis"""
        try:
            import redis
            
            config = self.db_configs['redis']
            r = redis.Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)
            
            value = r.get(key)
            r.close()
            return value
        except ImportError:
            return None
        except Exception as e:
            return None
    
    async def redis_set(self, key: str, value: str, expire: int = None) -> bool:
        """Установить значение в Redis"""
        try:
            import redis
            
            config = self.db_configs['redis']
            r = redis.Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)
            
            if expire:
                r.setex(key, expire, value)
            else:
                r.set(key, value)
            
            r.close()
            return True
        except ImportError:
            return False
        except Exception as e:
            return False
    
    async def redis_delete(self, key: str) -> bool:
        """Удалить ключ из Redis"""
        try:
            import redis
            
            config = self.db_configs['redis']
            r = redis.Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)
            
            result = r.delete(key)
            r.close()
            return result > 0
        except ImportError:
            return False
        except Exception as e:
            return False
    
    async def redis_keys(self, pattern: str = '*') -> List[str]:
        """Получить список ключей из Redis"""
        try:
            import redis
            
            config = self.db_configs['redis']
            r = redis.Redis(host=config['host'], port=config['port'], db=config['db'], decode_responses=True)
            
            keys = r.keys(pattern)
            r.close()
            return keys
        except ImportError:
            return []
        except Exception as e:
            return []
    
    # ============ УТИЛИТЫ ============
    
    def configure_database(self, db_type: str, config: Dict):
        """Настроить подключение к БД"""
        if db_type in self.db_configs:
            self.db_configs[db_type].update(config)
            return True
        return False
    
    async def test_connection(self, db_type: str) -> Dict[str, Any]:
        """Проверить подключение к БД"""
        results = {
            'database': db_type,
            'status': 'unknown',
            'details': ''
        }
        
        try:
            if db_type == 'sqlite':
                await self.sqlite_query("SELECT 1")
                results['status'] = 'connected'
                results['details'] = f"SQLite: {self.db_configs['sqlite']['path']}"
            
            elif db_type == 'postgres':
                result = await self.postgres_query("SELECT version()")
                if 'error' not in result[0]:
                    results['status'] = 'connected'
                    results['details'] = 'PostgreSQL connected'
                else:
                    results['status'] = 'error'
                    results['details'] = result[0]['error']
            
            elif db_type == 'mongodb':
                result = await self.mongodb_find('test', {}, limit=1)
                if not result or 'error' not in result[0]:
                    results['status'] = 'connected'
                    results['details'] = 'MongoDB connected'
                else:
                    results['status'] = 'error'
                    results['details'] = result[0]['error']
            
            elif db_type == 'redis':
                value = await self.redis_set('mirai_test', 'ok', expire=10)
                if value:
                    results['status'] = 'connected'
                    results['details'] = 'Redis connected'
                else:
                    results['status'] = 'error'
                    results['details'] = 'Redis connection failed'
        
        except Exception as e:
            results['status'] = 'error'
            results['details'] = str(e)
        
        return results
    
    async def get_database_info(self) -> Dict[str, Any]:
        """Получить информацию о всех БД"""
        info = {}
        
        for db_type in ['sqlite', 'postgres', 'mongodb', 'redis']:
            info[db_type] = await self.test_connection(db_type)
        
        return info


# Пример использования
if __name__ == '__main__':
    async def test():
        db = DatabaseManager()
        
        print("🗄️ Тестирование баз данных:\n")
        
        # SQLite
        print("📦 SQLite:")
        result = await db.sqlite_query("SELECT datetime('now') as current_time")
        print(f"   {result}\n")
        
        # Информация о всех БД
        print("📊 Статус всех баз данных:")
        info = await db.get_database_info()
        for db_name, status in info.items():
            print(f"   {db_name}: {status['status']} - {status['details']}")
    
    asyncio.run(test())
