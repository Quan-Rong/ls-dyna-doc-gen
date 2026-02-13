# LS-Dyna Documentation Generator

> **Projektversion**: 2.1.2  
> **Letzte Aktualisierung**: 2026-02-13

> **项目版本**: 2.1.2  
> **最后更新**: 2026-02-13

Ein Toolset zur automatischen Analyse von LS-Dyna Schlüsselwortdateien (`.key`) und zur Generierung strukturierter Markdown-Dokumentation. Dieses Projekt enthält zwei unabhängige Anwendungen: ein **CLI (Kommandozeilen) Tool** und eine **GUI (Grafische Benutzeroberfläche) Anwendung**.

一个用于自动解析 LS-Dyna 关键字文件（`.key`）并生成结构化 Markdown 文档的工具集。本项目包含两个独立的应用程序：**CLI（命令行）工具**和**GUI（图形界面）应用程序**。

---

## 📋 Inhaltsverzeichnis / 目录

1. [Projektübersicht / 项目概述](#1-projektübersicht--项目概述)
2. [Zwei Programme / 两个程序](#2-zwei-programme--两个程序)
3. [Schnellstart / 快速开始](#3-schnellstart--快速开始)
4. [Projektstruktur / 项目结构](#4-projektstruktur--项目结构)
5. [Kernfunktionen / 核心功能](#5-kernfunktionen--核心功能)
6. [KI-unterstützte Entwicklung / AI 辅助开发](#6-ki-unterstützte-entwicklung--ai-辅助开发)
7. [Änderungsprotokoll / 更新日志](#7-änderungsprotokoll--更新日志)

---

## 1. Projektübersicht / 项目概述

### 1.1 Projektkontext / 项目背景

LS-Dyna ist eine weit verbreitete Finite-Elemente-Analysesoftware für Automobilcrashsimulationen. In der praktischen Ingenieursarbeit bestehen vollständige Crashmodelle typischerweise aus mehreren Teilmodellen (`.key` Dateien), wobei jedes Teilmodell möglicherweise nur Teile enthält (wie Türen, Stoßstangen usw.) und nicht die vollständigen Simulationsparameter.

LS-Dyna 是广泛应用于汽车碰撞仿真的有限元分析软件。在实际工程中，整车碰撞模型通常由多个子模型（`.key` 文件）组成，每个子模型可能只包含部分组件（如车门、保险杠等），并不包含完整的仿真设置。

### 1.2 Projektziele / 项目目标

Entwicklung eines Toolsets für:
- Batch-Verarbeitung von LS-Dyna `.key` Dateien
- Automatische Generierung strukturierter Markdown-Dokumentation
- Bereitstellung von Modellinhalt-Checklisten zur schnellen Übersicht über enthaltene und nicht enthaltene Inhalte
- Unterstützung für Kommandozeilen- und grafische Benutzeroberfläche

开发一套工具集，用于：
- 批量处理 LS-Dyna `.key` 文件
- 自动生成结构化的 Markdown 文档
- 提供模型内容检查清单，快速了解模型包含和不包含的内容
- 支持命令行和图形界面两种使用方式

### 1.3 Zielgruppe / 目标用户

- **Hauptbenutzer**: CAE-Ingenieure, Simulationsanalysten
- **Anwendungsszenarien**: Batch-Dokumentationsgenerierung, Modellprüfung, Automatisierungsprozesse

- **主要用户**: CAE 工程师、仿真分析人员
- **使用场景**: 批量文档生成、模型审查、自动化流程

---

## 2. Zwei Programme / 两个程序

Dieses Projekt enthält zwei vollständig unabhängige Anwendungen, die sich eine gemeinsame Kerncodebasis teilen, sich aber nicht gegenseitig beeinflussen:

本项目包含两个完全独立的应用程序，它们共享核心代码库但互不干扰：

### 2.1 CLI-Programm (Kommandozeilen-Tool) / CLI 程序（命令行工具）

**Version**: v1.2.0  
**Einstiegspunkt**: `cli_app/main.py`  
**Anwendungsszenarien**: Batch-Verarbeitung, Automatisierungsskripte, Serverumgebungen

**版本**: v1.2.0  
**入口文件**: `cli_app/main.py`  
**适用场景**: 批量处理、自动化脚本、服务器环境

**Hauptmerkmale / 主要特性**:
- ✅ Batch-Verarbeitung mehrerer `.key` Dateien / 批量处理多个 `.key` 文件
- ✅ Inkrementeller Aufbau (intelligentes Überspringen bereits verarbeiteter Dateien) / 增量构建（智能跳过已处理文件）
- ✅ Unterstützung für Kommandozeilenparameter (`--force` zum erneuten Generieren) / 命令行参数支持（`--force` 强制重新生成）
- ✅ Geeignet für die Integration in Automatisierungsprozesse / 适合集成到自动化流程中

**Ausführungsweise / 运行方式**:
```bash
# Alle Dateien im Input/ Verzeichnis verarbeiten / 处理 Input/ 目录下的所有文件
python cli_app/main.py

# Bestimmte Datei verarbeiten / 处理指定文件
python cli_app/main.py Input/model.key

# Alle Dateien erneut generieren / 强制重新生成所有文件
python cli_app/main.py --force
```

**Änderungsprotokoll / 更新日志**: Siehe [CHANGELOG_CLI.md](CHANGELOG_CLI.md) / 参见 [CHANGELOG_CLI.md](CHANGELOG_CLI.md)

---

### 2.2 GUI-Programm (Grafische Benutzeroberfläche) / GUI 程序（图形界面）

**Version**: v2.1.1  
**Einstiegspunkt**: `gui_app/main_gui.py`  
**Anwendungsszenarien**: Interaktive Nutzung, Modellprüfung, Echtzeitvorschau

**版本**: v2.1.1  
**入口文件**: `gui_app/main_gui.py`  
**适用场景**: 交互式使用、模型审查、实时预览

**Hauptmerkmale / 主要特性**:
- ✅ Visuelles Dateimanagement (Dateiliste, Auswahl, Verarbeitung) / 可视化文件管理（文件列表、选择、处理）
- ✅ Echtzeit-Dokumentationsgenerierung und -vorschau / 实时文档生成和预览
- ✅ Modellinhalt-Checkliste (schnelle Übersicht über Modellinhalt) / 模型内容检查清单（快速了解模型包含的内容）
- ✅ Mehrere Dokumentationsregisterkarten (Detaillierte Dokumentation, Übersichtsdokumentation, KI-Anforderungen) / 多标签页文档查看（详细文档、概览文档、AI 需求）
- ✅ Integrierte LS-Dyna Befehlsreferenz / 内置 LS-Dyna 命令参考
- ✅ Fortschrittsverfolgung und Statusanzeige / 进度跟踪和状态显示

**Ausführungsweise / 运行方式**:
```bash
# GUI-Anwendung starten / 启动 GUI 应用程序
python gui_app/main_gui.py
```

**Änderungsprotokoll / 更新日志**: Siehe [CHANGELOG_GUI.md](CHANGELOG_GUI.md) / 参见 [CHANGELOG_GUI.md](CHANGELOG_GUI.md)

---

## 3. Schnellstart / 快速开始

### 3.1 Umgebungsanforderungen / 环境要求

- **Python**: Version 3.8 oder höher / 3.8 或更高版本
- **Abhängigkeiten / 依赖包**:
  - CLI-Programm: Nur Python-Standardbibliothek (keine zusätzliche Installation erforderlich) / CLI 程序：仅使用 Python 标准库（无需额外安装）
  - GUI-Programm: Benötigt PyQt5 (`pip install PyQt5`) / GUI 程序：需要 PyQt5（`pip install PyQt5`）

### 3.2 Installationsschritte / 安装步骤

1. **Projekt klonen oder herunterladen / 克隆或下载项目**
   ```bash
   git clone <repository-url>
   cd ls-dyna-doc-gen
   ```

2. **GUI-Abhängigkeiten installieren (nur für GUI-Programm erforderlich) / 安装 GUI 依赖（仅 GUI 程序需要）**
   ```bash
   pip install PyQt5
   ```

3. **Eingabedateien vorbereiten / 准备输入文件**
   - Legen Sie Ihre `.key` Dateien in das `Input/` Verzeichnis / 将你的 `.key` 文件放入 `Input/` 目录

### 3.3 Verwendungsbeispiele / 使用示例

**CLI-Programm verwenden / 使用 CLI 程序**:
```bash
# 1. .key Dateien in Input/ Verzeichnis ablegen / 将 .key 文件放入 Input/ 目录
# 2. CLI-Programm ausführen / 运行 CLI 程序
python cli_app/main.py

# 3. Generierte Dokumentation anzeigen (im Output/ Verzeichnis) / 查看生成的文档（在 Output/ 目录）
```

**GUI-Programm verwenden / 使用 GUI 程序**:
```bash
# 1. GUI-Anwendung starten / 启动 GUI 应用程序
python gui_app/main_gui.py

# 2. Dateien in der Benutzeroberfläche auswählen und verarbeiten / 在界面中选择文件并处理
# 3. Generierte Dokumentation in Echtzeit anzeigen / 实时查看生成的文档
```

---

## 4. Projektstruktur / 项目结构

```
ls-dyna-doc-gen/                     # Projektstammverzeichnis / 项目根目录
│
├── 📁 CLI-Programm / CLI 程序
│   ├── cli_app/
│   │   ├── main.py                  # CLI Einstiegspunkt / CLI 入口点
│   │   ├── cli_main.py              # CLI Hauptlogik / CLI 主逻辑
│   │   ├── docs/                    # CLI-bezogene Dokumentation / CLI 相关文档
│   │   │   ├── CLI_Requirements.md
│   │   │   └── CLI_ENTRY.md
│   │   └── __init__.py
│   └── CHANGELOG_CLI.md             # CLI Änderungsprotokoll / CLI 更新日志
│
├── 📁 GUI-Programm / GUI 程序
│   ├── gui_app/
│   │   ├── main_gui.py              # GUI Einstiegspunkt / GUI 入口点
│   │   ├── gui/                     # GUI Benutzeroberflächenmodule / GUI 界面模块
│   │   │   ├── main_window.py
│   │   │   ├── file_list.py
│   │   │   ├── content_view.py
│   │   │   └── ...
│   │   ├── controller/              # Geschäftslogik-Controller / 业务逻辑控制器
│   │   ├── models/                  # Datenmodelle / 数据模型
│   │   ├── logo/                    # GUI Ressourcendateien / GUI 资源文件
│   │   ├── docs/                    # GUI-bezogene Dokumentation / GUI 相关文档
│   │   │   ├── GUI_Requirements.md
│   │   │   └── GUI_ENTRY.md
│   │   └── __init__.py
│   └── CHANGELOG_GUI.md             # GUI Änderungsprotokoll / GUI 更新日志
│
├── 📁 Gemeinsame Kernbibliothek / 共享核心库
│   └── ls_dyna_md/                  # Kernfunktionspaket (von beiden Programmen gemeinsam genutzt) / 核心功能包（两个程序共享）
│       ├── parser.py                # LS-Dyna Dateiparser / LS-Dyna 文件解析器
│       ├── writers/                 # Dokumentationsgeneratoren / 文档生成器
│       │   ├── detailed_writer.py   # Detaillierte Dokumentationsgenerierung / 详细文档生成
│       │   ├── overview_writer.py    # Übersichtsdokumentationsgenerierung / 概览文档生成
│       │   ├── capability_writer.py  # Fähigkeitsmatrixgenerierung / 能力矩阵生成
│       │   └── requirements_writer.py # KI-Anforderungsgenerierung / AI 需求生成
│       └── utils/                   # Hilfsfunktionen / 工具函数
│           ├── descriptions.py      # Schlüsselwortbeschreibungen / 关键字描述
│           ├── engineering.py       # Ingenieursanalyse / 工程意义分析
│           └── supported_commands.py # Unterstützte Befehlsregistrierung / 支持的命令注册表
│
├── 📁 Eingabe-/Ausgabeverzeichnisse / 输入输出目录
│   ├── Input/                       # Eingabedateiverzeichnis (Platzierung von .key Dateien) / 输入文件目录（放置 .key 文件）
│   └── Output/                      # Ausgabedateiverzeichnis (generierte Dokumentation) / 输出文件目录（生成的文档）
│
├── 📁 Dokumentationsverzeichnisse / 文档目录
│   ├── docs/                        # Entwicklungsdokumentationsverzeichnis / 开发文档目录
│   │   ├── core/                    # Kernparser-Dokumentation / 核心解析器文档
│   │   │   ├── architecture.md      # Kernparser-Architekturdokumentation / 核心解析器架构文档
│   │   │   └── api_reference.md     # API-Referenzdokumentation / API 参考文档
│   │   ├── Development_Guide.md     # Entwicklungsleitfaden / 开发指南
│   │   ├── Project_Structure.md     # Projektstrukturdokumentation / 项目结构文档
│   │   └── ...                      # Weitere Entwicklungsdokumentation / 其他开发文档
│   └── ls_dyna_md/docs/             # Automatisch generierte Dokumentation / 自动生成的文档
│       └── SUPPORTED_COMMANDS.md    # Liste unterstützter Befehle (automatisch generiert) / 支持的命令列表（自动生成）
│
├── README.md                        # Diese Datei (Projektübersicht) / 本文件（项目总说明）
├── CHANGELOG_CLI.md                 # CLI-Programm Änderungsprotokoll / CLI 程序更新日志
└── CHANGELOG_GUI.md                 # GUI-Programm Änderungsprotokoll / GUI 程序更新日志
```

### 4.1 Verzeichnisbeschreibung / 目录说明

| Verzeichnis/Datei / 目录/文件 | Zweck / 用途 | Zugehöriges Programm / 所属程序 |
|----------|------|---------|
| `cli_app/` | CLI-Programm Hauptverzeichnis / CLI 程序主目录 | CLI |
| `cli_app/main.py` | CLI-Programm Einstiegspunkt / CLI 程序入口点 | CLI |
| `gui_app/` | GUI-Programm Hauptverzeichnis / GUI 程序主目录 | GUI |
| `gui_app/main_gui.py` | GUI-Programm Einstiegspunkt / GUI 程序入口点 | GUI |
| `ls_dyna_md/` | Kernfunktionspaket / 核心功能包 | **Gemeinsam / 共享** |
| `Input/` | Eingabedateiverzeichnis / 输入文件目录 | **Gemeinsam / 共享** |
| `Output/` | Ausgabedateiverzeichnis / 输出文件目录 | **Gemeinsam / 共享** |
| `docs/` | Projektdokumentation / 项目文档 | **Gemeinsam / 共享** |

---

## 5. Kernfunktionen / 核心功能

### 5.1 Dokumentationsgenerierung / 文档生成

Beide Programme unterstützen die Generierung folgender Dokumentationstypen:

两个程序都支持生成以下类型的文档：

1. **Detaillierte Referenzdokumentation** (`*_docs.md`) / **详细参考文档** (`*_docs.md`)
   - Strukturierte Markdown-Dokumentation / 结构化的 Markdown 文档
   - Enthält Tabellen: Parts, Materials, Sections usw. / 包含表格：Parts、Materials、Sections 等
   - Elementdatenbeispiele und Statistiken / 元素数据样本和统计信息

2. **Ingenieurübersichtsdokumentation** (`*_overview.md`) / **工程概览文档** (`*_overview.md`)
   - Erweiterte Ingenieurszusammenfassung / 高级工程摘要
   - Modellphysikalische Bedeutungsanalyse / 模型物理意义分析
   - Verbindungsbeziehungen und Anfangsbedingungen-Zusammenfassung / 连接关系和初始条件总结

3. **KI-Anforderungsdokumentation** (`*_AI_REQ.md`) / **AI 需求文档** (`*_AI_REQ.md`)
   - Wird automatisch generiert, wenn nicht unterstützte Schlüsselwörter gefunden werden / 当遇到不支持的关键字时自动生成
   - Enthält Code-Snippets und Implementierungsanweisungen / 包含代码片段和实现说明
   - Für KI-unterstützte Entwicklung / 用于 AI 辅助开发

### 5.2 Unterstützte Schlüsselwörter / 支持的关键字

Das System unterstützt 20+ LS-Dyna Schlüsselwortkategorien, einschließlich:

系统支持 20+ 种 LS-Dyna 关键字类别，包括：

- `PART`, `PART_COMPOSITE`, `PART_CONTACT`
- `MAT_*` (verschiedene Materialtypen) / (各种材料类型)
- `SECTION_*` (verschiedene Querschnittstypen) / (各种截面类型)
- `ELEMENT_*` (verschiedene Elementtypen) / (各种单元类型)
- `CONTACT_*` (verschiedene Kontaktdefinitionen) / (各种接触定义)
- `CONSTRAINED_*` (Einschränkungsdefinitionen) / (约束定义)
- `SET_*` (Mengendefinitionen) / (集合定义)
- `DAMPING_*` (Dämpfungsdefinitionen) / (阻尼定义)
- `DATABASE_*` (Datenbankausgabesteuerung) / (数据库输出控制)
- `INITIAL_*` (Anfangsbedingungen) / (初始条件)
- usw. / 等等...

Vollständige Liste siehe [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md) / 完整列表请参见 [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md)

---

## 6. KI-unterstützte Entwicklung / AI 辅助开发

Dieses Projekt enthält Architekturmerkmale, die speziell für KI-unterstützte Entwicklung entwickelt wurden:

本项目包含专为 AI 辅助开发设计的架构特性：

### 6.1 Fähigkeitsselbstreflexion (Capability Introspection) / 能力自省（Capability Introspection）

Das System verwaltet ein Echtzeit-Fähigkeitsmatrixdokument [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md) als **echte Referenz** für KI-Agenten, die klar definiert, welche LS-Dyna Schlüsselwörter derzeit unterstützt werden und wie sie internen Datenstrukturen zugeordnet werden.

系统维护一个实时的能力矩阵文档 [`ls_dyna_md/docs/SUPPORTED_COMMANDS.md`](ls_dyna_md/docs/SUPPORTED_COMMANDS.md)，作为 AI 代理的**真实参考**，明确定义了当前支持哪些 LS-Dyna 关键字以及它们如何映射到内部数据结构。

### 6.2 Automatisierte Anforderungstechnik / 自动化需求工程

Wenn der Parser auf nicht unterstützte LS-Dyna Schlüsselwörter stößt, isoliert er den spezifischen Befehlszusammenhang und generiert formale Anforderungsspezifikationen in `Output/*_AI_REQ.md`.

当解析器遇到不支持的 LS-Dyna 关键字时，它会隔离特定的命令上下文并在 `Output/*_AI_REQ.md` 中生成正式的需求规范。

- **Artefaktzweck**: Diese Dateien dienen als strukturierte **Aufgabenspezifikationen** für KI-Entwickler / **工件用途**: 这些文件作为 AI 开发者的结构化**任务规范**
- **Workflow-Integration**: Der Kontext dieser Artefakte kann direkt von KI-Codierungstools verwendet werden, um die notwendige `parser.py` Logik und `detailed_writer.py` Dokumentationsmethoden zu generieren / **工作流集成**: 这些工件的上下文可以直接被 AI 编码工具使用，生成必要的 `parser.py` 逻辑和 `detailed_writer.py` 文档方法
- **⚠️ Durchsatzhinweis**: Obwohl Code-Snippets zur Effizienzsteigerung optimiert wurden, können große Dateien mit vielen unbekannten Befehlen viel Kontext generieren. Stellen Sie bei der Analyse von Batch-Anforderungsdateien sicher, dass Ihre KI-Umgebung (Kontextfenster) und API-Durchsatz ausreichend sind / **⚠️ 吞吐量注意**: 虽然代码片段已优化以提高效率，但包含许多未知命令的大型文件可能会生成大量上下文。在分析批量需求文件时，请确保你的 AI 环境（上下文窗口）和 API 吞吐量足够

---

## 7. Änderungsprotokoll / 更新日志

- **CLI-Programm Änderungsprotokoll / CLI 程序更新日志**: [CHANGELOG_CLI.md](CHANGELOG_CLI.md)
- **GUI-Programm Änderungsprotokoll / GUI 程序更新日志**: [CHANGELOG_GUI.md](CHANGELOG_GUI.md)

---

## 📚 Weitere Dokumentation / 更多文档

- **Kernparser-Architektur / 核心解析器架构**: [`docs/core/architecture.md`](docs/core/architecture.md)
- **API-Referenz / API 参考**: [`docs/core/api_reference.md`](docs/core/api_reference.md)
- **Entwicklungsleitfaden / 开发指南**: [`docs/Development_Guide.md`](docs/Development_Guide.md)
- **Projektstruktur / 项目结构**: [`docs/Project_Structure.md`](docs/Project_Structure.md)
- **CLI-Programm Dokumentation / CLI 程序文档**: [`cli_app/docs/CLI_ENTRY.md`](cli_app/docs/CLI_ENTRY.md)
- **GUI-Programm Dokumentation / GUI 程序文档**: [`gui_app/docs/GUI_ENTRY.md`](gui_app/docs/GUI_ENTRY.md)

---

## 🤝 Beitragen / 贡献

Beiträge und Vorschläge sind willkommen! Bitte lesen Sie die Entwicklungsdokumentation, um zu erfahren, wie Sie Funktionen erweitern können.

欢迎贡献代码和提出建议！请参考开发文档了解如何扩展功能。

---

**Projektwartung / 项目维护**: LS-Dyna Documentation Generator Team  
**Letzte Aktualisierung / 最后更新**: 2026-02-12
