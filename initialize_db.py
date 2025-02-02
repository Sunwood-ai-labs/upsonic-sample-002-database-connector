import csv
from pathlib import Path
from database import DatabaseTool

def load_csv_data(file_path: Path) -> list[dict]:
    """CSVファイルからデータを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # コメント行をスキップ
            lines = [line for line in f if not line.startswith('#')]
            if not lines:
                print(f"❌ CSVファイルが空です: {file_path}")
                return []
            return list(csv.DictReader(lines))
    except FileNotFoundError:
        print(f"❌ CSVファイルが見つかりません: {file_path}")
        return []
    except csv.Error as e:
        print(f"❌ CSV読み込みエラー: {str(e)}")
        return []

def initialize_database():
    """データベース初期化スクリプト"""
    db = DatabaseTool()
    data_dir = Path(__file__).parent / 'data'
    
    # テーブル作成
    schema = [
        # 既存のテーブルを削除
        "DROP TABLE IF EXISTS clues",
        "DROP TABLE IF EXISTS characters",
        "DROP TABLE IF EXISTS incidents",
        
        # テーブルを新規作成
        """CREATE TABLE characters (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            description TEXT
        )""",
        """CREATE TABLE incidents (
            id SERIAL PRIMARY KEY,
            description TEXT UNIQUE
        )""",
        """CREATE TABLE clues (
            id SERIAL PRIMARY KEY,
            character_id INTEGER REFERENCES characters(id),
            incident_id INTEGER REFERENCES incidents(id),
            description TEXT,
            UNIQUE (character_id, incident_id)
        )"""
    ]
    
    print("🚀 テーブル作成を開始...")
    for query in schema:
        result = db.execute_query(query)
        if isinstance(result, dict) and result.get('status') == 'error':
            print(f"❌ スキーマ作成エラー: {result['message']}")
            return

    # CSVデータ読み込み
    characters = load_csv_data(data_dir / 'characters.csv')
    incidents = load_csv_data(data_dir / 'incidents.csv')
    clues = load_csv_data(data_dir / 'clues.csv')
    
    if not all([characters, incidents, clues]):
        print("❌ CSVデータの読み込みに失敗しました")
        return

    # データ挿入
    print("📥 データ挿入を開始...")
    
    # キャラクター挿入
    char_map = {}
    for char in characters:
        result = db.execute_query(
            "INSERT INTO characters (name, description) VALUES (%s, %s) RETURNING id",
            (char['name'], char['description'])
        )
        if isinstance(result, dict):
            print(f"❌ キャラクター挿入エラー: {result.get('message', '不明なエラー')}")
            return
        char_map[char['name']] = result[0]['id']

    # 事件挿入
    incident_map = {}
    for incident in incidents:
        result = db.execute_query(
            "INSERT INTO incidents (description) VALUES (%s) RETURNING id",
            (incident['description'],)
        )
        if isinstance(result, dict):
            print(f"❌ 事件挿入エラー: {result.get('message', '不明なエラー')}")
            return
        incident_map[incident['description']] = result[0]['id']

    # 手がかり挿入
    for clue in clues:
        char_id = char_map.get(clue['character_name'])
        incident_id = incident_map.get(clue['incident_description'])
        
        if not char_id or not incident_id:
            print(f"⚠️ 関連データが見つかりません: {clue}")
            continue
        
        result = db.execute_query(
            """INSERT INTO clues (character_id, incident_id, description)
            VALUES (%s, %s, %s)""",
            (char_id, incident_id, clue['description'])
        )
        if isinstance(result, dict) and result.get('status') == 'error':
            print(f"❌ 手がかり挿入エラー: {result['message']}")
            return

    print("✅ データベースの初期化が正常に完了しました")

if __name__ == "__main__":
    initialize_database()
