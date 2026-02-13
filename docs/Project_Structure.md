# 项目结构设计 - 双程序共存方案

> **版本**: 1.0.0  
> **创建日期**: 2026-02-12  
> **文档状态**: 初始版本

---

## 📋 目录

1. [概述](#1-概述)
2. [目录结构](#2-目录结构)
3. [程序区分](#3-程序区分)
4. [共享代码](#4-共享代码)
5. [运行方式](#5-运行方式)
6. [开发指南](#6-开发指南)

---

## 1. 概述

本项目包含**两个独立的程序**，它们共享核心代码但完全分离：

1. **CLI 程序**（命令行工具）- 现有程序
2. **GUI 程序**（图形界面）- 新开发程序

### 1.1 设计原则

- ✅ **完全分离**：两个程序有独立的入口点和目录结构
- ✅ **共享核心**：共同使用 `ls_dyna_md/` 核心包
- ✅ **互不干扰**：修改一个程序不影响另一个
- ✅ **清晰命名**：目录和文件名明确区分两个程序

---

## 2. 目录结构

### 2.1 完整项目结构

```
ls-dyna-doc-gen/                      # 项目根目录
│
├── 📁 CLI 程序（命令行工具）
│   ├── cli_app/
│   │   ├── main.py                   # CLI 入口点
│   │   ├── cli_main.py               # CLI 业务逻辑
│   │   └── docs/                     # CLI 相关文档
│   └── CHANGELOG_CLI.md              # CLI 更新日志
│
├── 📁 GUI 程序（图形界面）
│   ├── gui_app/                      # GUI 程序主目录
│   │   ├── __init__.py
│   │   ├── main_gui.py               # GUI 入口点
│   │   ├── config.py                 # GUI 配置
│   │   │
│   │   ├── gui/                      # GUI 界面模块
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py        # 主窗口
│   │   │   ├── file_list.py          # 文件列表组件
│   │   │   ├── content_view.py       # 内容显示组件
│   │   │   ├── checklist_view.py     # 检查清单视图
│   │   │   ├── document_view.py      # 文档查看视图
│   │   │   └── progress_dialog.py    # 进度对话框
│   │   │
│   │   ├── controller/               # 业务逻辑控制器
│   │   │   ├── __init__.py
│   │   │   ├── file_controller.py    # 文件处理控制器
│   │   │   ├── document_controller.py # 文档生成控制器
│   │   │   └── checklist_controller.py # 检查清单控制器
│   │   │
│   │   └── models/                   # 数据模型
│   │       ├── __init__.py
│   │       ├── file_model.py         # 文件数据模型
│   │       ├── document_model.py     # 文档数据模型
│   │       └── checklist_model.py    # 检查清单数据模型
│   │
│   └── run_gui.py                    # GUI 启动脚本（可选，简化启动）
│
├── 📁 共享核心代码
│   └── ls_dyna_md/                   # 核心包（两个程序共享）
│       ├── __init__.py
│       ├── parser.py                 # 解析器
│       ├── writers/                  # 文档生成器
│       │   ├── __init__.py
│       │   ├── detailed_writer.py
│       │   ├── overview_writer.py
│       │   ├── capability_writer.py
│       │   └── requirements_writer.py
│       └── utils/                    # 工具函数
│           ├── __init__.py
│           ├── descriptions.py
│           ├── engineering.py
│           └── supported_commands.py
│
├── 📁 共享资源
│   ├── Input/                        # 输入文件目录（两个程序共享）
│   ├── Output/                       # 输出文件目录（两个程序共享）
│   └── docs/                         # 文档目录
│       ├── development/              # 开发文档
│       └── user/                     # 用户文档
│
├── README.md                         # 项目主 README
├── CHANGELOG_CLI.md                  # CLI 程序更新日志
└── CHANGELOG_GUI.md                  # GUI 程序更新日志
```

### 2.2 关键目录说明

| 目录/文件 | 用途 | 所属程序 |
|----------|------|---------|
| `cli_app/main.py` | CLI 程序入口 | CLI |
| `gui_app/` | GUI 程序主目录 | GUI |
| `gui_app/main_gui.py` | GUI 程序入口 | GUI |
| `ls_dyna_md/` | 核心功能包 | **共享** |
| `Input/` | 输入文件 | **共享** |
| `Output/` | 输出文件 | **共享** |

---

## 3. 程序区分

### 3.1 CLI 程序（命令行工具）

**标识特征**：
- ✅ 入口文件：`cli_app/main.py`
- ✅ 运行方式：`python cli_app/main.py`
- ✅ 版本：v1.2.0（现有程序）
- ✅ 功能：批量处理 `.key` 文件，生成文档

**目录结构**：
```
ls-dyna-doc-gen/
├── cli_app/                   # ← CLI 程序目录
│   ├── main.py                # ← CLI 入口
│   ├── cli_main.py            # ← CLI 业务逻辑
│   └── docs/                  # ← CLI 文档
└── ls_dyna_md/                # ← 使用共享核心
```

### 3.2 GUI 程序（图形界面）

**标识特征**：
- ✅ 入口文件：`gui_app/main_gui.py`
- ✅ 运行方式：`python gui_app/main_gui.py` 或 `python run_gui.py`
- ✅ 版本：v2.0.0（新程序）
- ✅ 功能：图形界面，文件管理，实时预览，检查清单

**目录结构**：
```
ls-dyna-doc-gen/
├── gui_app/                   # ← GUI 程序目录
│   ├── main_gui.py            # ← GUI 入口
│   ├── gui/                   # ← GUI 界面模块
│   ├── controller/            # ← 业务逻辑
│   └── models/                # ← 数据模型
└── ls_dyna_md/                # ← 使用共享核心
```

---

## 4. 共享代码

### 4.1 共享核心包：`ls_dyna_md/`

两个程序都使用 `ls_dyna_md/` 包中的核心功能：

- ✅ `ls_dyna_md.parser.LSDynaParser` - 解析器
- ✅ `ls_dyna_md.writers.*` - 文档生成器
- ✅ `ls_dyna_md.utils.*` - 工具函数

### 4.2 使用方式

**CLI 程序**（`cli_app/main.py`）：
```python
from ls_dyna_md import LSDynaParser, DetailedWriter, OverviewWriter
```

**GUI 程序**（`gui_app/main_gui.py`）：
```python
from ls_dyna_md import LSDynaParser, DetailedWriter, OverviewWriter
```

### 4.3 共享资源

- ✅ `Input/` - 输入文件目录（两个程序都可以读取）
- ✅ `Output/` - 输出文件目录（两个程序都可以写入）
- ✅ `docs/` - 文档目录（两个程序共享）

---

## 5. 运行方式

### 5.1 运行 CLI 程序

```bash
# 方式 1：直接运行
python cli_app/main.py

# 方式 2：处理指定文件
python cli_app/main.py Input/model.key

# 方式 3：强制重新生成
python cli_app/main.py --force
```

### 5.2 运行 GUI 程序

```bash
# 方式 1：直接运行入口文件
python gui_app/main_gui.py

# 方式 2：使用启动脚本（如果创建了 run_gui.py）
python run_gui.py
```

### 5.3 开发模式

**开发 CLI 程序**：
- 编辑 `cli_app/main.py` 和 CLI 相关文件
- 测试：`python cli_app/main.py`

**开发 GUI 程序**：
- 编辑 `gui_app/` 目录下的文件
- 测试：`python gui_app/main_gui.py`

---

## 6. 开发指南

### 6.1 添加新功能到 CLI 程序

1. 修改 `cli_app/main.py` 或 CLI 相关文件
2. 如需核心功能，修改 `ls_dyna_md/` 包
3. 测试：`python cli_app/main.py`

### 6.2 添加新功能到 GUI 程序

1. 修改 `gui_app/` 目录下的相应文件
   - GUI 界面 → `gui_app/gui/`
   - 业务逻辑 → `gui_app/controller/`
   - 数据模型 → `gui_app/models/`
2. 如需核心功能，修改 `ls_dyna_md/` 包
3. 测试：`python gui_app/main_gui.py`

### 6.3 修改共享核心代码

1. 修改 `ls_dyna_md/` 包中的文件
2. **同时测试两个程序**：
   - 测试 CLI：`python cli_app/main.py`
   - 测试 GUI：`python gui_app/main_gui.py`

### 6.4 文件命名规范

**CLI 程序文件**：
- 入口：`cli_app/main.py`
- 其他 CLI 文件：`cli_*.py` 或放在 `cli/` 目录（如果创建）

**GUI 程序文件**：
- 所有文件都在 `gui_app/` 目录下
- 入口：`gui_app/main_gui.py`
- GUI 模块：`gui_app/gui/*.py`
- 控制器：`gui_app/controller/*.py`
- 模型：`gui_app/models/*.py`

**共享核心文件**：
- 所有文件都在 `ls_dyna_md/` 包中

---

## 7. 版本管理

### 7.1 版本号规则

- **CLI 程序**：v1.x.x（现有程序，向后兼容）
- **GUI 程序**：v2.0.0+（新程序，独立版本）

### 7.2 版本标识

在代码中明确标识程序类型：

**CLI 程序**（`cli_app/main.py`）：
```python
print(f"LS-Dyna Documentation Generator v{__version__} (CLI)")
```

**GUI 程序**（`gui_app/main_gui.py`）：
```python
print(f"LS-Dyna Documentation Generator v{__version__} (GUI)")
```

---

## 8. 文档组织

### 8.1 文档位置

- **开发文档**：`docs/`（主目录）
- **用户文档**：`docs/user/`
- **GUI 架构文档**：`gui_app/docs/Architecture_Design.md`
- **核心解析器架构文档**：`docs/core/architecture.md`
- **项目结构文档**：本文档

### 8.2 文档更新

- 修改 CLI 程序 → 更新 CLI 相关文档
- 修改 GUI 程序 → 更新 GUI 相关文档（`gui_app/docs/Architecture_Design.md`）
- 修改核心代码 → 更新核心功能文档

---

## 9. 总结

### 9.1 关键点

1. ✅ **完全分离**：CLI 和 GUI 程序有独立的目录和入口
2. ✅ **共享核心**：两个程序都使用 `ls_dyna_md/` 包
3. ✅ **清晰命名**：目录结构明确区分两个程序
4. ✅ **互不干扰**：修改一个程序不影响另一个

### 9.2 快速识别

- **CLI 程序**：找 `cli_app/main.py`
- **GUI 程序**：找 `gui_app/` 目录
- **共享核心**：找 `ls_dyna_md/` 包

---

**文档结束**
