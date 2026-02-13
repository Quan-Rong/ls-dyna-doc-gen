"""
File Model

Data model for file information and processing status.
"""

import os
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class FileStatus(Enum):
    """File processing status."""
    UNPROCESSED = "unprocessed"  # 未处理
    PROCESSING = "processing"     # 处理中
    PROCESSED = "processed"      # 已处理
    ERROR = "error"              # 错误


@dataclass
class FileModel:
    """File data model."""
    path: str
    name: str = ""
    size: int = 0
    modified_time: datetime = None
    status: FileStatus = FileStatus.UNPROCESSED
    error_message: str = ""
    output_files: list = None
    
    def __post_init__(self):
        """Initialize derived fields."""
        if not self.name:
            self.name = os.path.basename(self.path)
        if not self.size and os.path.exists(self.path):
            self.size = os.path.getsize(self.path)
        if not self.modified_time and os.path.exists(self.path):
            self.modified_time = datetime.fromtimestamp(os.path.getmtime(self.path))
        if self.output_files is None:
            self.output_files = []
    
    def get_size_str(self) -> str:
        """Get formatted file size string."""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        else:
            return f"{self.size / (1024 * 1024):.2f} MB"
    
    def get_modified_time_str(self) -> str:
        """Get formatted modified time string."""
        if self.modified_time:
            return self.modified_time.strftime("%Y-%m-%d %H:%M:%S")
        return ""
    
    def check_output_exists(self, output_dir: str) -> bool:
        """Check if output files exist."""
        base_name = os.path.splitext(self.name)[0]
        docs_path = os.path.join(output_dir, f"{base_name}_docs.md")
        overview_path = os.path.join(output_dir, f"{base_name}_overview.md")
        return os.path.exists(docs_path) and os.path.exists(overview_path)
    
    def get_output_paths(self, output_dir: str) -> dict:
        """Get output file paths."""
        base_name = os.path.splitext(self.name)[0]
        return {
            'docs': os.path.join(output_dir, f"{base_name}_docs.md"),
            'overview': os.path.join(output_dir, f"{base_name}_overview.md"),
            'requirements': os.path.join(output_dir, f"{base_name}_AI_REQ.md")
        }
