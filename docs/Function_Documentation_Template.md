# LS-Dyna 模型分析工具 - 函数文档

> **版本**: 1.0.0  
> **创建日期**: 2026-02-12  
> **最后更新**: 2026-02-12  
> **文档状态**: 初始版本

---

## 📋 目录

1. [文档说明](#1-文档说明)
2. [GUI 模块](#2-gui-模块)
3. [Controller 模块](#3-controller-模块)
4. [Models 模块](#4-models-模块)
5. [Core 模块](#5-core-模块)
6. [更新记录](#6-更新记录)

---

## 1. 文档说明

### 1.1 文档目的

本文档记录所有模块、类和函数的详细说明，便于：
- AI 程序理解代码功能
- 开发者快速定位功能
- 新成员快速上手

### 1.2 文档格式

每个函数/类按照以下格式记录：

```markdown
### 模块名.类名.函数名

**位置**: `path/to/file.py:行号`

**签名**: 
```python
def function_name(param1: type, param2: type) -> return_type:
```

**描述**: 
函数功能描述

**参数**:
- `param1` (type): 参数1描述
- `param2` (type): 参数2描述

**返回**:
- `return_type`: 返回值描述

**异常**:
- `ExceptionType`: 异常情况描述

**示例**:
```python
result = function_name("example", 123)
```

**相关函数**:
- `related_function()`: 相关函数说明
```

### 1.3 更新规则

- **新增函数**: 立即添加到文档
- **修改函数**: 更新文档中的签名和描述
- **删除函数**: 从文档中移除（保留历史记录）

---

## 2. GUI 模块

### 2.1 MainWindow

#### gui.main_window.MainWindow

**位置**: `gui/main_window.py:1`

**签名**: 
```python
class MainWindow(QMainWindow):
    def __init__(self):
```

**描述**: 
主窗口类，管理整个应用程序的界面和交互。

**属性**:
- `file_list` (FileList): 文件列表组件
- `content_view` (ContentView): 内容显示组件
- `file_controller` (FileController): 文件处理控制器
- `document_controller` (DocumentController): 文档生成控制器

**方法**:
- `setup_ui()`: 设置界面布局
- `on_file_selected()`: 处理文件选择事件
- `on_process_clicked()`: 处理处理按钮点击

**示例**:
```python
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
```

---

#### gui.main_window.MainWindow.setup_ui

**位置**: `gui/main_window.py:50`

**签名**: 
```python
def setup_ui(self) -> None:
```

**描述**: 
初始化并设置主窗口的界面布局，包括文件列表、内容显示区域和操作按钮。

**返回**:
- `None`

**示例**:
```python
window = MainWindow()
window.setup_ui()
```

---

#### gui.main_window.MainWindow.on_file_selected

**位置**: `gui/main_window.py:100`

**签名**: 
```python
def on_file_selected(self, file_path: str) -> None:
```

**描述**: 
处理文件选择事件，更新内容显示区域显示选中文件的信息。

**参数**:
- `file_path` (str): 选中的文件路径

**返回**:
- `None`

**示例**:
```python
window.on_file_selected("/path/to/file.key")
```

---

#### gui.main_window.MainWindow.on_process_clicked

**位置**: `gui/main_window.py:150`

**签名**: 
```python
def on_process_clicked(self, force: bool = False) -> None:
```

**描述**: 
处理处理按钮点击事件，开始处理选中的文件。

**参数**:
- `force` (bool): 是否强制重新处理（忽略已存在的输出文件）

**返回**:
- `None`

**示例**:
```python
window.on_process_clicked(force=True)
```

---

### 2.2 FileList

#### gui.file_list.FileList

**位置**: `gui/file_list.py:1`

**签名**: 
```python
class FileList(QWidget):
    def __init__(self, parent=None):
```

**描述**: 
文件列表组件，显示文件列表并处理文件选择。

**方法**:
- `add_file()`: 添加文件到列表
- `remove_file()`: 从列表移除文件
- `get_selected_files()`: 获取选中的文件

---

#### gui.file_list.FileList.add_file

**位置**: `gui/file_list.py:50`

**签名**: 
```python
def add_file(self, file_path: str) -> None:
```

**描述**: 
添加文件到文件列表。

**参数**:
- `file_path` (str): 文件路径

**返回**:
- `None`

**异常**:
- `FileNotFoundError`: 文件不存在

**示例**:
```python
file_list.add_file("/path/to/file.key")
```

---

#### gui.file_list.FileList.get_selected_files

**位置**: `gui/file_list.py:100`

**签名**: 
```python
def get_selected_files(self) -> List[str]:
```

**描述**: 
获取当前选中的文件列表。

**返回**:
- `List[str]`: 选中文件的路径列表

**示例**:
```python
selected = file_list.get_selected_files()
# ['/path/to/file1.key', '/path/to/file2.key']
```

---

### 2.3 ChecklistView

#### gui.checklist_view.ChecklistView

**位置**: `gui/checklist_view.py:1`

**签名**: 
```python
class ChecklistView(QWidget):
    def __init__(self, parent=None):
```

**描述**: 
检查清单视图组件，显示检查清单并按类别分组。

**方法**:
- `render_checklist()`: 渲染检查清单
- `expand_category()`: 展开类别
- `collapse_category()`: 折叠类别

---

#### gui.checklist_view.ChecklistView.render_checklist

**位置**: `gui/checklist_view.py:50`

**签名**: 
```python
def render_checklist(self, checklist_data: ChecklistModel) -> None:
```

**描述**: 
渲染检查清单数据，按类别分组显示。

**参数**:
- `checklist_data` (ChecklistModel): 检查清单数据模型

**返回**:
- `None`

**示例**:
```python
checklist_view.render_checklist(checklist_model)
```

---

## 3. Controller 模块

### 3.1 FileController

#### controller.file_controller.FileController

**位置**: `controller/file_controller.py:1`

**签名**: 
```python
class FileController:
    def __init__(self):
```

**描述**: 
文件处理控制器，管理文件处理流程。

**方法**:
- `process_file()`: 处理单个文件
- `process_files()`: 批量处理文件
- `check_file_status()`: 检查文件状态

---

#### controller.file_controller.FileController.process_file

**位置**: `controller/file_controller.py:50`

**签名**: 
```python
def process_file(self, file_path: str, force: bool = False) -> FileModel:
```

**描述**: 
处理单个文件，包括解析和文档生成。

**参数**:
- `file_path` (str): 文件路径
- `force` (bool): 是否强制重新处理

**返回**:
- `FileModel`: 文件模型对象

**异常**:
- `FileNotFoundError`: 文件不存在
- `ParseError`: 解析错误

**示例**:
```python
controller = FileController()
file_model = controller.process_file("/path/to/file.key", force=True)
```

---

#### controller.file_controller.FileController.process_files

**位置**: `controller/file_controller.py:100`

**签名**: 
```python
def process_files(self, file_paths: List[str], force: bool = False, 
                  progress_callback: Optional[Callable] = None) -> List[FileModel]:
```

**描述**: 
批量处理文件，支持进度回调。

**参数**:
- `file_paths` (List[str]): 文件路径列表
- `force` (bool): 是否强制重新处理
- `progress_callback` (Optional[Callable]): 进度回调函数 `(current: int, total: int) -> None`

**返回**:
- `List[FileModel]`: 文件模型列表

**示例**:
```python
def on_progress(current, total):
    print(f"Processing {current}/{total}")

files = controller.process_files(
    ["/path/to/file1.key", "/path/to/file2.key"],
    progress_callback=on_progress
)
```

---

### 3.2 DocumentController

#### controller.document_controller.DocumentController

**位置**: `controller/document_controller.py:1`

**签名**: 
```python
class DocumentController:
    def __init__(self):
```

**描述**: 
文档生成控制器，管理文档生成流程。

**方法**:
- `generate_documents()`: 生成所有文档
- `generate_detailed_doc()`: 生成详细文档
- `generate_overview_doc()`: 生成概览文档

---

#### controller.document_controller.DocumentController.generate_documents

**位置**: `controller/document_controller.py:50`

**签名**: 
```python
def generate_documents(self, parse_data: dict, base_path: str) -> DocumentModel:
```

**描述**: 
生成所有类型的文档（详细文档、概览文档、能力矩阵、需求文档）。

**参数**:
- `parse_data` (dict): 解析数据
- `base_path` (str): 输出文件的基础路径（不含扩展名）

**返回**:
- `DocumentModel`: 文档模型对象

**示例**:
```python
controller = DocumentController()
doc_model = controller.generate_documents(parse_data, "/output/file")
```

---

### 3.3 ChecklistController

#### controller.checklist_controller.ChecklistController

**位置**: `controller/checklist_controller.py:1`

**签名**: 
```python
class ChecklistController:
    def __init__(self):
```

**描述**: 
检查清单控制器，生成检查清单数据。

**方法**:
- `generate_checklist()`: 生成检查清单
- `categorize_keywords()`: 分类关键字
- `count_keywords()`: 统计关键字数量

---

#### controller.checklist_controller.ChecklistController.generate_checklist

**位置**: `controller/checklist_controller.py:50`

**签名**: 
```python
def generate_checklist(self, parse_data: dict) -> ChecklistModel:
```

**描述**: 
根据解析数据生成检查清单模型。

**参数**:
- `parse_data` (dict): 解析数据（包含 keywords Counter）

**返回**:
- `ChecklistModel`: 检查清单模型对象

**示例**:
```python
controller = ChecklistController()
checklist = controller.generate_checklist(parse_data)
```

---

#### controller.checklist_controller.ChecklistController.categorize_keywords

**位置**: `controller/checklist_controller.py:100`

**签名**: 
```python
def categorize_keywords(self, keywords: Counter) -> dict:
```

**描述**: 
将关键字按 9 大类分类。

**参数**:
- `keywords` (Counter): 关键字计数器

**返回**:
- `dict`: 分类字典，格式为 `{category_name: [keyword_list]}`

**示例**:
```python
from collections import Counter
keywords = Counter({'*CONTROL_TERMINATION': 1, '*MAT_ELASTIC': 5})
categories = controller.categorize_keywords(keywords)
```

---

## 4. Models 模块

### 4.1 FileModel

#### models.file_model.FileModel

**位置**: `models/file_model.py:1`

**签名**: 
```python
class FileModel:
    def __init__(self, path: str):
```

**描述**: 
文件数据模型，存储文件信息和状态。

**属性**:
- `path` (str): 文件路径
- `name` (str): 文件名
- `size` (int): 文件大小（字节）
- `modified_time` (datetime): 修改时间
- `status` (str): 处理状态（PENDING/PROCESSING/COMPLETED/ERROR）
- `output_files` (dict): 输出文件字典

**方法**:
- `update_status()`: 更新状态
- `get_output_path()`: 获取输出文件路径

---

#### models.file_model.FileModel.update_status

**位置**: `models/file_model.py:50`

**签名**: 
```python
def update_status(self, status: str) -> None:
```

**描述**: 
更新文件处理状态。

**参数**:
- `status` (str): 新状态（PENDING/PROCESSING/COMPLETED/ERROR）

**返回**:
- `None`

**示例**:
```python
file_model.update_status("PROCESSING")
```

---

### 4.2 ChecklistModel

#### models.checklist_model.ChecklistModel

**位置**: `models/checklist_model.py:1`

**签名**: 
```python
class ChecklistModel:
    def __init__(self):
```

**描述**: 
检查清单数据模型，存储检查清单数据。

**属性**:
- `categories` (dict): 分类字典
- `statistics` (dict): 统计信息

**方法**:
- `add_category()`: 添加分类
- `get_category()`: 获取分类
- `calculate_statistics()`: 计算统计信息

---

## 5. Core 模块

### 5.1 Parser

**说明**: Core 模块复用原有 `ls_dyna_md` 包的代码，函数文档参考原有文档或代码中的文档字符串。

**主要类**:
- `LSDynaParser`: LS-Dyna 文件解析器

**主要方法**:
- `parse()`: 解析文件

---

## 6. 更新记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| 1.0.0 | 2026-02-12 | 初始版本创建，定义文档模板 | - |

---

**文档结束**

**注意**: 本文档是模板文档。在实际开发过程中，需要根据实际实现的函数逐步完善本文档。
