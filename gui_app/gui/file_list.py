"""
File List Widget

Widget for displaying and managing file list.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                               QLabel, QPushButton, QHBoxLayout, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from typing import Optional
from ..models.file_model import FileModel, FileStatus
import os


class FileListWidget(QWidget):
    """Widget for displaying file list."""
    
    # Signals - use object type to allow None
    file_selected = pyqtSignal(object)  # Can be FileModel or None
    files_changed = pyqtSignal(list)
    
    def __init__(self, parent=None):
        """Initialize file list widget."""
        super().__init__(parent)
        self.files = []  # List of FileModel instances
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_widget = QWidget()
        header_widget.setProperty("class", "card")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(12, 12, 12, 12)
        
        title_layout = QHBoxLayout()
        header_label = QLabel("文件列表")
        header_label.setProperty("class", "header")
        title_layout.addWidget(header_label)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.add_file_btn = QPushButton("📁 添加文件")
        self.add_file_btn.clicked.connect(self.on_add_file)
        self.add_folder_btn = QPushButton("📂 添加文件夹")
        self.add_folder_btn.clicked.connect(self.on_add_folder)
        self.remove_btn = QPushButton("🗑️ 移除")
        self.remove_btn.setProperty("class", "secondary")
        self.remove_btn.clicked.connect(self.on_remove_selected)
        
        button_layout.addWidget(self.add_file_btn)
        button_layout.addWidget(self.add_folder_btn)
        button_layout.addWidget(self.remove_btn)
        header_layout.addLayout(button_layout)
        
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.list_widget, 1)
        
        # Status label
        self.status_label = QLabel("0 个文件")
        self.status_label.setProperty("class", "status")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def add_file(self, file_model: FileModel):
        """Add a file to the list.
        
        Args:
            file_model: FileModel instance
        """
        if file_model not in self.files:
            self.files.append(file_model)
            self._update_list()
            self.files_changed.emit(self.files)
    
    def add_files(self, file_models: list):
        """Add multiple files to the list.
        
        Args:
            file_models: List of FileModel instances
        """
        for file_model in file_models:
            if file_model not in self.files:
                self.files.append(file_model)
        self._update_list()
        self.files_changed.emit(self.files)
    
    def remove_file(self, file_model: FileModel):
        """Remove a file from the list.
        
        Args:
            file_model: FileModel instance
        """
        if file_model in self.files:
            self.files.remove(file_model)
            self._update_list()
            self.files_changed.emit(self.files)
    
    def get_selected_files(self) -> list:
        """Get selected files.
        
        Returns:
            List of selected FileModel instances
        """
        selected_items = self.list_widget.selectedItems()
        selected_files = []
        for item in selected_items:
            file_model = item.data(Qt.UserRole)
            if file_model:
                selected_files.append(file_model)
        return selected_files
    
    def get_all_files(self) -> list:
        """Get all files.
        
        Returns:
            List of all FileModel instances
        """
        return self.files.copy()
    
    def update_file_status(self, file_model: FileModel):
        """Update file status in the list.
        
        Args:
            file_model: FileModel instance with updated status
        """
        self._update_list()
    
    def _update_list(self):
        """Update list widget display."""
        # Save currently selected files before clearing
        selected_files = self.get_selected_files()
        
        # Temporarily block selection signals to avoid clearing content
        self.list_widget.blockSignals(True)
        
        self.list_widget.clear()
        
        selected_items = []
        for file_model in self.files:
            item = QListWidgetItem()
            item.setText(self._format_file_item(file_model))
            item.setData(Qt.UserRole, file_model)
            self._set_item_icon(item, file_model.status)
            self.list_widget.addItem(item)
            
            # If this file was selected before, mark it for re-selection
            if file_model in selected_files:
                selected_items.append(item)
        
        # Restore selection
        for item in selected_items:
            item.setSelected(True)
        
        # Unblock signals
        self.list_widget.blockSignals(False)
        
        count = len(self.files)
        processed = sum(1 for f in self.files if f.status == FileStatus.PROCESSED)
        self.status_label.setText(f"共 {count} 个文件，已处理 {processed} 个")
    
    def _format_file_item(self, file_model: FileModel) -> str:
        """Format file item text.
        
        Args:
            file_model: FileModel instance
            
        Returns:
            Formatted string
        """
        status_icon = {
            FileStatus.UNPROCESSED: "○",
            FileStatus.PROCESSING: "⏳",
            FileStatus.PROCESSED: "✓",
            FileStatus.ERROR: "✗"
        }.get(file_model.status, "○")
        
        return f"{status_icon} {file_model.name} ({file_model.get_size_str()})"
    
    def _set_item_icon(self, item: QListWidgetItem, status: FileStatus):
        """Set item icon based on status."""
        # Icons can be added later if needed
        pass
    
    def on_add_file(self):
        """Handle add file button click."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择 LS-Dyna 文件",
            "",
            "LS-Dyna Files (*.key *.k);;All Files (*.*)"
        )
        
        if file_paths:
            from ..controller.file_controller import FileController
            controller = FileController()
            for file_path in file_paths:
                try:
                    file_model = controller.create_file_model(file_path)
                    self.add_file(file_model)
                except Exception as e:
                    print(f"Error adding file {file_path}: {e}")
    
    def on_add_folder(self):
        """Handle add folder button click."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹"
        )
        
        if folder_path:
            from ..controller.file_controller import FileController
            controller = FileController()
            file_models = []
            
            # Find all .key and .k files
            for ext in ['*.key', '*.k']:
                import glob
                for file_path in glob.glob(os.path.join(folder_path, ext)):
                    try:
                        file_model = controller.create_file_model(file_path)
                        file_models.append(file_model)
                    except Exception as e:
                        print(f"Error adding file {file_path}: {e}")
            
            if file_models:
                self.add_files(file_models)
    
    def on_remove_selected(self):
        """Handle remove selected button click."""
        selected_files = self.get_selected_files()
        for file_model in selected_files:
            self.remove_file(file_model)
    
    def on_selection_changed(self):
        """Handle selection change."""
        selected_files = self.get_selected_files()
        if selected_files:
            self.file_selected.emit(selected_files[0])
        else:
            # Emit None when no file is selected to clear content
            self.file_selected.emit(None)
