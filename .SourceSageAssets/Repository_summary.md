# 📁 Project: upsonic-sample-001-news-digest-analyzer

## 🌳 ディレクトリ構造

```plaintext
OS: linux
Directory: /home/maki/prj/upsonic-sample-box/upsonic-sample-001-news-digest-analyzer
Ignore File: .SourceSageignore (auto-generated)

└─ upsonic-sample-001-news-digest-analyzer/
   ├─ .SourceSageignore
   ├─ main.py
   └─ README.md
```

## 📊 統計情報

### 📈 ファイル別行数

| ファイル | 行数 |
|---------|------|
| .SourceSageignore | 35行 |
| main.py | 21行 |
| README.md | 21行 |

### 📋 合計行数: 77行


## 📄 ファイル内容

### 📝 `.SourceSageignore`

```
# バージョン管理システム関連
.git
.gitignore

# キャッシュファイル
__pycache__
.pytest_cache
**/__pycache__/**
*.pyc

# ビルド・配布関連
build
dist
*.egg-info
node_modules

# 一時ファイル・出力
output
output.md
test_output
.SourceSageAssets
.SourceSageAssetsDemo

# アセット
*.png
*.svg
assets

# その他
LICENSE
example
folder
package-lock.json
.DS_Store

```

### 📝 `main.py`

**Type**: Python Source File

```py
from upsonic import UpsonicClient, ObjectResponse, Task, AgentConfiguration
from upsonic.client.tools import Search

# クライアントの作成と設定
client = UpsonicClient("localserver")
client.set_config("OPENAI_API_KEY", "YOUR_API_KEY")

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

```

### 📝 `README.md`

**Type**: Markdown Documentation

```md
# 📰 Upsonicニュース要約サンプル

このプロジェクトは、Upsonicフレームワークを使用して、ニュース記事を要約する基本的なサンプルです。

## 🚀 概要

このサンプルでは、Upsonicの基本的な機能であるLLM呼び出しを使用して、指定されたトピックに関する最新のニュース記事を検索し、要約します。

## 🛠️ 使い方

1.  `main.py`ファイル内の`YOUR_API_KEY`を、自身のOpenAI APIキーに置き換えます。
2.  以下のコマンドを実行して、サンプルコードを実行します。

    ```bash
    python main.py
    ```

## 📚 参考資料

- [Upsonic 公式ドキュメント](https://upsonic.ai)

```
