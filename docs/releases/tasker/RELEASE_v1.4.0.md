## Release Notes — Tasker v1.4.x

| | |
|---|---|
| **Skill** | `tasker` |
| **Version** | `v1.4.1` |
| **Type** | Refactor + additive hardening |
| **Compatibility** | Backward-compatible; no capability removed |

### 🎯 What's New (v1.3 → v1.4.1)

**v1.4.0 — 瘦身 + 去伪精确 + 降摩擦（-48% 行数，能力不减）**
- **去重**：Retry/Retreat cap、Tool-Call Audit、Depth Control 各自从散落三处收敛到单一权威定义。
- **去伪精确**：删除关键词加权算术评分（query=1/fix=5/delete=10），改为按风险意图的启发式判级（S 只读 / M 有界改动 / L 高爆炸半径·生产·不可逆）+ 升级因子。
- **去不可执行约束**：删除秒级步骤超时（60s/300s/900s），保留模型可真正计数的状态转换轮次上限（S≤4 / M≤8 / L≤15）与 execute 重试上限（3 次）。
- **降摩擦**：新增 Confirmation Policy —— S 级无副作用可直接执行 + 事后一句验收，确认门槛只留给 M/L 与有副作用任务。
- **解耦**：Multi-Agent Handoff 由硬编码技能名改为按能力匹配，仅在目标技能已安装时点名。
- **补范例**：新增一个 M 级完整 transcript（intake→close）。

**v1.4.1 — 净增量（全保留旧内容，+19 行）**
- **决策卡**：顶部 4 行速查（级别 / 门槛 / 输出 / 证据），无需扫全文即可定调。
- **反例区**：4 个对抗式违规示范（无工具调用即宣称完成、"我检查过了"式假验证、顺手越权、串行读取）。
- **可执行验证**：`validation_method` 必须是能跑的命令/测试/可观测结果，不接受"我检查过了"。
- **并行调用**：无依赖的读取/检查应在一次消息内并行发起。
- **可恢复性**：进度报告携带 `State | Level | done` 状态行，长对话被摘要后仍能续跑，不从头重来。
- **工具名锚点**：PTV 补真实工具示例（Read / Grep / Bash），并注明按环境实际提供。

### 📝 Changelog

- `v1.2.0` → `v1.3.0`：引入 Retreat/Retry 机制、时间预算、上下文修正评分、多代理交接、深度调节器、不满根因追踪。
- `v1.3.0` → `v1.4.0`：见上（结构性精简）。
- `v1.4.0` → `v1.4.1`：见上（增量硬化）。

---

*Tasker v1.4 — Do less to the doc, guarantee more in the doing.*
