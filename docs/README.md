# 开发文档目录

> **最后更新**: 2026-02-12

---

## 📚 文档导航

### 🚀 快速开始

**新开发者**: 从 [开发指南](Development_Guide.md) 开始

**AI 开发者**: 从 [开发指南](Development_Guide.md) 开始，重点关注架构和函数文档

---

## 📋 文档列表

### 1. [开发指南](Development_Guide.md) ⭐ **入口文档**

**用途**: 所有文档的入口和导航中心

**内容**:
- 文档体系概述
- 快速开始指南
- 文档导航
- 开发流程
- 常见问题
- AI 开发指南

**适合**: 所有开发者（必读）

---

### 2. [CLI 入口文档](../../cli_app/docs/CLI_ENTRY.md) ⭐ **AI 深度读取指南**

**用途**: 为 AI 开发者提供 CLI 程序的深度理解指南

**内容**:
- 程序概述和快速定位
- 代码结构详解
- 数据流分析
- 核心模块深度解析
- 扩展指南
- 相关文档索引

**适合**: AI 开发者（必读，理解 CLI 程序）

**位置**: `cli_app/docs/CLI_ENTRY.md`

---

### 3. [GUI 入口文档](../../gui_app/docs/GUI_ENTRY.md) ⭐ **AI 深度读取指南**

**用途**: 为 AI 开发者提供 GUI 程序的深度理解指南

**内容**:
- 程序概述和快速定位
- 代码结构详解（MVC 架构）
- 数据流分析
- 核心模块深度解析
- 扩展指南
- 相关文档索引

**适合**: AI 开发者（必读，理解 GUI 程序）

**位置**: `gui_app/docs/GUI_ENTRY.md`

---

### 4. [CLI 需求文档](../../cli_app/docs/CLI_Requirements.md)

**用途**: 定义 CLI 程序的功能需求和非功能需求

**内容**:
- 项目概述
- 功能需求（FR-CLI-001 到 FR-CLI-012）
- 非功能需求（NFR-CLI-001 到 NFR-CLI-009）
- 约束条件
- 用户场景
- 需求优先级
- AI 开发者指南

**适合**: 项目负责人、开发者、AI 开发者

**位置**: `cli_app/docs/CLI_Requirements.md`

---

### 5. [GUI 需求文档](../../gui_app/docs/GUI_Requirements.md)

**用途**: 定义 GUI 程序的功能需求和非功能需求

**内容**:
- 项目概述
- 功能需求（FR-001 到 FR-022）
- 非功能需求（NFR-001 到 NFR-012）
- 约束条件
- 用户场景
- 需求优先级
- AI 开发者指南

**适合**: 项目负责人、开发者、AI 开发者

**位置**: `gui_app/docs/GUI_Requirements.md`

---

### 6. [开发流程文档](Development_Process.md)

**用途**: 定义开发、测试、文档更新流程

**内容**:
- 开发流程概述
- 开发阶段（需求分析 → 版本发布）
- 代码规范（PEP 8、文档字符串、注释）
- 文档更新流程
- 版本管理流程
- 测试流程
- 代码审查

**适合**: 开发者、AI 开发者

---

### 7. [架构设计文档](../../gui_app/docs/Architecture_Design.md) ⭐ **核心文档**

**用途**: 定义 GUI 系统架构和模块设计

**内容**:
- 架构概述
- 系统架构（目录结构、模块依赖）
- 模块设计（GUI、Controller、Models、Core）
- 数据流设计
- GUI 架构设计
- 数据结构设计
- 接口设计
- 技术选型

**适合**: 所有开发者（必读，特别是 AI 开发者）

**位置**: `gui_app/docs/Architecture_Design.md`

---

### 7.1 [核心解析器架构文档](core/architecture.md) ⭐ **核心文档**

**用途**: 详细说明核心解析器 `LSDynaParser` 的架构设计

**内容**:
- 项目目标
- 核心类设计
- 数据结构
- 处理流程
- 支持的关键字列表
- 扩展性设计

**适合**: 所有开发者（理解核心解析器）

**位置**: `docs/core/architecture.md`

---

### 7.2 [API 参考文档](core/api_reference.md) ⭐ **核心文档**

**用途**: 提供核心解析器 `LSDynaParser` 的 API 参考

**内容**:
- 核心类说明
- 主要方法说明（`__init__`, `parse`, `generate_markdown`）
- 内部辅助方法说明
- 参数说明
- 物理意义说明

**适合**: 所有开发者（开发时参考）

**位置**: `docs/core/api_reference.md`

---

### 8. [项目结构文档](Project_Structure.md) ⭐ **重要文档**

**用途**: 明确区分 CLI 和 GUI 两个程序，说明项目结构

**内容**:
- 双程序共存方案
- CLI 程序结构（命令行工具）
- GUI 程序结构（图形界面）
- 共享核心代码说明
- 目录结构详解
- 运行方式
- 开发指南

**适合**: 所有开发者（必读，了解项目结构）

---

### 9. [版本管理文档](Version_Management.md)

**用途**: 定义版本号规则和更新流程

**内容**:
- 版本号规则（语义化版本）
- 版本变更类型（MAJOR/MINOR/PATCH）
- 版本更新流程
- 版本历史
- 版本发布检查清单

**适合**: 所有开发者

---

### 10. [函数文档模板](Function_Documentation_Template.md) ⭐ **核心文档**

**用途**: 记录所有函数/类的详细说明

**内容**:
- 文档格式说明
- GUI 模块函数文档
- Controller 模块函数文档
- Models 模块函数文档
- Core 模块函数文档

**适合**: 所有开发者（必读，特别是 AI 开发者）

**注意**: 本文档是模板，需要根据实际代码逐步完善

---

### 11. [更新日志](UPDATE_LOG.md)

**用途**: 记录每次迭代的详细变更

**内容**:
- 版本变更记录（按版本倒序）
- 变更类型（Added/Changed/Fixed/Removed）
- 影响范围
- 升级说明

**适合**: 所有开发者

---

### 12. [GitHub 同步指南](Github_Sync_Guide.md)

**用途**: GitHub 同步脚本使用说明

**内容**:
- 如何使用 `Github_Sync.bat` 脚本
- 默认同步和自定义提交信息
- 脚本逻辑说明
- 常见问题解答

**适合**: 所有开发者

---

## 🗺️ 按角色导航

### 项目负责人

**必读**:
1. [开发指南](Development_Guide.md)
2. [架构设计文档](../../gui_app/docs/Architecture_Design.md)
3. [版本管理文档](Version_Management.md)
4. [更新日志](UPDATE_LOG.md)

### 开发者

**必读**:
1. [开发指南](Development_Guide.md)
2. [架构设计文档](../../gui_app/docs/Architecture_Design.md)
3. [开发流程文档](Development_Process.md)
4. [函数文档模板](Function_Documentation_Template.md)
5. [版本管理文档](Version_Management.md)

### AI 开发者

**必读**:
1. **CLI 程序开发**:
   - [CLI 入口文档](../../cli_app/docs/CLI_ENTRY.md) - **重点**，深度理解 CLI 程序
   - [CLI 需求文档](../../cli_app/docs/CLI_Requirements.md) - 了解 CLI 功能需求
   - [项目结构文档](Project_Structure.md) - 了解项目组织
   
2. **GUI 程序开发**:
   - [GUI 入口文档](../../gui_app/docs/GUI_ENTRY.md) - **重点**，深度理解 GUI 程序
   - [GUI 需求文档](../../gui_app/docs/GUI_Requirements.md) - 了解 GUI 功能需求
   - [架构设计文档](../../gui_app/docs/Architecture_Design.md) - **重点**，理解 GUI 架构
   
3. **通用文档**:
   - [开发指南](Development_Guide.md) - 了解工作流程
   - [函数文档模板](Function_Documentation_Template.md) - **重点**，理解函数接口
   - [开发流程文档](Development_Process.md) - 了解开发规范
   - [更新日志](UPDATE_LOG.md) - 了解最新变更

---

## 🗺️ 按任务导航

### 实现新功能

**CLI 程序**:
1. 阅读 [CLI 需求文档](../../cli_app/docs/CLI_Requirements.md) 确认需求
2. 阅读 [CLI 入口文档](../../cli_app/docs/CLI_ENTRY.md) 了解程序结构
3. 设计实现方案
4. 实现代码
5. 更新 [函数文档模板](Function_Documentation_Template.md)
6. 更新 [更新日志](UPDATE_LOG.md)
7. 更新版本号（[版本管理文档](Version_Management.md)）

**GUI 程序**:
1. 阅读 [GUI 需求文档](../../gui_app/docs/GUI_Requirements.md) 确认需求
2. 阅读 [GUI 入口文档](../../gui_app/docs/GUI_ENTRY.md) 和 [架构设计文档](../../gui_app/docs/Architecture_Design.md) 了解架构
3. 设计实现方案
4. 更新 [架构设计文档](../../gui_app/docs/Architecture_Design.md)（如架构变更）
5. 实现代码
6. 更新 [函数文档模板](Function_Documentation_Template.md)
7. 更新 [更新日志](UPDATE_LOG.md)
8. 更新版本号（[版本管理文档](Version_Management.md)）

### 修复 Bug

**步骤**:
1. 阅读 [函数文档模板](Function_Documentation_Template.md) 了解相关函数
2. 修复代码
3. 更新 [更新日志](UPDATE_LOG.md)
4. 更新版本号（[版本管理文档](Version_Management.md)）

### 添加新关键字支持

**步骤**:
1. 阅读 [核心解析器架构文档](core/architecture.md) 了解解析器架构
2. 阅读 [函数文档模板](Function_Documentation_Template.md) 了解解析器函数
3. 修改解析器代码
4. 更新文档生成器（如需要）
5. 更新 [函数文档模板](Function_Documentation_Template.md)
6. 更新 [更新日志](UPDATE_LOG.md)
7. 更新版本号（[版本管理文档](Version_Management.md)）

---

## 📝 文档更新规则

### 必须更新的情况

- **GUI 架构变更** → 更新 [架构设计文档](../../gui_app/docs/Architecture_Design.md)
- **核心解析器架构变更** → 更新 [核心解析器架构文档](core/architecture.md)
- **函数变更** → 更新 [函数文档模板](Function_Documentation_Template.md)
- **任何变更** → 更新 [更新日志](UPDATE_LOG.md)
- **版本变更** → 更新 [版本管理文档](Version_Management.md)

### 更新检查清单

每次开发迭代完成后，检查：

- [ ] [架构设计文档](../../gui_app/docs/Architecture_Design.md) 已更新（如 GUI 架构变更）
- [ ] [核心解析器架构文档](core/architecture.md) 已更新（如解析器架构变更）
- [ ] [函数文档模板](Function_Documentation_Template.md) 已更新（如函数变更）
- [ ] [更新日志](UPDATE_LOG.md) 已更新（所有变更）
- [ ] 版本号已更新（[版本管理文档](Version_Management.md)）
- [ ] 所有文档中的版本号一致

---

## 🔗 相关文档

### 用户文档

- `../user/User_Guide.md` - 用户使用指南（待创建）

### 项目文档

- `../../README.md` - 项目主 README
- `../../CHANGELOG_CLI.md` - CLI 程序变更日志
- `../../CHANGELOG_GUI.md` - GUI 程序变更日志
- [`core/architecture.md`](core/architecture.md) - 核心解析器架构文档
- [`core/api_reference.md`](core/api_reference.md) - API 参考文档
- `../../ls_dyna_md/docs/SUPPORTED_COMMANDS.md` - 支持的关键字列表（自动生成）

---

**文档结束**
