from upsonic import UpsonicClient, ObjectResponse, Task, AgentConfiguration
from upsonic.client.tools import Search
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# APIキーの取得
# api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")

# クライアントの作成と設定
client = UpsonicClient("localserver")
# client.set_config("OPENAI_API_KEY", api_key)
client.set_config("ANTHROPIC_API_KEY", api_key)
client.default_llm_model = "claude/claude-3-5-sonnet"

# タスクとエージェントの定義
task = Task(description="AnthropicとOpenAIの最新ニュースを調査する", tools=[Search])

product_manager_agent = AgentConfiguration(
    job_title="プロダクトマネージャー",
    company_url="https://upsonic.ai",
    company_objective="人々がタスクを完了するのを助けるAIエージェントフレームワークを構築する",
)

# タスクの実行と結果の表示
client.agent(product_manager_agent, task)
result = task.response
print(result)
