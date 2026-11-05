# 规划：品牌更名为 Tealun Dev PDCA

状态：已实现，等仓库改名后合并（插件 1.0.1；台账 EV-20261105-001） · 2026-11-05

## 1. 理解卡

- **目标**：把品牌从泛化的 Tealun Skills 改成用途明确的 Tealun Dev PDCA。品牌只出现在别人发现和安装插件的地方：仓库名、市场名、上架名称、下载文件名、README、LICENSE、每个技能末尾的出处行。用户日常调用时尽量简短，不重复出现品牌。
- **用户已决定**（2026-11-05）：
  - 方案 A：六个技能的名字不变，品牌靠每个 SKILL.md 末尾的出处行和 LICENSE 来体现；
  - 仓库改名为 `tealun-dev-pdca`，由用户在 GitHub 上操作。
- **非目标**：
  - 不改技能名称、行为和触发描述；
  - 不改 WorkBuddy 套件包的名字 `dev-pdca` 和它的打包机制；
  - `dev-pdca.zip` 要不要移出插件文件夹，另行决定，本次不涉及。

## 2. 契约

- `done_definition`：
  - 除历史记录（台账、过往规划、发布说明、CHANGELOG 旧条目）外，仓库里不再出现旧名；
  - 插件名改为 `dev-pdca`，市场名改为 `tealun`，上架名称为 "Tealun Dev PDCA"，下载文件为 `tealun-dev-pdca-<版本>.zip` 和 `.plugin`；
  - 六个 SKILL.md 末尾各有一行出处；
  - 插件升到 1.0.1，套件包升到 1.5.1，并写好 CHANGELOG；
  - 等用户改完仓库名再合并，然后发布。
- `validation_method`：
  - `git grep` 统计旧名残留；
  - `claude plugin validate`，对插件清单和市场清单各跑一次；
  - `build_plugin.py --check --since v1.0.0`、`build_suite.py --check`、`check_ledger.py`、unittest；
  - 检查构建产物的文件名和包内的清单。
- `fail_condition`：
  - validate 不接受 `dev-pdca` 或 `tealun` 作为名称；
  - 改名后仍有链接指向不存在的地址；
  - 出处行改变了技能的触发方式或行为。

## 3. 用到的台账条目

- EV-20261104-004（Institutionalized）：它的 Next Planning Input 有一条“`dev-pdca.zip` 是否移出插件文件夹”。这不属于本次范围，仍由用户决定。
- EV-20261102-001、EV-20261102-003（外部平台规则）：新名字要符合插件目录的命名规则。`build_plugin.py --check` 已经覆盖这一点，validate 会再查一次。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| R1 | 仓库名：`tealun/tealun-dev-pdca` | 被 fork 或复刻后，仓库名里仍带着品牌 |
| R2 | 插件名：`dev-pdca`；`displayName`：`Tealun Dev PDCA` | 插件名是调用前缀（`/dev-pdca:tasker`），短一些好用；上架页显示 displayName |
| R3 | 市场名：`tealun`，安装命令为 `/plugin install dev-pdca@tealun` | 安装时能看到品牌 |
| R4 | 下载文件：`tealun-dev-pdca-<版本>.zip` / `.plugin`，`build_plugin.py` 的打包名与插件名分开设置 | 下载时能看到品牌，也不和 WorkBuddy 的 `dev-pdca.zip` 混淆 |
| R5 | 每个 SKILL.md 正文末尾加一行：`Part of Tealun Dev PDCA by Tealun · https://github.com/tealun/tealun-dev-pdca · MIT`；frontmatter 字段集合不变 | 用户选的方案 A。出处放在正文末尾，不影响执行；frontmatter 不动，就不需要再改字段校验 |
| R6 | LICENSE 版权行改为 `Copyright (c) 2026 Tealun` | MIT 要求复制时保留版权声明，原来写的 `Tealun-Skills contributors` 里没有作者本人的名字 |
| R7 | 版本：插件 1.0.1（按 AGENTS.md，只改清单和文档的升 patch）；套件包 1.5.1（包内技能文件有变化）；技能版本不变（出处行不改变行为） | 遵守 AGENTS.md 的升版规则 |
| R8 | 旧名的历史记录不改：台账、过往规划、`docs/releases/`、CHANGELOG 旧条目 | 历史记录要保持当时的原样 |
| R9 | 合并顺序：PR 先开好、CI 通过；等用户改完仓库名再合并；之后由用户推送 `v1.0.1` | 新链接在仓库改名之前会是 404；本会话推不了 tag |
| R10 | 已安装旧插件 `tealun-skills` 的用户要卸载后重装；CHANGELOG 和 README 写明迁移步骤 | 插件名变了，不会自动更新过去 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：validate 接受新的插件名和市场名 | 已核实：plugin.json 只有一条 CLAUDE.md 警告；marketplace.json 通过；打包后的清单通过 | 已完成 |
| V2：仓库改名后，旧地址能跳转到新地址，定时审计和 Tiko.day 引用的仓库都还能用 | 用新地址 fetch；首次周审计的运行情况 | 用户改名后 / 2026-11-09 |

## 6. 实施中发现的问题

- 版本升到 1.0.1 后，单元测试 `test_skill_change_needs_version_bump` 失败。原因是这个测试把基线 tag 写死成 `v1.0.0`，默认清单版本和 tag 一致，版本一变，“没升版本”的情形就构造不出来了。缺陷在测试本身，脚本逻辑没有问题。修正：测试改为从清单读取当前版本、给 fixture 打对应的 tag，测试文件里不再出现写死的版本号。变异检查：把脚本里的 `<=` 改成 `<` 后，这个测试失败；恢复后通过。
