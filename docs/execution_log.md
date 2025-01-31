## ⚙️ 処理フローと実行ログ

### 実行環境
- コマンド: `python3 main.py`
- 環境: ローカル環境

### 処理フロー

```mermaid
graph TD
    A[Upsonicサーバー接続<br>LocalServer] --> B[企業情報検索<br>コスト: $0.0039<br>時間: 4.08秒]
    B --> C[企業目的分析<br>コスト: $0.0045<br>時間: 4.34秒]
    C --> D[職務情報分析<br>コスト: $0.0069<br>時間: 6.09秒]
    D --> E[サブタスクリスト生成<br>コスト: $0.0068<br>時間: 6.16秒]

    subgraph サブタスク実行
    F[Anthropic情報収集<br>コスト: $0.0418<br>時間: 26.05秒]
    G[OpenAI情報収集<br>コスト: $0.1096<br>時間: 40.64秒]
    H[比較サマリー作成<br>コスト: $0.0145<br>時間: 17.73秒]
    F --> G
    G --> H
    end

    E --> F
    H --> I[日本語要約生成<br>コスト: $0.0166<br>時間: 17.03秒]
    I --> J[総コスト: $0.1825<br>総時間: 101.44秒]

```

- このフローチャートは、コードの実行順序を可視化したものです。
- 各ステップは、UpsonicクライアントがLLMを呼び出し、結果を生成するプロセスを表しています。

### 実行ログ

1. **Upsonicサーバーへの接続**:
   - コード実行開始時に、Upsonicクライアントがローカルサーバーへの接続を確立します。

   ```log
   ╭─────────────────── Upsonic - Server Connection ────────────────────╮
   │  Server Type:                  Local(LocalServer)                  │
   │  Connection Status:            ✓ Established                       │
   ╰────────────────────────────────────────────────────────────────────╯
   ```

2. **LLM呼び出し (1回目: 企業情報)**:
   -  `client.agent(product_manager_agent, task)` が実行されると、最初のエージェント呼び出しが行われます。
   -  この呼び出しで、LLMはUpsonic.aiに関する企業情報を分析し、`CompanyObjective` 形式で結果を生成します。

   ```log
   ╭────────────────────── Upsonic - Call Result ───────────────────────╮
   │  LLM Model:          claude/claude-3-5-sonnet                      │
   │  Company Objective:  Enter and establish a strong presence         │
   │                      in the Enterprise AI market by                │
   │                      providing comprehensive AI solutions          │
   │                      and development tools                         │
   │  Response Format:    CompanyObjective                              │
   │  Estimated Cost:     ~0.0045$                                      │
   │  Time Taken:         4.34 seconds                                  │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   - ログから、`claude/claude-3-5-sonnet` モデルが使用され、処理に4.34秒かかったことがわかります。

3. **LLM呼び出し (2回目: 職務情報)**:
   -  続いて、プロダクトマネージャーの職務に関する情報が `HumanObjective` 形式で生成されます。

   ```log
   ╭────────────────────── Upsonic - Call Result ───────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Job Title:        プロダクトマネージャー (Product Manager)        │
   │  Job Description:  ... (職務記述) ...                             │
   │  Response Format:  HumanObjective                                  │
   │  Estimated Cost:   ~0.0069$                                        │
   │  Time Taken:       6.09 seconds                                    │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   -  ここでも `claude/claude-3-5-sonnet` モデルが使用され、6.09秒で処理されています。

4. **LLM呼び出し (3回目: サブタスクリスト)**:
   -  タスクがサブタスクに分割され、`SubTaskList` 形式でリストアップされます。

   ```log
   ╭────────────────────── Upsonic - Call Result ───────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Total Subtasks:   3                                               │
   │  Subtask:          Search for the latest news about                │
   │                    Anthropic                                       │
   │  Required Output:  Recent news, developments, and updates          │
   │  Tools:            ['Search__google',                              │
   │                    'Search__read_website']                         │
   │  Response Format:  SubTaskList                                     │
   │  Estimated Cost:   ~0.0068$                                        │
   │  Time Taken:       6.16 seconds                                    │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   -  3つのサブタスク(AnthropicとOpenAIのニュース検索、比較サマリー作成)が定義され、各サブタスクに必要なツールも指定されています。

5. **LLM呼び出し (4回目 & 5回目: エージェント結果 - Anthropic & OpenAI)**:
   -  各サブタスクが実行され、AnthropicとOpenAIそれぞれの最新ニュースに関するエージェントの結果が `str` 形式で生成されます。

   ```log
   ╭────────────────────── Upsonic - Agent Result ──────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Result:           Based on the search results, here are           │
   │                    the latest major developments about             │
   │                    Anthropic:                                      │
   │                    ... (Anthropicのニュース要約) ...               │
   │  Response Format:  str                                             │
   │  Estimated Cost:   ~0.0418$                                        │
   │  Time Taken:       26.05 seconds                                   │
   ╰────────────────────────────────────────────────────────────────────╯

   ╭────────────────────── Upsonic - Agent Result ──────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Result:           Based on the search results and                 │
   │                    available information, here are the             │
   │                    latest major developments about                 │
   │                    OpenAI:                                         │
   │                    ... (OpenAIのニュース要約) ...                  │
   │  Response Format:  str                                             │
   │  Estimated Cost:   ~0.1096$                                        │
   │  Time Taken:       40.64 seconds                                   │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   -  Anthropicのニュース要約には26.05秒、OpenAIのニュース要約には40.64秒かかっています。

6. **LLM呼び出し (6回目 & 7回目: エージェント結果 - 比較サマリー & 日本語要約)**:
   -  最後に、AnthropicとOpenAIの比較サマリーと、日本語での要約が `str` 形式で生成されます。

   ```log
   ╭────────────────────── Upsonic - Agent Result ──────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Result:           I'll help you compile a comprehensive           │
   │                    comparative summary ...                         │
   │                    Comparative Summary of Latest                   │
   │                    Developments: Anthropic vs OpenAI (as           │
   │                    of January 2025)                                │
   │                    ... (比較サマリー) ...                           │
   │  Response Format:  str                                             │
   │  Estimated Cost:   ~0.0145$                                        │
   │  Time Taken:       17.73 seconds                                   │
   ╰────────────────────────────────────────────────────────────────────╯

   ╭────────────────────── Upsonic - Agent Result ──────────────────────╮
   │  LLM Model:        claude/claude-3-5-sonnet                        │
   │  Result:           以前の調査結果から、AnthropicとOpenA...           │
   │                    ... (日本語要約) ...                             │
   │  Response Format:  str                                             │
   │  Estimated Cost:   ~0.0166$                                        │
   │  Time Taken:       17.03 seconds                                   │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   -  比較サマリー生成には17.73秒、日本語要約生成には17.03秒かかっています。

7. **Upsonicエージェントの合計コスト**:
   -  最後に、Upsonicエージェントの合計コストと実行時間がログに出力されます。

   ```log
   ╭──────────────────── Upsonic - Agent Total Cost ────────────────────╮
   │  Estimated Cost:                ~0.1825$                           │
   │  Time Taken:                    101.44 seconds                     │
   ╰────────────────────────────────────────────────────────────────────╯
   ```
   -  合計コストは約0.1825ドル、合計実行時間は101.44秒です。
