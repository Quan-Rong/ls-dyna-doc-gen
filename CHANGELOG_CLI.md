# 📜 CLI Application Changelog

All notable changes to the CLI (Command Line Interface) application will be documented in this file.

## [1.2.0] - 2026-02-12 (AI Collaboration Suite)

### Added

- **Capability Matrix**: Automatically generates `ls_dyna_md/docs/SUPPORTED_COMMANDS.md` listing all 20+ supported LS-Dyna keyword categories with detailed parameters and examples.
- **AI Requirements Generator**: When unknown keywords are encountered, the system now generates a `*_AI_REQ.md` file containing code snippets and implementation instructions for AI assistants.
- **Comprehensive Audit**: Updated the internal keyword registry to explicitly support `SET_*`, `CONSTRAINED_*`, `DATABASE_*`, `TITLE`, `PARAMETER`, `INCLUDE`, `DAMPING`, and generic `ELEMENT_*` definitions.

### Changed

- Modified `parser.py` to robustly capture context snippets for unknown keywords.
- Updated `main.py` to generate documentation artifacts on every run.

## [1.1.0] - 2026-02-12 (Incremental Build Feature)

### Added

- **Incremental Processing**: The script now intelligently skips files that have already been analyzed (checking for existing outputs), saving time on subsequent runs.
- **Force Mode**: Added `--force` command-line argument to bypass the incremental check and re-analyze all files.
- **Summary Statistics**: Added a final summary of processed, skipped, and failed files.

## [1.0.0] - 2026-02-12 (Initial Stable Release)

### Added

- **Modular Architecture**: Split the monolithic script into `parser`, `writers`, and `utils` for better maintainability.
- **Automated Workflow**:
  - `main.py` now automatically scans the `Input/` folder for `.key` files.
  - All outputs are saved to the `Output/` folder.
- **Detailed Documentation**:
  - Enhanced markdown generation with emojis and tables.
  - Support for LS-Dyna keyword statistics, materials, sections, and contacts documentation.
- **Overview Report**:
  - Automatically generates an engineering summary (`_overview.md`).
  - Analyzes physical meaning of elements, contacts, and initial conditions.
- **Version Control**: Introduced semantic versioning starting at v1.0.0.
