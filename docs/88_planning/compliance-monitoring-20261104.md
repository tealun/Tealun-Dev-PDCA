# 规划：遵守率监测与第三批修正

状态：已实现（tasker 1.12.0、bugfixer 1.7.0、evolver 1.2.1、dev-pdca 1.5.0；台账 EV-20261104-003，EV-20261104-002 升级为 Institutionalized） · 2026-11-04 · 前两批见 `review-followup-20261104.md`、`review-followup-2-20261104.md`

## 1. 理解卡

- **目标**：从 L3（工程化）升到 L4（可度量），也就是用真实会话的数据证明规则确实改变了行为。用户已经同意建一个每周运行的定时审计；云端技能由用户自己更新。
- **事实**：本会话能用 `list_sessions` / `list_events` 读取用户的云端会话，所以审计可以独立做，不依赖执行者自报。云端同步的技能版本落后于仓库（tasker 1.8.3、bugfixer 1.5.0、planner 2.0.0、evolver 无版本、explainer 未同步），用户更新之前测到的是旧规则。
- **盲区**：本地 WorkBuddy 和 Claude Code 的会话读不到，只能靠用户提供记录。

## 2. 契约

- `done_definition`：历史会话的独立核验数据写进 compliance-log；T10、T11 修正；三个脚本有单元测试并接入 CI；compliance-log 的格式由脚本检查；修正后重新派全新 agent 试跑；每周定时审计创建完成并能读到；版本、CHANGELOG、套件包同步。
- `validation_method`：`python3 -m unittest`；`check_ledger.py`（含 compliance-log）；`build_suite.py --check`；试跑报告；读取刚创建的定时任务。
- `fail_condition`：审计 agent 修改了被审计的会话或仓库；compliance-log 的格式检查误拦已有行；T11 修正之后，真正的回归问题不再转给 bugfixer。

## 3. 用到的台账条目

- EV-20261104-001（Corrected）：G5 一直没在真实规划周期里验证过。本次的历史数据补录能提供第一批独立证据，定时审计负责持续验证。
- EV-20261104-002（Guarded）：Next Planning Input 要求优先处理 T11、T10，并重新试跑，本次全部落实。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| M1 | 历史数据由独立 agent 只读会话记录来补录，记录方式标为“独立” | 执行者自评偏乐观，之前两个周期都是自评 |
| M2 | 每周一 02:17 UTC 运行一次定时任务，每次新开一个会话：读取过去 7 天的相关会话并按 G1–G5 打分，核对云端技能版本，满 10 个周期后计算遵守率；结果以 PR 提交到 Tealun-Skills，不自动合并 | 用户选择每周；新开会话避免上下文累积；用 PR 让用户保留决定权 |
| M3 | T11：bugfixer 正文定义什么算“还是不对”：交付的行为坏了，或者没做到已经约定的结果。改措辞、标点、风格、命名、在已确认目标内换文件、改范围，属于需求修正，交给 tasker 退回 clarify 或 plan 重做；Post-Error Restraint Gate 只适用于仓库或项目选错 | 试跑发现，“末尾不要句号”按字面会转给 bugfixer，“不是这个文件”会冻结一切写入 |
| M4 | T10：只有确实还剩事情时才写下一步；没有就写“下一步：无”，不能为了凑格式编一个可选的下一步 | 消除 Output Contract 和 Delivery Gate 之间的冲突 |
| M5 | 用 Python 标准库 `unittest` 给 `append_evolution_ledger.py`、`check_ledger.py`、`build_suite.py` 的校验函数写测试，接入 CI | 不新增依赖 |
| M6 | `check_ledger.py` 同时检查 compliance-log：每行 7 列，Gate 只能是 G1–G5，适用、遵守、记录方式的取值限定在规定集合内 | 定时任务会自动追加，格式漂移必须被拦下 |
| M7 | 版本：tasker 1.12.0、bugfixer 1.7.0、evolver 1.2.1、dev-pdca 1.5.0 | 改了触发和输出行为 |
| M8 | 定时审计改为绑定本会话（`trig_01LJbnpYL5EkX54SD6jBqTEY`，每周一 02:17 UTC，首次 2026-11-09），由本会话派独立 agent 打分。原先每次新开会话的任务 `trig_01F223FXgcCZtDofjzVo9T7v` 已停用 | 2026-11-04 手动验证：新开的会话（`cse_01MaaD3mGBattqaEHyKbark5`）的工具列表里没有 `list_sessions` / `list_events`，读不到会话记录，审计中止，没有写入任何内容。本会话有这两个工具，补录数据时已实际用过 |

## 5. 第二次试跑（全新 agent，只拿到 tasker、bugfixer、evolver 的 SKILL.md）

- T11 生效：“末尾不要句号”留在 tasker 处理，按需求修正；“不是 SUPPORT.md，是 CONTRIBUTING.md”按范围纠正处理，没有触发 Post-Error Restraint Gate；“还是没加上”转给 bugfixer。
- T10 生效：快速通道的收尾没有硬编下一步。
- 新发现，已修正：快速通道里“格式跟随相邻行惯例”盖过了用户原文，加了一个用户没要的句号，这是上一批 F4 引入的缺陷；收尾三行和四个固定栏目之间的关系没说清；换文件时要不要撤掉之前改错的那处、之前的细化要求带不带到新文件；bugfixer 观察到没有缺陷时缺少退出方式；evolver 描述和正文对检查点的说法不一致，“收尾”的界限也不清。
- 留作后续：Dissatisfaction 一节是否适用于细节纠正；“可信地会复发”没有判定门槛；同一条回复里 evolver 提议和 bugfixer 提问并存时怎么排；Workspace Identity 的冲突行在说不出具体可疑目标时怎么写。

## 6. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：定时审计能读到会话记录并开出 PR | 新开会话的方案：未通过（缺少读会话的工具，见 M8）。改为绑定本会话后，读会话这一步已在补录时验证过；开 PR 这一步待首次运行 | 2026-11-09 |
| V2：第二次试跑后的修正有没有引入新冲突 | 下一次试跑 | 下次修改 tasker 时 |
