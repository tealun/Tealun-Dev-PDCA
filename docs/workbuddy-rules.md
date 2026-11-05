# WorkBuddy 上架规则对照表

`dev-pdca.zip`（由 `build_suite.py` 生成到 `dist/`，发版时附在 Release 上）上传 WorkBuddy 前要满足的全部已知规则，以及每条规则在本地由谁检查。新增规则时，先在这里加一行，再补校验；能校验的必须写进 `scripts/build_suite.py`，不能校验的写明原因。

来源：**实测** = 上传或审核实际报错过；**第三方** = [wb-skill-converter 的 workbuddy-schema.md](https://github.com/starve001/wb-skill-converter/blob/main/references/workbuddy-schema.md)，非官方文档。

逐段核对记录：2026-11-05 读完第三方 schema 全文，覆盖“字段全解”“category 取值”“打包与上传规则”“付费技能的数据结构”“两个真实驳回案例”五节。付费一节说的是运营后台的表单字段，不写进 `SKILL.md`，所以没有登记。来源更新后，按这五节重新逐段核对。

| 规则 | 来源 | 本地检查 |
| --- | --- | --- |
| 目录最多三层：根目录 / 二级目录 / 文件 | 实测 | `package_files()`：超过即报错 |
| 包内只能有一个 `SKILL.md`（多个会被判为多 skill 包、资产无效） | 实测 + 第三方 | `validate_package()`：只允许根目录一个；子技能入口改名为 `<名称>.md` |
| 其他 `.md` 不能带技能 frontmatter | 推断（规避被识别为第二个技能） | `validate_package()`：子技能入口去掉 frontmatter |
| 必填 `display_name`、`display_name_en`、`description_zh`、`description_en` | 实测 | `validate()` |
| 必填 `name`、`description`、`version` | 第三方 | `validate()`：存在且 `version` 为 x.y.z |
| `name` 符合 `^[a-z0-9][a-z0-9-]{0,39}$` | 第三方 | `validate()` |
| `display_name_en` ≤ 60 字符 | 第三方 | `validate()` |
| `description_zh` ≤ 500 字符 | 第三方 | `validate()` |
| `description_en` ≤ 1000 字符 | 实测 | `validate()` |
| `examples_zh`、`examples_en` 各 1–3 条 | 实测 | `validate()` |
| frontmatter 必须是合法 YAML（值里有 `: ` 要加引号） | 第三方 | 示例值统一加引号；入口 frontmatter 改动后用 YAML 解析读回 |
| 编码 UTF-8 无 BOM | 第三方 | `validate_package()` |
| 排除 `__pycache__`、`.git`、`.DS_Store`、`node_modules`、`*.pyc` | 第三方 | `EXCLUDE_PATTERNS`（2026-11-05 补上 `.git`、`node_modules`） |
| 压缩包根目录直接放 `SKILL.md`，不要多套一层目录 | 第三方 | 不校验：实测内含 `dev-pdca/` 文件夹的包已解析通过；如被拒，改传 `dist/` 下的 `-flat.zip` |
| `name` 全平台唯一 | 第三方 | 不能本地校验：只有上传时平台才能判断 |
| `category` 建议填写 | 第三方 | 已填 `developer`；不要求必填 |
| `category` 取市场出现过的值（`productivity`、`developer`、`writing` 等 20 个） | 第三方 | `validate()`：填了就必须在 `WORKBUDDY_CATEGORIES` 里 |
| `workbuddy-` 前缀疑似官方保留，自定义技能避免使用 | 第三方 | `validate()`：`name` 不能以 `workbuddy-` 开头 |
| 换行统一 LF（CRLF 一般能用，但不建议） | 第三方 | 打包时 `read_normalized()` 把 CRLF 转成 LF；`validate_package()` 发现包内文本还有 CR 就报错 |
| `description` 约定与 `description_zh` 同值（市场列表与技能召回都用它） | 第三方 | 不校验：1.5.1 的 `description` 是中英混写的路由描述，与 `description_zh` 不同，上传和解析都没有报错；是否改为同值待 Tealun 决定（`docs/88_planning/release-gate-20261105.md` D1） |
| 付费资产的展示名只允许中英文、数字和 `-` `—`，不能含空格或特殊字符（免费时没有这个限制） | 第三方 | 不校验：dev-pdca 免费发布，这条不适用；当前 `display_name` 含空格，转付费前必须改，是否提前改待 Tealun 决定（同上 D2） |
| `agent_created: true` 建议填写，标记由 agent 创建，之后 `skill_manage` 才能修改 | 第三方 | 不填也不校验：dev-pdca 在仓库里维护，通过上传发布，不经平台 agent 修改 |
| 不要写 `allowed-tools`、`argument-hint`、`model`、`tools`、`disable-model-invocation`、`user-invocable`、`triggers`（写了不报错，但属于噪音） | 第三方 | 不校验：入口保留 `argument-hint`、`user-invocable`，与仓库内技能的字段保持一致；平台不报错 |
| `permissions`、`homepage`、`repository`、`tags` 等可选字段有就保留 | 第三方 | 不校验：没有使用 |
| 上传后的解析预览是只读的，改任何内容都要回到编辑态重新提交；改动（含文案）通常要重新过审 | 第三方 | 不校验：属于平台流程。审核期间不重新上传 |
