"""
Document View Widget

Widget for displaying markdown documents.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLabel,
                               QPushButton, QHBoxLayout, QFileDialog)
from PyQt5.QtCore import Qt
from ..models.document_model import DocumentModel
import os


class DocumentViewWidget(QWidget):
    """Widget for displaying documents."""
    
    def __init__(self, parent=None):
        """Initialize document view widget."""
        super().__init__(parent)
        self.document_model = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_widget = QWidget()
        header_widget.setProperty("class", "card")
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setContentsMargins(12, 12, 12, 12)
        
        header_label = QLabel("文档内容")
        header_label.setProperty("class", "header")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Buttons
        self.open_folder_btn = QPushButton("📂 打开文件夹")
        self.open_folder_btn.setProperty("class", "secondary")
        self.open_folder_btn.clicked.connect(self.on_open_folder)
        header_layout.addWidget(self.open_folder_btn)
        
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        # Text editor (plain text for now, can be enhanced with markdown renderer)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFontFamily("Consolas")
        self.text_edit.setFontPointSize(10)
        layout.addWidget(self.text_edit, 1)
        
        self.setLayout(layout)
    
    def display_document(self, document_model: DocumentModel):
        """Display document model.
        
        Args:
            document_model: DocumentModel instance
        """
        self.document_model = document_model
        if document_model and document_model.content:
            self.text_edit.setPlainText(document_model.content)
        else:
            self.text_edit.setPlainText("文档内容为空或未生成。")
    
    def clear(self):
        """Clear document display."""
        self.text_edit.clear()
        self.document_model = None
    
    def on_open_folder(self):
        """Open folder containing the document."""
        if self.document_model and self.document_model.file_path:
            folder_path = os.path.dirname(self.document_model.file_path)
            if os.path.exists(folder_path):
                import subprocess
                import platform
                if platform.system() == 'Windows':
                    os.startfile(folder_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', folder_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', folder_path])
