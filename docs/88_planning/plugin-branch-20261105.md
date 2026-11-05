# 规划：插件目录跟踪专用的 plugin 分支

状态：实现中 · 2026-11-05

## 1. 理解卡

- **现状**：插件目录 Validate 已经通过（main @ c83cb02），但出现 6 个 policy hold 和 5 个 warning：
  - Uses a credential from the user's machine；
  - Image or font file that the plugin's code could run（5 处）；
  - Contains a download-and-run command（3 处）；
  - CLAUDE.md at the plugin root isn't loaded；
  - icon（这一项页面注明不需要处理）。
- **原因**：插件文件夹就是仓库根目录，所以目录把 `.github/`（CI 用的 `GH_TOKEN`、`npx -y`）、`scripts/`、`tests/`、文档和 CLAUDE.md 都当成插件的一部分来扫描。这些都是开发工具，不在插件运行时的范围内。
- **用户已决定**（2026-11-05）：方案 B，让目录只扫描构建出来的干净插件。这一条替代 `plugin-release-20261104.md` 里“门户跟踪 main”的决定。
- **非目标**：
  - 仓库结构、技能目录、main 分支的开发流程都不动；
  - 不发新版本；
  - 不改 claude.ai 自建市场和 Claude Code 的安装方式（它们照旧读 main）。

## 2. 契约

- `done_definition`：
  - 新增 `.github/workflows/plugin-branch.yml`：推送 `v*` tag 或手动触发时，构建插件，用固定版本的 CLI 校验，再把 `dist/tealun-dev-pdca/` 的内容提交到 `plugin` 分支；
  - 合并后手动触发一次，`plugin` 分支里只有插件内容；
  - 这个分支的内容通过本地 `claude plugin validate`，导出内容与存储内容一致；
  - 文档和规则同步更新。
- `validation_method`：
  - 工作流 YAML 能正常解析；
  - 在本地临时仓库里完整演练一遍提交脚本（新建分支、再更新一次）；
  - 触发后检查 `plugin` 分支的文件清单；
  - 对该分支内容跑 validate 和导出比对。
- `fail_condition`：
  - `plugin` 分支里混入开发文件；
  - 推送到 `plugin` 分支后触发了 main 的 CI，导致 CI 失败；
  - 工作流拿不到写权限。

## 3. 用到的台账条目

- EV-20261105-002（Guarded）：两次修复后 Validate 已经通过，在原行升级为 Institutionalized，补上证据 c83cb02。
- EV-20261102-001、EV-20261102-003（外部平台规则）：`docs/claude-directory-rules.md` 补登这次的 hold 和 warning 类型，以及对应的处理方式。

## 4. 决策

| # | 决策 | 理由 |
|---|---|---|
| B1 | 插件目录跟踪 `plugin` 分支，插件路径留空 | 扫描范围只剩技能、清单、README、LICENSE 和图标 |
| B2 | `plugin` 分支只由 CI 写入：推送 `v*` tag 时，或手动触发 `workflow_dispatch` 时（用于首次填充和补发）。每次是在已有分支上追加一个提交，不重写历史 | 只有发布过的版本才进入目录；改动可以追溯 |
| B3 | 分支内容就是 `build_plugin.py` 的打包结果（`dist/tealun-dev-pdca/`），和 Release 附件同源 | 只有一份构建产物 |
| B4 | `suite-package.yml` 的 push 触发排除 `plugin` 分支 | 那个分支上没有脚本，跑 main 的 CI 必然失败 |
| B5 | 提交前在工作流里用 `npx -y @anthropic-ai/claude-code@2.1.318 plugin validate` 校验打包结果 | 不合格的内容不会进入分支 |

## 5. 待核实

| 项 | 证据形式 | 何时 |
|---|---|---|
| V1：用户在门户改为跟踪 `plugin` 分支后，之前的 policy hold 和 warning 是否消失 | 门户的 Validation 列表 | 用户重新 Validate 后 |
