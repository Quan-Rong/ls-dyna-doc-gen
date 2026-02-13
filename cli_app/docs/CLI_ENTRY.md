# CLI 程序入口文档 - AI 深度读取指南

> **版本**: 1.0.0  
> **创建日期**: 2026-02-12  
> **最后更新**: 2026-02-12  
> **程序版本**: v1.1.0 (CLI)

---

## 🎯 文档目的

本文档为 **AI 开发者** 提供深度理解 CLI 程序所需的所有信息。阅读本文档后，AI 应该能够：

1. **理解程序功能**：知道 CLI 程序做什么
2. **理解代码结构**：知道代码如何组织
3. **理解数据流**：知道数据如何流动
4. **理解扩展点**：知道如何添加新功能
5. **找到相关文档**：知道去哪里查找详细信息

---

## 📋 目录

1. [程序概述](#1-程序概述)
2. [快速定位](#2-快速定位)
3. [代码结构详解](#3-代码结构详解)
4. [数据流分析](#4-数据流分析)
5. [核心模块深度解析](#5-核心模块深度解析)
6. [扩展指南](#6-扩展指南)
7. [相关文档索引](#7-相关文档索引)

---

## 1. 程序概述

### 1.1 程序是什么？

**CLI 程序**（命令行工具）是一个**批量文档生成工具**，用于：

- 解析 LS-Dyna `.key` 文件（有限元分析输入文件）
- 自动生成结构化的 Markdown 文档
- 支持批量处理多个文件
- 支持增量构建（跳过已处理的文件）

### 1.2 程序入口

**入口文件**: `cli_app/main.py`

```python
# cli_app/main.py 是入口点，实际逻辑在 cli_app/cli_main.py
from cli_app.cli_main import main

if __name__ == "__main__":
    main()
```

**运行方式**:
```bash
python cli_app/main.py                    # 处理 Input/ 目录下所有文件
python cli_app/main.py file.key           # 处理指定文件
python cli_app/main.py --force            # 强制重新生成所有文件
```

### 1.3 程序版本

- **当前版本**: v1.1.0
- **版本位置**: `ls_dyna_md/__init__.py` 中的 `__version__`

---

## 2. 快速定位

### 2.1 关键文件位置

| 文件/目录 | 路径 | 作用 |
|----------|------|------|
| **入口文件** | `cli_app/main.py` | CLI 程序入口点 |
| **业务逻辑** | `cli_app/cli_main.py` | CLI 主逻辑（文件处理、批量处理） |
| **核心解析器** | `ls_dyna_md/parser.py` | LS-Dyna 文件解析器 |
| **文档生成器** | `ls_dyna_md/writers/` | 各种文档生成器 |
| **工具函数** | `ls_dyna_md/utils/` | 关键字描述、工程含义等 |

### 2.2 程序目录结构

```
ls_dyna_md/                        # 项目根目录
│
├── cli_app/
│   ├── main.py                    # ← CLI 入口点（调用 cli_main）
│
├── cli_app/                       # ← CLI 程序目录
│   ├── __init__.py
│   └── cli_main.py                # ← CLI 业务逻辑
│       ├── ensure_io_dirs()      # 确保输入/输出目录存在
│       ├── process_file()        # 处理单个文件
│       └── main()                 # 主函数（批量处理）
│
├── ls_dyna_md/                    # ← 共享核心包（CLI 和 GUI 共用）
│   ├── __init__.py
│   ├── parser.py                   # 解析器（LSDynaParser）
│   ├── writers/                    # 文档生成器
│   │   ├── detailed_writer.py     # 详细文档生成器
│   │   ├── overview_writer.py     # 概览文档生成器
│   │   ├── capability_writer.py   # 能力矩阵生成器
│   │   └── requirements_writer.py # AI 需求生成器
│   └── utils/                      # 工具函数
│       ├── descriptions.py        # 关键字描述
│       ├── engineering.py         # 工程含义
│       └── supported_commands.py  # 支持的命令列表
│
├── Input/                         # 输入文件目录
├── Output/                        # 输出文件目录
└── docs/                          # 文档目录
```

---

## 3. 代码结构详解

### 3.1 CLI 程序模块 (`cli_app/cli_main.py`)

#### 3.1.1 `ensure_io_dirs()`

**功能**: 确保输入/输出目录存在

**逻辑**:
1. 获取项目根目录
2. 检查 `Input/`、`Output/`、`docs/` 目录
3. 如果不存在，自动创建
4. 返回目录路径

**关键代码**:
```python
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, INPUT_DIR)
```

#### 3.1.2 `process_file(filepath, output_base_dir)`

**功能**: 处理单个 `.key` 文件，生成文档

**数据流**:
```
输入文件 (filepath)
    ↓
LSDynaParser.parse() → 解析数据
    ↓
DetailedWriter.generate_markdown() → *_docs.md
    ↓
OverviewWriter.generate_overview() → *_overview.md
    ↓
RequirementsWriter.generate_requirements() → *_AI_REQ.md (如有未识别关键字)
```

**关键步骤**:
1. 创建 `LSDynaParser` 实例
2. 调用 `parser.parse()` 解析文件
3. 使用 `DetailedWriter` 生成详细文档
4. 使用 `OverviewWriter` 生成概览文档
5. 使用 `RequirementsWriter` 生成 AI 需求文档（如有未识别关键字）

**输出文件**:
- `{base_name}_docs.md` - 详细参考文档
- `{base_name}_overview.md` - 工程概览（包含检查清单）
- `{base_name}_AI_REQ.md` - AI 实现需求（如有未识别关键字）

#### 3.1.3 `main()`

**功能**: 主函数，批量处理文件

**处理流程**:
1. 打印程序标题和版本
2. 确保输入/输出目录存在
3. 生成能力矩阵文档 (`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`)
4. 解析命令行参数：
   - `--force`: 强制重新生成
   - 文件路径: 处理指定文件或目录
   - 无参数: 处理 `Input/` 目录下所有文件
5. 遍历文件列表：
   - 检查输出文件是否已存在（增量构建）
   - 如果不存在或 `--force`，调用 `process_file()`
6. 统计并打印处理结果

**关键逻辑**:
```python
# 增量构建：跳过已处理的文件
if os.path.exists(docs_path) and os.path.exists(overview_path) and not force_mode:
    print(f"⏩ Skipping {filename} (Output exists)")
    skipped_count += 1
    continue
```

---

## 4. 数据流分析

### 4.1 完整数据流

```
用户运行: python cli_app/main.py
    ↓
main() 函数启动
    ↓
ensure_io_dirs() → 创建 Input/Output/docs 目录
    ↓
CapabilityWriter.generate_doc() → 生成 ls_dyna_md/docs/SUPPORTED_COMMANDS.md
    ↓
扫描 Input/ 目录 → 获取 .key 文件列表
    ↓
遍历每个文件:
    ├─ 检查输出文件是否存在（增量构建）
    ├─ 如果不存在或 --force:
    │   ├─ process_file()
    │   │   ├─ LSDynaParser(filepath) → 创建解析器
    │   │   ├─ parser.parse() → 解析文件，填充数据结构
    │   │   ├─ DetailedWriter(parser) → 生成详细文档
    │   │   ├─ OverviewWriter(parser) → 生成概览文档
    │   │   └─ RequirementsWriter(parser) → 生成 AI 需求（如有）
    │   └─ 更新统计信息
    └─ 打印处理结果
```

### 4.2 解析器数据结构

**LSDynaParser** 解析后填充的数据结构（`parser.py`）:

```python
# 基本信息
self.title = "模型标题"
self.metadata = {}  # 元数据
self.header_comments = []  # 头部注释

# 实体数据
self.parts = []  # 部件列表
self.materials = []  # 材料列表
self.sections = []  # 截面列表
self.contacts = []  # 接触定义
self.sets = []  # 集合定义
self.constraints = []  # 约束定义
self.curves = []  # 曲线定义
self.nodes = []  # 节点范围
self.elements = defaultdict(list)  # 单元字典 {type: [element_data]}

# 统计信息
self.node_count = 0  # 节点总数
self.node_ranges = []  # 节点范围列表
self.keywords = {}  # 关键字计数
self.unknown_keywords = {}  # 未识别的关键字
```

### 4.3 文档生成流程

**DetailedWriter** (`ls_dyna_md/writers/detailed_writer.py`):
- 输入: `LSDynaParser` 实例（已解析）
- 输出: `{base_name}_docs.md`
- 内容: 详细的参数表格、部件列表、材料列表等

**OverviewWriter** (`ls_dyna_md/writers/overview_writer.py`):
- 输入: `LSDynaParser` 实例（已解析）
- 输出: `{base_name}_overview.md`
- 内容: 工程概览、检查清单、物理含义总结

**RequirementsWriter** (`ls_dyna_md/writers/requirements_writer.py`):
- 输入: `LSDynaParser` 实例（已解析，包含 `unknown_keywords`）
- 输出: `{base_name}_AI_REQ.md`（仅当有未识别关键字时）
- 内容: 未识别关键字的实现需求，供 AI 开发者实现

---

## 5. 核心模块深度解析

### 5.1 解析器 (`ls_dyna_md/parser.py`)

**类**: `LSDynaParser`

**核心方法**:
- `__init__(filepath)`: 初始化，设置文件路径
- `parse()`: 解析文件，填充数据结构

**解析逻辑**:
1. 逐行读取文件
2. 识别关键字（以 `*` 开头）
3. 根据关键字类型，调用相应的解析方法
4. 提取参数、实体数据
5. 统计关键字使用情况

**关键正则表达式**:
```python
self.re_keyword = re.compile(r'^\*([A-Za-z0-9_]+)(.*)')  # 匹配关键字
self.re_param = re.compile(r'^\s*[RI]\s+([A-Za-z0-9_]+)\s+([0-9\.\-\+eE]+)')  # 匹配参数
```

**扩展点**: 添加新关键字支持时，在 `parse()` 方法中添加相应的解析逻辑。

### 5.2 文档生成器 (`ls_dyna_md/writers/`)

#### 5.2.1 DetailedWriter

**功能**: 生成详细参考文档

**生成内容**:
- 模型基本信息
- 部件列表（表格）
- 材料列表（表格）
- 截面列表（表格）
- 接触定义
- 约束定义
- 其他关键字详情

**关键方法**:
- `generate_markdown(output_path)`: 生成 Markdown 文档

#### 5.2.2 OverviewWriter

**功能**: 生成工程概览文档

**生成内容**:
- 模型概览
- **检查清单**（9 大类分类）
- 物理含义总结
- 工程建议

**关键方法**:
- `generate_overview(output_path)`: 生成概览文档

#### 5.2.3 CapabilityWriter

**功能**: 生成能力矩阵文档

**生成内容**:
- 支持的关键字列表
- 关键字到数据结构的映射
- 关键字描述

**输出文件**: `ls_dyna_md/docs/SUPPORTED_COMMANDS.md`

**用途**: 为 AI 开发者提供"系统能做什么"的参考。

#### 5.2.4 RequirementsWriter

**功能**: 生成 AI 实现需求文档

**生成内容**:
- 未识别关键字的列表
- 关键字出现的行号
- 关键字上下文代码片段
- 实现建议

**输出文件**: `Output/{base_name}_AI_REQ.md`（仅当有未识别关键字时）

**用途**: 为 AI 开发者提供"系统不能做什么，需要实现什么"的任务清单。

### 5.3 工具函数 (`ls_dyna_md/utils/`)

#### 5.3.1 `descriptions.py`

**功能**: 提供关键字的描述文本

**数据结构**: 字典，键为关键字名，值为描述文本

#### 5.3.2 `engineering.py`

**功能**: 提供关键字的工程含义

**数据结构**: 字典，键为关键字名，值为工程含义文本

#### 5.3.3 `supported_commands.py`

**功能**: 定义支持的关键字列表和元数据

**数据结构**: 字典，包含关键字名称、类别、描述等

---

## 6. 扩展指南

### 6.1 添加新关键字支持

**步骤**:
1. 在 `ls_dyna_md/parser.py` 的 `parse()` 方法中添加关键字识别逻辑
2. 创建相应的数据结构存储解析结果
3. 在 `ls_dyna_md/utils/descriptions.py` 中添加描述
4. 在 `ls_dyna_md/utils/engineering.py` 中添加工程含义
5. 在 `ls_dyna_md/utils/supported_commands.py` 中注册关键字
6. 在 `ls_dyna_md/writers/detailed_writer.py` 中添加文档生成逻辑
7. 在 `ls_dyna_md/writers/overview_writer.py` 中添加概览生成逻辑

**参考文档**: 
- `ls_dyna_md/docs/SUPPORTED_COMMANDS.md` - 查看现有关键字的实现方式
- `Output/*_AI_REQ.md` - 查看未识别关键字的实现需求

### 6.2 修改 CLI 程序行为

**修改位置**: `cli_app/cli_main.py`

**常见修改**:
- 修改输入/输出目录: 修改 `INPUT_DIR`、`OUTPUT_DIR` 常量
- 修改文件过滤规则: 修改 `glob.glob()` 的模式
- 修改处理逻辑: 修改 `process_file()` 函数
- 添加新的命令行参数: 修改 `main()` 函数的参数解析逻辑

### 6.3 修改文档生成格式

**修改位置**: `ls_dyna_md/writers/` 目录下的相应文件

**常见修改**:
- 修改 Markdown 格式: 修改 `generate_markdown()` 或 `generate_overview()` 方法
- 添加新的文档类型: 创建新的 Writer 类
- 修改检查清单分类: 修改 `OverviewWriter` 中的分类逻辑

---

## 7. 相关文档索引

### 7.1 需求文档

- **CLI 需求文档**: [`CLI_Requirements.md`](CLI_Requirements.md)
  - CLI 程序的功能需求
  - 使用场景
  - 需求优先级

### 7.2 架构文档

- **项目结构文档**: [`Project_Structure.md`](Project_Structure.md)
  - 双程序共存方案
  - CLI 和 GUI 程序区分
  - 目录结构详解

- **核心解析器架构文档**: [`../../docs/core/architecture.md`](../../docs/core/architecture.md)
- **GUI 架构设计文档**: [`../../gui_app/docs/Architecture_Design.md`](../../gui_app/docs/Architecture_Design.md)（如需要了解 GUI 架构）
  - 系统架构（主要针对 GUI，但核心部分通用）
  - 模块设计
  - 数据流设计

### 7.3 开发文档

- **开发指南**: [`Development_Guide.md`](Development_Guide.md)
  - 开发流程
  - 代码规范
  - 文档更新规则

- **开发流程文档**: [`Development_Process.md`](Development_Process.md)
  - 开发阶段
  - 测试流程
  - 版本管理

### 7.4 核心功能文档

- **能力矩阵**: `ls_dyna_md/docs/SUPPORTED_COMMANDS.md`（自动生成）
  - 支持的关键字列表
  - 关键字到数据结构的映射

- **AI 需求文档**: `Output/*_AI_REQ.md`（自动生成，如有未识别关键字）
  - 未识别关键字的实现需求

### 7.5 其他文档

- **版本管理**: [`Version_Management.md`](Version_Management.md)
- **更新日志**: [`UPDATE_LOG.md`](UPDATE_LOG.md)
- **函数文档模板**: [`Function_Documentation_Template.md`](Function_Documentation_Template.md)

---

## 8. AI 开发者快速开始

### 8.1 理解程序

1. **阅读本文档**（当前文档）- 了解 CLI 程序整体结构
2. **阅读需求文档** - [`CLI_Requirements.md`](CLI_Requirements.md) - 了解程序要做什么
3. **阅读核心代码** - `cli_app/cli_main.py` 和 `ls_dyna_md/parser.py` - 了解实现细节

### 8.2 修改程序

1. **确定修改范围**:
   - CLI 程序行为 → 修改 `cli_app/cli_main.py`
   - 解析逻辑 → 修改 `ls_dyna_md/parser.py`
   - 文档生成 → 修改 `ls_dyna_md/writers/` 目录
   - 工具函数 → 修改 `ls_dyna_md/utils/` 目录

2. **参考现有实现**:
   - 查看 `ls_dyna_md/docs/SUPPORTED_COMMANDS.md` 了解现有关键字实现
   - 查看 `Output/*_AI_REQ.md` 了解未识别关键字的实现需求

3. **测试修改**:
   ```bash
   python cli_app/main.py Input/test.key
   ```

### 8.3 添加新功能

1. **理解需求**: 阅读 `CLI_Requirements.md`
2. **理解架构**: 阅读 [`../../docs/Project_Structure.md`](../../docs/Project_Structure.md) 和 [`../../docs/core/architecture.md`](../../docs/core/architecture.md)（核心解析器架构）
3. **理解现有实现**: 阅读相关代码文件
4. **实现功能**: 按照扩展指南添加代码
5. **测试功能**: 运行程序测试
6. **更新文档**: 更新相关文档

---

## 9. 关键信息总结

### 9.1 程序入口

- **文件**: `cli_app/main.py`
- **函数**: `cli_app.cli_main.main()`

### 9.2 核心流程

```
扫描文件 → 解析文件 → 生成文档 → 输出文件
```

### 9.3 关键模块

1. **CLI 逻辑**: `cli_app/cli_main.py`
2. **解析器**: `ls_dyna_md/parser.py`
3. **文档生成器**: `ls_dyna_md/writers/`
4. **工具函数**: `ls_dyna_md/utils/`

### 9.4 输出文件

- `Output/{base_name}_docs.md` - 详细文档
- `Output/{base_name}_overview.md` - 概览文档
- `Output/{base_name}_AI_REQ.md` - AI 需求（如有）
- `ls_dyna_md/docs/SUPPORTED_COMMANDS.md` - 能力矩阵

---

**文档结束**

> **提示**: 本文档是 AI 开发者的入口文档。如需深入了解某个模块，请参考"相关文档索引"部分列出的文档。
