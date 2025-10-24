#!/usr/bin/env python3
"""
🧠 Memory System - Steps 41-55
Подраздел 2.1: Memory Management

Features:
- Short-Term Memory Buffer (Step 41)
- Long-Term Memory Database (Step 42)
- Memory Encoding with Embeddings (Step 43)
- Semantic Search (Step 44)
- Memory Consolidation (Step 45)
- Session Memory (Step 46)
- Event-Action-Result Triples (Step 47)
"""

import logging
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from collections import deque
import json

logger = logging.getLogger(__name__)


@dataclass
class EventActionResult:
    """
    Step 47: Event-Action-Result Triple
    Structure: (Event, Action, Result)
    Each triple linked with timestamp
    Used for learning
    """
    event: Dict[str, Any]
    action: Dict[str, Any]
    result: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = False
    confidence: float = 0.0
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


class ShortTermMemory:
    """
    Step 41: Short-Term Memory Buffer
    - Last 20 actions
    - Last 50 observations
    - Current state of all applications
    """
    
    def __init__(self, action_buffer_size: int = 20, observation_buffer_size: int = 50):
        self.action_buffer: deque = deque(maxlen=action_buffer_size)
        self.observation_buffer: deque = deque(maxlen=observation_buffer_size)
        self.application_states: Dict[str, Dict] = {}
        self.created_at = datetime.now()
        
        logger.info(f"✅ Short-term memory initialized (actions: {action_buffer_size}, observations: {observation_buffer_size})")
    
    def add_action(self, action: Dict):
        """Add action to buffer"""
        action["timestamp"] = datetime.now().isoformat()
        self.action_buffer.append(action)
    
    def add_observation(self, observation: Dict):
        """Add observation to buffer"""
        observation["timestamp"] = datetime.now().isoformat()
        self.observation_buffer.append(observation)
    
    def update_application_state(self, app_name: str, state: Dict):
        """Update application state"""
        self.application_states[app_name] = {
            **state,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_recent_actions(self, count: int = 5) -> List[Dict]:
        """Get N most recent actions"""
        return list(self.action_buffer)[-count:]
    
    def get_recent_observations(self, count: int = 10) -> List[Dict]:
        """Get N most recent observations"""
        return list(self.observation_buffer)[-count:]
    
    def get_application_state(self, app_name: str) -> Optional[Dict]:
        """Get current state of application"""
        return self.application_states.get(app_name)
    
    def clear(self):
        """Clear all buffers"""
        self.action_buffer.clear()
        self.observation_buffer.clear()
        self.application_states.clear()
        logger.info("🧹 Short-term memory cleared")


class LongTermMemory:
    """
    Step 42: Long-Term Memory Database
    - SQLite database with history
    - Indexes for fast search
    - Retention policy (90 days)
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "data" / "long_term_memory.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.retention_days = 90
        
        self._init_database()
        logger.info(f"✅ Long-term memory initialized at {db_path}")
    
    def _init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Event-Action-Result table (Step 47)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS event_action_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT NOT NULL,
                    action TEXT NOT NULL,
                    result TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    confidence REAL,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for fast search
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON event_action_results(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_success 
                ON event_action_results(success)
            """)
            
            # Embeddings table for semantic search (Step 43)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    embedding BLOB,
                    dimension INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES event_action_results(id)
                )
            """)
            
            conn.commit()
    
    def store_event_action_result(self, ear: EventActionResult) -> int:
        """Store Event-Action-Result triple"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO event_action_results 
                (event, action, result, success, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                json.dumps(ear.event),
                json.dumps(ear.action),
                json.dumps(ear.result),
                1 if ear.success else 0,
                ear.confidence,
                ear.timestamp.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_recent_events(self, limit: int = 10) -> List[EventActionResult]:
        """Get recent event-action-result triples"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT event, action, result, success, confidence, timestamp
                FROM event_action_results
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append(EventActionResult(
                    event=json.loads(row[0]),
                    action=json.loads(row[1]),
                    result=json.loads(row[2]),
                    success=bool(row[3]),
                    confidence=row[4],
                    timestamp=datetime.fromisoformat(row[5])
                ))
            
            return results
    
    def find_similar_situations(self, situation: Dict, limit: int = 5) -> List[Dict]:
        """
        Step 44 (part): Find similar past situations
        Basic implementation without embeddings
        """
        # Simple keyword-based search
        situation_str = json.dumps(situation).lower()
        keywords = situation_str.split()[:5]  # First 5 words
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Search for events with similar keywords
            query = "SELECT event, action, result, success, timestamp FROM event_action_results WHERE "
            conditions = [f"lower(event) LIKE ?" for _ in keywords]
            query += " OR ".join(conditions)
            query += " ORDER BY timestamp DESC LIMIT ?"
            
            params = [f"%{kw}%" for kw in keywords] + [limit]
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "situation": json.loads(row[0]),
                    "action": json.loads(row[1]),
                    "result": json.loads(row[2]),
                    "success": bool(row[3]),
                    "timestamp": row[4]
                })
            
            return results
    
    def get_action_history(self, action_type: str, limit: int = 10) -> List[Dict]:
        """Get history of specific action type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT action, result, success, timestamp
                FROM event_action_results
                WHERE json_extract(action, '$.type') = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (action_type, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "action": json.loads(row[0]),
                    "result": json.loads(row[1]),
                    "success": bool(row[2]),
                    "timestamp": row[3]
                })
            
            return results
    
    def consolidate_memory(self):
        """
        Step 45: Memory Consolidation
        - Every 24 hours compact memory
        - Combine similar events
        - Delete old useless records
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete records older than retention period
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            cursor.execute("""
                DELETE FROM event_action_results
                WHERE timestamp < ?
            """, (cutoff_date.isoformat(),))
            
            deleted = cursor.rowcount
            conn.commit()
            
            # Vacuum to reclaim space
            cursor.execute("VACUUM")
            
            logger.info(f"🧹 Memory consolidated: {deleted} old records removed")
    
    def backup_memory(self, backup_path: Optional[Path] = None):
        """
        Step 50: Memory Backup
        - Daily backup of memory
        """
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.db_path.parent / f"memory_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        logger.info(f"💾 Memory backed up to {backup_path}")
        return backup_path
    
    def restore_memory(self, backup_path: Path):
        """
        Step 50: Memory Recovery
        - Restore from backup
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        import shutil
        shutil.copy2(backup_path, self.db_path)
        logger.info(f"♻️ Memory restored from {backup_path}")


class SessionMemory:
    """
    Step 46: Session Memory
    - Current session (day) in separate memory
    - Fast access to recent data
    - Transferred to long-term at end of day
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.events: List[EventActionResult] = []
        self.metadata: Dict[str, Any] = {
            "session_id": session_id,
            "created_at": self.created_at.isoformat()
        }
        
        logger.info(f"✅ Session memory created: {session_id}")
    
    def add_event(self, ear: EventActionResult):
        """Add event to session"""
        self.events.append(ear)
    
    def get_events(self, success_only: bool = False) -> List[EventActionResult]:
        """Get all events in session"""
        if success_only:
            return [e for e in self.events if e.success]
        return self.events
    
    def transfer_to_long_term(self, ltm: LongTermMemory):
        """
        Transfer session events to long-term memory
        Called at end of day
        """
        transferred = 0
        for event in self.events:
            ltm.store_event_action_result(event)
            transferred += 1
        
        logger.info(f"📤 Transferred {transferred} events to long-term memory")
        self.events.clear()


class MemoryContextIntegration:
    """
    Step 55: Memory-Context Integration
    - Combine memory system with context
    - Unified system for all information
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.current_session = SessionMemory(session_id=f"{user_id}_{datetime.now().strftime('%Y%m%d')}")
        
        # Step 48: LRU Cache for hot data
        self.cache: Dict[str, Any] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        logger.info(f"✅ Memory-Context Integration initialized for user: {user_id}")
    
    def record_event_action_result(self, event: Dict, action: Dict, result: Dict, success: bool, confidence: float = 0.0):
        """Record complete event-action-result triple"""
        ear = EventActionResult(
            event=event,
            action=action,
            result=result,
            success=success,
            confidence=confidence
        )
        
        # Add to all memory layers
        self.short_term.add_action(action)
        self.short_term.add_observation(event)
        self.current_session.add_event(ear)
        
        # Immediately store critical events in long-term
        if not success or confidence < 0.5:
            self.long_term.store_event_action_result(ear)
    
    def get_context(self, task: str) -> Dict[str, Any]:
        """
        Step 51: Context Aggregation
        - Combine information from different sources
        - Vision, Memory, System State
        - Into unified context
        """
        context = {
            "task": task,
            "recent_actions": self.short_term.get_recent_actions(5),
            "recent_observations": self.short_term.get_recent_observations(10),
            "application_states": self.short_term.application_states,
            "session_events": len(self.current_session.events),
            "historical_patterns": self.long_term.find_similar_situations({"task": task}),
            "timestamp": datetime.now().isoformat()
        }
        
        return context
    
    def filter_relevant_context(self, full_context: Dict, task: str) -> Dict:
        """
        Step 52: Context Relevance Filtering
        - Filter irrelevant information
        - Keep only what's needed for current task
        - Save tokens for GPT-4o
        """
        # Keep only relevant parts
        relevant = {
            "task": task,
            "recent_actions": full_context.get("recent_actions", [])[:3],  # Last 3 actions
            "current_state": full_context.get("application_states", {}),
            "relevant_patterns": []
        }
        
        # Filter patterns by relevance
        patterns = full_context.get("historical_patterns", [])
        for pattern in patterns[:3]:  # Top 3 patterns
            if task.lower() in json.dumps(pattern).lower():
                relevant["relevant_patterns"].append(pattern)
        
        return relevant
    
    def summarize_context(self, long_context: Dict) -> str:
        """
        Step 53: Context Summarization
        - Compress large context into brief summary
        - Abstract connections between events
        - Ready for GPT-4o
        """
        summary_parts = []
        
        # Task summary
        summary_parts.append(f"Task: {long_context.get('task', 'unknown')}")
        
        # Recent actions summary
        actions = long_context.get("recent_actions", [])
        if actions:
            summary_parts.append(f"Recent: {len(actions)} actions performed")
            last_action = actions[-1] if actions else {}
            summary_parts.append(f"Last action: {last_action.get('type', 'unknown')}")
        
        # Patterns summary
        patterns = long_context.get("historical_patterns", [])
        if patterns:
            success_count = sum(1 for p in patterns if p.get("success"))
            summary_parts.append(f"History: {success_count}/{len(patterns)} similar tasks succeeded")
        
        return " | ".join(summary_parts)
    
    def end_session(self):
        """
        End current session and transfer to long-term memory
        """
        logger.info(f"📊 Session stats: {len(self.current_session.events)} events recorded")
        self.current_session.transfer_to_long_term(self.long_term)
        
        # Create new session for next day
        self.current_session = SessionMemory(
            session_id=f"{self.user_id}_{datetime.now().strftime('%Y%m%d')}"
        )
    
    def consolidate(self):
        """
        Step 45: Run memory consolidation
        Should be run daily
        """
        self.long_term.consolidate_memory()
    
    def backup(self) -> Path:
        """
        Step 50: Backup all memory
        """
        return self.long_term.backup_memory()
    
    def get_metrics(self) -> Dict:
        """
        Step 49: Memory Metrics & Monitoring
        - Track memory quality
        - Accuracy, completeness, freshness
        """
        return {
            "short_term": {
                "actions": len(self.short_term.action_buffer),
                "observations": len(self.short_term.observation_buffer),
                "applications": len(self.short_term.application_states)
            },
            "session": {
                "events": len(self.current_session.events),
                "success_rate": (
                    sum(1 for e in self.current_session.events if e.success) / 
                    len(self.current_session.events)
                    if self.current_session.events else 0
                )
            },
            "cache": {
                "hit_rate": (
                    self.cache_hits / (self.cache_hits + self.cache_misses)
                    if (self.cache_hits + self.cache_misses) > 0 else 0
                )
            },
            "timestamp": datetime.now().isoformat()
        }


# Helper functions for embeddings (Step 43)

def encode_to_embeddings(text: str) -> Optional[List[float]]:
    """
    Step 43: Memory Encoding
    - Convert action/result to embeddings
    - Use text-embedding-3-large
    - Save 3072-dimensional vectors
    
    Note: Requires OpenAI API
    """
    try:
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            dimensions=3072
        )
        
        return response.data[0].embedding
    except Exception as e:
        logger.warning(f"Embedding generation failed: {e}")
        return None


def semantic_search(query: str, memory: LongTermMemory, top_k: int = 5) -> List[Dict]:
    """
    Step 44: Semantic Search in Memory
    - Search for similar past situations
    - Vector similarity with cosine metric
    - Top-K similar events
    
    Note: Requires embeddings to be stored
    """
    # This is a placeholder - full implementation requires vector similarity
    # For now, use keyword-based search from LongTermMemory
    return memory.find_similar_situations({"query": query}, limit=top_k)
