"""
MIRAI RAG System - Retrieval Augmented Generation

Возможности:
- Разбиение больших документов на чанки
- Векторизация через OpenAI Embeddings
- Хранение в Chroma DB
- Семантический поиск
- Работа с контекстом больше GPT лимита
"""

import os
from typing import List, Dict, Optional
from pathlib import Path
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import tiktoken


class MiraiRAG:
    """
    RAG система для MIRAI

    Позволяет работать с документами любого размера через:
    1. Разбиение на чанки (chunks)
    2. Создание векторных эмбеддингов
    3. Семантический поиск релевантных частей
    4. Подача только нужного контекста в GPT
    """

    def __init__(
        self,
        collection_name: str = "mirai_knowledge",
        persist_directory: str = "data/chroma_db",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Инициализация RAG системы

        Args:
            collection_name: Имя коллекции в Chroma
            persist_directory: Папка для хранения БД
            chunk_size: Размер чанка в символах
            chunk_overlap: Перекрытие между чанками
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Проверить OpenAI API ключ
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY не найден в переменных окружения!")

        # Создать embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"  # Дешевле чем ada-002
        )

        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        # Загрузить или создать vectorstore
        try:
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
            )
            logging.info(f"✅ RAG система инициализирована: {collection_name}")
        except Exception as e:
            logging.warning(f"⚠️ Создаю новую коллекцию: {e}")
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
            )

        # Tokenizer для подсчета токенов
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Подсчитать количество токенов в тексте"""
        return len(self.tokenizer.encode(text))

    def add_text(
        self, text: str, metadata: Dict = None, source: str = "unknown"
    ) -> int:
        """
        Добавить текст в RAG систему

        Args:
            text: Текст для добавления
            metadata: Дополнительные метаданные
            source: Источник текста

        Returns:
            Количество созданных чанков
        """
        logging.info(f"📝 Добавляю текст в RAG ({len(text)} символов)...")

        # Разбить на чанки
        chunks = self.text_splitter.split_text(text)

        # Создать документы
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = {
                "source": source,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "chunk_length": len(chunk),
                "tokens": self.count_tokens(chunk),
            }

            # Добавить пользовательские метаданные
            if metadata:
                doc_metadata.update(metadata)

            documents.append(Document(page_content=chunk, metadata=doc_metadata))

        # Добавить в vectorstore
        self.vectorstore.add_documents(documents)

        total_tokens = sum(doc.metadata["tokens"] for doc in documents)
        logging.info(
            f"✅ Добавлено {len(chunks)} чанков "
            f"({total_tokens} токенов) в RAG систему"
        )

        return len(chunks)

    def add_file(self, file_path: str, metadata: Dict = None) -> int:
        """
        Добавить файл в RAG систему

        Args:
            file_path: Путь к файлу
            metadata: Дополнительные метаданные

        Returns:
            Количество созданных чанков
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        logging.info(f"📄 Загружаю файл: {file_path.name}")

        # Прочитать файл
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Добавить метаданные файла
        file_metadata = {
            "filename": file_path.name,
            "filepath": str(file_path),
            "file_size": len(text),
        }

        if metadata:
            file_metadata.update(metadata)

        return self.add_text(text, metadata=file_metadata, source=str(file_path))

    def search(
        self, query: str, k: int = 5, filter_metadata: Dict = None
    ) -> List[Document]:
        """
        Семантический поиск в RAG системе

        Args:
            query: Поисковый запрос
            k: Количество результатов
            filter_metadata: Фильтр по метаданным

        Returns:
            List релевантных документов
        """
        logging.info(f"🔍 Поиск в RAG: '{query[:50]}...' (k={k})")

        results = self.vectorstore.similarity_search(query, k=k, filter=filter_metadata)

        total_tokens = sum(self.count_tokens(doc.page_content) for doc in results)
        logging.info(f"✅ Найдено {len(results)} чанков ({total_tokens} токенов)")

        return results

    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """
        Поиск с оценками релевантности

        Returns:
            List[(Document, score)] где score - похожесть (0-1)
        """
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        logging.info(f"🔍 Найдено {len(results)} результатов")
        for i, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get("source", "unknown")
            logging.info(f"  {i}. Score: {score:.3f} | Source: {source[:50]}")

        return results

    def get_context_for_query(
        self, query: str, max_tokens: int = 4000, k: int = 10
    ) -> str:
        """
        Получить оптимальный контекст для запроса

        Собирает релевантные чанки пока не достигнут лимит токенов

        Args:
            query: Поисковый запрос
            max_tokens: Максимум токенов контекста
            k: Количество кандидатов для поиска

        Returns:
            Собранный контекст
        """
        # Найти релевантные чанки
        results = self.search(query, k=k)

        context_parts = []
        total_tokens = 0

        for doc in results:
            chunk = doc.page_content
            tokens = self.count_tokens(chunk)

            if total_tokens + tokens <= max_tokens:
                context_parts.append(chunk)
                total_tokens += tokens
            else:
                break

        context = "\n\n---\n\n".join(context_parts)

        logging.info(
            f"✅ Собран контекст: {len(context_parts)} чанков, "
            f"{total_tokens} токенов"
        )

        return context

    def get_stats(self) -> Dict:
        """Получить статистику RAG системы"""
        collection = self.vectorstore._collection
        count = collection.count()

        return {
            "collection_name": self.collection_name,
            "total_chunks": count,
            "persist_directory": str(self.persist_directory),
        }

    def clear(self):
        """Очистить всю коллекцию"""
        self.vectorstore.delete_collection()
        logging.warning("🗑️ Коллекция очищена!")

    def delete_by_source(self, source: str):
        """Удалить все чанки из определенного источника"""
        # Chroma пока не поддерживает удаление по метаданным напрямую
        # Нужно найти ID и удалить
        logging.warning(f"🗑️ Удаление по source: {source}")


# Пример использования
def main():
    logging.basicConfig(level=logging.INFO)

    print("🧪 Тестирование RAG системы MIRAI...\n")

    # Создать RAG
    rag = MiraiRAG(collection_name="test_knowledge")

    # Тест 1: Добавить длинный текст
    print("📝 Тест 1: Добавление длинного текста...")
    long_text = (
        """
    Python - это высокоуровневый язык программирования общего назначения.
    Он был создан Гвидо ван Россумом в 1991 году.
    Python известен своей простотой и читаемостью кода.
    
    Основные особенности Python:
    1. Динамическая типизация
    2. Автоматическое управление памятью
    3. Богатая стандартная библиотека
    4. Поддержка множественных парадигм программирования
    
    Python используется в различных областях:
    - Веб-разработка (Django, Flask)
    - Машинное обучение (TensorFlow, PyTorch)
    - Анализ данных (Pandas, NumPy)
    - Автоматизация и скриптинг
    
    """
        * 3
    )  # Повторить 3 раза для большего объема

    chunks_added = rag.add_text(
        long_text,
        metadata={"category": "programming", "language": "ru"},
        source="python_intro.txt",
    )
    print(f"✅ Добавлено чанков: {chunks_added}\n")

    # Тест 2: Семантический поиск
    print("📝 Тест 2: Семантический поиск...")
    results = rag.search("машинное обучение", k=3)
    print(f"✅ Найдено результатов: {len(results)}")
    for i, doc in enumerate(results, 1):
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  {i}. {preview}...")
    print()

    # Тест 3: Получить контекст для запроса
    print("📝 Тест 3: Сборка контекста...")
    context = rag.get_context_for_query(
        "Расскажи про особенности Python", max_tokens=500
    )
    print(f"✅ Контекст собран: {len(context)} символов")
    print(f"Превью: {context[:200]}...\n")

    # Тест 4: Статистика
    print("📝 Тест 4: Статистика RAG...")
    stats = rag.get_stats()
    print(f"✅ Статистика:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    print()

    print("✅ Все тесты RAG пройдены!")


if __name__ == "__main__":
    # Загрузить .env для OpenAI ключа
    from dotenv import load_dotenv

    load_dotenv()

    main()
