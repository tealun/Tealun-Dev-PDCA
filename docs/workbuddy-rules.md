# WorkBuddy 上架规则对照表

`dev-pdca.zip` 上传 WorkBuddy 前要满足的全部已知规则，以及每条规则在本地由谁检查。新增规则时，先在这里加一行，再补校验；能校验的必须写进 `scripts/build_suite.py`，不能校验的写明原因。

来源：**实测** = 上传或审核实际报错过；**第三方** = [wb-skill-converter 的 workbuddy-schema.md](https://github.com/starve001/wb-skill-converter/blob/main/references/workbuddy-schema.md)，非官方文档。

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
| 排除 `__pycache__`、`.DS_Store`、`*.pyc` 等 | 第三方 | `EXCLUDE_PATTERNS` |
| 压缩包根目录直接放 `SKILL.md`，不要多套一层目录 | 第三方 | 不校验：实测内含 `dev-pdca/` 文件夹的包已解析通过；如被拒，改传 `dist/` 下的 `-flat.zip` |
| `name` 全平台唯一 | 第三方 | 不能本地校验：只有上传时平台才能判断 |
| `category` 建议填写 | 第三方 | 已填 `developer`，不强制校验 |
