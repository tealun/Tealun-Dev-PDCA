# Support

如果你在使用 Tealun Dev PDCA 时遇到问题，请优先按下面的顺序排查。

## 先确认三件事

1. 你的 Agent 工具是否支持目录型 `SKILL.md` 技能包。
2. 你是否已经重新打开 Agent CLI 或新建会话。
3. 同步脚本是否把技能复制到了正确的 `skills` 目录。

可以先运行：

```bash
./sync-skills.sh --list-targets
```

Windows：

```powershell
.\sync-skills.ps1 --list-targets
```

## 提交问题时请附上

- 操作系统：Windows、macOS、Linux 或 WSL
- 使用的 Agent 工具及版本
- 运行过的同步命令
- 期望发生什么
- 实际发生什么
- 相关报错或截图

请不要提交 API key、账号令牌、私有仓库地址、客户数据或其他敏感信息。

## 适合提交 issue 的情况

- 同步脚本没有识别已安装工具
- 某个技能的触发说明不清楚
- 技能行为和文档描述不一致
- 文档安装步骤不完整

## 不适合提交 issue 的情况

- 某个 Agent 工具本身不支持 Agent Skills
- 私有项目代码需要排查
- 涉及账号、权限、账单或平台后台配置的问题

对于私有项目问题，建议只贴最小可复现描述，不要上传敏感文件。
