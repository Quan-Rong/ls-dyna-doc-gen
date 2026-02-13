# LS-Dyna Documentation Generator

> **项目版本**: 2.1.2  
> **最后更新**: 2026-02-13

一个用于自动解析 LS-Dyna 关键字文件（`.key`）并生成结构化 Markdown 文档的工具集。本项目包含两个独立的应用程序：**CLI（命令行）工具**和**GUI（图形界面）应用程序**。

---

## 📋 目录

1. [项目概述](#1-项目概述)
2. [两个程序](#2-两个程序)
3. [快速开始](#3-快速开始)
4. [项目结构](#4-项目结构)
5. [核心功能](#5-核心功能)
6. [AI 辅助开发](#6-ai-辅助开发)
7. [更新日志](#7-更新日志)

---

## 1. 项目概述

### 1.1 项目背景

LS-Dyna 是广泛应用于汽车碰撞仿真的有限元分析软件。在实际工程中，整车碰撞模型通常由多个子模型（`.key` 文件）组成，每个子模型可能只包含部分组件（如车门、保险杠等），并不包含完整的仿真设置。

### 1.2 项目目标

开发一套工具集，用于：
- 批量处理 LS-Dyna `.key` 文件
- 自动生成结构化的 Markdown 文档
- 提供模型内容检查清单，快速了解模型包含和不包含的内容
- 支持命令行和图形界面两种使用方式

### 1.3 目标用户

- **主要用户**: CAE 工程师、仿真分析人员
- **使用场景**: 批量文档生成、模型审查、自动化流程

---

## 2. 两个程序

本项目包含两个完全独立的应用程序，它们共享核心代码库但互不干扰：

### 2.1 CLI 程序（命令行工具）

**版本**: v1.2.0  
**入口文件**: `cli_app/main.py`  
**适用场景**: 批量处理、自动化脚本、服务器环境

**主要特性**:
- ✅ 批量处理多个 `.key` 文件
- ✅ 增量构建（智能跳过已处理文件）
- ✅ 命令行参数支持（`--force` 强制重新生成）
- ✅ 适合集成到自动化流程中

**运行方式**:
```bash
# 处理 Input/ 目录下的所有文件
python cli_app/main.py

# 处理指定文件
python cli_app/main.py Input/model.key

# 强制重新生成所有文件
python cli_app/main.py --force
```

**更新日志**: 参见 [CHANGELOG_CLI.md](CHANGELOG_CLI.md)

---

### 2.2 GUI 程序（图形界面）

**版本**: v2.1.1  
**入口文件**: `gui_app/main_gui.py`  
**适用场景**: 交互式使用、模型审查、实时预览

**主要特性**:
- ✅ 可视化文件管理（文件列表、选择、处理）
- ✅ 实时文档生成和预览
- ✅ 模型内容检查清单（快速了解模型包含的内容）
- ✅ 多标签页文档查看（详细文档、概览文档、AI 需求）
- ✅ 内置 LS-Dyna 命令参考
- ✅ 进度跟踪和状态显示

**运行方式**:
```bash
# 启动 GUI 应用程序
python gui_app/main_gui.py
```

**更新日志**: 参见 [CHANGELOG_GUI.md](CHANGELOG_GUI.md)

---

## 3. 快速开始

### 3.1 环境要求

- **Python**: 3.8 或更高版本
- **依赖包**:
  - CLI 程序：仅使用 Python 标准库（无需额外安装）
  - GUI 程序：需要 PyQt5（`pip install PyQt5`）

### 3.2 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone <repository-url>
   cd ls_dyna_md
   ```

2. **安装 GUI 依赖（仅 GUI 程序需要）**
   ```bash
   pip install PyQt5
   ```

3. **准备输入文件**
   - 将你的 `.key` 文件放入 `Input/` 目录

### 3.3 使用示例

**使用 CLI 程序**:
```bash
# 1. 将 .key 文件放入 Input/ 目录
# 2. 运行 CLI 程序
python cli_app/main.py

# 3. 查看生成的文档（在 Output/ 目录）
```

**使用 GUI 程序**:
```bash
# 1. 启动 GUI 应用程序
python gui_app/main_gui.py

# 2. 在界面中选择文件并处理
# 3. 实时查看生成的文档
```

---

## 4. 项目结构

```
ls_dyna_md/                          # 项目根目录
│
├── 📁 CLI 程序
│   ├── cli_app/
│   │   ├── main.py                  # CLI 入口点
│   │   ├── cli_main.py              # CLI 主逻辑
│   │   ├── docs/                    # CLI 相关文档
│   │   │   ├── CLI_Requirements.md
│   │   │   └── CLI_ENTRY.md
│   │   └── __init__.py
│   └── CHANGELOG_CLI.md             # CLI 更新日志
│
├── 📁 GUI 程序
│   ├── gui_app/
│   │   ├── main_gui.py              # GUI 入口点
│   │   ├── gui/                     # GUI 界面模块
│   │   │   ├── main_window.py
│   │   │   ├── file_list.py
│   │   │   ├── content_view.py
│   │   │   └── ...
│   │   ├── controller/              # 业务逻辑控制器
│   │   ├── models/                  # 数据模型
│   │   ├── logo/                    # GUI 资源文件
│   │   ├── docs/                    # GUI 相关文档
│   │   │   ├── GUI_Requirements.md
│   │   │   └── GUI_ENTRY.md
│   │   └── __init__.py
│   └── CHANGELOG_GUI.md             # GUI 更新日志
│
├── 📁 共享核心库
│   └── ls_dyna_md/                  # 核心功能包（两个程序共享）
│       ├── parser.py                # LS-Dyna 文件解析器
│       ├── writers/                 # 文档生成器
│       │   ├── detailed_writer.py   # 详细文档生成
│       │   ├── overview_writer.py    # 概览文档生成
│       │   ├── capability_writer.py  # 能力矩阵生成
│       │   └── requirements_writer.py # AI 需求生成
│       └── utils/                   # 工具函数
│           ├── descriptions.py      # 关键字描述
│           ├── engineering.py       # 工程意义分析
│           └── supported_commands.py # 支持的命令注册表
│
├── 📁 输入输出目录
│   ├── Input/                       # 输入文件目录（放置 .key 文件）
│   └── Output/                      # 输出文件目录（生成的文档）
│
├── 📁 文档目录
│   ├── docs/                        # 开发文档目录
│   │   ├── core/                    # 核心解析器文档
│   │   │   ├── architecture.md      # 核心解析器架构文档
│   │   │   └── api_reference.md     # API 参考文档
│   │   ├── Development_Guide.md     # 开发指南
│   │   ├── Project_Structure.md     # 项目结构文档
│   │   └── ...                      # 其他开发文档
│   └── ls_dyna_md/docs/             # 自动生成的文档
│       └── SUPPORTED_COMMANDS.md    # 支持的命令列表（自动生成）
│
├── README.md                        # 本文件（项目总说明）
├── CHANGELOG_CLI.md                 # CLI 程序更新日志
└── CHANGELOG_GUI.md                 # GUI 程序更新日志
```

### 4.1 目录说明

| 目录/文件 | 用途 | 所属程序 |
|----------|------|---------|
| `cli_app/` | CLI 程序主目录 | CLI |
| `cli_app/main.py` | CLI 程序入口点 | CLI |
| `gui_app/` | GUI 程序主目录 | GUI |
| `gui_app/main_gui.py` | GUI 程序入口点 | GUI |
| `ls_dyna_md/` | 核心功能包 | **共享** |
| `Input/` | 输入文件目录 | **共享** |
| `Output/` | 输出文件目录 | **共享** |
| `docs/` | 项目文档 | **共享** |

---

## 5. 核心功能

### 5.1 文档生成

两个程序都支持生成以下类型的文档：

1. **详细参考文档** (`*_docs.md`)
   - 结构化的 Markdown 文档
   - 包含表格：Parts、Materials、Sections 等
   - 元素数据样本和统计信息

2. **工程概览文档** (`*_overview.md`)
   - 高级工程摘要
   - 模型物理意义分析
   - 连接关系和初始条件总结

3. **AI 需求文档** (`*_AI_REQ.md`)
   - 当遇到不支持的关键字时自动生成
   - 包含代码片段和实现说明
   - 用于 AI 辅助开发

### 5.2 支持的关键字

系统支持 20+ 种 LS-Dyna 关键字类别，包括：
- `PART`, `PART_COMPOSITE`, `PART_CONTACT`
- `MAT_*` (各种材料类型)
- `SECTION_*` (各种截面类型)
- `ELEMENT_*` (各种单元类型)
- `CONTACT_*` (各种接触定义)
- `CONSTRAINED_*` (约束定义)
- `SET_*` (集合定义)
- `DAMPING_*` (阻尼定义)
- `DATABASE_*` (数据库输出控制)
- `INITIAL_*` (初始条件)
- 等等...

完整列表请参见 [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md)

---

## 6. AI 辅助开发

本项目包含专为 AI 辅助开发设计的架构特性：

### 6.1 能力自省（Capability Introspection）

系统维护一个实时的能力矩阵文档 [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md)，作为 AI 代理的**真实参考**，明确定义了当前支持哪些 LS-Dyna 关键字以及它们如何映射到内部数据结构。

### 6.2 自动化需求工程

当解析器遇到不支持的 LS-Dyna 关键字时，它会隔离特定的命令上下文并在 `Output/*_AI_REQ.md` 中生成正式的需求规范。

- **工件用途**: 这些文件作为 AI 开发者的结构化**任务规范**
- **工作流集成**: 这些工件的上下文可以直接被 AI 编码工具使用，生成必要的 `parser.py` 逻辑和 `detailed_writer.py` 文档方法
- **⚠️ 吞吐量注意**: 虽然代码片段已优化以提高效率，但包含许多未知命令的大型文件可能会生成大量上下文。在分析批量需求文件时，请确保你的 AI 环境（上下文窗口）和 API 吞吐量足够

---

## 7. 更新日志

- **CLI 程序更新日志**: [CHANGELOG_CLI.md](CHANGELOG_CLI.md)
- **GUI 程序更新日志**: [CHANGELOG_GUI.md](CHANGELOG_GUI.md)

---

## 📚 更多文档

- **核心解析器架构**: [`docs/core/architecture.md`](docs/core/architecture.md)
- **API 参考**: [`docs/core/api_reference.md`](docs/core/api_reference.md)
- **开发指南**: [`docs/Development_Guide.md`](docs/Development_Guide.md)
- **项目结构**: [`docs/Project_Structure.md`](docs/Project_Structure.md)
- **CLI 程序文档**: [`cli_app/docs/CLI_ENTRY.md`](cli_app/docs/CLI_ENTRY.md)
- **GUI 程序文档**: [`gui_app/docs/GUI_ENTRY.md`](gui_app/docs/GUI_ENTRY.md)

---

## 🤝 贡献

欢迎贡献代码和提出建议！请参考开发文档了解如何扩展功能。

---

**项目维护**: LS-Dyna Documentation Generator Team  
**最后更新**: 2026-02-12
