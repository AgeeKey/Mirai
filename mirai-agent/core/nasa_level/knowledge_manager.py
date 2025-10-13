"""
NASA-Level Knowledge Manager
SQLite-based knowledge base with full-text search, versioning, and semantic retrieval
"""

import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """A piece of learned knowledge"""
    technology: str
    version: int
    research: str
    code: str
    quality_grade: str
    proficiency: float
    tests_passed: int
    tests_total: int
    learned_at: str
    metadata: Dict


class KnowledgeManager:
    """
    Manages learned knowledge with:
    - SQLite storage with FTS5 full-text search
    - Version tracking
    - Fast retrieval
    - Semantic search capabilities
    """
    
    def __init__(self, db_path: str = "/tmp/nasa_knowledge.db"):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Main knowledge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                technology TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                research TEXT,
                code TEXT NOT NULL,
                quality_grade TEXT,
                proficiency REAL,
                tests_passed INTEGER,
                tests_total INTEGER,
                learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                UNIQUE(technology, version)
            )
        """)
        
        # Full-text search index
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
                technology,
                research,
                code,
                content='knowledge',
                content_rowid='id'
            )
        """)
        
        # Triggers to keep FTS in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS knowledge_ai AFTER INSERT ON knowledge BEGIN
                INSERT INTO knowledge_fts(rowid, technology, research, code)
                VALUES (new.id, new.technology, new.research, new.code);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS knowledge_ad AFTER DELETE ON knowledge BEGIN
                DELETE FROM knowledge_fts WHERE rowid = old.id;
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS knowledge_au AFTER UPDATE ON knowledge BEGIN
                UPDATE knowledge_fts 
                SET technology = new.technology,
                    research = new.research,
                    code = new.code
                WHERE rowid = new.id;
            END
        """)
        
        # Index for fast lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_technology 
            ON knowledge(technology)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_learned_at 
            ON knowledge(learned_at DESC)
        """)
        
        self.conn.commit()
        logger.info(f"📚 Knowledge database initialized: {self.db_path}")
    
    def save_knowledge(
        self,
        technology: str,
        research: str,
        code: str,
        quality_grade: str,
        proficiency: float,
        tests_passed: int = 0,
        tests_total: int = 0,
        metadata: Dict = None
    ) -> int:
        """Save learned knowledge (creates new version)"""
        
        # Get current version
        current_version = self.get_latest_version(technology)
        new_version = current_version + 1
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge (
                technology, version, research, code,
                quality_grade, proficiency,
                tests_passed, tests_total, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            technology,
            new_version,
            research,
            code,
            quality_grade,
            proficiency,
            tests_passed,
            tests_total,
            json.dumps(metadata or {})
        ))
        
        self.conn.commit()
        entry_id = cursor.lastrowid
        
        logger.info(
            f"💾 Saved: {technology} v{new_version} "
            f"(grade: {quality_grade}, proficiency: {proficiency:.1%})"
        )
        
        return entry_id
    
    def get_knowledge(
        self,
        technology: str,
        version: Optional[int] = None
    ) -> Optional[KnowledgeEntry]:
        """Get knowledge for a technology (latest version by default)"""
        
        cursor = self.conn.cursor()
        
        if version is None:
            cursor.execute("""
                SELECT * FROM knowledge
                WHERE technology = ?
                ORDER BY version DESC
                LIMIT 1
            """, (technology,))
        else:
            cursor.execute("""
                SELECT * FROM knowledge
                WHERE technology = ? AND version = ?
            """, (technology, version))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return self._row_to_entry(row)
    
    def get_all_technologies(self) -> List[str]:
        """Get list of all learned technologies"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT technology 
            FROM knowledge 
            ORDER BY technology
        """)
        return [row[0] for row in cursor.fetchall()]
    
    def get_latest_version(self, technology: str) -> int:
        """Get the latest version number for a technology"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT MAX(version) FROM knowledge
            WHERE technology = ?
        """, (technology,))
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def get_version_history(self, technology: str) -> List[KnowledgeEntry]:
        """Get all versions of a technology"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM knowledge
            WHERE technology = ?
            ORDER BY version ASC
        """, (technology,))
        
        return [self._row_to_entry(row) for row in cursor.fetchall()]
    
    def search(
        self,
        query: str,
        limit: int = 10
    ) -> List[KnowledgeEntry]:
        """Full-text search across all knowledge"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT k.* FROM knowledge k
            JOIN knowledge_fts fts ON k.id = fts.rowid
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        return [self._row_to_entry(row) for row in cursor.fetchall()]
    
    def get_recent(self, limit: int = 10) -> List[KnowledgeEntry]:
        """Get recently learned technologies"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM knowledge
            ORDER BY learned_at DESC
            LIMIT ?
        """, (limit,))
        
        return [self._row_to_entry(row) for row in cursor.fetchall()]
    
    def get_top_quality(self, limit: int = 10) -> List[KnowledgeEntry]:
        """Get highest quality knowledge entries"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM knowledge
            WHERE quality_grade IN ('A', 'B')
            ORDER BY proficiency DESC, learned_at DESC
            LIMIT ?
        """, (limit,))
        
        return [self._row_to_entry(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        cursor = self.conn.cursor()
        
        # Total entries
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        total_entries = cursor.fetchone()[0]
        
        # Unique technologies
        cursor.execute("SELECT COUNT(DISTINCT technology) FROM knowledge")
        unique_techs = cursor.fetchone()[0]
        
        # Average proficiency
        cursor.execute("SELECT AVG(proficiency) FROM knowledge")
        avg_proficiency = cursor.fetchone()[0] or 0.0
        
        # Grade distribution
        cursor.execute("""
            SELECT quality_grade, COUNT(*) as count
            FROM knowledge
            GROUP BY quality_grade
            ORDER BY quality_grade
        """)
        grade_dist = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Recent activity (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM knowledge
            WHERE learned_at >= datetime('now', '-7 days')
        """)
        recent_count = cursor.fetchone()[0]
        
        return {
            'total_entries': total_entries,
            'unique_technologies': unique_techs,
            'average_proficiency': avg_proficiency,
            'grade_distribution': grade_dist,
            'learned_last_7_days': recent_count
        }
    
    def delete_technology(self, technology: str) -> int:
        """Delete all versions of a technology"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM knowledge WHERE technology = ?", (technology,))
        self.conn.commit()
        deleted = cursor.rowcount
        
        if deleted > 0:
            logger.info(f"🗑️  Deleted {deleted} versions of {technology}")
        
        return deleted
    
    def export_knowledge(self, technology: str) -> Optional[Dict]:
        """Export knowledge as JSON"""
        entry = self.get_knowledge(technology)
        if not entry:
            return None
        
        return {
            'technology': entry.technology,
            'version': entry.version,
            'research': entry.research,
            'code': entry.code,
            'quality_grade': entry.quality_grade,
            'proficiency': entry.proficiency,
            'tests_passed': entry.tests_passed,
            'tests_total': entry.tests_total,
            'learned_at': entry.learned_at,
            'metadata': entry.metadata
        }
    
    def import_knowledge(self, data: Dict) -> int:
        """Import knowledge from JSON"""
        return self.save_knowledge(
            technology=data['technology'],
            research=data.get('research', ''),
            code=data['code'],
            quality_grade=data['quality_grade'],
            proficiency=data['proficiency'],
            tests_passed=data.get('tests_passed', 0),
            tests_total=data.get('tests_total', 0),
            metadata=data.get('metadata', {})
        )
    
    def _row_to_entry(self, row: sqlite3.Row) -> KnowledgeEntry:
        """Convert database row to KnowledgeEntry"""
        return KnowledgeEntry(
            technology=row['technology'],
            version=row['version'],
            research=row['research'] or '',
            code=row['code'],
            quality_grade=row['quality_grade'],
            proficiency=row['proficiency'],
            tests_passed=row['tests_passed'],
            tests_total=row['tests_total'],
            learned_at=row['learned_at'],
            metadata=json.loads(row['metadata'] or '{}')
        )
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("📚 Knowledge database closed")
    
    def __del__(self):
        self.close()


# Demo/Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*80)
    print("🧪 NASA-Level Knowledge Manager Test")
    print("="*80)
    
    # Create manager
    km = KnowledgeManager("/tmp/test_knowledge.db")
    
    # Add some test knowledge
    print("\n➕ Adding test knowledge...")
    
    km.save_knowledge(
        technology="requests",
        research="HTTP library for Python. Simple API for making HTTP requests.",
        code="import requests\n\nresponse = requests.get('https://api.example.com')\nprint(response.json())",
        quality_grade="A",
        proficiency=0.92,
        tests_passed=5,
        tests_total=5,
        metadata={'depth': 'basic', 'source': 'test'}
    )
    
    km.save_knowledge(
        technology="pandas",
        research="Data manipulation library. DataFrames for tabular data.",
        code="import pandas as pd\n\ndf = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})\nprint(df.head())",
        quality_grade="B",
        proficiency=0.85,
        tests_passed=4,
        tests_total=5,
        metadata={'depth': 'intermediate'}
    )
    
    # Update requests (creates v2)
    km.save_knowledge(
        technology="requests",
        research="HTTP library - UPDATED with auth examples",
        code="import requests\n\nresponse = requests.get('https://api.example.com', auth=('user', 'pass'))",
        quality_grade="A",
        proficiency=0.95,
        tests_passed=5,
        tests_total=5
    )
    
    # Test retrieval
    print("\n🔍 Getting latest 'requests' knowledge...")
    entry = km.get_knowledge("requests")
    if entry:
        print(f"  Version: {entry.version}")
        print(f"  Grade: {entry.quality_grade}")
        print(f"  Proficiency: {entry.proficiency:.1%}")
        print(f"  Code:\n{entry.code[:100]}...")
    
    # Test version history
    print("\n📜 Version history for 'requests':")
    history = km.get_version_history("requests")
    for h in history:
        print(f"  v{h.version}: grade={h.quality_grade}, proficiency={h.proficiency:.1%}")
    
    # Test search
    print("\n🔎 Searching for 'HTTP'...")
    results = km.search("HTTP")
    print(f"  Found {len(results)} results")
    for r in results:
        print(f"    - {r.technology} v{r.version}")
    
    # Test stats
    print("\n📊 Knowledge base statistics:")
    stats = km.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test export
    print("\n📤 Exporting 'pandas' knowledge...")
    exported = km.export_knowledge("pandas")
    if exported:
        print(f"  Exported {len(json.dumps(exported))} bytes")
    
    print("\n✅ Knowledge Manager test complete!")
    
    km.close()
