from upsonic import UpsonicClient, Task, AgentConfiguration
from database import DatabaseTool
import os

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
