# LS-Dyna 模型分析工具 - 架构设计文档

> **版本**: 2.0.0  
> **创建日期**: 2026-02-12  
> **最后更新**: 2026-02-12  
> **文档状态**: 初始版本

---

## 📋 目录

1. [架构概述](#1-架构概述)
2. [系统架构](#2-系统架构)
3. [模块设计](#3-模块设计)
4. [数据流设计](#4-数据流设计)
5. [GUI 架构设计](#5-gui-架构设计)
6. [数据结构设计](#6-数据结构设计)
7. [接口设计](#7-接口设计)
8. [技术选型](#8-技术选型)
9. [更新记录](#9-更新记录)

---

## 1. 架构概述

### 1.1 设计目标

1. **模块化**: 清晰的模块划分，便于维护和扩展
2. **可扩展**: 易于添加新功能和关键字支持
3. **可维护**: 完整的文档，便于 AI 和人类开发者理解
4. **程序分离**: GUI 程序与 CLI 程序完全分离，互不干扰
5. **共享核心**: 两个程序共享 `ls_dyna_md/` 核心包

> **注意**: 本项目包含两个独立的程序：
> - **CLI 程序**（命令行工具）：入口 `cli_app/main.py`，版本 v1.2.0
> - **GUI 程序**（图形界面）：入口 `gui_app/main_gui.py`，版本 v2.0.0
> 
> 详细的项目结构说明请参考：[项目结构文档](Project_Structure.md)

### 1.2 架构原则

1. **分离关注点**: 解析、文档生成、GUI 分离
2. **单一职责**: 每个模块/类只负责一个功能
3. **依赖注入**: 减少模块间耦合
4. **接口抽象**: 定义清晰的接口，便于测试和扩展

### 1.3 架构层次

```
┌─────────────────────────────────────┐
│         GUI 层 (Presentation)        │
│  - 文件管理界面                       │
│  - 内容显示界面                       │
│  - 操作控制界面                       │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     业务逻辑层 (Business Logic)       │
│  - 文件处理控制器                     │
│  - 文档生成控制器                     │
│  - 检查清单生成器                     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      核心功能层 (Core Function)       │
│  - 解析器 (Parser)                   │
│  - 文档生成器 (Writers)              │
│  - 工具函数 (Utils)                  │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│        数据层 (Data Layer)           │
│  - 关键字定义                         │
│  - 配置数据                           │
└─────────────────────────────────────┘
```

---

## 2. 系统架构

### 2.1 目录结构

> **重要**: 以下结构仅显示 **GUI 程序** 的目录。CLI 程序位于 `cli_app/` 目录（`cli_app/main.py`）。
> 完整项目结构请参考：[项目结构文档](Project_Structure.md)

```
ls_dyna_md/                        # 项目根目录
│
├── 📁 CLI 程序（命令行工具，现有程序）
│   ├── cli_app/
│   │   └── main.py                # CLI 入口点
│   └── (其他 CLI 相关文件)
│
├── 📁 GUI 程序（图形界面，新开发）
│   └── gui_app/                   # GUI 程序主目录
│       ├── __init__.py
│       ├── main_gui.py            # GUI 入口点
│       ├── config.py               # GUI 配置文件
│       │
│       ├── gui/                   # GUI 界面模块
│       │   ├── __init__.py
│       │   ├── main_window.py     # 主窗口
│       │   ├── file_list.py       # 文件列表组件
│       │   ├── content_view.py    # 内容显示组件
│       │   ├── checklist_view.py  # 检查清单视图
│       │   ├── document_view.py   # 文档查看视图
│       │   └── progress_dialog.py # 进度对话框
│       │
│       ├── controller/            # 业务逻辑控制器
│       │   ├── __init__.py
│       │   ├── file_controller.py        # 文件处理控制器
│       │   ├── document_controller.py    # 文档生成控制器
│       │   └── checklist_controller.py   # 检查清单控制器
│       │
│       └── models/                # 数据模型
│           ├── __init__.py
│           ├── file_model.py      # 文件数据模型
│           ├── document_model.py  # 文档数据模型
│           └── checklist_model.py # 检查清单数据模型
│
├── 📁 共享核心代码
│   └── ls_dyna_md/                # 核心包（CLI 和 GUI 共享）
│       ├── __init__.py
│       ├── parser.py              # 解析器
│       ├── writers/               # 文档生成器
│       │   ├── __init__.py
│       │   ├── detailed_writer.py
│       │   ├── overview_writer.py
│       │   ├── capability_writer.py
│       │   └── requirements_writer.py
│       └── utils/                 # 工具函数
│           ├── __init__.py
│           ├── descriptions.py
│           ├── engineering.py
│           └── supported_commands.py
│
└── docs/                          # 文档目录
    ├── development/               # 开发文档
    │   ├── Requirements.md
    │   ├── Development_Process.md
    │   ├── Architecture_Design.md # 本文档（GUI 架构设计）
    │   ├── Project_Structure.md   # 项目结构文档
    │   ├── Version_Management.md
    │   ├── Function_Documentation_Template.md
    │   └── UPDATE_LOG.md
    └── user/                      # 用户文档
        └── User_Guide.md
```

### 2.2 模块依赖关系

**GUI 程序模块依赖**：

```
gui_app/
  ├── gui/
  │   ├── main_window.py
  │   │   ├── → controller/file_controller.py
  │   │   ├── → controller/document_controller.py
  │   │   └── → models/file_model.py
  │   │
  │   ├── file_list.py
  │   │   └── → models/file_model.py
  │   │
  │   ├── content_view.py
  │   │   ├── → checklist_view.py
  │   │   ├── → document_view.py
  │   │   └── → models/document_model.py
  │   │
  │   └── checklist_view.py
  │       └── → models/checklist_model.py
  │
  ├── controller/
  │   ├── file_controller.py
  │   │   ├── → ls_dyna_md.parser (共享核心)
  │   │   └── → models/file_model.py
  │   │
  │   ├── document_controller.py
  │   │   ├── → ls_dyna_md.writers.* (共享核心)
  │   │   └── → models/document_model.py
  │   │
  │   └── checklist_controller.py
  │       ├── → ls_dyna_md.parser (共享核心)
  │       └── → models/checklist_model.py
  │
  └── models/
      └── (数据模型，独立于核心)
```

**共享核心包** (`ls_dyna_md/`)：
- 被 CLI 程序（`cli_app/main.py`）使用
- 被 GUI 程序（`gui_app/`）使用
- 两个程序通过 `from ls_dyna_md import ...` 导入

---

## 3. 模块设计

### 3.1 GUI 模块

#### 3.1.1 MainWindow (主窗口)

**文件**: `gui_app/gui/main_window.py`

**职责**:
- 管理整个应用程序窗口
- 协调各个子组件
- 处理用户操作事件

**主要方法**:
- `__init__()`: 初始化窗口和组件
- `setup_ui()`: 设置界面布局
- `on_file_selected()`: 处理文件选择事件
- `on_process_clicked()`: 处理处理按钮点击
- `on_file_list_changed()`: 处理文件列表变化

**依赖**:
- `file_list.py`: 文件列表组件
- `content_view.py`: 内容显示组件
- `file_controller.py`: 文件处理控制器

#### 3.1.2 FileList (文件列表)

**文件**: `gui_app/gui/file_list.py`

**职责**:
- 显示文件列表
- 处理文件选择
- 显示文件状态

**主要方法**:
- `add_file()`: 添加文件到列表
- `remove_file()`: 从列表移除文件
- `get_selected_files()`: 获取选中的文件
- `update_file_status()`: 更新文件状态

**数据模型**: `FileModel`

#### 3.1.3 ContentView (内容显示)

**文件**: `gui_app/gui/content_view.py`

**职责**:
- 管理多个标签页
- 切换不同视图
- 显示文档内容

**主要方法**:
- `show_checklist()`: 显示检查清单视图
- `show_document()`: 显示文档视图
- `show_detail_tabs()`: 显示详细内容标签页
- `update_content()`: 更新内容

**子组件**:
- `ChecklistView`: 检查清单视图
- `DocumentView`: 文档查看视图

#### 3.1.4 ChecklistView (检查清单视图)

**文件**: `gui_app/gui/checklist_view.py`

**职责**:
- 显示检查清单
- 按类别分组显示
- 支持展开/折叠

**主要方法**:
- `render_checklist()`: 渲染检查清单
- `expand_category()`: 展开类别
- `collapse_category()`: 折叠类别

**数据模型**: `ChecklistModel`

#### 3.1.5 DocumentView (文档查看视图)

**文件**: `gui/document_view.py`

**职责**:
- 显示 Markdown 文档
- 支持搜索
- 支持滚动

**主要方法**:
- `load_document()`: 加载文档
- `search_text()`: 搜索文本
- `render_markdown()`: 渲染 Markdown

### 3.2 Controller 模块

#### 3.2.1 FileController (文件处理控制器)

**文件**: `controller/file_controller.py`

**职责**:
- 管理文件处理流程
- 调用解析器
- 管理处理状态

**主要方法**:
- `process_file()`: 处理单个文件
- `process_files()`: 批量处理文件
- `check_file_status()`: 检查文件状态
- `get_file_info()`: 获取文件信息

**依赖**:
- `core/parser.py`: 解析器
- `models/file_model.py`: 文件模型

#### 3.2.2 DocumentController (文档生成控制器)

**文件**: `controller/document_controller.py`

**职责**:
- 管理文档生成流程
- 调用文档生成器
- 管理输出文件

**主要方法**:
- `generate_documents()`: 生成所有文档
- `generate_detailed_doc()`: 生成详细文档
- `generate_overview_doc()`: 生成概览文档
- `generate_capability_doc()`: 生成能力矩阵

**依赖**:
- `core/writers/*.py`: 文档生成器
- `models/document_model.py`: 文档模型

#### 3.2.3 ChecklistController (检查清单控制器)

**文件**: `controller/checklist_controller.py`

**职责**:
- 生成检查清单数据
- 分类关键字
- 统计信息

**主要方法**:
- `generate_checklist()`: 生成检查清单
- `categorize_keywords()`: 分类关键字
- `count_keywords()`: 统计关键字数量

**依赖**:
- `core/parser.py`: 解析器
- `models/checklist_model.py`: 检查清单模型

### 3.3 Models 模块

#### 3.3.1 FileModel (文件模型)

**文件**: `models/file_model.py`

**职责**:
- 存储文件信息
- 管理文件状态

**属性**:
- `path`: 文件路径
- `name`: 文件名
- `size`: 文件大小
- `modified_time`: 修改时间
- `status`: 处理状态（未处理/已处理/处理中/错误）
- `output_files`: 输出文件列表

#### 3.3.2 DocumentModel (文档模型)

**文件**: `models/document_model.py`

**职责**:
- 存储文档内容
- 管理文档类型

**属性**:
- `file_path`: 源文件路径
- `doc_type`: 文档类型（docs/overview/capability/requirements）
- `content`: 文档内容
- `metadata`: 元数据（生成时间等）

#### 3.3.3 ChecklistModel (检查清单模型)

**文件**: `models/checklist_model.py`

**职责**:
- 存储检查清单数据
- 管理分类信息

**属性**:
- `categories`: 分类字典
  - 每个分类包含:
    - `name`: 分类名称
    - `keywords`: 关键字列表
    - `status`: 状态（包含/不包含）
    - `count`: 数量

### 3.4 Core 模块

**说明**: Core 模块复用原有 `ls_dyna_md` 包的代码，保持不变。

**主要模块**:
- `parser.py`: LS-Dyna 文件解析器
- `writers/`: 文档生成器
- `utils/`: 工具函数

---

## 4. 数据流设计

### 4.1 文件处理流程

```
用户选择文件
    ↓
FileModel 创建
    ↓
FileController.process_file()
    ↓
Parser.parse() → 解析数据
    ↓
DocumentController.generate_documents()
    ↓
Writers 生成文档
    ↓
DocumentModel 更新
    ↓
ChecklistController.generate_checklist()
    ↓
ChecklistModel 更新
    ↓
GUI 更新显示
```

### 4.2 检查清单生成流程

```
解析数据 (Parser)
    ↓
关键字列表 (keywords)
    ↓
ChecklistController.categorize_keywords()
    ↓
按 9 大类分类
    ↓
统计每个关键字数量
    ↓
生成 ChecklistModel
    ↓
ChecklistView 渲染显示
```

### 4.3 文档生成流程

```
解析数据 (Parser)
    ↓
DocumentController.generate_documents()
    ↓
├── DetailedWriter → *_docs.md (空内容不显示)
├── OverviewWriter → *_overview.md (必须包含检查清单)
├── CapabilityWriter → SUPPORTED_COMMANDS.md
└── RequirementsWriter → *_AI_REQ.md (如有未识别关键字)
    ↓
DocumentModel 更新
    ↓
DocumentView 显示
```

---

## 5. GUI 架构设计

### 5.1 界面布局

```
┌─────────────────────────────────────────────────────────┐
│                   主窗口 (MainWindow)                     │
├──────────────┬──────────────────────────┬───────────────┤
│              │                          │               │
│  文件列表区   │     内容显示区            │   操作按钮区   │
│  (FileList)  │    (ContentView)         │  (可选)       │
│              │                          │               │
│  - 文件1     │  ┌────────────────────┐  │ [处理选中]    │
│  - 文件2     │  │ 检查清单视图        │  │ [处理所有]    │
│  - 文件3     │  │ (ChecklistView)    │  │ [强制处理]    │
│  ...         │  └────────────────────┘  │               │
│              │                          │               │
│              │  ┌────────────────────┐  │               │
│              │  │ 详细内容标签页      │  │               │
│              │  │ - 控制卡片         │  │               │
│              │  │ - 边界条件         │  │               │
│              │  │ - 材料            │  │               │
│              │  │ ...               │  │               │
│              │  └────────────────────┘  │               │
│              │                          │               │
│              │  ┌────────────────────┐  │               │
│              │  │ 文档查看           │  │               │
│              │  │ (DocumentView)     │  │               │
│              │  └────────────────────┘  │               │
│              │                          │               │
└──────────────┴──────────────────────────┴───────────────┘
```

### 5.2 组件交互

```
MainWindow
  ├── 监听 FileList 的选择事件
  │   └── 更新 ContentView 显示
  │
  ├── 监听处理按钮点击
  │   └── 调用 FileController
  │       └── 更新进度显示
  │
  └── 监听处理完成事件
      └── 刷新 ContentView
```

### 5.3 状态管理

**文件状态**:
- `PENDING`: 未处理
- `PROCESSING`: 处理中
- `COMPLETED`: 已完成
- `ERROR`: 处理失败

**UI 状态**:
- `IDLE`: 空闲
- `PROCESSING`: 处理中
- `READY`: 就绪（有内容可显示）

---

## 6. 数据结构设计

### 6.1 解析数据结构

**Parser 输出结构** (保持原有):
```python
{
    'parts': [...],           # 部件列表
    'sections': [...],        # 截面列表
    'materials': [...],       # 材料列表
    'elements': {...},        # 单元字典
    'keywords': Counter(...), # 关键字计数
    'node_count': int,        # 节点数
    'node_ranges': [...],     # 节点范围
    # ... 其他数据
}
```

### 6.2 检查清单数据结构

```python
{
    'categories': {
        'control': {
            'name': '控制与求解器设置',
            'keywords': [
                {
                    'name': '*CONTROL_TERMINATION',
                    'display_name': '终止条件',
                    'status': True,      # 包含
                    'count': 1           # 数量
                },
                {
                    'name': '*CONTROL_ENERGY',
                    'display_name': '能量控制',
                    'status': False,     # 不包含
                    'count': 0
                },
                # ...
            ]
        },
        'boundary': {...},
        # ... 其他 8 个类别
    },
    'statistics': {
        'total_categories': 9,
        'categories_with_content': 5,
        'total_keywords_checked': 45,
        'keywords_found': 12
    }
}
```

### 6.3 文件模型数据结构

```python
{
    'path': str,              # 文件路径
    'name': str,              # 文件名
    'size': int,              # 文件大小（字节）
    'modified_time': datetime,# 修改时间
    'status': str,            # 状态
    'output_files': {         # 输出文件
        'docs': str,          # *_docs.md 路径
        'overview': str,      # *_overview.md 路径
        'requirements': str   # *_AI_REQ.md 路径（可选）
    },
    'parse_data': dict        # 解析数据（可选，缓存）
}
```

---

## 7. 接口设计

### 7.1 Parser 接口

**保持原有接口不变**:
```python
class LSDynaParser:
    def parse(self, file_path: str) -> dict:
        """解析文件，返回解析数据"""
        pass
```

### 7.2 Writer 接口

**保持原有接口不变**:
```python
class DetailedWriter:
    def write(self, parse_data: dict, output_path: str) -> None:
        """生成详细文档"""
        pass

class OverviewWriter:
    def write(self, parse_data: dict, output_path: str) -> None:
        """生成概览文档（包含检查清单）"""
        pass
```

### 7.3 Controller 接口

```python
class FileController:
    def process_file(self, file_path: str, force: bool = False) -> FileModel:
        """处理单个文件"""
        pass
    
    def process_files(self, file_paths: List[str], force: bool = False) -> List[FileModel]:
        """批量处理文件"""
        pass

class DocumentController:
    def generate_documents(self, parse_data: dict, base_path: str) -> DocumentModel:
        """生成所有文档"""
        pass

class ChecklistController:
    def generate_checklist(self, parse_data: dict) -> ChecklistModel:
        """生成检查清单"""
        pass
```

---

## 8. 技术选型

### 8.1 GUI 框架

**选择**: PyQt5 或 PySide6

**理由**:
- 功能强大，界面美观
- 跨平台支持
- 丰富的组件库
- 良好的文档

**备选**: Tkinter (轻量级，但功能有限)

### 8.2 Markdown 渲染

**选择**: `markdown` + `PyQt5.QWebEngineView` 或 `markdown2` + HTML

**理由**:
- 支持完整的 Markdown 语法
- 可以自定义样式
- 支持代码高亮

### 8.3 其他依赖

- **无第三方依赖**: 尽量使用标准库
- **可选依赖**: 
  - `markdown`: Markdown 渲染
  - `PyQt5` 或 `PySide6`: GUI 框架

---

## 9. 更新记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| 2.0.0 | 2026-02-12 | 初始版本创建，定义新架构 | - |

---

**文档结束**
