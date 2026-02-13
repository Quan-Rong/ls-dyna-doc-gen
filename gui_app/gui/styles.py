"""
Modern Stylesheet for GUI Application

Provides modern, beautiful styling for the LS-Dyna Documentation Generator GUI.
"""

# Modern color palette
COLORS = {
    # Primary colors
    'primary': '#2563eb',  # Blue
    'primary_hover': '#1d4ed8',
    'primary_pressed': '#1e40af',
    
    # Secondary colors
    'secondary': '#64748b',  # Slate
    'secondary_hover': '#475569',
    
    # Success/Error colors
    'success': '#10b981',  # Green
    'error': '#ef4444',    # Red
    'warning': '#f59e0b',  # Amber
    'info': '#3b82f6',     # Blue
    
    # Background colors
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_tertiary': '#f1f5f9',
    'bg_dark': '#1e293b',
    
    # Text colors
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_tertiary': '#94a3b8',
    'text_light': '#ffffff',
    
    # Border colors
    'border': '#e2e8f0',
    'border_focus': '#2563eb',
    
    # Shadow
    'shadow': 'rgba(0, 0, 0, 0.1)',
    'shadow_hover': 'rgba(0, 0, 0, 0.15)',
}

# Modern stylesheet
MODERN_STYLESHEET = f"""
/* Main Window */
QMainWindow {{
    background-color: {COLORS['bg_secondary']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {COLORS['bg_secondary']}, 
                                stop:1 {COLORS['bg_tertiary']});
}}

/* Widgets */
QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    font-family: "Segoe UI", "Microsoft YaHei", "SimHei", sans-serif;
    font-size: 12pt;
}}

/* Push Buttons - Modern Style */
QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['text_light']};
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 500;
    min-height: 36px;
    font-size: 12pt;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_pressed']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_tertiary']};
    color: {COLORS['text_tertiary']};
}}

/* Secondary Button */
QPushButton[class="secondary"] {{
    background-color: {COLORS['bg_tertiary']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
}}

QPushButton[class="secondary"]:hover {{
    background-color: {COLORS['bg_secondary']};
    border-color: {COLORS['primary']};
}}

/* Danger Button */
QPushButton[class="danger"] {{
    background-color: {COLORS['error']};
}}

QPushButton[class="danger"]:hover {{
    background-color: #dc2626;
}}

/* List Widget - Modern Style */
QListWidget {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    background-color: transparent;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 2px;
    min-height: 24px;
}}

QListWidget::item:hover {{
    background-color: {COLORS['bg_secondary']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: {COLORS['text_light']};
}}

QListWidget::item:selected:hover {{
    background-color: {COLORS['primary_hover']};
}}

/* Tree Widget - Modern Style */
QTreeWidget {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
    outline: none;
    alternate-background-color: {COLORS['bg_secondary']};
}}

QTreeWidget::item {{
    padding: 6px;
    border-radius: 4px;
    min-height: 24px;
}}

QTreeWidget::item:hover {{
    background-color: {COLORS['bg_secondary']};
}}

QTreeWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: {COLORS['text_light']};
}}

QTreeWidget::item:selected:hover {{
    background-color: {COLORS['primary_hover']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_tertiary']};
    color: {COLORS['text_primary']};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    font-weight: 600;
}}

/* Tab Widget - Modern Style */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['bg_primary']};
    top: -1px;
}}

QTabBar::tab {{
    background-color: {COLORS['bg_tertiary']};
    color: {COLORS['text_secondary']};
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 20px;
    margin-right: 2px;
    font-weight: 500;
    min-width: 100px;
}}

QTabBar::tab:hover {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_primary']};
}}

QTabBar::tab:selected {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['primary']};
    border-bottom: 2px solid {COLORS['primary']};
}}

/* Text Edit - Modern Style */
QTextEdit {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px;
    selection-background-color: {COLORS['primary']};
    selection-color: {COLORS['text_light']};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12pt;
    line-height: 1.6;
}}

QTextEdit:focus {{
    border: 2px solid {COLORS['border_focus']};
    padding: 11px;
}}

/* Label - Modern Style */
QLabel {{
    color: {COLORS['text_primary']};
}}

QLabel[class="header"] {{
    font-size: 18pt;
    font-weight: 600;
    color: {COLORS['text_primary']};
    padding: 8px 0px;
}}

QLabel[class="subheader"] {{
    font-size: 14pt;
    font-weight: 500;
    color: {COLORS['text_secondary']};
    padding: 4px 0px;
}}

QLabel[class="status"] {{
    color: {COLORS['text_secondary']};
    font-size: 11pt;
    padding: 4px 0px;
}}

/* Checkbox - Modern Style */
QCheckBox {{
    spacing: 8px;
    color: {COLORS['text_primary']};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['bg_primary']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['primary']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['primary']};
    border-color: {COLORS['primary']};
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjMzMzMgNEw2IDEyTDIuNjY2NjcgOC42NjY2NyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
}}

/* Progress Bar - Modern Style */
QProgressBar {{
    border: none;
    border-radius: 8px;
    background-color: {COLORS['bg_tertiary']};
    height: 24px;
    text-align: center;
    color: {COLORS['text_primary']};
    font-weight: 500;
}}

QProgressBar::chunk {{
    background-color: {COLORS['primary']};
    border-radius: 8px;
}}

/* Dialog - Modern Style */
QDialog {{
    background-color: {COLORS['bg_primary']};
    border-radius: 12px;
}}

/* Scrollbar - Modern Style */
QScrollBar:vertical {{
    background-color: {COLORS['bg_tertiary']};
    width: 12px;
    border: none;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['secondary']};
    border-radius: 6px;
    min-height: 30px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['secondary_hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS['bg_tertiary']};
    height: 12px;
    border: none;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['secondary']};
    border-radius: 6px;
    min-width: 30px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['secondary_hover']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* Status Icons */
QLabel[class="status-success"] {{
    color: {COLORS['success']};
    font-weight: 600;
}}

QLabel[class="status-error"] {{
    color: {COLORS['error']};
    font-weight: 600;
}}

QLabel[class="status-warning"] {{
    color: {COLORS['warning']};
    font-weight: 600;
}}

/* Card Style (for panels) */
QWidget[class="card"] {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 16px;
    margin: 4px;
}}

/* Sidebar Style */
QWidget[class="sidebar"] {{
    background-color: {COLORS['bg_tertiary']};
    border-right: 1px solid {COLORS['border']};
}}

/* File List Item Status Colors */
QListWidget::item[status="processed"] {{
    color: {COLORS['success']};
}}

QListWidget::item[status="error"] {{
    color: {COLORS['error']};
}}

QListWidget::item[status="processing"] {{
    color: {COLORS['warning']};
}}

/* Message Box Styling */
QMessageBox {{
    background-color: {COLORS['bg_primary']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
    padding: 8px 20px;
}}

/* Command List Widget */
QListWidget[class="command-list"] {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
    outline: none;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11pt;
}}

QListWidget[class="command-list"]::item {{
    background-color: transparent;
    border-radius: 6px;
    padding: 6px 10px;
    margin: 2px;
    min-height: 22px;
}}

QListWidget[class="command-list"]::item:hover {{
    background-color: {COLORS['bg_secondary']};
}}

QListWidget[class="command-list"]::item:selected {{
    background-color: {COLORS['primary']};
    color: {COLORS['text_light']};
}}

QTextEdit[class="command-description"] {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px;
    selection-background-color: {COLORS['primary']};
    selection-color: {COLORS['text_light']};
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 12pt;
    line-height: 1.6;
}}

QTextEdit[class="command-description"]:focus {{
    border: 2px solid {COLORS['border_focus']};
    padding: 11px;
}}

/* Splitter */
QSplitter::handle {{
    background-color: {COLORS['border']};
    width: 2px;
    height: 2px;
}}

QSplitter::handle:hover {{
    background-color: {COLORS['primary']};
}}
"""
