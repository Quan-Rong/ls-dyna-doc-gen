"""
Checklist View Widget

Widget for displaying checklist.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                               QLabel, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ..models.checklist_model import ChecklistModel, ChecklistCategory


class ChecklistViewWidget(QWidget):
    """Widget for displaying checklist."""
    
    def __init__(self, parent=None):
        """Initialize checklist view widget."""
        super().__init__(parent)
        self.checklist_model = None
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
        
        header_label = QLabel("检查清单")
        header_label.setProperty("class", "header")
        header_layout.addWidget(header_label)
        
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        # Tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["项目", "状态", "数量"])
        self.tree_widget.setColumnWidth(0, 350)
        self.tree_widget.setColumnWidth(1, 80)
        self.tree_widget.setColumnWidth(2, 100)
        self.tree_widget.header().setStretchLastSection(False)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.setAnimated(True)
        layout.addWidget(self.tree_widget, 1)
        
        # Statistics label
        self.stats_label = QLabel("")
        self.stats_label.setProperty("class", "status")
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
    
    def display_checklist(self, checklist_model: ChecklistModel):
        """Display checklist model.
        
        Args:
            checklist_model: ChecklistModel instance
        """
        self.checklist_model = checklist_model
        self.tree_widget.clear()
        
        if not checklist_model:
            return
        
        # Add categories
        for cat_name, category in checklist_model.categories.items():
            cat_item = QTreeWidgetItem(self.tree_widget)
            cat_item.setText(0, cat_name)
            
            # Status icon
            if category.has_content:
                cat_item.setText(1, "✓")
                cat_item.setText(2, f"{category.total_count} 个")
                cat_item.setForeground(0, self.tree_widget.palette().color(self.tree_widget.palette().Text))
            else:
                cat_item.setText(1, "○")
                cat_item.setText(2, "0 个")
                # Gray out empty categories
                gray_color = QColor(148, 163, 184)  # text_tertiary
                cat_item.setForeground(0, gray_color)
                cat_item.setForeground(1, gray_color)
                cat_item.setForeground(2, gray_color)
            
            # Add keywords
            for kw_info in category.keywords:
                kw_item = QTreeWidgetItem(cat_item)
                kw_item.setText(0, f"*{kw_info['name']}")
                kw_item.setText(1, "✓")
                kw_item.setText(2, f"{kw_info['count']} 个")
            
            # Expand category if it has content
            if category.has_content:
                cat_item.setExpanded(True)
        
        # Update statistics
        stats = checklist_model.statistics
        stats_text = f"总计: {stats.get('total_keywords', 0)} 个关键字, "
        stats_text += f"{stats.get('categories_with_content', 0)} 个类别有内容"
        self.stats_label.setText(stats_text)
    
    def clear(self):
        """Clear checklist display."""
        self.tree_widget.clear()
        self.stats_label.setText("")
        self.checklist_model = None
