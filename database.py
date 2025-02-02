import os
import psycopg2
from typing import List, Dict, Union

# データベース接続情報
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 5434)
db_user = os.getenv("DB_USER", "upsonic")
db_password = os.getenv("DB_PASSWORD", "password")
db_name = os.getenv("DB_NAME", "upsonic_db")

class DatabaseConnectionError(Exception):
    """データベース接続エラーのカスタム例外"""
    pass

class DatabaseTool:
    def __init__(self):
        self._conn_params = {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'password': db_password,
            'dbname': db_name
        }
    
    def _get_connection(self):
        """データベース接続を確立（内部メソッド）"""
        try:
            return psycopg2.connect(**self._conn_params)
        except psycopg2.OperationalError as e:
            raise DatabaseConnectionError(f"接続失敗: {str(e)}") from e
    
    def execute_query(self, query: str, params: tuple = None) -> Union[List[Dict], Dict]:
        """
        汎用クエリ実行メソッド
        Args:
            query (str): 実行するSQLクエリ
            params (tuple): クエリパラメータ
        Returns:
            クエリ結果（SELECT時）または実行結果メッセージ
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    if cur.description:
                        columns = [col.name for col in cur.description]
                        return [dict(zip(columns, row)) for row in cur.fetchall()]
                    conn.commit()
                    return {"status": "success", "affected_rows": cur.rowcount}
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    db_tool = DatabaseTool()
    
    print("=== データ検証用クエリ ===")
    print("\nキャラクター一覧:")
    print(db_tool.execute_query("SELECT * FROM characters;"))
    
    print("\n事件一覧:")
    print(db_tool.execute_query("SELECT * FROM incidents;"))
    
    print("\n手がかり一覧:")
    print(db_tool.execute_query("""
        SELECT c.id, ch.name, i.description, c.description 
        FROM clues c
        JOIN characters ch ON c.character_id = ch.id
        JOIN incidents i ON c.incident_id = i.id;
    """))
