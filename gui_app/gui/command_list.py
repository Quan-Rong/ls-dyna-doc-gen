"""
Command List Widget

Displays LS-DYNA commands found in the parsed file.
Clicking a command shows its description and parameters.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QLabel, QTextEdit, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ls_dyna_md.utils.supported_commands import SUPPORTED_COMMANDS_DATA


class CommandListWidget(QWidget):
    """Widget to display LS-DYNA commands and their descriptions."""
    
    def __init__(self, parent=None):
        """Initialize command list widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title label
        title_label = QLabel("LS-DYNA 命令列表")
        title_label.setProperty("class", "subheader")
        layout.addWidget(title_label)
        
        # Splitter for command list and description (vertical layout: top list, bottom description)
        splitter = QSplitter(Qt.Vertical)
        
        # Top: Command list
        self.command_list = QListWidget()
        self.command_list.setProperty("class", "command-list")
        self.command_list.itemClicked.connect(self.on_command_selected)
        splitter.addWidget(self.command_list)
        
        # Bottom: Command description
        desc_widget = QWidget()
        desc_layout = QVBoxLayout()
        desc_layout.setSpacing(8)
        desc_layout.setContentsMargins(12, 12, 12, 12)
        
        desc_title = QLabel("命令说明")
        desc_title.setProperty("class", "subheader")
        desc_layout.addWidget(desc_title)
        
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setProperty("class", "command-description")
        self.description_text.setPlaceholderText("点击上方命令查看详细说明...")
        desc_layout.addWidget(self.description_text)
        
        desc_widget.setLayout(desc_layout)
        splitter.addWidget(desc_widget)
        
        # Set splitter proportions (50% list, 50% description)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def clear(self):
        """Clear command list and description."""
        self.command_list.clear()
        self.description_text.clear()
        self.description_text.setPlaceholderText("点击上方命令查看详细说明...")
    
    def load_commands(self, parser):
        """Load commands from parser.
        
        Args:
            parser: LSDynaParser instance
        """
        self.clear()
        
        if not parser or not hasattr(parser, 'keywords'):
            return
        
        # Get all unique commands
        commands = sorted(parser.keywords.keys())
        
        for cmd in commands:
            count = parser.keywords[cmd]
            # Format: "COMMAND_NAME (出现次数)"
            item_text = f"{cmd} ({count})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, cmd)  # Store original command name
            self.command_list.addItem(item)
        
        # If no commands, show placeholder
        if not commands:
            self.description_text.setPlaceholderText("未找到任何命令")
    
    def on_command_selected(self, item):
        """Handle command selection.
        
        Args:
            item: Selected QListWidgetItem
        """
        if not item:
            return
        
        command_name = item.data(Qt.UserRole)
        if not command_name:
            return
        
        # Get command description
        description = self.get_command_description(command_name)
        self.description_text.setHtml(description)
    
    def get_command_description(self, command_name):
        """Get formatted description for a command.
        
        Args:
            command_name: Command name (e.g., "PART", "MAT_PIECEWISE_LINEAR_PLASTICITY")
            
        Returns:
            HTML formatted description
        """
        # Try exact match first
        if command_name in SUPPORTED_COMMANDS_DATA:
            cmd_data = SUPPORTED_COMMANDS_DATA[command_name]
            return self.format_description(command_name, cmd_data)
        
        # Try prefix matching for patterns like "MAT_***", "SECTION_***"
        # Sort patterns by length (longest first) to match more specific patterns first
        patterns = sorted(SUPPORTED_COMMANDS_DATA.items(), 
                         key=lambda x: len(x[0]) if "***" in x[0] else 0, 
                         reverse=True)
        
        for pattern, cmd_data in patterns:
            if "***" in pattern:
                prefix = pattern.replace("***", "")
                if command_name.startswith(prefix):
                    return self.format_description(command_name, cmd_data)
        
        # No description found
        return self.format_unknown_command(command_name)
    
    def format_description(self, command_name, cmd_data):
        """Format command description as HTML.
        
        Args:
            command_name: Command name
            cmd_data: Command data dictionary with desc, params, example
            
        Returns:
            HTML formatted string
        """
        html = f"""
        <div style="font-family: 'Microsoft YaHei', Arial, sans-serif;">
            <h3 style="color: #2c3e50; margin-top: 0;">*{command_name}</h3>
            
            <h4 style="color: #34495e; margin-top: 16px; margin-bottom: 8px;">功能说明</h4>
            <p style="line-height: 1.6; color: #555;">{cmd_data.get('desc', '暂无说明')}</p>
            
            <h4 style="color: #34495e; margin-top: 16px; margin-bottom: 8px;">参数说明</h4>
            <p style="line-height: 1.6; color: #555;">{cmd_data.get('params', '暂无参数说明')}</p>
        """
        
        if 'example' in cmd_data:
            html += f"""
            <h4 style="color: #34495e; margin-top: 16px; margin-bottom: 8px;">示例</h4>
            <pre style="background-color: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 11pt; line-height: 1.4;">{cmd_data['example']}</pre>
            """
        
        html += "</div>"
        return html
    
    def format_unknown_command(self, command_name):
        """Format description for unknown command.
        
        Args:
            command_name: Command name
            
        Returns:
            HTML formatted string
        """
        return f"""
        <div style="font-family: 'Microsoft YaHei', Arial, sans-serif;">
            <h3 style="color: #2c3e50; margin-top: 0;">*{command_name}</h3>
            <p style="line-height: 1.6; color: #999; font-style: italic;">
                该命令暂未收录说明信息。如需了解详细信息，请参考 LS-DYNA 官方文档。
            </p>
        </div>
        """
