# 规划：评审遗留项（第二批）

状态：已实现（tasker 1.11.0、evolver 1.2.0、planner 2.3.0、dev-pdca 1.4.0；台账 EV-20261104-002） · 2026-11-04 · 上一批见 `review-followup-20261104.md`

## 1. 理解卡

- **来源**：第一批落实后，同一份评审还剩一些项。用户决定不等遵守率数据，按会话里给出的建议直接做完。frontmatter 那项只改本仓库，不动 design-to-dev。
- **不做**：三处 escape hatch 规则合并（技能可能单独安装，各写一份短版是有意为之，见 `delivery-gate.md` D8）；周期级转交预算（见上一批 D4）。

## 2. 契约

- `done_definition`：下面 F1–F7 全部落到源码；版本号和 CHANGELOG 同步；套件包重建；派全新 agent 试跑 tasker 快速通道和 evolver 新触发规则，并按反馈迭代；台账和遵守率各追加记录。
- `validation_method`：`build_suite.py --check`；`check_ledger.py`；frontmatter YAML 解析；台账脚本在非 Git 临时目录实跑；读回改动段落；试跑报告。
- `fail_condition`：快速通道绕过了 AGENTS.md 要求的“完成定义加可执行检查加证据”；evolver 改动后，第二次被纠正时不再触发；frontmatter 改动导致 WorkBuddy 打包校验失败。

## 3. 用到的台账条目

- EV-20261104-001：Next Planning Input 写的是“拆分 tasker 的各道 Gate、去掉 evolver 的静默追踪，按遵守率再决定”。用户决定不等数据，这条在本次落实（F3、F4、F5）。
- EV-20261102-001、EV-20261102-003（WorkBuddy 规则）：F7 改 frontmatter 时，`docs/workbuddy-rules.md` 里 WorkBuddy 必填顶层 `version` 这一规则仍然有效，不能违反。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| F1 | `append_evolution_ledger.py` 不在 Git 仓库里时，退回使用 `--root` 指定的目录，并在输出里写 `git=unavailable` | evolver 正文本来就这么写；现在的脚本直接抛异常，和正文矛盾 |
| F2 | `tasker/INTRO.md` 和 `RELEASE_*.md` 移到 `docs/releases/tasker/`，INTRO 开头注明这是历史文档，以 SKILL.md 为准 | 本地安装不再带上它们，发布说明保留在仓库里；`build_suite.py` 的排除规则保留，不影响 |
| F3 | tasker 的 Code Commenting Gate、Commit and Push Closeout 移到 references，主文件只留一行加载条件 | 两者只在加注释的任务、提交任务中用到；Workspace Identity Gate 和 Delivery Gate 防止改错仓库，每次都要过，留在主文件 |
| F4 | tasker 为小改动新增快速通道：用户已经说清具体改什么、改动限于一个文件（或紧密相连的一对文件）、不碰共享契约/配置/安装/发布/凭据/生产、可以直接回退，以上全部满足时，用一行写出完成定义和检查，用户的指令就算确认，不加载 verification.md，收尾给检查的实际输出。目标确认、写后读回、Delivery Gate 照常执行；检查失败就退出快速通道，按完整的 M 级流程走 | 保留 AGENTS.md 要求的契约和证据，只去掉形式化的部分 |
| F5 | evolver 去掉会话中途的静默追踪（第三阶段、三个候选、约六轮这几个阈值）；隐式触发只保留两个时点：第二次被接受的纠正之后、周期收尾时，各做一次 advisory 评估。候选登记只在显式的 tracking mode 下维护 | 消除常驻上下文的成本；保留 AGENTS.md 规定的两个触发时点 |
| F6 | 台账复查：Closure Level 为 `Corrected` 或 `Guarded` 的行算作未闭合。planner 读台账时，未闭合的行与本次范围相关就必须处理；evolver 拿到后续证据时，原地升级该行的 Closure Level 和 Guard Verification，不另起新行 | 让条目能被关闭；不另加过期规则 |
| F7 | frontmatter 不迁移字段：六个子技能保留 `name`、`description`、`argument-hint`、`user-invocable`、`disable-model-invocation`、`version`，由 `build_suite.py` 校验字段集合一致，并校验 description 不超过 1024、version 为 x.y.z | V1 查证：Agent Skills 规范只定义 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`，没有顶层 `version`；skills-ref 校验器（README 自称仅作演示）会拒绝所有其他字段。但 Claude Code 文档列出了 `argument-hint` 等字段，并说明不认识的字段会被忽略；WorkBuddy 要求顶层 `version`（`docs/workbuddy-rules.md`）。为了迎合演示用的校验器，会丢掉 Claude Code 的功能和 WorkBuddy 的必填字段，得不偿失；真正的问题是字段不一致，用校验锁住 |
| F8 | 版本：tasker 1.11.0、evolver 1.2.0、planner 2.3.0、dev-pdca 1.4.0；如果 F7 改动其他技能，再同步升小版本号 | 改了行为 |
| F9 | 派全新 agent 试跑：只给 tasker 和 evolver 的 SKILL.md 路径，在 scratchpad 里的本仓库副本上做一个真实的小改动，走快速通道，收尾时套用 evolver 的新触发规则，列出不清楚、矛盾或缺失的地方 | AGENTS.md 规定大改工作流后要试跑；样本是副本，不写入任何真实仓库 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：Agent Skills 规范和 Claude Code 分别认哪些顶层字段，严格校验器是否拒绝规范外字段 | 已核实：agentskills.io/specification 字段表；skills-ref `validator.py` 的 `ALLOWED_FIELDS`；code.claude.com/docs/en/skills（这一页的字段表来自摘要，不是原文） | 已完成 |
| V2：F9 试跑报告 | 已完成，见 §6 | 已完成 |

## 6. 试跑结果（F9）

全新 agent 只拿到 tasker 和 evolver 的 SKILL.md，在 scratchpad 的本仓库副本上跑了 4 个场景，判断结果都符合预期：
- 在 SUPPORT.md 末尾加一行：走了快速通道，检查输出了 diff；
- 修改 `build_suite.py` 的常量：判定为构建脚本，不走快速通道；
- “把 README 改一改”：用户没指明具体改动，不走快速通道；
- 两次纠正：evolver 在两个检查点各运行一次，都静默退出。

它列出了 20 处指令问题。由本次改动引入的已经修复：
- 快速通道与 `verification.md` 里“每个 M/L 任务都要读”冲突；
- 快速通道收尾格式与 M/L 结构化输出冲突，“major deliveries”没有定义；
- target 一栏比 Workspace Identity Gate 的要求少；
- “不留设计选择”没有可判定的标准；
- 快速通道确认和通用确认规则的关系不清楚；
- evolver 检查点的时机，以及“周期”“被接受的纠正”没有定义；
- Evidence Sweep 只写了 direct-mode 收尾，用的是只在 tracking mode 才有的候选登记；
- 第一个检查点静默退出后，是否还影响收尾检查点。

试跑还顺带发现 README 中英文第 33 行仍写着“开始跟踪”，已同步更新。

改动之前就存在的问题，本次不处理，留作后续输入：
- T5：写入前没有要求记录工作区里已有的未提交改动；
- T6、T8：构建脚本的级别，以及“共享契约”没有定义；
- T9：中英文平行文档是否属于必须同步的工作；
- T10：没有下一步时，compact 输出要求的 next action 和 Delivery Gate 冲突；
- T11：“末尾不要句号”这类细节纠正在字面上符合转 bugfixer 的条件；
- T12：第一条回复前要检查多少内容；
- E4：advisory 提议前要不要先查台账路径；
- E7：守住了但输入错了的防线该怎么归类；
- E8：“存在权威产物或负责人”这个条件几乎总能满足，起不到过滤作用。
