# Tealun Dev PDCA 仓库的 Agent 指令

本仓库开发的就是 Tealun Dev PDCA，自己的工作也要用这些技能。技能源码在仓库根目录的 `planner/`、`tasker/`、`bugfixer/`、`auditor/`、`evolver/`、`explainer/`；`suite/dev-pdca/` 是套件包入口。

## 配套技能：要调用，不要只“照着精神做”

触发条件满足时，通过技能工具调用对应技能；技能工具里看不到时，直接读取本仓库对应目录的 `SKILL.md` 并按步骤执行。只按“大意”去做不算调用。每个会话的第一条回复，先说明这六个技能里哪些可用；缺哪个就直说。

- **planner：任何规划意图，不论大小。** 新技能、技能结构调整、发布方式、文档体系或流程。在改文件之前调用，先把决定写进对应文档。
- **tasker：任何对文件或状态的改动，包括看起来很小的修补。** 动手前写清完成定义和一个可执行的检查；收尾时给出证据（命令输出、读回结果），不要只给描述。只读的问答不需要。
- **bugfixer：用户说有问题或“还是不对”、某个检查失败、CI 失败、外部平台（如 WorkBuddy）上传或审核被拒时。** 先复现或直接观察，证明原因，只修这个原因，再验证最初的症状已经消失。
- **auditor：推送影响安装脚本、发布包或共享规则的改动之前，发布之前，以及任何审计请求。**
- **evolver：用户报告的问题修好并验证之后、同一周期内第二次被纠正之后、以及每个工作周期结束时。** 把经验和对应的防线记到 `docs/98_evolution/evolution-ledger.md`。每个周期结束时，同时在 `docs/98_evolution/compliance-log.md` 按其中 5 道 Gate 各记一行，写明是否遵守和证据。
- **explainer：用户想看懂某块代码、某个功能流程、某次改动或改动影响时。** 只读，产出写进目标项目的 `docs/explainer/`。

## 本仓库的硬规则

- **发布到外部平台之前，先查清它的全部规则。** 字段、长度、数量、目录结构等要求逐条登记到对照表（WorkBuddy 见 `docs/workbuddy-rules.md`），每条要么写进 `scripts/build_suite.py` 的本地校验，要么写明不校验的原因；本地通过后再上传。不要用平台的报错来逐条试规则，也不要只挑带数字的规则做校验。
- **改了任何技能目录或 `suite/dev-pdca/SKILL.md`，** 运行 `python3 scripts/build_suite.py --check`，确认套件包能通过校验并正常打出。`dev-pdca.zip` 不提交进仓库：仓库根目录就是插件文件夹，里面放 zip 会让插件目录转人工审核。这个包由 `release.yml` 构建并附到 Release 上。
- **改了技能的行为或触发描述，** 同步更新该技能的 `version` 和 `CHANGELOG.md`。
- **改了任何技能目录，** 同时升 `.claude-plugin/plugin.json` 的 `version`，并在 `CHANGELOG.md` 加一节 `## tealun-dev-pdca <版本>`。升法：任一技能升 major 或删掉技能，插件升 major；新增技能或任一技能升 minor，插件升 minor；其余改动（技能只升 patch，或只改了文档、清单）插件升 patch。插件市场清单在 `tealun/tealun-plugins`，本仓库不放 `marketplace.json`。CI 用 `build_plugin.py --check --since <上一个 tag>` 拦截没升版本的改动。
- **发布只靠推送 `v<版本>` tag，** 由 `.github/workflows/release.yml` 构建并创建 Release。不手动上传 Release 附件，不把 `.plugin` 或插件 zip 提交进仓库。
- **`plugin` 分支只由 `.github/workflows/plugin-branch.yml` 写入，** 插件目录跟踪这个分支。它只包含打包好的插件，不要手动往里提交，也不要把开发文件放进去。
- **提交 Claude 插件目录之前，** 先把目录规则登记进 `docs/claude-directory-rules.md`。每条要么写进 `build_plugin.py --check`，要么写明不校验的原因。
- **本仓库是公开的。** 文件和提交信息里不写内部决策、会话编号、私有仓库名和商业安排；遵守率记录只写周期名称，不写会话编号。
- **新增技能或大改技能的工作流之后、发布之前，** 派一个只拿到该技能 `SKILL.md` 路径的全新 agent，在真实项目上按技能执行一次，要求它列出指令不清、矛盾或缺失之处；核验它的产出后按反馈迭代。用作样本的项目一律只读：规划里写明，产出写到会话 scratchpad，不写进样本仓库。
