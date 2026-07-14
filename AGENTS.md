# 操作指令

## 1. 项目基础信息
- **项目名称**：文本数据清洗工具（Text Data Cleaner）
- **开发语言**：Python 3.10+（仅使用标准库，不引入第三方依赖）
- **主程序文件**：`clean.py`
- **测试文件**：`test_input.txt`（包含混合空格、空行、重复行的测试文本）
- **考核记录文件**：`AI开发考核_梁嘉俊_文本数据清洗工具.jsonl`

## 2. 核心开发规则
- **逐轮迭代**：将完整功能拆解为 10 个步骤，每轮只完成一个明确的小目标。
- **代码规范**：必须包含 `if __name__ == "__main__":` 入口，所有核心逻辑封装在函数中。
- **测试验证**：每轮代码修改后，必须使用 `test_input.txt` 进行运行测试，确保功能正常且不破坏已有功能。

## 3. Git 提交规范（极其重要）
- **提交频率**：每完成一个功能点，必须独立提交一次 Git。
- **Commit Message 格式**：`feat(round N): [功能描述]`（例如：`feat(round 2): 去除首尾空白行`）。
- **禁止合并**：严禁使用 `git rebase` 或 `git commit --amend` 修改历史提交记录。

## 4. JSONL 过程记录自动生成规范（核心考核依据）
每次 Git 提交完成后，Codex **必须**自动向 `AI开发考核_梁嘉俊_文本数据清洗工具.jsonl` 文件中**追加一行**符合以下字段定义的 JSON 数据：

- `round_id`：当前轮次序号（从 1 开始递增）。
- `prompt_content`：本轮用户输入的完整自然语言指令。
- `modify_diff`：**本轮 Git 提交所产生的 Unified Diff 格式代码差异**（必须包含 `@@` 行号信息，可通过 `git diff HEAD~1 HEAD` 获取）。
- `commit_hash`：本轮 Git 提交的完整哈希值（40位或短7位均可）。
- `modify_time`：当前操作时间（格式：`YYYY-MM-DD HH:MM:SS`）。
- `agent_type`：固定填写 `"Codex"`。
- `dev_language`：固定填写 `"Python"`。

**JSONL 追加示例**（Codex 请严格参照此格式，转义换行符 `\n`）：
{"round_id":1,"prompt_content":"使用Python实现基础CLI框架...","modify_diff":"@@ -0,0 +1,20 @@ ...","commit_hash":"abc1234","modify_time":"2026-07-14 14:30:00","agent_type":"Codex","dev_language":"Python"}

## 5. 工作流约束
- 收到指令后，先规划修改方案。
- 修改 `clean.py` 文件。
- 执行测试（如 `python clean.py test_input.txt`）。
- 若测试通过，执行 `git add .` 和 `git commit`。
- **关键步骤**：获取本次 commit 的 hash 和 diff，立即更新 JSONL 文件。
- 最后，向用户回复本次操作的简要总结和 commit hash。
