"""
MIRAI FAISS-based RAG System
Fast and efficient local vector storage using FAISS
"""

import json
import logging
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np
import tiktoken
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class FAISSRAGSystem:
    """
    RAG system using FAISS for local vector storage
    
    Features:
    - Fast similarity search
    - Local embeddings (no API calls)
    - Persistent storage
    - Chunk management with metadata
    """

    def __init__(
        self,
        collection_name: str = "mirai_knowledge",
        persist_directory: str = "data/faiss_index",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ):
        """
        Initialize FAISS RAG system

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist index
            embedding_model: Sentence-transformer model name
            chunk_size: Text chunk size in tokens
            chunk_overlap: Overlap between chunks
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize embedding model (local, no API)
        logger.info(f"📥 Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

        # Initialize or load FAISS index
        self.index = None
        self.documents = []  # Store document metadata
        self.load_or_create_index()

        # Metrics for hit@k tracking
        self.metrics = {
            "total_queries": 0,
            "hits_at_1": 0,
            "hits_at_3": 0,
            "hits_at_5": 0,
            "avg_retrieval_time_ms": 0.0,
        }

    def load_or_create_index(self):
        """Load existing index or create new one"""
        index_path = self.persist_directory / f"{self.collection_name}.index"
        docs_path = self.persist_directory / f"{self.collection_name}.docs.pkl"
        metrics_path = self.persist_directory / f"{self.collection_name}.metrics.json"

        if index_path.exists() and docs_path.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(index_path))

                # Load documents metadata
                with open(docs_path, "rb") as f:
                    self.documents = pickle.load(f)

                # Load metrics
                if metrics_path.exists():
                    with open(metrics_path, "r") as f:
                        self.metrics = json.load(f)

                logger.info(
                    f"✅ Loaded FAISS index: {len(self.documents)} documents"
                )
            except Exception as e:
                logger.error(f"Failed to load index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Create new FAISS index"""
        # Use IndexFlatL2 for exact search (good for small datasets)
        # For larger datasets, consider IndexIVFFlat or IndexHNSWFlat
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.documents = []
        logger.info(f"✅ Created new FAISS index (dim={self.embedding_dim})")

    def save_index(self):
        """Save index and documents to disk"""
        index_path = self.persist_directory / f"{self.collection_name}.index"
        docs_path = self.persist_directory / f"{self.collection_name}.docs.pkl"
        metrics_path = self.persist_directory / f"{self.collection_name}.metrics.json"

        try:
            # Save FAISS index
            faiss.write_index(self.index, str(index_path))

            # Save documents metadata
            with open(docs_path, "wb") as f:
                pickle.dump(self.documents, f)

            # Save metrics
            with open(metrics_path, "w") as f:
                json.dump(self.metrics, f, indent=2)

            logger.info(f"💾 Saved index: {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))

    def chunk_text(self, text: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Split text into chunks with overlap

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of chunk dicts with text and metadata
        """
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunk_data = {
                "text": chunk_text,
                "tokens": len(chunk_tokens),
                "metadata": metadata or {},
                "chunk_index": len(chunks),
            }
            chunks.append(chunk_data)

            start += self.chunk_size - self.chunk_overlap

        return chunks

    def add_document(
        self, text: str, source: str, metadata: Optional[Dict] = None
    ) -> int:
        """
        Add document to index

        Args:
            text: Document text
            source: Source identifier (file path, URL, etc.)
            metadata: Additional metadata

        Returns:
            Number of chunks added
        """
        # Prepare metadata
        doc_metadata = metadata or {}
        doc_metadata["source"] = source

        # Chunk the text
        chunks = self.chunk_text(text, doc_metadata)

        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)

        # Add to FAISS index
        embeddings_np = np.array(embeddings).astype("float32")
        self.index.add(embeddings_np)

        # Store document metadata
        for chunk in chunks:
            self.documents.append(chunk)

        logger.info(
            f"📄 Added document: {source} ({len(chunks)} chunks, "
            f"{self.count_tokens(text)} tokens)"
        )

        return len(chunks)

    def add_documents_from_directory(
        self, directory: str, pattern: str = "*.md"
    ) -> int:
        """
        Add all documents from directory

        Args:
            directory: Directory path
            pattern: File pattern (e.g., "*.md", "*.txt")

        Returns:
            Total number of chunks added
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            logger.warning(f"Directory not found: {directory}")
            return 0

        total_chunks = 0
        files = list(dir_path.glob(pattern))

        logger.info(f"📂 Indexing {len(files)} files from {directory}")

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                chunks = self.add_document(
                    text=text,
                    source=str(file_path.relative_to(dir_path.parent)),
                    metadata={"filename": file_path.name, "extension": file_path.suffix},
                )
                total_chunks += chunks

            except Exception as e:
                logger.error(f"Failed to index {file_path}: {e}")

        self.save_index()
        logger.info(f"✅ Indexed {total_chunks} chunks from {len(files)} files")
        return total_chunks

    def search(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Search for relevant chunks

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of (document, score) tuples
        """
        import time

        start_time = time.time()

        if self.index.ntotal == 0:
            logger.warning("Index is empty")
            return []

        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], show_progress_bar=False)
        query_embedding_np = np.array(query_embedding).astype("float32")

        # Search
        distances, indices = self.index.search(query_embedding_np, min(top_k, self.index.ntotal))

        # Prepare results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                # Convert L2 distance to similarity score (0-1)
                score = 1.0 / (1.0 + distance)
                results.append((doc, score))

        # Update metrics
        elapsed_ms = (time.time() - start_time) * 1000
        self.metrics["total_queries"] += 1
        
        # Update average retrieval time
        n = self.metrics["total_queries"]
        self.metrics["avg_retrieval_time_ms"] = (
            self.metrics["avg_retrieval_time_ms"] * (n - 1) + elapsed_ms
        ) / n

        logger.debug(f"🔍 Search completed in {elapsed_ms:.2f}ms, found {len(results)} results")

        return results

    def get_relevant_context(
        self, query: str, max_chunks: int = 5, max_tokens: int = 2000
    ) -> str:
        """
        Get relevant context for query

        Args:
            query: Search query
            max_chunks: Maximum number of chunks to retrieve
            max_tokens: Maximum total tokens in context

        Returns:
            Concatenated context string
        """
        results = self.search(query, top_k=max_chunks)

        context_parts = []
        total_tokens = 0

        for doc, score in results:
            text = doc["text"]
            tokens = doc["tokens"]

            if total_tokens + tokens <= max_tokens:
                source = doc["metadata"].get("source", "unknown")
                context_parts.append(f"[Source: {source}]\n{text}")
                total_tokens += tokens
            else:
                break

        context = "\n\n---\n\n".join(context_parts)
        return context

    def update_hit_metrics(self, query: str, relevant_sources: List[str], k: int = 5):
        """
        Update hit@k metrics

        Args:
            query: Query that was searched
            relevant_sources: List of sources that should be in results
            k: Number of top results to check
        """
        results = self.search(query, top_k=k)

        # Check if relevant source is in top results
        found_sources = {doc["metadata"].get("source") for doc, _ in results}

        for relevant_source in relevant_sources:
            if relevant_source in found_sources:
                # Update hit counts
                if k >= 1:
                    self.metrics["hits_at_1"] += 1
                if k >= 3:
                    self.metrics["hits_at_3"] += 1
                if k >= 5:
                    self.metrics["hits_at_5"] += 1
                break  # Count once per query

    def get_hit_rate(self, k: int = 5) -> float:
        """
        Get hit@k rate

        Args:
            k: Number of top results

        Returns:
            Hit rate as percentage (0-100)
        """
        total = self.metrics["total_queries"]
        if total == 0:
            return 0.0

        if k == 1:
            hits = self.metrics["hits_at_1"]
        elif k == 3:
            hits = self.metrics["hits_at_3"]
        elif k == 5:
            hits = self.metrics["hits_at_5"]
        else:
            return 0.0

        return (hits / total) * 100.0

    def get_stats(self) -> Dict:
        """Get RAG system statistics"""
        return {
            "total_documents": len(self.documents),
            "index_size": self.index.ntotal,
            "embedding_dim": self.embedding_dim,
            "metrics": self.metrics,
            "hit_rate_1": self.get_hit_rate(1),
            "hit_rate_3": self.get_hit_rate(3),
            "hit_rate_5": self.get_hit_rate(5),
        }

    def clear(self):
        """Clear all documents and index"""
        self._create_new_index()
        logger.info("🗑️ Cleared index")


if __name__ == "__main__":
    # Test the RAG system
    print("🧪 Testing FAISS RAG System...")
    
    rag = FAISSRAGSystem(persist_directory="/tmp/test_faiss")
    
    # Add test documents
    rag.add_document(
        text="MIRAI is an autonomous AI agent for trading and self-improvement.",
        source="test_doc_1.md",
        metadata={"topic": "overview"}
    )
    
    rag.add_document(
        text="The agent uses GPT-4o-mini for fast inference and decision making.",
        source="test_doc_2.md",
        metadata={"topic": "architecture"}
    )
    
    # Search
    results = rag.search("What is MIRAI?", top_k=3)
    print(f"\n✅ Search results: {len(results)}")
    for doc, score in results:
        print(f"  Score: {score:.3f} - {doc['text'][:80]}...")
    
    # Get context
    context = rag.get_relevant_context("AI agent", max_chunks=3)
    print(f"\n✅ Context retrieved: {len(context)} chars")
    
    # Stats
    stats = rag.get_stats()
    print(f"\n✅ Stats: {stats}")
