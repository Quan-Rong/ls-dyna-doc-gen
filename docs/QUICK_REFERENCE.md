# 快速参考 - 双程序结构

> **最后更新**: 2026-02-12

---

## 🎯 核心概念

本项目包含**两个独立的程序**，它们共享核心代码但完全分离：

1. **CLI 程序**（命令行工具）- 现有程序，版本 v1.1.0
2. **GUI 程序**（图形界面）- 新开发程序，版本 v2.0.0

---

## 📁 目录结构（简化版）

```
ls-dyna-doc-gen/               # 项目根目录
│
├── cli_app/                   # ← CLI 程序目录
│   ├── main.py                # ← CLI 程序入口
│   └── cli_main.py            # CLI 业务逻辑
│
├── gui_app/                   # ← GUI 程序目录
│   ├── main_gui.py            # ← GUI 程序入口
│   ├── gui/                   # GUI 界面模块
│   ├── controller/            # 业务逻辑
│   └── models/                # 数据模型
│
└── ls_dyna_md/                # ← 共享核心包（两个程序都使用）
    ├── parser.py
    ├── writers/
    └── utils/
```

---

## 🚀 运行方式

### CLI 程序（命令行工具）

```bash
python cli_app/main.py
```

### GUI 程序（图形界面）

```bash
python gui_app/main_gui.py
```

---

## 🔍 快速识别

| 程序 | 入口文件 | 目录 | 版本 |
|------|---------|------|------|
| CLI | `cli_app/main.py` | `cli_app/` | v1.2.0 |
| GUI | `gui_app/main_gui.py` | `gui_app/` | v2.1.1 |

---

## 📚 详细文档

- **完整项目结构**: [Project_Structure.md](Project_Structure.md)
- **GUI 架构设计**: [../../gui_app/docs/Architecture_Design.md](../../gui_app/docs/Architecture_Design.md)
- **核心解析器架构**: [architecture.md](architecture.md)
- **开发指南**: [Development_Guide.md](Development_Guide.md)

---

**文档结束**
