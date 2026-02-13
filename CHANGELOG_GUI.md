# 📜 GUI Application Changelog

All notable changes to the GUI (Graphical User Interface) application will be documented in this file.

## [2.1.2] - 2026-02-13 (Fixed Document Generation Path Issue)

### Fixed

- **Document Generation Path**: Fixed issue where GUI application was not generating markdown files in the `Output/` folder
  - Issue: GUI program used relative paths for output directory, causing files to be generated in wrong location or not at all
  - Solution: Updated `DocumentController` and `FileController` to use absolute paths based on project root directory
  - Location: `gui_app/controller/document_controller.py`, `gui_app/controller/file_controller.py`
  - Added: New utility function `get_project_root()` in `gui_app/utils/path_utils.py` to ensure consistent path resolution

## [2.1.1] - 2026-02-12 (GUI Bug Fixes and UI Improvements)

### Fixed

- **libpng Warning Suppression**: Fixed libpng warning about incorrect sRGB profile that appeared in console output
  - Issue: Console showed "libpng warning: iCCP: known incorrect sRGB profile" messages
  - Solution: Added StderrFilter class to filter libpng warnings from stderr output
  - Location: `gui_app/main_gui.py`

### Changed

- **LS-Dyna Command List Layout**: Changed command list panel layout from horizontal (left-right) to vertical (top-bottom)
  - Command list now appears at the top
  - Command description appears at the bottom
  - Improved readability and user experience
  - Location: `gui_app/gui/command_list.py`

## [2.1.0] - 2026-02-12 (GUI Layout Improvements)

### Changed

- **Resizable Panel Layout**: Improved main window layout using QSplitter for adjustable panel widths
  - Dragging the left edge of the window adjusts the middle content panel width
  - Dragging the right edge of the window adjusts the right-side LS-Dyna command list panel width
  - Left file list panel remains fixed width

### Fixed

- **Content Loss After Processing**: Fixed issue where tab contents (checklist, detailed docs, overview docs) were cleared after file processing completed
  - Issue: Tab contents were lost after processing
  - Cause: Selection state was lost during list updates, triggering selection change signal with None
  - Solution: Use `blockSignals` to temporarily block signals during list updates, preserving and restoring selection state

## [2.0.0] - 2026-02-12 (Initial GUI Release)

### Added

- **Graphical User Interface**: Complete GUI application built with PyQt5
- **File Management**: Visual file list with selection and processing capabilities
- **Document Generation**: Integrated document generation with progress tracking
- **Checklist View**: Model content checklist for quick analysis
- **Document View**: Tabbed interface for detailed docs, overview docs, and AI requirements
- **LS-Dyna Command Reference**: Built-in command list with descriptions
- **Version Control**: Introduced semantic versioning starting at v2.0.0.
