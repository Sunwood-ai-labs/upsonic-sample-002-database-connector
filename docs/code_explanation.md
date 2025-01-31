## 💻 コードの解説

### 環境設定 (`main.py`):
```python
from dotenv import load_dotenv
import os
from database import DatabaseTool, initialize_database
from agent import run_agent

# 環境変数の読み込み
load_dotenv()

# APIキーの取得
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEYが設定されていません。.envファイルを確認してください。")

# データベース初期化
db_tool_instance = DatabaseTool()
initialize_database(db_tool_instance)

# エージェント実行
run_agent()
```
- `.env`ファイルから環境変数を読み込み
- APIキーの存在チェックを行い、未設定の場合はエラーを表示
- `database.py` と `agent.py` から必要な関数とクラスをインポート
- データベースの初期化処理を実行
- エージェントを実行

### データベース操作ツールと初期化 (`database.py`):
```python
import os
import psycopg2

# データベース接続情報 (環境変数から取得)
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 5432)
db_user = os.getenv("DB_USER", "upsonic")
db_password = os.getenv("DB_PASSWORD", "password")
db_name = os.getenv("DB_NAME", "upsonic_db")

class DatabaseTool:
    def execute_query(self, query: str):
        # ... (クエリ実行処理) ...
        pass

def initialize_database(db_tool):
    # ... (データベース初期化処理) ...
    pass
```
- データベース接続情報と `DatabaseTool` クラス、`initialize_database` 関数を定義
- `DatabaseTool` クラスは、SQL クエリを実行する `execute_query` メソッドを持つ
- `initialize_database` 関数は、データベースの初期化処理を行う

### エージェント定義と実行 (`agent.py`):
```python
from upsonic import UpsonicClient, Task, AgentConfiguration
from database import DatabaseTool

# クライアントの作成と設定
client = UpsonicClient("localserver")
client.set_config("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
client.default_llm_model = "claude/claude-3-5-sonnet"

# タスクとエージェントの定義
task = Task(
    description="""
    あなたはマーダーミステリーの真相を解明する探偵です。
    データベースから事件、登場人物、手がかりの情報を取得し、事件の真相を推理してください。
    """,
    tools=[DatabaseTool]
)

product_manager_agent = AgentConfiguration(
    job_title="マーダーミステリー探偵",
    company_url="架空の探偵事務所",
    company_objective="マーダーミステリーの真相を解明する",
)

def run_agent():
    # タスクの実行と結果の表示
    client.agent(product_manager_agent, task)
    result = task.response
    print(result)
```
- Upsonic クライアント、タスク、エージェントの定義を記述
- `DatabaseTool` を利用
- `run_agent` 関数でエージェントを実行
