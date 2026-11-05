# 规划：插件发布规范化

状态：已实现（插件 1.0.0；台账 EV-20261104-004） · 2026-11-04 · 来源：Claude Docs《Tealun-Skills 插件发布规范化方案》（https://claude.ai/artifact/4p6v5Pf3LWe4h1zEE7ix8u），基线 `ef077a6`

## 1. 理解卡

- **目标**：
  1. 仓库本身成为一个合规的 Claude 插件，`claude plugin validate` 通过，可以提交到插件目录；
  2. 推送 `v*` tag 时，CI 自动构建 `tealun-skills-<版本>.plugin` 并发布到 GitHub Release，README 给出始终指向最新版的下载链接；
  3. 版本只有一个来源，改了技能却没升版本时，CI 会拦下。
- **非目标**：
  - 不把 `.plugin` 提交进仓库；
  - 不改技能的目录位置、行为或描述；
  - `dev-pdca.zip` 沿用现有机制；
  - 不替用户在开发者门户提交。
- **用户已决定**（2026-11-04）：
  - 图标用 `assets/dev-pdca-avatar.png`；
  - 首版 `1.0.0`，S1–S5 做完、auditor 审计通过、CI 全绿后，直接合并并推送 `v1.0.0`；
  - 开发者门户跟踪 `main`，发布时手动点 Publish（2026-11-05 改为跟踪 `plugin` 分支，见 `plugin-branch-20261105.md`）；
  - 目录提交由用户本人在 claude.ai/directory/manage 完成。

## 2. 契约

- `done_definition`：
  - S1–S5 落进仓库；
  - 验收 1–5 全部贴出实际输出；
  - 推送 `v1.0.0` 后，Release 上有 `tealun-skills-1.0.0.plugin` 和 `dev-pdca.zip`（验收 6）；
  - 台账和遵守率记录各追加一条。
- `validation_method`：
  - `claude plugin validate`（本机 CLI 2.1.318）；
  - `build_plugin.py --check`、`build_suite.py --check`、`check_ledger.py`、unittest；
  - 两个反例；
  - 构建两次，比对 sha256；
  - 检查解压后的文件清单；
  - Release 页面上的附件。
- `fail_condition`：
  - 校验出现方案第 2 节以外的错误或警告；
  - CI 拿不到 Claude Code CLI，无法在发布流程里跑 validate（按方案，这一步失败就停，不跳过）；
  - 目录规则查证结果与方案冲突。

## 3. 用到的台账条目

- EV-20261102-001、EV-20261102-003（发布到外部平台前，先登记它的全部规则）：落在 S5 的 `docs/claude-directory-rules.md`。规则要以原文页面为准，不能只照抄方案的转述（见 V2）。
- EV-20261104-001（G5）：本节就是它要求的交接列示。
- EV-20261104-003（文字规则约束不住，评估 hooks）：与本次无关，本次不处理。

## 4. 决策

沿用方案的 D1–D9，这里不再复述。只补充以下几项：

| # | 决策 | 理由 |
|---|---|---|
| P1 | D9 定稿：`icon` 指向 `./assets/dev-pdca-avatar.png`，构建时一起放进包里 | 用户已选 |
| P2 | 插件版本 `1.0.0` 写在 `plugin.json`，CHANGELOG 的“现有技能”一节加一行插件版本 | D2、D3 |
| P3 | `build_plugin.py --check` 的检查项按方案 S2 实现，单元测试接进现有的 `tests/test_scripts.py` | 沿用上一批的测试基础 |
| P4 | 发布流程用 `npx -y @anthropic-ai/claude-code@<固定版本>` 运行 validate；版本固定，不用 latest | 发布结果要可复现；和 CI 的其余步骤一样，失败就停 |
| P5 | Release 同时附上 `tealun-skills-<版本>.zip` 和 `.plugin`，两个文件内容完全相同；README 指导用户上传 `.zip` | V2 核实：官方文档只写了 claude.ai 用 zip 上传安装（Customize > Plugins > Add > Upload plugin），找不到 `.plugin` 格式的说明 |
| P6 | 把官方清单里的规则写进 `build_plugin.py --check`：会被拒收的规则报错，会转人工审核的规则只打印警告；逐条对照见 `docs/claude-directory-rules.md` | AGENTS.md 规定：平台规则要先登记、再写成本地检查 |
| P7 | 根目录的 `dev-pdca.zip` 会让插件转人工审核。按非目标，这次不动它，留给用户决定 | 官方清单写明 `.zip` 会转人工审核；按规划，`dev-pdca.zip` 沿用现有机制 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：加上 `plugin.json` 后，validate 只报方案第 2 节列出的警告 | validate 的输出原文 | S1 |
| V2：目录提交规则、`plugin.json` 字段、`.plugin` 格式与官方文档一致 | 已核实，与方案有 3 处不同：① 官方文档没有 `.plugin` 格式，改为附 zip（P5）；② 方案里的图标规格和“只在首次提交时生效”在官方页面找不到原文，已标为“方案转述”；③ `.zip` 会转人工审核（P7） | 已完成 |
| V3：发布流程里 npx 能拉到 CLI，validate 能跑通 | 已核实：release 运行 41942867251 的 12 个步骤全部 success，其中 CLI validate 那一步也 success；Release v1.0.0 带 3 个附件，`.plugin` 和 `.zip` 的 sha256 都是 `3fb9e925…`，和本地两次构建的结果相同；`dev-pdca.zip` 的 sha256 是 `45c56380…`，和 main 上的文件相同；`releases/latest` 指向 v1.0.0 | 已完成（2026-11-05） |

## 6. 实施中发现的问题

- 反例 ② 暴露了 `build_plugin.py` 的一个缺陷：已被 Git 跟踪、但从工作区删掉的文件仍会出现在 `git ls-files` 的结果里，对它执行 `stat()` 会抛异常，所以脚本直接崩溃，没有报出“引用的文件缺失”。已按 bugfixer 流程修复：过滤掉不存在的文件。补了一条回归测试，并做了变异检查：撤掉修复后这条测试失败，恢复后通过。
