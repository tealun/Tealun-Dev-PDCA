# Claude 插件目录规则对照表

提交 Claude 插件目录前要满足的已知规则，以及每条规则由什么检查。新增规则时，先在这里加一行，再补校验；能写成本地检查的就写进 `scripts/build_plugin.py --check`，写不了的要注明原因。

插件文件夹就是仓库根目录（`.claude-plugin/plugin.json` 所在目录），目录会读取其中所有被跟踪的文件。

**来源**（2026-11-04 读取）：
- **提交**：[Submit a plugin](https://claude.com/docs/plugins/submit)
- **清单**：[Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist.md)
- **构建**：[Build a plugin](https://claude.com/docs/plugins/build.md)
- **参考**：[Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- **CLI**：`claude plugin validate`（2.1.318）的实际输出
- **方案**：Claude Docs《Tealun-Skills 插件发布规范化方案》的转述；以上官方页面里找不到原文

**检查级别**：
- **阻断**：`--check` 报错，CI 失败；
- **提示**：`--check` 打印 warning，不阻断，因为目录对这类问题的处理是转人工审核，不是拒收。

## 提交与托管

| 规则 | 来源 | 本地检查 |
| --- | --- | --- |
| 目录只从 github.com 上的仓库读取插件 | 提交 | 不校验：仓库托管在 GitHub 上是既定事实 |
| 提交和验证期间仓库可以是私有的，上架前必须公开 | 提交 | 不校验：仓库是否公开是 GitHub 设置；提交时由用户在开发者门户确认 |
| 每个插件文件夹单独提交一次；同一组织对同一仓库加文件夹只能有一个提交 | 提交 | 不校验：本仓库只有一个插件文件夹 |
| 每个组织 24 小时内最多创建 10 个提交，草稿和撤回的提交也计入 | 提交 | 不校验：属于门户操作次数 |
| 首次提交之后，目录跟踪的分支一有新提交就会扫描、检查、发布；本仓库跟踪 `plugin` 分支（2026-11-05 起，见下文“扫描范围”） | 提交 | 不校验：在门户里设置 |
| 第一个版本必须由 Anthropic 审核员批准才能上线；在此之前点 Publish 只是登记一个请求。门户的 Auto-publish 开关只对之后通过检查的版本生效 | 门户 | 不校验：门户流程。2026-11-05 提交时开关保持开启，门户显示“暂不适用：本插件的每个版本都要经审核员” |
| 同一仓库加文件夹已有提交（含草稿）时，再新建会报 `SUBMISSION_EXISTS`；继续已保存的草稿时，仓库、文件夹和分支都不能改，要换来源只能删掉草稿重建 | 门户 | 不校验：门户操作。本仓库的草稿创建于切换分支之前，继续时 Source 已显示跟踪 `plugin` |
| 目录每约 6 小时检查一次跟踪的分支；配置 GitHub push webhook 后，推送几分钟内就会被拾取。webhook 的 secret 只显示一次 | 门户 | 不校验：仓库设置。2026-11-05 已配置，GitHub 显示首次投递成功，门户显示 Webhook connected |
| 提交时要回答数据处理问卷（个人数据、外发数据、数据保留、是否面向未成年人）并勾选 4 项合规声明，答案要和 `PRIVACY.md` 一致 | 门户 | 不校验：问卷属于门户操作。本插件的答案是 No · No · Not retained · No；唯一的脚本 `evolver/scripts/append_evolution_ledger.py` 只在本地调用 `git rev-parse`，没有网络访问 |
| 每次扫描都会按目录规则重新校验，并做安全扫描（未披露的外发数据、隐藏代码、修改权限设置）；首次提交没通过安全扫描会直接被拒；另有政策审核 | 提交 | 部分校验：`claude plugin validate` 只覆盖目录规则的一部分，不做安全扫描和政策审核 |

## 清单（plugin.json）

| 规则 | 来源 | 本地检查 |
| --- | --- | --- |
| 清单位于 `.claude-plugin/plugin.json`，`name` 必填 | 参考 | 阻断：`check()` 第 1 项 |
| 应设置 `description`、`author`、`version`，缺少会给警告 | 清单 | 阻断：`check()` 要求三项都有 |
| 名称只能用小写字母、数字、连字符，最长 64 字符，首尾必须是字母或数字；不能是保留名（`claude`、`anthropic`、`official`、`plugin`、`mcp`、`test`）；不能以 `claude-`、`anthropic-`、`anthropics-`、`cc-plugin-` 开头 | 清单 | 阻断：`check()` 的命名规则 |
| 设了 `version` 就要在每次发布时升高；Claude Code 会固定使用这个版本，直到它改变 | 提交、参考 | 阻断：`--since <上一个 tag>`，技能有改动但版本没升高 |
| `skills` 是相对插件根目录、以 `./` 开头的目录路径；本仓库的技能不在 `skills/` 下，所以显式列出 | 参考 | 阻断：`check()` 第 2、3 项（和根目录下含 `SKILL.md` 的文件夹一致，每个技能都有 `SKILL.md` 且名称对得上） |
| 上架页的文字取自 `plugin.json` 和 README；上架后，名称和简短描述跟随线上版本 | 提交 | 不校验：属于文案内容 |
| `icon` 是插件内图片文件的路径；Claude Code 不读它，目录在提交时读取 | 参考 | 阻断：`icon` 指向的文件必须存在 |
| 图标规格：512–2048 px 正方形、小于 2 MB、不接受 SVG/WebP；只在第一次提交或保存时生效 | 方案 | 不校验：官方页面没找到原文。本仓库图标为 512×512 PNG，已满足上述说法 |

## 文件与内容

| 规则 | 来源 | 本地检查 |
| --- | --- | --- |
| 插件文件夹里要有 README，代码块之外至少 40 个单词 | 清单 | 阻断：`check()` 统计 `README.md`（目前 455 个） |
| 要有 `LICENSE` 文件，或在 `plugin.json` 设置 `license` | 清单 | 阻断：两者都没有时报错 |
| 单个文件超过 5 MiB，校验会停止 | 清单 | 阻断：逐个检查被跟踪的文件 |
| 不能有符号链接 | 清单 | 阻断：逐个检查被跟踪的文件 |
| 不能有子模块和 LFS 指针 | 清单 | 不校验：仓库里没有 `.gitmodules`，也没有用 LFS |
| 仓库导出（git archive）的内容必须和仓库存储的完全一致：`.gitattributes` 里不能有 `export-ignore`、`filter`（包括 LFS）或会改动换行的 `eol` 规则，也不能有 Git replace refs；文件名不能含冒号或反斜杠、不能以点或空格结尾、不能是 Windows 设备名、不能有只差大小写的同名文件 | 实测（2026-11-05 门户 Validate 报错原文） | 阻断：`content_rewriting_attributes()` 不允许 `.gitattributes` 出现任何会改写内容的属性（第一次只去掉 `eol=crlf`，Validate 仍报错；改为 `* -text` 后再验证）；`export_mismatches()` 导出索引后逐个比对；文件名规则目前没有触发，暂不单独校验 |
| 图片和字体以外的文件超过 256 KiB，转人工审核 | 清单 | 提示：`directory_warnings()` |
| 文件超过 512 个，转人工审核 | 清单 | 提示：`directory_warnings()`（目前 84 个） |
| 只允许文本、SVG、PNG、JPEG、GIF、WebP 和字体；其他二进制文件（如 `.zip`、`.ico`、`.pdf`）转人工审核 | 清单 | 提示：`directory_warnings()`。目前没有命中：`dev-pdca.zip` 已于 2026-11-05 移出仓库，见下文“已解决的问题” |
| 删掉 `.DS_Store`、`Thumbs.db`、`desktop.ini`、`__MACOSX` | 清单 | 提示：`directory_warnings()` |
| 包启动器要固定版本（如 `npx pkg@1.2.3`），`@latest` 和不固定的版本范围会被拦下 | 清单 | 不校验：插件本身不调用启动器。发布流程里的 `npx @anthropic-ai/claude-code@2.1.318` 已固定版本 |
| 凭据不能写死在代码里 | 清单 | 不校验：插件不需要任何凭据 |
| 顶层有 `bin/` 目录时，claude.ai 和 Cowork 无法安装 | 清单 | 不校验：没有 `bin/`，且打包时只收技能目录、README、LICENSE 和图标 |
| 安全扫描读不懂的编译或压缩代码，转人工审核 | 清单 | 不校验：技能目录里只有 Markdown 和 Python 源码 |

## 安装包

| 规则 | 来源 | 本地检查 |
| --- | --- | --- |
| claude.ai 的安装方式：Customize > Plugins > Add > Upload plugin，上传 zip；zip 根目录（或唯一的顶层目录）里要有 `.claude-plugin/plugin.json` | 构建 | 阻断：单元测试检查包的结构；发布流程用 CLI 校验解包后的 `dist/tealun-dev-pdca/` |
| `.plugin` 后缀 | 方案 | 不校验：官方页面没有 `.plugin` 格式的说明。Release 同时附上内容完全相同的 `.zip` 和 `.plugin`，README 指导用户上传 `.zip` |

## 扫描范围：插件目录跟踪 `plugin` 分支（2026-11-05 起）

目录会把插件文件夹里的所有文件都当成插件来扫描。插件文件夹原本是仓库根目录，于是在 `main @ c83cb02` 上，开发工具被报出了 6 个 policy hold 和 5 个 warning：

| 门户报出的项 | 级别 | 来源 | 处理方式 |
| --- | --- | --- | --- |
| Uses a credential from the user's machine | policy hold | `.github/workflows/release.yml` 的 `GH_TOKEN`（推断） | 不进入 `plugin` 分支 |
| Image or font file that the plugin's code could run（5 处） | policy hold | 仓库里的脚本和测试（推断，详情没有展开） | 不进入 `plugin` 分支 |
| Contains a download-and-run command（3 处） | warning | `release.yml` 的 `npx -y`、文档里的安装命令（推断） | 不进入 `plugin` 分支；切换到 `plugin` 分支后仍有 1 处，来自 README 里 clone 后运行同步脚本的说明，已在 2026-11-05 删除同步脚本及相关说明；`build_plugin.py --check` 的 `DOWNLOAD_AND_RUN` 检查 README，有这类写法就阻断 |
| CLAUDE.md at the plugin root isn't loaded | warning | 根目录的 `CLAUDE.md` | 不进入 `plugin` 分支 |
| Field from another tool's manifest（`icon`） | warning | `plugin.json` | 页面说明不需要处理 |

处理方式：由 `.github/workflows/plugin-branch.yml` 把打包好的插件（技能、`plugin.json`、README、LICENSE、图标）提交到 `plugin` 分支，插件目录改为跟踪这个分支，插件路径留空。用本地 CLI 对这个分支的内容做 validate，结果是 "These checks found nothing to report"，导出内容和存储内容一致。

## 首次提交的扫描结果（v1.0.1 · `plugin @ 596d45e`，2026-11-05）

安全扫描通过（用时 3 分钟），目录政策“通过但有 warning”，状态为 In review，已点 Publish 请求审核员发布。门户报出的项：

| 门户报出的项 | 代码 | 级别 | 处理方式 |
| --- | --- | --- | --- |
| Images and fonts passed without a code check：`assets/dev-pdca-avatar.png` | `ASSETS_PASSED_UNREAD` | note | 不处理：格式正确的图片不按代码读取，其中可打印的文字仍会被筛查 |
| Unrecognized field in plugin.json：`documentationUrl`、`privacyPolicyUrl`、`supportUrl` | `UNKNOWN_KEY` | warning | 不处理：这三个是只供上架页读取的字段，Claude Code 加载时忽略；门户写明 No action needed |
| Field from another tool's manifest：`icon` | `UNKNOWN_KEY_CROSS_TOOL` | warning | 不处理：目录读取 `icon` 作为上架图标，Claude Code 加载时忽略；门户写明 No action needed |

这些项不写成本地检查：它们是对合法字段的提示，不是错误。`build_plugin.py --check` 要求 `icon` 指向的文件存在，三个链接字段由 `plugin.json` 维护。

## 已解决的问题

**`dev-pdca.zip` 曾会让插件转人工审核（2026-11-05 已解决）。** 它是 WorkBuddy 套件包，按规划的非目标原样留在仓库根目录，而仓库根目录就是插件文件夹。按清单的规则，`.zip` 文件会转人工审核：不会被拒，但每个版本都要等审核员处理。另外，`claude plugin validate`（2.1.318）的目录检查没有报出这一条，说明它只覆盖了目录规则的一部分，以清单页面为准。用户决定把它移出：仓库不再跟踪这个文件，由 `release.yml` 构建后附到 Release 上，见 `docs/88_planning/suite-zip-out-20261105.md`。
