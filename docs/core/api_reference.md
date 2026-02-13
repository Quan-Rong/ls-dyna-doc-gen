# LS-Dyna Parser API Reference

## 核心类: `LSDynaParser`

负责从 `.k` 文件中提取关键信息并按照 CAE 使用习惯进行归类、统计和文档生成。

### 1. `__init__(self, filename)`

- **功能**: 初始化解析器，设定文件路径和内部数据结构。
- **参数**:
  - `filename`: 输入的 LS-Dyna 关键文件名 (str)。
- **物理意义**:
  - 准备数据容器，如 `materials`, `sections`, `parts` 列表。
  - 清空计数器 (node_count, element_count)。

### 2. `parse(self)`

- **功能**: 主解析循环，遍历整个文件行。
- **关键逻辑**:
  - **`*KEYWORD` 识别**: 扫描所有以 `*` 开头的行。
  - **前缀分发**: 匹配关键字前缀 (如 `*PART`, `*SECTION`, `*MAT`)，调用特定的数据提取逻辑。
  - **上下文管理**: 使用 `current_keyword` 和 `current_title` 维护解析状态。
- **物理意义**:
  - 将非结构化的文本流转化为结构化的 CAE 对象。
  - 处理 Title 行的特殊位置（关键字行下方）。

### 3. `generate_markdown(self, output_path)`

- **功能**: 生成最终的 Markdown 报告。
- **参数**:
  - `output_path`: 输出 Markdown 文件路径 (str)。
- **流程**:
  1. Header Info (文件名, 大小, 生成时间)。
  2. Table of Contents (自动生成章节索引)。
  3. 各模块详细报告 (调用 `_write_*` 系列辅助函数)。

---

## 内部辅助方法 (Internal Helpers)

### 4. `_write_mesh_statistics(self, md)`

- **功能**: 输出全模型的网格统计概览。
- **输出内容**:
  - 节点总数 (`node_count`)。
  - 单元总数 (Shell, Solid, Beam)。
  - 唯一 Part 数量。
  - 唯一 Material/Section ID 数量。
- **物理意义**:
  - 快速评估模型规模 (Model Size CHECK)。
  - 验证网格导入是否完整（例如节点数是否符合预期）。

### 5. `_write_constraints(self, md)`

- **功能**: 输出 `*CONSTRAINED` 相关定义。
- **重点支持**:
  - `JOINT`: 运动副 (Revolute, Spherical) -> 机构运动学。
  - `NODAL_RIGID_BODY`: 刚体定义 -> 部件刚性化处理。
  - `EXTRA_NODES`: 刚体附加节点。
- **物理意义**:
  - 检查多体动力学系统的构建是否正确。
  - 验证刚体和柔性体之间的连接关系。

### 6. `_write_includes(self, md)`

- **功能**: 输出 `*INCLUDE` 和 `*INCLUDE_TRANSFORM`列表。
- **关注点**:
  - `TRANSFORM` 关键字及其 ID 偏移量 (`IDOFF`, `IDTRAN`)。
- **物理意义**:
  - 检查子模型的装配树结构。
  - 确认坐标变换和 ID 偏移是否被激活，防止 ID 冲突。
