# LS-Dyna 模型分析工具 - 开发指南

> **版本**: 1.0.0  
> **创建日期**: 2026-02-12  
> **最后更新**: 2026-02-12  
> **文档状态**: 初始版本

---

## 📋 目录

1. [文档概述](#1-文档概述)
2. [快速开始](#2-快速开始)
3. [文档导航](#3-文档导航)
4. [开发流程](#4-开发流程)
5. [常见问题](#5-常见问题)
6. [AI 开发指南](#6-ai-开发指南)

---

## 1. 文档概述

### 1.1 文档体系

本项目建立了完整的开发文档体系，包括：

1. **需求文档** (`Requirements.md`)
   - 功能需求和非功能需求
   - 用户场景
   - 需求优先级

2. **开发流程文档** (`Development_Process.md`)
   - 开发阶段和流程
   - 代码规范
   - 文档更新流程
   - 测试流程

3. **GUI 架构设计文档** (`../../gui_app/docs/Architecture_Design.md`)
   - GUI 系统架构
   - GUI 模块设计
   - 数据流设计
   - GUI 架构设计
   
4. **核心解析器架构文档** (`core/architecture.md`)
   - 核心解析器架构
   - 解析器模块设计

5. **项目结构文档** (`Project_Structure.md`)
   - 双程序共存方案
   - CLI 和 GUI 程序区分
   - 共享核心代码说明
   - 目录结构详解

5. **版本管理文档** (`Version_Management.md`)
   - 版本号规则
   - 版本更新流程
   - 版本历史

6. **函数文档** (`Function_Documentation_Template.md`)
   - 所有函数/类的详细说明
   - 参数、返回值、示例

7. **更新日志** (`UPDATE_LOG.md`)
   - 每次迭代的详细变更记录

### 1.2 文档更新原则

**重要**: 每次开发迭代都必须更新相关文档！

**必须更新的文档**:
- GUI 架构变更 → 更新 `../../gui_app/docs/Architecture_Design.md`
- 核心解析器架构变更 → 更新 `core/architecture.md`
- 函数变更 → 更新 `Function_Documentation.md`
- 任何变更 → 更新 `UPDATE_LOG.md`
- 版本变更 → 更新 `Version_Management.md`

---

## 2. 快速开始

### 2.1 新开发者入门

**步骤**:
1. 阅读本文档（开发指南）
2. **重要**: 阅读 `Project_Structure.md` 了解项目结构（CLI 和 GUI 程序区分）
3. 阅读 `Requirements.md` 了解需求
4. 阅读 `../../gui_app/docs/Architecture_Design.md` 了解 GUI 架构
5. 阅读 `core/architecture.md` 了解核心解析器架构
6. 阅读 `Development_Process.md` 了解开发流程
6. 查看 `Function_Documentation_Template.md` 了解函数文档格式
7. 查看 `UPDATE_LOG.md` 了解历史变更

### 2.2 AI 开发者入门

**步骤**:
1. 阅读 `Requirements.md` 了解功能需求
2. 阅读 `../../gui_app/docs/Architecture_Design.md` 了解 GUI 系统架构
3. 阅读 `core/architecture.md` 了解核心解析器架构
4. 阅读 `Function_Documentation.md` 了解函数接口
4. 阅读 `Development_Process.md` 了解开发规范
5. 查看 `UPDATE_LOG.md` 了解最新变更

**关键信息**:
- 架构设计文档包含完整的模块结构和数据流
- 函数文档包含所有函数的详细说明
- 开发流程文档包含代码规范和文档更新规则

---

## 3. 文档导航

### 3.1 按角色导航

#### 3.1.1 项目负责人

**需要阅读**:
- `Requirements.md`: 了解需求
- `../../gui_app/docs/Architecture_Design.md`: 了解 GUI 架构
- `core/architecture.md`: 了解核心解析器架构
- `Version_Management.md`: 了解版本管理
- `UPDATE_LOG.md`: 了解变更历史

#### 3.1.2 开发者

**需要阅读**:
- `Requirements.md`: 了解需求
- `../../gui_app/docs/Architecture_Design.md`: 了解 GUI 架构
- `core/architecture.md`: 了解核心解析器架构
- `Development_Process.md`: 了解开发流程
- `Function_Documentation.md`: 了解函数接口
- `Version_Management.md`: 了解版本管理

#### 3.1.3 AI 开发者

**需要阅读**:
- `Requirements.md`: 了解需求
- `../../gui_app/docs/Architecture_Design.md`: 了解 GUI 架构（重点）
- `core/architecture.md`: 了解核心解析器架构（重点）
- `Function_Documentation.md`: 了解函数接口（重点）
- `Development_Process.md`: 了解开发规范
- `UPDATE_LOG.md`: 了解最新变更

### 3.2 按任务导航

#### 3.2.1 实现新功能

**步骤**:
1. 阅读 `Requirements.md` 确认需求
2. 阅读 `../../gui_app/docs/Architecture_Design.md` 了解 GUI 架构（或 `core/architecture.md` 了解核心解析器架构）
3. 设计实现方案
4. 更新相应的架构文档（如架构变更）
5. 实现代码
6. 更新 `Function_Documentation.md`
7. 更新 `UPDATE_LOG.md`
8. 更新版本号（`Version_Management.md`）

#### 3.2.2 修复 Bug

**步骤**:
1. 阅读 `Function_Documentation.md` 了解相关函数
2. 修复代码
3. 更新 `UPDATE_LOG.md`
4. 更新版本号（`Version_Management.md`）

#### 3.2.3 添加新关键字支持

**步骤**:
1. 阅读 `architecture.md` 了解核心解析器架构
2. 阅读 `Function_Documentation.md` 了解解析器函数
3. 修改解析器代码
4. 更新文档生成器（如需要）
5. 更新 `Function_Documentation.md`
6. 更新 `UPDATE_LOG.md`
7. 更新版本号（`Version_Management.md`）

---

## 4. 开发流程

### 4.1 标准开发流程

```
1. 需求分析
   ↓ 阅读 Requirements.md
   
2. 架构设计
   ↓ 阅读 GUI 架构文档 (../../gui_app/docs/Architecture_Design.md) 或核心解析器架构文档 (core/architecture.md)
   ↓ 设计实现方案
   ↓ 更新相应的架构文档（如需要）
   
3. 编码实现
   ↓ 遵循 Development_Process.md 中的代码规范
   ↓ 编写函数文档字符串
   
4. 测试
   ↓ 运行单元测试
   ↓ 运行集成测试
   
5. 文档更新
   ↓ 更新 GUI 架构文档 (../../gui_app/docs/Architecture_Design.md) 或核心解析器架构文档 (core/architecture.md)（如架构变更）
   ↓ 更新 Function_Documentation.md
   ↓ 更新 UPDATE_LOG.md
   ↓ 更新版本号（Version_Management.md）
   
6. 代码审查
   ↓ 检查代码质量
   ↓ 检查文档完整性
   
7. 版本发布
   ↓ 完成所有检查清单
   ↓ 提交代码和文档
```

### 4.2 文档更新检查清单

每次开发迭代完成后，检查：

- [ ] GUI 架构文档 (`../../gui_app/docs/Architecture_Design.md`) 或核心解析器架构文档 (`core/architecture.md`) 已更新（如架构变更）
- [ ] `Function_Documentation.md` 已更新（如函数变更）
- [ ] `UPDATE_LOG.md` 已更新（所有变更）
- [ ] 版本号已更新（`Version_Management.md`）
- [ ] 所有文档中的版本号一致

---

## 5. 常见问题

### 5.1 文档相关问题

**Q: 什么时候需要更新架构文档？**

A: 当有以下情况时：
- 新增模块/类
- 修改模块结构
- 修改数据流
- 修改接口设计

**Q: 什么时候需要更新函数文档？**

A: 当有以下情况时：
- 新增函数/类
- 修改函数签名
- 修改函数行为
- 修改函数参数/返回值

**Q: 版本号什么时候需要更新？**

A: 参考 `Version_Management.md`：
- 重大变更 → 主版本号 +1
- 新增功能 → 次版本号 +1
- Bug 修复 → 修订号 +1
- 仅文档更新 → 版本号不变（但要在更新日志中记录）

### 5.2 开发相关问题

**Q: 如何确定新功能的实现位置？**

A: 
1. 阅读 `../../gui_app/docs/Architecture_Design.md` 了解 GUI 模块职责
2. 根据功能类型选择对应模块：
   - GUI 功能 → `gui/` 模块
   - 业务逻辑 → `controller/` 模块
   - 数据模型 → `models/` 模块
   - 核心功能 → `ls_dyna_md/` 模块

**Q: 如何添加新关键字支持？**

A:
1. 阅读 `architecture.md` 了解核心解析器架构
2. 修改 `core/parser.py` 添加解析逻辑
3. 更新 `core/utils/supported_commands.py` 注册关键字
4. 更新 `core/utils/descriptions.py` 添加描述
5. 更新文档生成器（如需要）
6. 更新文档

**Q: 如何确保代码质量？**

A:
1. 遵循 `Development_Process.md` 中的代码规范
2. 编写完整的函数文档字符串
3. 编写单元测试
4. 运行代码检查工具（pylint, flake8）
5. 进行代码审查

---

## 6. AI 开发指南

### 6.1 AI 开发者工作流程

**步骤**:
1. **理解需求**
   - 阅读 `Requirements.md` 了解功能需求
   - 阅读 `UPDATE_LOG.md` 了解最新变更

2. **理解架构**
   - 阅读 `../../gui_app/docs/Architecture_Design.md` 了解 GUI 系统架构
   - 阅读 `architecture.md` 了解核心解析器架构
   - 理解模块职责和数据流

3. **定位功能**
   - 阅读 `Function_Documentation.md` 了解函数接口
   - 根据功能需求定位相关函数

4. **实现代码**
   - 遵循 `Development_Process.md` 中的代码规范
   - 编写完整的函数文档字符串
   - 保持代码风格一致

5. **更新文档**
   - 更新 GUI 架构文档 (`../../gui_app/docs/Architecture_Design.md`) 或核心解析器架构文档 (`core/architecture.md`)（如架构变更）
   - 更新 `Function_Documentation.md`（如函数变更）
   - 更新 `UPDATE_LOG.md`（所有变更）
   - 更新版本号（如需要）

### 6.2 AI 开发者注意事项

**重要原则**:
1. **文档先行**: 在实现代码前，先理解架构和需求
2. **文档同步**: 代码和文档同步更新，不滞后
3. **向后兼容**: 新功能不影响现有功能
4. **完整更新**: 所有相关文档都要更新

**关键文档**:
- `../../gui_app/docs/Architecture_Design.md`: GUI 系统架构（必须理解）
- `architecture.md`: 核心解析器架构（必须理解）
- `Function_Documentation.md`: 函数接口（必须理解）
- `Development_Process.md`: 开发规范（必须遵循）
- `UPDATE_LOG.md`: 变更历史（必须更新）

**常见错误**:
- ❌ 只更新代码，不更新文档
- ❌ 只更新部分文档，遗漏其他文档
- ❌ 不更新版本号
- ❌ 不遵循代码规范
- ❌ 不编写函数文档字符串

---

## 7. 文档维护

### 7.1 文档更新频率

- **每次开发迭代**: 必须更新相关文档
- **重大变更**: 立即更新所有相关文档
- **Bug 修复**: 更新 `UPDATE_LOG.md` 和版本号

### 7.2 文档质量检查

**检查项**:
- [ ] 文档结构清晰
- [ ] 内容准确完整
- [ ] 示例代码正确
- [ ] 版本号一致
- [ ] 更新记录完整

### 7.3 文档版本控制

- 所有文档使用 Git 版本控制
- 每次更新提交时，在提交信息中说明更新的文档
- 重要变更在文档中记录更新历史

---

## 8. 联系与支持

### 8.1 文档问题

如发现文档问题：
1. 检查 `UPDATE_LOG.md` 了解最新变更
2. 检查相关文档是否有更新
3. 如确认是文档错误，更新文档并记录在 `UPDATE_LOG.md` 中

### 8.2 开发问题

如遇到开发问题：
1. 查阅相关文档
2. 查看 `Function_Documentation.md` 了解函数接口
3. 查看 `UPDATE_LOG.md` 了解历史变更
4. 查看代码中的文档字符串

---

## 9. 附录

### 9.1 文档索引

| 文档 | 路径 | 用途 |
|------|------|------|
| 开发指南 | `Development_Guide.md` | 本文档，文档入口 |
| 需求文档 | `Requirements.md` | 功能需求和非功能需求 |
| 开发流程 | `Development_Process.md` | 开发流程和代码规范 |
| GUI 架构设计 | `../../gui_app/docs/Architecture_Design.md` | GUI 系统架构和模块设计 |
| 核心解析器架构 | `core/architecture.md` | 核心解析器架构和模块设计 |
| 版本管理 | `Version_Management.md` | 版本号规则和更新流程 |
| 函数文档 | `Function_Documentation.md` | 函数/类的详细说明 |
| 更新日志 | `UPDATE_LOG.md` | 每次迭代的变更记录 |

### 9.2 快速参考

**开发前必读**:
1. `Requirements.md` - 了解需求
2. `../../gui_app/docs/Architecture_Design.md` - 了解 GUI 架构
3. `core/architecture.md` - 了解核心解析器架构
4. `Development_Process.md` - 了解流程

**开发中参考**:
1. `Function_Documentation.md` - 了解函数接口
2. `Development_Process.md` - 了解代码规范

**开发后必做**:
1. 更新 GUI 架构文档 (`../../gui_app/docs/Architecture_Design.md`) 或核心解析器架构文档 (`core/architecture.md`)（如需要）
2. 更新 `Function_Documentation.md`（如需要）
3. 更新 `UPDATE_LOG.md`（必须）
4. 更新版本号（如需要）

---

**文档结束**
