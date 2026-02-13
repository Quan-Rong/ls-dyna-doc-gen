"""
Document Model

Data model for document information.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DocumentType(Enum):
    """Document type."""
    DOCS = "docs"           # 详细文档
    OVERVIEW = "overview"    # 概览文档
    REQUIREMENTS = "requirements"  # AI需求文档


@dataclass
class DocumentModel:
    """Document data model."""
    file_path: str
    doc_type: DocumentType
    content: str = ""
    metadata: dict = None
    
    def __post_init__(self):
        """Initialize metadata."""
        if self.metadata is None:
            self.metadata = {
                'generated_time': datetime.now(),
                'file_size': 0
            }
