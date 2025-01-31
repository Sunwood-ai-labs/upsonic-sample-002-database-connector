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
