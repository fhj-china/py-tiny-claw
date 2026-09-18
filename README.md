# py-tiny-claw

基于《AI智能体开发基础》教材实现的极简 Agent Harness 引擎（Python 版），
严格遵循教材的四层架构：

```
py-tiny-claw/
├── cmd/
│   └── claw/
│       └── main.py          # 入口：装配大脑、手脚，启动引擎
├── internal/
│   ├── engine/
│   │   └── loop.py          # 核心心脏：两阶段 ReAct 主循环（Thinking + Action）
│   ├── provider/
│   │   ├── interface.py     # LLMProvider 抽象接口
│   │   ├── openai.py        # OpenAI 格式适配器（对接智谱 GLM）
│   │   └── claude.py        # Claude 格式适配器（对接智谱 GLM）
│   ├── schema/
│   │   └── message.py       # 统一数据结构：Message / ToolCall / ToolResult ...
│   └── tools/
│       ├── registry.py      # 工具注册表：BaseTool / Registry / RegistryImpl
│       └── read_file.py     # 第一个物理工具：读取工作区文件
└── requirements.txt
```

## 快速开始

1. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 设置智谱 API Key（`https://open.bigmodel.cn` 控制台获取）：

   ```powershell
   # Windows PowerShell
   $env:ZHIPU_API_KEY="你的key"
   ```

3. 在项目根目录创建一个测试文件：

   ```powershell
   echo "Hello, py-tiny-claw 引擎！" > hello.txt
   ```

4. 运行：

   ```bash
   python -m cmd.claw.main
   ```

## 核心机制

- **ReAct 循环**：模型输出纯文本 -> 任务完成；输出 ToolCall -> 执行工具并追加观察结果，进入下一轮 Turn。
- **两阶段思考**：`enable_thinking=True` 时，每轮先剥夺工具强制模型规划（Phase 1），再恢复工具行动（Phase 2）。
- **Provider 同声传译**：Main Loop 只认识内部 `schema.Message`，厂商 SDK 差异被隔离在 provider 目录。
- **物理边界**：AgentEngine 锁定 `work_dir`，read_file 只能读取工作区内的文件。
