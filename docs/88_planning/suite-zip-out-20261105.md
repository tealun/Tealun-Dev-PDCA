# 规划：dev-pdca.zip 移出仓库，为提交插件目录做准备

状态：实现中 · 2026-11-05

## 1. 理解卡

- **目标**：提交 Claude 插件目录时，插件文件夹（仓库根目录）里不再有二进制文件。这样每个版本都走自动扫描，不再转人工审核。
- **起因**：官方提交清单写明，插件文件夹里的 `.zip` 等二进制文件会转人工审核。`dev-pdca.zip` 是唯一触发这一条的文件（`build_plugin.py --check` 的提示：`dev-pdca.zip: .zip files are held for a reviewer`）。
- **用户已决定**（2026-11-05）：先把它移出仓库，再提交插件目录。
- **非目标**：
  - 不改套件包的内容、名称和 WorkBuddy 打包规则；
  - 不改技能本身；
  - 不发新版本。插件目录直接读仓库 main，WorkBuddy 用户从 Release 下载，现有的 v1.0.1 Release 已经附带 `dev-pdca.zip`。

## 2. 契约

- `done_definition`：
  - 仓库不再跟踪 `dev-pdca.zip`，并在 `.gitignore` 里忽略它；
  - `build_suite.py` 把包输出到 `dist/dev-pdca.zip`，`--check` 改为“校验并在内存里构建，确认能打出包”；
  - `release.yml` 先构建再附上 `dist/dev-pdca.zip`，附件名不变；
  - README、QUICKSTART、CONTRIBUTING、AGENTS.md、两份规则对照表的下载地址和规则同步更新；
  - `build_plugin.py --check` 不再打印目录审核警告。
- `validation_method`：
  - `build_suite.py --check` 和 `build_suite.py`；
  - `build_plugin.py --check --since v1.0.1`，输出里没有 warning；
  - unittest；
  - `claude plugin validate`；
  - `git ls-files | grep zip` 结果为空。
- `fail_condition`：
  - Release 流程拿不到 `dev-pdca.zip`；
  - 文档里还有指向仓库根目录 zip 的链接。

## 3. 用到的台账条目

- EV-20261104-004：Next Planning Input 里“`dev-pdca.zip` 是否移出插件文件夹”这一项，由本次落实（用户决定移出）。
- EV-20261102-001、EV-20261102-003（WorkBuddy 规则）：套件包的校验（层级、单个 SKILL.md、字段长度）全部保留，只改输出位置。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| Z1 | `dev-pdca.zip` 不再提交到仓库，构建输出到 `dist/dev-pdca.zip`（`dist/` 已被忽略） | 插件文件夹里不留二进制文件 |
| Z2 | `--check` 改为：校验并在内存里构建，不再和仓库里提交的成品比对 | 仓库里没有成品了，不存在“过期”的问题；包由 CI 从源码现场生成 |
| Z3 | Release 附件名保持 `dev-pdca.zip`，README 的下载链接改为 `releases/latest/download/dev-pdca.zip` | 这个地址永远指向最新版，WorkBuddy 用户点一下就能下载 |
| Z4 | AGENTS.md 删掉“重新生成并一起提交”这条规则，改成“改完运行 `build_suite.py --check`，CI 会拦截” | 规则要和实际流程一致 |
| Z5 | 插件版本不升 | 没有改动技能目录，按 AGENTS.md 不需要升 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：下一次推 tag 时，Release 上照样有 `dev-pdca.zip` | Release 附件列表 | 下次发版 |
| V2：提交插件目录后，自动扫描不再因为二进制文件转人工审核 | 门户里显示的扫描结果 | 用户提交之后 |
