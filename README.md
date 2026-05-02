# Talk Agent - 智能对话Agent系统

一个基于Python的智能对话Agent系统，支持对话管理、任务执行和交互式对话功能。

## 项目概述

Talk Agent是一个模块化的对话Agent系统，旨在提供智能对话交互、对话管理和任务执行功能。该系统采用清晰的架构设计，易于扩展和维护。

## 功能特性

### 核心功能
- **智能对话交互**：与用户进行自然语言对话
- **对话管理**：保存、加载、搜索和删除对话记录
- **任务执行**：创建和执行各种异步任务
- **命令行界面**：通过命令行操作和管理
- **交互模式**：支持交互式对话体验

### 技术特点
- 模块化设计，易于扩展
- 支持异步操作
- 对话历史持久化存储
- 完整的测试覆盖
- 清晰的代码结构和文档

## 项目结构

```
agent_project/
├── src/
│   ├── agent/           # Agent核心模块
│   │   └── agent.py
│   ├── dialogue/        # 对话管理模块
│   │   └── dialogue_manager.py
│   ├── tasks/          # 任务执行模块
│   │   └── task_executor.py
│   └── utils/          # 工具函数模块
│       └── utils.py
├── tests/              # 测试文件
│   ├── test_agent.py
│   ├── test_dialogue_manager.py
│   └── test_task_executor.py
├── main.py             # 主入口文件
└── requirements.txt    # 依赖文件
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

### 命令行使用

```bash
# 列出对话
python main.py dialogue list

# 加载对话
python main.py dialogue load <dialogue_id>

# 搜索对话
python main.py dialogue search <keyword>

# 删除对话
python main.py dialogue delete <dialogue_id>

# 列出任务
python main.py task list

# 交互模式
python main.py interactive
```

## 使用示例

### 交互模式

```bash
python main.py interactive
```

在交互模式下，您可以：

```
=== Agent交互模式 ===
输入 'exit' 退出，输入 'help' 查看帮助

您: 你好
助手: 你好！我是AssistantAgent，有什么可以帮助您的吗？

您: 保存对话
对话已保存，ID: dialogue_20240502_213000

您: exit
```

### 对话管理

```bash
# 列出所有对话
python main.py dialogue list

# 加载特定对话
python main.py dialogue load dialogue_20240502_213000
```

### 任务执行

```bash
# 列出所有任务
python main.py task list
```

## 开发指南

### 运行测试

```bash
pytest tests/
```

### 代码规范

项目使用以下工具进行代码质量检查：
- Black: 代码格式化
- Flake8: 代码风格检查

```bash
# 格式化代码
black src/ tests/

# 检查代码风格
flake8 src/ tests/
```

## 贡献指南

欢迎 contributions！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目作者：luyanqiang
- 邮箱：xyy010830@gmail.com
- GitHub：https://github.com/Luyanqing666/talk_agent

## 致谢

感谢所有为这个项目做出贡献的开发者！

## 更新日志

### v1.0.0 (2026-04-12)
- 初始版本发布
- 实现基本Agent功能
- 添加对话管理模块
- 添加任务执行模块
- 完整的测试覆盖

## 未来计划

- [ ] 集成更复杂的NLP模型
- [ ] 添加Web界面
- [ ] 支持更多任务类型
- [ ] 改进对话管理功能
- [ ] 添加用户认证系统

---

*由 Talk Agent 团队开发*
