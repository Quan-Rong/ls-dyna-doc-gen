# LS-Dyna Model Documentation Generator (dyn_to_md) Architecture

## 1. 项目目标

本项目 (`dyn_to_md.py`) 是一个用于 LS-Dyna 关键文件 (`.k` 或 `.dyn`) 的分析与文档自动化工具。
其核心目标是将复杂的 CAE 模型文件转化为结构化、可读性强的 Markdown 文档，供工程师审查模型结构、统计网格信息以及验证物理参数。

## 2. 核心类设计: `LSDynaParser`

整个系统的核心类，负责解析输入文件并管理模型数据。

### 2.1 依赖关系 & 模块

- **Include Parser**: 处理 `*INCLUDE` 和 `*INCLUDE_TRANSFORM`，构建完整的模型树。
- **Entity Storage**: 分类存储不同类型的 LS-Dyna 关键字（如 Materials, Sections, Parts, Contacts）。

### 2.2 数据结构 (Data Model)

- `self.includes`: 存储包含文件的列表 (filename, transform_id)。
- `self.materials`: 列表结构，每个元素包含 `type`, `title`, 开关参数等。
- `self.sections`: 列表结构，存储截面属性与 `SECID`。
- `self.elements`: 字典结构，按 `ELEMENT_TYPE` (Shell, Solid, Beam, Shell_Thickness, Seatbelt_Accelerometer 等) 分类统计数量及采样。
- `self.contacts`: 列表结构，存储接触定义、类型及 SSID/MSID 数据。
- `self.constraints`: 列表结构，存储刚体 (`CONSTRAINED_NODAL_RIGID_BODY`) 和关节 (`JOINT`)。
- `self.spotweld_constraints`: 列表结构，存储焊点插值约束 (`CONSTRAINED_INTERPOLATION_SPOTWELD`) 及其 PID/NSID/厚度/半径。
- `self.damping`: 列表结构，存储阻尼定义 (`DAMPING_PART_STIFFNESS` 等) 及其参数数据。
- `self.database_outputs`: 列表结构，存储数据库输出控制 (`DATABASE_CROSS_SECTION_PLANE_ID`, `DATABASE_HISTORY_NODE` 等)。
- `self.initial_conditions`: 列表结构，存储初始条件 (`INITIAL_AXIAL_FORCE_BEAM` 等)。
- `self.sets`: 列表结构，包含 SID 提取，支持 BEAM/SHELL/PART/NODE 各类集合。

## 3. 处理流程 (Pipeline)

1. **初始化**: `LSDynaParser(filename)` 读取主文件路径。
2. **解析 (parse)**:
   - 逐行读取文件。
   - 识别 `*KEYWORD` 块。
   - 根据关键字前缀 (如 `*MAT_`, `*SECTION_`, `*DAMPING_`, `*DATABASE_`, `*INITIAL_`) 分发到对应的处理逻辑。
   - 提取标题 (Title) 和关键参数 (PID, MID, SECID, ELFORM, SSID, MSID 等)。
3. **生成 (generate_markdown)**: 19 个章节
   - 1-4: 文件头、关键字摘要、元数据、装配树
   - 5-6: 网格统计、节点定义
   - 7-9: 部件、材料、截面
   - 10: 单元（Shell, Shell_Thickness, Solid, Beam, Beam_Orientation, Mass, Seatbelt_Accelerometer）
   - 11-13: 接触 (含 SSID/MSID)、约束 (含焊点插值)、集合
   - 14-15: 曲线、参数
   - 16-18: **阻尼定义、数据库输出控制、初始条件** (新增)
   - 19: 完整关键字统计

## 4. 支持的关键字列表 (Supported Keywords)

| 关键字前缀 | 解析方式 | 提取数据 |
|---|---|---|
| `*PART`, `*PART_COMPOSITE`, `*PART_CONTACT` | 专用解析 | PID, SECID, MID, Title |
| `*MAT_*` | 专用解析 | Material type, Properties |
| `*SECTION_*` | 专用解析 | Section type, Properties |
| `*ELEMENT_*` | 专用解析 | 计数, 采样, 格式说明 |
| `*CONTACT_*` | 专用解析 | SSID, MSID, Title |
| `*CONSTRAINED_*` | 专用解析 | Rigid Body/Joint/Spotweld 数据 |
| `*SET_*` | 专用解析 | SID, Title |
| `*DAMPING_*` | 专用解析 | 阻尼参数 |
| `*DATABASE_*` | 专用解析 | 输出控制数据 |
| `*INITIAL_*` | 专用解析 | 初始条件数据 |
| `*DEFINE_CURVE*` | 通用解析 | Title |
| `*INCLUDE*` | 专用解析 | 文件名, Transform ID |
| `*PARAMETER` | 专用解析 | 参数名/值 |

## 5. 扩展性设计 (Future Scope)

- **多文件递归解析**: 目前主要处理单文件，未来需支持递归读取 `*INCLUDE` 文件内容。
- **高级连接分析**: 自动识别 Spotweld 连接关系，生成连接矩阵。
- **定宽格式解析**: 支持 LS-Dyna 的 I10 定宽格式（当前仅支持空格分隔）。
