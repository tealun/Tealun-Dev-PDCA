# Changelog

本文件记录 Tealun Skills 项目层面的重要变化。单个技能的历史说明可能位于各自目录内。

## Unreleased

- `dev-pdca` 补充 `examples_zh` / `examples_en`（WorkBuddy「试试这样问我」示例，各 5 条，覆盖五个子技能，按实际使用场景改写）和 `author`；`build_suite.py` 校验示例字段存在。
- `description_en` 压缩到 WorkBuddy 上限 1000 字符以内；`build_suite.py` 校验 `description_zh` / `description_en` 不超过 1000 字符。
- `dev-pdca` 的 `description_zh` / `description_en` 改写为完整的能力介绍：逐个说明五个子技能各自守住什么，以及它们之间如何自动接力。
- `dev-pdca` 入口补充 WorkBuddy 上架必填的 frontmatter：`display_name`、`display_name_en`、`description_zh`、`description_en`；`build_suite.py` 校验这四项。
- `dev-pdca` 套件包改为最多三层目录（`dev-pdca/<子技能>/<文件>`），以满足 WorkBuddy 的层级限制：子技能的 `references/`、`scripts/` 文件在打包时移到子技能目录下，文中引用路径同步改写；不再打包 Codex 专用的 `agents/` 元数据。仓库内技能源码结构不变。
- 新增套件包 `dev-pdca` 1.0.0（`suite/dev-pdca/SKILL.md`）：一个入口技能按 PDCA 分派到 5 个子技能，面向 WorkBuddy 等只能上传单个技能的平台。子技能文件按 `./<name>/SKILL.md`、`../<name>/SKILL.md` 顺序解析，套件包与仓库/插件两种目录结构都能用；原本分散在各技能描述里的自动转交条件，集中为会话级规则。
- 新增 `scripts/build_suite.py`：校验入口描述长度、版本号和子技能完整性，生成仓库根目录的 `dev-pdca.zip`（可直接下载上传）和 `dist/` 下的 `-flat.zip`。构建结果逐字节可复现，`--check` 用来发现成品与源码不一致。
- 新增 CI `.github/workflows/suite-package.yml`：每次推送校验 `dev-pdca.zip` 与技能源码一致。
- README（中英文）与插件清单改为以 PDCA 开发闭环介绍技能分工与衔接，并增加套件包安装方式。
- 新增面向开源用户的项目 README。
- 新增快速开始、支持、贡献、行为准则、安全策略和许可证文件。
- 明确技能集合、安装方式、兼容工具和反馈路径。
- `bugfixer` 增加生成物新鲜度/版本失效检查，以及部署进程找不到 CLI 二进制时的环境差异排查规则。
- `tasker` 增加提交/推送收口校验：区分用户改动与任务文件、回读本地提交，并用远端分支 SHA 验证推送结果；多阶段任务在阶段边界 checkpoint，清理仅限明确生成物。
- `bugfixer` 1.6.0：原症状验证消失后，项目有测试框架时要补一条不带修复就会失败的自动化回归测试（没有测试框架时补最接近的可执行检查）；条件允许时临时撤掉修复做一次变异检查，证明这条测试真的能拦住问题。没有可用框架时写明原因并作为未防护缺口报告。
- 新增 `docs/agent-instructions-snippet.md`：可直接粘贴到项目 `CLAUDE.md` / `AGENTS.md` 的中英文技能触发片段，以及在云端会话里把技能固定版本放进项目的做法。
- 新增 Claude Code 插件市场清单 `.claude-plugin/marketplace.json`：`/plugin marketplace add tealun/Tealun-Skills` 后 `/plugin install tealun-skills@tealun-skills` 即可安装五个技能。技能目录位置不变，同步脚本照常可用。
- README 增加插件安装方式、「让 Agent 真的调用技能」指令片段；新增英文版 `README.en.md`，两份 README 顶部互相链接。

## 现有技能

- `planner` 2.0.0
- `tasker` 1.8.3
- `auditor` 4.1.0
- `bugfixer` 1.6.0
- `evolver` 当前技能文件未声明版本
