# 规划：插件市场迁到 tealun/tealun-plugins

状态：已实现（tealun-plugins main 首次提交，本仓库 #30 已合并；之后仓库由 claude-plugins 改名，见 M7）· 2026-11-05

## 1. 理解卡

- **目标**：用户名下以后会有多个插件，各自一个仓库。市场 `tealun` 只保留一份清单，放在单独的仓库 `tealun/tealun-plugins`，每个插件在清单里占一条，指向自己的仓库。
- **用户已决定**（2026-11-05）：
  - 新技能单独建仓库；
  - 市场仓库为 `tealun/tealun-plugins`，市场名仍是 `tealun`。
- **非目标**：
  - 不改插件目录的提交，目录只读 `plugin` 分支，那里没有 `marketplace.json`；
  - 不改 Release 安装包和 WorkBuddy 套件包；
  - 不升插件版本，不推 tag，因为技能目录没有改动。

## 2. 契约

- `done_definition`：
  - `tealun/tealun-plugins` 有 `marketplace.json`（名为 `tealun`，`dev-pdca` 指向 `tealun/tealun-dev-pdca` 的 `plugin` 分支）、README、LICENSE、AGENTS.md，以及运行 `claude plugin validate` 的 CI；
  - tealun-dev-pdca 删掉 `marketplace.json`；README、QUICKSTART、CONTRIBUTING、规则表里的安装命令全部改成新市场，并写明老用户的迁移步骤；
  - `build_plugin.py` 不再读取 `marketplace.json`，改为检查 `plugin.json` 列出的技能和根目录下的技能文件夹一致。
- `validation_method`：
  - 对新清单运行 `claude plugin validate`；
  - 在隔离的 HOME 里添加新市场并安装 `dev-pdca@tealun`，确认装到的是 `plugin` 分支的内容；
  - tealun-dev-pdca 的 `build_plugin.py --check`、`build_suite.py --check`、`check_ledger.py`、unittest；
  - 用 `git grep` 统计旧的安装命令，历史记录之外的残留应为 0。
- `fail_condition`：
  - `github` 类型的 source 加 `ref` 无法安装；
  - 删掉 `marketplace.json` 后，校验或测试失去对“新增技能目录却没写进清单”的拦截。

## 3. 用到的台账条目

- EV-20261102-001、EV-20261102-003（外部平台规则先登记、再写成本地检查）：市场清单的格式由 `claude plugin validate` 校验，写进新仓库的 CI。
- EV-20261105-003（插件目录跟踪 `plugin` 分支）：市场也指向 `plugin` 分支。这样用户只会装到已发布的版本，main 上没发布的改动不会被装到。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| M1 | 市场仓库 `tealun/tealun-plugins`，市场名 `tealun` | 用户决定；一份清单列出全部插件，用户只需添加一次 |
| M2 | `dev-pdca` 条目：`{"source":"github","repo":"tealun/tealun-dev-pdca","ref":"plugin"}` | 只有推 tag 后 CI 才会更新 `plugin` 分支，所以用户只会装到已发布的版本。已在隔离环境里实测安装成功，装到的是 1.0.1 |
| M3 | 插件仓库不再带 `marketplace.json` | 两份同名为 `tealun` 的市场会冲突 |
| M4 | `build_plugin.py` 第 2 项检查改为：`plugin.json` 的 `skills` 和根目录下含 `SKILL.md` 的文件夹一致 | 保留原来“新增技能目录却没写进清单”的拦截，不再依赖市场清单 |
| M5 | 以后新增插件：在 `tealun-plugins` 的清单里加一条，指向该插件仓库的 `plugin` 分支（或它的发布分支），新仓库里不放市场清单 | 和 M2、M3 一致 |
| M6 | 老用户迁移：先 `/plugin marketplace remove tealun`，再 `/plugin marketplace add tealun/tealun-plugins`，然后重新安装 | 市场的来源变了，旧的市场不会自动跟过来 |
| M7 | 2026-11-05 仓库由 `claude-plugins` 改名为 `tealun-plugins` | 用户决定：Claude 桌面端用仓库名标记市场来源（显示 "by claude-plugins"），容易被误读为官方插件 |
| M8 | README 不写旧市场的迁移说明 | 用户 2026-11-05 决定：除用户本人外没人用过旧市场 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：新市场推送到 GitHub 后，按 README 的命令能安装 | 用户在自己的 Claude Code 里迁移后，`/plugin` 列表里能看到 dev-pdca 1.0.1 | 用户迁移时 |
