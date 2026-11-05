# 规划：plugin 分支只在 Release 成功后写入；补登 WorkBuddy 规则

状态：已实现，待下次发版核实 V1 · 2026-11-05

## 1. 理解卡

- **起因**：发布前审计报出三处问题，均已在仓库里复现或核对过原文：
  1. `plugin-branch.yml` 和 `release.yml` 由同一次 `v*` 推送触发，两者并行运行。`plugin-branch.yml` 只跑 `build_plugin.py --check`，不带 `--tag`，也不跑单元测试和台账检查。由此产生两个后果：
     - Release 失败的 tag 仍会写进 `plugin` 分支；
     - 在 main 上手动触发时，会把还没发布的 main 内容写进 `plugin` 分支。

     插件目录跟踪的就是 `plugin` 分支，所以这是发布闸门的缺口。
  2. `docs/workbuddy-rules.md` 漏登了第三方 schema（[workbuddy-schema.md](https://github.com/starve001/wb-skill-converter/blob/main/references/workbuddy-schema.md)，2026-11-05 读取）里的若干规则。原文逐条核对后，确认漏登以下几条：
     - `description` 约定与 `description_zh` 同值；
     - `workbuddy-` 前缀疑似保留；
     - 付费资产的展示名不能含空格；
     - `agent_created` 建议填写；
     - 换行统一用 LF；
     - 打包排除 `.git` 和 `node_modules`；
     - category 取值表；
     - “不要写”的字段清单；
     - 改动通常要重新过审。
  3. `publish_plugin_branch.sh` 首次发布时建了本地孤立分支 `publish-<branch>`，之后没有删除。在本地临时远端上演练：远端分支删掉后，从同一个 clone 再发布，报 `fatal: a branch named 'publish-plugin' already exists`。
- **非目标**：
  - 不改技能目录和 `suite/dev-pdca/SKILL.md`；
  - 不发新版本；
  - 不重新上传 WorkBuddy（1.5.1 正在审核）；
  - 不改 `plugin` 分支现有内容。

## 2. 契约

- `done_definition`：
  - `plugin` 分支的写入改由 `release.yml` 中 `needs: release` 的作业触发：Release 失败就不写。
  - `plugin-branch.yml` 只剩手动补写一个用途：必须指定 tag，且这个 tag 已有 GitHub Release；会重跑 `build_plugin.py --check --tag`。手动触发入口不再接受 main。
  - 两条路径共用同一份作业定义（可复用工作流），不复制步骤。
  - 发布脚本不再创建本地分支；重复运行、远端分支被删后再运行都能成功。
  - WorkBuddy 规则表逐条登记上述规则：能写成检查的写进 `build_suite.py`，其余写明不校验的原因。
- `validation_method`：
  - 两个工作流 YAML 能解析，且 `needs`、`uses`、`inputs` 的结构正确；
  - 发布脚本在本地临时远端上跑 4 个场景：首次发布、内容不变、内容变化、远端分支删除后再发布；
  - `build_suite.py --check`、unittest、`check_ledger.py`、`build_plugin.py --check --since v1.0.1` 全部通过；
  - 新增的检查用变异测试证明会报错。
- `fail_condition`：
  - `plugin` 分支仍然有不经过 Release 的写入路径；
  - 新检查让当前的 1.5.1 包校验失败；
  - 可复用工作流拿不到写权限。

## 3. 用到的台账条目

- EV-20261105-003（Institutionalized）：其中“今后改插件内容：推 tag，由 CI 更新 plugin 分支”的说法依然成立，本次只收紧到“Release 成功后”。
- EV-20261102-001、EV-20261102-003（外部平台规则要登记完整）：规则 2 正是这条防线的遗漏。新开 EV-20261105-005 记录两处缺口。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| R1 | `plugin-branch.yml` 改为可复用工作流（`workflow_call` + `workflow_dispatch`，都必须给 `tag`）。`release.yml` 新增作业 `plugin-branch: needs: release`，调用它 | 只有 Release 成功的 tag 才进入 `plugin` 分支；两条路径只有一份步骤定义 |
| R2 | 工作流检出 `inputs.tag`，先用 `gh release view` 确认 Release 存在，再跑 `--check --tag` | 手动补写只能针对已经发布的版本，不能针对 main 或分支 |
| R3 | 发布脚本始终使用分离的 worktree，用 `write-tree` + `commit-tree` 生成提交，首次发布时不带父提交 | 不创建本地分支，彻底消除残留分支 |
| R4 | 新增检查：`name` 不以 `workbuddy-` 开头；`category` 在已知取值内；排除 `.git`、`node_modules`；包内文本不含 CR | 都是可以机械判断的规则 |
| R5 | 不校验并写明原因：`description` 与 `description_zh` 同值、付费展示名无空格、`agent_created`、“不要写”的字段 | 前两条与 1.5.1 现状不符，改动会改变上架文案，见“待决” |

## 5. 待决（要 Tealun 拍板，等 WorkBuddy 审核结果后再定）

| 项 | 现状 | 选项 |
|---|---|---|
| D1：`description` 是否改成与 `description_zh` 同值 | 1.5.1 的 `description` 是中英混写的路由描述，与 `description_zh` 不同；上传和解析都没有报错 | 保持现状 / 改为同值（技能召回会改用营销文案） |
| D2：`display_name` 去掉空格 | 当前是“开发闭环 dev-pdca”，含空格；这条规则只适用于付费资产，dev-pdca 是免费的 | 保持现状 / 改为“开发闭环dev-pdca”或“开发闭环-dev-pdca” |

## 6. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：下一个版本 tag 推送后，`plugin-branch` 作业在 `release` 之后运行，`plugin` 分支随之更新 | Actions 运行记录、`plugin` 分支日志 | 下次发版 |
