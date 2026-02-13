"""
Content View Widget

Widget for managing multiple content views (tabs).
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget)
from .checklist_view import ChecklistViewWidget
from .document_view import DocumentViewWidget


class ContentViewWidget(QWidget):
    """Widget for managing content views."""
    
    def __init__(self, parent=None):
        """Initialize content view widget."""
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(False)
        
        # Checklist tab (always visible)
        self.checklist_view = ChecklistViewWidget()
        self.tab_widget.addTab(self.checklist_view, "📋 检查清单")
        
        # Document tabs (will be added dynamically)
        self.docs_tab = DocumentViewWidget()
        self.tab_widget.addTab(self.docs_tab, "📄 详细文档")
        
        self.overview_tab = DocumentViewWidget()
        self.tab_widget.addTab(self.overview_tab, "📊 概览文档")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def show_checklist(self, checklist_model):
        """Show checklist.
        
        Args:
            checklist_model: ChecklistModel instance
        """
        self.checklist_view.display_checklist(checklist_model)
    
    def clear_checklist(self):
        """Clear checklist view."""
        self.checklist_view.clear()
    
    def show_document(self, document_model, doc_type: str = "docs"):
        """Show document.
        
        Args:
            document_model: DocumentModel instance
            doc_type: Document type ("docs" or "overview")
        """
        if doc_type == "docs":
            self.docs_tab.display_document(document_model)
        elif doc_type == "overview":
            self.overview_tab.display_document(document_model)
    
    def clear(self):
        """Clear all views."""
        self.checklist_view.clear()
        self.docs_tab.clear()
        self.overview_tab.clear()
