# 规划：落实 2026-11-04 专家评审的五项改进

状态：已实现（tasker 1.10.0、bugfixer 1.6.2、planner 2.2.0、evolver 1.1.0、dev-pdca 1.3.0；台账 EV-20261104-001）· 2026-11-04

## 1. 理解卡

- **来源**：外部评审报告《Tealun-Skills 专家团评审报告》（评审对象是 `~/.workbuddy` 下的本地安装版，不是仓库源码或发布包）。会话中逐条对照仓库 `b86eaa0` 核实，结论如下：
  - 成立：tasker 的 description 占了其他技能的触发场景；planner 不读演进台账；evolver 缺 frontmatter 字段、没有日常中文触发词；“roughly four”这条阈值在 4 处重复定义。
  - 部分成立：18KB 发布说明文件不会进入上下文，`build_suite.py` 也已把它们排除在发布包外，只有 `sync-skills.sh` 的整目录复制会把它们装到本地。
  - 证据不足：“五五开”“3KB 效果无统计学差异”这类结论都没有实测。
- **问题**：技能是按 description 选的，正文里的转交规则帮不上选择；PDCA 从 A 回到 P 的入口缺失；遵守率没有任何记录。
- **非目标**：本次不拆分 tasker 的各道 Gate，不去掉 evolver 的静默追踪，不处理三处重复的“escape hatch”规则，也不给台账脚本加非 Git 目录降级。这几项牵涉设计取舍或优先级较低，留到后续周期。

## 2. 契约

- `done_definition`：五项改动落进源码；版本号和 CHANGELOG 同步；套件包重建；台账追加一条记录；遵守率记录建立，并写入本周期的第一批数据。
- `validation_method`：`python3 scripts/build_suite.py --check`；`python3 scripts/check_ledger.py`；frontmatter YAML 解析；用 grep 确认技能文件里不再出现 `roughly four`；读回改动段落。
- `fail_condition`：description 超过 1024 字符；收窄后 tasker 不再覆盖“任何改动”这一 AGENTS.md 规定的触发场景；新文字带有 D11 所指的逃逸口。

## 3. 决策

| # | 决策 | 理由 |
|---|---|---|
| D1 | tasker 的 description 只写“执行对文件或状态的改动”，并逐个写出反路由：失败用 bugfixer、评审用 auditor、规划用 planner、读懂代码用 explainer、复盘用 evolver。删去 debugging/review/planning/analysis 以及对应的中文词 | 选技能时只看 description；保留“任何改动”，和 AGENTS.md 及 dev-pdca 的路由一致 |
| D2 | 兜底转交阈值只在 bugfixer 正文 Discussion-aware Activation 定义一处，去掉 “roughly”，并把“一轮诊断交换”定义成可以计数的单位。tasker 正文、dev-pdca 会话规则改为引用这一处；两份 description 都不再写这条阈值 | 明确的失败信号本来就能判定，模糊之处只在兜底计数；只留一个定义来源，不会再漂移 |
| D3 | 明确的转交信号（检查失败、“还是不对”、运行时症状、修复没达到预期）仍然在 tasker 和 bugfixer 两边都列出 | 两个技能都可能单独安装，对方不在时也要能触发 |
| D4 | 不加周期级转交预算 | bugfixer 只在症状验证消失后才交回，反复转交意味着又出现了新的失败，这是合理的；预算只会增加计数规则 |
| D5 | planner Interaction Loop 第 1 步要求先读演进台账：找出和本次规划范围相关的 `Next Planning Input`，逐条写进 Decisions 或 To Verify，或写明不适用的理由；交接时列出读了哪些条目 | 补上 A→P 的入站契约；放在规划的第一步，在其他决定之前生效 |
| D6 | 暂不加台账 revisit 和过期机制 | 有了入站读取，台账条目就会被反复检查；先观察，过期规则留待数据证明有必要时再加 |
| D7 | evolver 补上 `argument-hint`、`user-invocable: true`、`disable-model-invocation: false`；description 加入复盘、总结经验、吸取教训、下次别再犯；description 里关于 advisory 收尾和写入授权的过程描述移回正文（正文本来就有） | 修正可移植性；让用户的日常说法也能触发 evolver |
| D8 | 遵守率记录放在 `docs/98_evolution/compliance-log.md`，每个工作周期结束时由 evolver 按固定的 5 道 Gate 记录：是否适用、是否遵守、证据位置、记录方式（自评或独立核验）。满 10 个周期后计算每道 Gate 的遵守率 | 回应评审的根本质疑；用现有的周期收尾来记录，不需要新流程；单独标出自评，避免自己给自己打分 |
| D9 | 版本：tasker 1.10.0、bugfixer 1.6.2、planner 2.2.0、evolver 1.1.0、dev-pdca 1.3.0 | 都改了行为或触发描述 |
| D10 | 不派全新 agent 试跑 | 本次只修改触发描述和接口，没有改动工作流；遵守率记录会持续追踪实际效果 |

## 4. 用到的台账条目

- EV-20261102-002（技能可用却没有调用）：没有防线能检查调用是否真的发生，这一条反映到 D8 的 G1 中。
- 其他条目与本次范围无关（PDF 生成、提交收口、WorkBuddy 上传、台账编号、Delivery Gate）。

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：收窄后，“做一次代码 review”“修复这个报错”“帮我规划”等说法不再选中 tasker | compliance-log 记录到的真实会话 | 后续周期 |
| V2：planner 在下一次规划时确实读了台账 | 下一次规划的交接内容里有台账条目 | 下一次规划周期 |
