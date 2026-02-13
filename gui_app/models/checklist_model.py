"""
Checklist Model

Data model for checklist information.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ChecklistCategory:
    """Checklist category data."""
    name: str
    keywords: List[Dict[str, any]] = field(default_factory=list)  # [{'name': 'CONTROL_TERMINATION', 'count': 1, 'has': True}]
    has_content: bool = False
    total_count: int = 0


@dataclass
class ChecklistModel:
    """Checklist data model."""
    categories: Dict[str, ChecklistCategory] = field(default_factory=dict)
    statistics: Dict[str, int] = field(default_factory=dict)
    
    def get_total_keywords(self) -> int:
        """Get total number of keywords."""
        return sum(cat.total_count for cat in self.categories.values())
    
    def get_has_content_count(self) -> int:
        """Get number of categories with content."""
        return sum(1 for cat in self.categories.values() if cat.has_content)
