"""
Progress Dialog

Dialog for showing processing progress.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QProgressBar,
                               QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal


class ProgressDialog(QDialog):
    """Dialog for showing processing progress."""
    
    # Signals
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None, total: int = 0):
        """Initialize progress dialog.
        
        Args:
            parent: Parent widget
            total: Total number of files to process
        """
        super().__init__(parent)
        self.total = total
        self.current = 0
        self.setup_ui()
        self.setWindowTitle("处理进度")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title_label = QLabel("处理进度")
        title_label.setProperty("class", "header")
        layout.addWidget(title_label)
        
        # Status label
        self.status_label = QLabel("准备处理...")
        self.status_label.setProperty("class", "subheader")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.total)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Current file label
        self.current_file_label = QLabel("")
        self.current_file_label.setProperty("class", "status")
        self.current_file_label.setWordWrap(True)
        layout.addWidget(self.current_file_label)
        
        layout.addSpacing(8)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("class", "secondary")
        self.cancel_btn.clicked.connect(self.on_cancel)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Apply styles
        from .styles import MODERN_STYLESHEET
        self.setStyleSheet(MODERN_STYLESHEET)
    
    def update_progress(self, current: int, current_file: str = ""):
        """Update progress.
        
        Args:
            current: Current file index (0-based, or total when finished)
            current_file: Current file name
        """
        # Ensure current doesn't exceed total
        if self.total > 0:
            current = min(current, self.total)
        else:
            current = max(0, current)
        
        self.current = current
        self.progress_bar.setValue(current)
        
        if self.total > 0:
            percentage = int((current / self.total) * 100)
            if current >= self.total:
                self.status_label.setText(f"完成: {self.total}/{self.total} (100%)")
            else:
                self.status_label.setText(f"处理中: {current}/{self.total} ({percentage}%)")
        else:
            self.status_label.setText(f"处理中: {current}")
        
        if current_file:
            self.current_file_label.setText(f"当前文件: {current_file}")
        elif current >= self.total and self.total > 0:
            self.current_file_label.setText("所有文件处理完成")
    
    def on_cancel(self):
        """Handle cancel button click."""
        self.cancelled.emit()
        self.reject()
    
    def closeEvent(self, event):
        """Handle close event."""
        self.cancelled.emit()
        event.accept()
