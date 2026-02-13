"""
Main Window

Main application window.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QPushButton, QCheckBox, QLabel, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from typing import Optional
from .file_list import FileListWidget
from .content_view import ContentViewWidget
from .progress_dialog import ProgressDialog
from .command_list import CommandListWidget
from .styles import MODERN_STYLESHEET
from ..models.file_model import FileModel, FileStatus
from ..controller.file_controller import FileController
from ..controller.document_controller import DocumentController
from ..controller.checklist_controller import ChecklistController
from .. import __version__ as gui_version
import os


class ProcessingThread(QThread):
    """Thread for processing files in background."""
    
    # Signals
    progress = pyqtSignal(int, str)  # current, filename
    file_completed = pyqtSignal(FileModel, bool, str)  # file_model, success, error
    finished = pyqtSignal()
    
    def __init__(self, files: list, force: bool = False, parent=None):
        """Initialize processing thread.
        
        Args:
            files: List of FileModel instances
            force: Force regeneration
            parent: Parent widget
        """
        super().__init__(parent)
        self.files = files
        self.force = force
        self.cancelled = False
    
    def run(self):
        """Run processing."""
        import traceback
        
        try:
            file_controller = FileController()
            doc_controller = DocumentController()
            checklist_controller = ChecklistController()
            
            # Generate capability doc once
            try:
                doc_controller.generate_capability_doc()
            except Exception as e:
                # If capability doc generation fails, log but continue
                print(f"Warning: Failed to generate capability doc: {e}")
            
            for idx, file_model in enumerate(self.files):
                if self.cancelled:
                    break
                
                # Update progress before processing
                self.progress.emit(idx, file_model.name)
                
                try:
                    # Check if already processed
                    if not self.force and file_model.check_output_exists(file_controller.output_dir):
                        file_model.status = FileStatus.PROCESSED
                        self.file_completed.emit(file_model, True, None)
                        # Update progress after completion
                        self.progress.emit(idx + 1, file_model.name)
                        continue
                    
                    # Parse file (with status update for processing)
                    parser = file_controller.parse_file(file_model, update_status=True)
                    if not parser:
                        error_msg = file_model.error_message or "Failed to parse file"
                        file_model.status = FileStatus.ERROR
                        file_model.error_message = error_msg
                        self.file_completed.emit(file_model, False, error_msg)
                        # Update progress after completion (even if failed)
                        self.progress.emit(idx + 1, file_model.name)
                        continue
                    
                    # Generate documents
                    results = doc_controller.generate_documents(parser, file_model, self.force)
                    if not results['success']:
                        error_msg = results.get('error', 'Unknown error during document generation')
                        file_model.status = FileStatus.ERROR
                        file_model.error_message = error_msg
                        self.file_completed.emit(file_model, False, error_msg)
                        # Update progress after completion (even if failed)
                        self.progress.emit(idx + 1, file_model.name)
                        continue
                    
                    # Update file model
                    file_model.status = FileStatus.PROCESSED
                    file_model.output_files = [
                        results.get('docs_path'),
                        results.get('overview_path'),
                        results.get('requirements_path')
                    ]
                    
                    self.file_completed.emit(file_model, True, None)
                    # Update progress after successful completion
                    self.progress.emit(idx + 1, file_model.name)
                    
                except Exception as e:
                    # Log the full traceback for debugging
                    error_msg = f"Unexpected error: {str(e)}"
                    print(f"Error processing {file_model.name}: {error_msg}")
                    traceback.print_exc()
                    
                    file_model.status = FileStatus.ERROR
                    file_model.error_message = error_msg
                    self.file_completed.emit(file_model, False, error_msg)
                    # Update progress after completion (even if failed)
                    self.progress.emit(idx + 1, file_model.name)
            
            # Ensure progress is at 100% when finished
            if self.files:
                self.progress.emit(len(self.files), "")
            
        except Exception as e:
            # Catch any unexpected errors in the entire processing loop
            print(f"Fatal error in processing thread: {e}")
            traceback.print_exc()
        finally:
            self.finished.emit()
    
    def cancel(self):
        """Cancel processing."""
        self.cancelled = True


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.current_file = None
        self.processing_thread = None
        self.progress_dialog = None
        self.setup_ui()
        self.apply_styles()
        self.setWindowTitle(f"LS-Dyna 文档生成器 v{gui_version}")
        self.resize(1400, 900)
        self.setMinimumSize(1000, 600)
        # Initialize with empty content
        self.content_view.clear()
        self.command_list.clear()
    
    def setup_ui(self):
        """Setup UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main vertical layout
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setSpacing(12)
        main_vertical_layout.setContentsMargins(16, 16, 16, 16)
        
        # Header with logo
        header_widget = QWidget()
        header_widget.setProperty("class", "card")
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.setContentsMargins(16, 12, 16, 12)
        
        # Logo
        # __file__ is gui_app/gui/main_window.py, so dirname twice gets gui_app/
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 "logo", "Gestamp_Logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Scale logo to appropriate size (height: 60px, maintain aspect ratio)
            scaled_pixmap = pixmap.scaled(200, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            header_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel(f"LS-Dyna 文档生成器 v{gui_version}")
        title_label.setProperty("class", "header")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        header_widget.setLayout(header_layout)
        main_vertical_layout.addWidget(header_widget)
        
        # Main horizontal splitter for content
        # This allows dragging window edges to adjust panel widths
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setChildrenCollapsible(False)  # Prevent panels from being collapsed completely
        
        # Left: File list (fixed width, not resizable via splitter)
        self.file_list = FileListWidget()
        self.file_list.file_selected.connect(self.on_file_selected)
        self.file_list.files_changed.connect(self.on_files_changed)
        main_splitter.addWidget(self.file_list)
        
        # Middle: Content view (resizable via left edge drag)
        self.content_view = ContentViewWidget()
        main_splitter.addWidget(self.content_view)
        
        # Right sidebar: Control panel and command list (resizable via right edge drag)
        right_sidebar = QWidget()
        right_sidebar.setMinimumWidth(350)
        right_sidebar_layout = QVBoxLayout()
        right_sidebar_layout.setSpacing(12)
        right_sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Control buttons panel
        control_widget = QWidget()
        control_widget.setProperty("class", "card")
        control_layout = QVBoxLayout()
        control_layout.setSpacing(12)
        control_layout.setContentsMargins(16, 16, 16, 16)
        
        control_label = QLabel("操作面板")
        control_label.setProperty("class", "header")
        control_layout.addWidget(control_label)
        
        control_layout.addSpacing(8)
        
        self.process_selected_btn = QPushButton("处理选中文件")
        self.process_selected_btn.clicked.connect(self.on_process_selected)
        control_layout.addWidget(self.process_selected_btn)
        
        self.process_all_btn = QPushButton("处理所有文件")
        self.process_all_btn.clicked.connect(self.on_process_all)
        control_layout.addWidget(self.process_all_btn)
        
        control_layout.addSpacing(16)
        
        self.force_checkbox = QCheckBox("强制重新处理")
        control_layout.addWidget(self.force_checkbox)
        
        control_layout.addStretch()
        
        control_widget.setLayout(control_layout)
        right_sidebar_layout.addWidget(control_widget)
        
        # Command list panel
        command_list_widget = QWidget()
        command_list_widget.setProperty("class", "card")
        command_list_layout = QVBoxLayout()
        command_list_layout.setSpacing(0)
        command_list_layout.setContentsMargins(0, 0, 0, 0)
        
        self.command_list = CommandListWidget()
        command_list_layout.addWidget(self.command_list)
        
        command_list_widget.setLayout(command_list_layout)
        right_sidebar_layout.addWidget(command_list_widget, 1)  # Give it more space
        
        right_sidebar.setLayout(right_sidebar_layout)
        main_splitter.addWidget(right_sidebar)
        
        # Set initial sizes (file_list: 250px, content_view: flexible, right_sidebar: 400px)
        # The sizes will be set after the splitter is added to the layout
        main_vertical_layout.addWidget(main_splitter, 1)  # Give it stretch factor
        
        # Set initial splitter sizes after adding to layout
        # This ensures proper initial sizing
        main_splitter.setSizes([250, 800, 400])
        central_widget.setLayout(main_vertical_layout)
    
    def apply_styles(self):
        """Apply modern stylesheet to the window."""
        self.setStyleSheet(MODERN_STYLESHEET)
    
    def on_file_selected(self, file_model: Optional[FileModel]):
        """Handle file selection.
        
        Args:
            file_model: Selected FileModel instance or None
        """
        self.current_file = file_model
        self.load_file_content(file_model)
    
    def on_files_changed(self, files: list):
        """Handle files list change.
        
        Args:
            files: List of FileModel instances
        """
        # Update button states if needed
        pass
    
    def load_file_content(self, file_model: Optional[FileModel]):
        """Load and display file content.
        
        Args:
            file_model: FileModel instance or None
        """
        # First, clear all content
        self.content_view.clear()
        self.command_list.clear()
        
        if not file_model:
            return
        
        # Only load existing documents if file is already processed
        # Don't parse or process until user clicks "Process" button
        if file_model.status == FileStatus.PROCESSED:
            try:
                # Load documents if they exist (without parsing the file)
                doc_controller = DocumentController()
                output_paths = file_model.get_output_paths(doc_controller.output_dir)
                
                # Load overview
                from ..models.document_model import DocumentType
                if os.path.exists(output_paths['overview']):
                    try:
                        doc_model = doc_controller.load_document(
                            output_paths['overview'],
                            DocumentType.OVERVIEW
                        )
                        if doc_model:
                            self.content_view.show_document(doc_model, "overview")
                    except Exception as e:
                        # If loading fails, clear it
                        self.content_view.overview_tab.clear()
                else:
                    # Clear overview if file doesn't exist
                    self.content_view.overview_tab.clear()
                
                # Load docs
                if os.path.exists(output_paths['docs']):
                    try:
                        doc_model = doc_controller.load_document(
                            output_paths['docs'],
                            DocumentType.DOCS
                        )
                        if doc_model:
                            self.content_view.show_document(doc_model, "docs")
                    except Exception as e:
                        # If loading fails, clear it
                        self.content_view.docs_tab.clear()
                else:
                    # Clear docs if file doesn't exist
                    self.content_view.docs_tab.clear()
                
                # Try to load commands and checklist only if we can safely parse
                # This should only happen after processing, not on file selection
                # For now, we'll skip this to avoid auto-parsing on selection
                # Commands and checklist will be loaded after processing completes
                        
            except Exception as e:
                # Silently handle errors - don't show error dialog on file selection
                # Just clear the content
                self.content_view.clear()
                self.command_list.clear()
        else:
            # If file is not processed, show empty state
            # User needs to click "Process" button to process
            self.content_view.overview_tab.clear()
            self.content_view.docs_tab.clear()
            self.content_view.clear_checklist()
    
    def load_file_content_after_processing(self, file_model: FileModel):
        """Load and display file content after processing is complete.
        
        This method is called after a file has been processed, and will:
        1. Load existing documents
        2. Parse file to get commands and checklist
        3. Display all content
        
        Args:
            file_model: FileModel instance
        """
        # First, clear all content
        self.content_view.clear()
        self.command_list.clear()
        
        if not file_model:
            return
        
        # Only load if file is processed
        if file_model.status != FileStatus.PROCESSED:
            return
        
        try:
            # Parse file to get commands and checklist (without status update)
            file_controller = FileController()
            parser = file_controller.parse_file(file_model, update_status=False)
            
            if parser:
                # Load commands into command list
                try:
                    self.command_list.load_commands(parser)
                except Exception as e:
                    # If loading commands fails, just clear it
                    self.command_list.clear()
                
                # Generate and show checklist
                try:
                    checklist_controller = ChecklistController()
                    checklist = checklist_controller.generate_checklist(parser)
                    self.content_view.show_checklist(checklist)
                except Exception as e:
                    # If checklist generation fails, clear it
                    self.content_view.clear_checklist()
            
            # Load documents
            doc_controller = DocumentController()
            output_paths = file_model.get_output_paths(doc_controller.output_dir)
            
            # Load overview
            from ..models.document_model import DocumentType
            if os.path.exists(output_paths['overview']):
                try:
                    doc_model = doc_controller.load_document(
                        output_paths['overview'],
                        DocumentType.OVERVIEW
                    )
                    if doc_model:
                        self.content_view.show_document(doc_model, "overview")
                except Exception as e:
                    # If loading fails, clear it
                    self.content_view.overview_tab.clear()
            else:
                # Clear overview if file doesn't exist
                self.content_view.overview_tab.clear()
            
            # Load docs
            if os.path.exists(output_paths['docs']):
                try:
                    doc_model = doc_controller.load_document(
                        output_paths['docs'],
                        DocumentType.DOCS
                    )
                    if doc_model:
                        self.content_view.show_document(doc_model, "docs")
                except Exception as e:
                    # If loading fails, clear it
                    self.content_view.docs_tab.clear()
            else:
                # Clear docs if file doesn't exist
                self.content_view.docs_tab.clear()
                    
        except Exception as e:
            # Silently handle errors - don't show error dialog
            # Just clear the content
            self.content_view.clear()
            self.command_list.clear()
    
    def on_process_selected(self):
        """Handle process selected button click."""
        selected_files = self.file_list.get_selected_files()
        if not selected_files:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("提示")
            msg.setText("请先选择要处理的文件。")
            msg.setStyleSheet(MODERN_STYLESHEET)
            msg.exec_()
            return
        
        self.process_files(selected_files)
    
    def on_process_all(self):
        """Handle process all button click."""
        all_files = self.file_list.get_all_files()
        if not all_files:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("提示")
            msg.setText("没有文件需要处理。")
            msg.setStyleSheet(MODERN_STYLESHEET)
            msg.exec_()
            return
        
        self.process_files(all_files)
    
    def process_files(self, files: list):
        """Process files.
        
        Args:
            files: List of FileModel instances
        """
        if self.processing_thread and self.processing_thread.isRunning():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("警告")
            msg.setText("正在处理文件，请等待完成。")
            msg.setStyleSheet(MODERN_STYLESHEET)
            msg.exec_()
            return
        
        force = self.force_checkbox.isChecked()
        
        # Create progress dialog
        self.progress_dialog = ProgressDialog(self, len(files))
        self.progress_dialog.cancelled.connect(self.on_processing_cancelled)
        
        # Create and start processing thread
        self.processing_thread = ProcessingThread(files, force)
        self.processing_thread.progress.connect(self.progress_dialog.update_progress)
        self.processing_thread.file_completed.connect(self.on_file_completed)
        self.processing_thread.finished.connect(self.on_processing_finished)
        
        self.processing_thread.start()
        self.progress_dialog.show()
    
    def on_file_completed(self, file_model: FileModel, success: bool, error: str):
        """Handle file processing completion.
        
        Args:
            file_model: FileModel instance
            success: Whether processing was successful
            error: Error message if failed
        """
        # Update file list
        self.file_list.update_file_status(file_model)
        
        # If this is the current file and processing was successful, reload content
        # This includes loading commands and checklist after processing
        if file_model == self.current_file and success:
            self.load_file_content_after_processing(file_model)
    
    def on_processing_finished(self):
        """Handle processing finished."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        # Reload content for current file if it's processed
        # This ensures content is displayed even if selection didn't change
        if self.current_file and self.current_file.status == FileStatus.PROCESSED:
            self.load_file_content_after_processing(self.current_file)
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("完成")
        msg.setText("文件处理完成！")
        msg.setStyleSheet(MODERN_STYLESHEET)
        msg.exec_()
    
    def on_processing_cancelled(self):
        """Handle processing cancellation."""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.cancel()
            self.processing_thread.wait()
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
