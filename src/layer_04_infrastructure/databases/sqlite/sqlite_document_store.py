import sqlite3
import json
from typing import List, Dict, Any, Optional
from src.config import DB_SQLITE_PATH
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)

class SqliteDocumentStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SqliteDocumentStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str = DB_SQLITE_PATH):
        if self._initialized:
            return
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()
        self._initialized = True

    def _init_db(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                collection_name TEXT,
                document_id TEXT,
                data TEXT,
                PRIMARY KEY (collection_name, document_id)
            )
        """)
        self._conn.commit()

    def set_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        try:
            cursor = self._conn.cursor()
            json_data = json.dumps(data, ensure_ascii=False)
            cursor.execute("""
                INSERT OR REPLACE INTO collections (collection_name, document_id, data)
                VALUES (?, ?, ?)
            """, (collection, doc_id, json_data))
            self._conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error set_document in {collection}/{doc_id}: {e}")
            return False

    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT data FROM collections WHERE collection_name = ? AND document_id = ?
            """, (collection, doc_id))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Error get_document in {collection}/{doc_id}: {e}")
            return None

    def delete_document(self, collection: str, doc_id: str) -> bool:
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                DELETE FROM collections WHERE collection_name = ? AND document_id = ?
            """, (collection, doc_id))
            self._conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error delete_document in {collection}/{doc_id}: {e}")
            return False

    def list_documents(self, collection: str) -> List[Dict[str, Any]]:
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT data FROM collections WHERE collection_name = ?
            """, (collection,))
            rows = cursor.fetchall()
            return [json.loads(row[0]) for row in rows]
        except Exception as e:
            logger.error(f"Error list_documents in {collection}: {e}")
            return []

    def query_documents(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Simple query helper that filters documents in-memory to simulate Firestore queries.
        """
        docs = self.list_documents(collection)
        result = []
        for doc in docs:
            match = True
            for k, v in filters.items():
                # Support nested filters or direct filters
                if k in doc:
                    if doc[k] != v:
                        match = False
                        break
                else:
                    match = False
                    break
            if match:
                result.append(doc)
        return result
