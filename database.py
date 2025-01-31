import os
import psycopg2

# データベース接続情報
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 5434)
db_user = os.getenv("DB_USER", "upsonic")
db_password = os.getenv("DB_PASSWORD", "password")
db_name = os.getenv("DB_NAME", "upsonic_db")

class DatabaseTool:
    def execute_query(self, query: str):
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cur = conn.cursor()
            cur.execute(query)
            if cur.description:
                results = cur.fetchall()
                columns = [col.name for col in cur.description]
                return [dict(zip(columns, row)) for row in results]
            else:
                conn.commit()
                return {"message": "Query executed successfully"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            if conn:
                cur.close()
                conn.close()

def initialize_database(db_tool):
    db_tool.execute_query("""
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        );
    """)
    db_tool.execute_query("""
        CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            description TEXT
        );
    """)
    db_tool.execute_query("""
        CREATE TABLE IF NOT EXISTS clues (
            id SERIAL PRIMARY KEY,
            character_id INTEGER REFERENCES characters(id),
            incident_id INTEGER REFERENCES incidents(id),
            description TEXT
        );
    """)

    db_tool.execute_query("""
        INSERT INTO characters (name, description) VALUES
            ('Detective Miller', '主人公の刑事。'),
            ('Ms. Scarlett', '謎の美女。'),
            ('Professor Plum', '知的な大学教授。');
    """)
    db_tool.execute_query("""
        INSERT INTO incidents (description) VALUES
            ('ある邸宅で起きた殺人事件。');
    """)
    db_tool.execute_query("""
        INSERT INTO clues (character_id, incident_id, description) VALUES
            (1, 1, '被害者の部屋で発見された謎のメッセージ。'),
            (2, 1, '事件当日、Ms. Scarlettは邸宅に滞在していた。'),
            (3, 1, 'Professor Plumは被害者と過去に深い因縁があった。');
    """)
