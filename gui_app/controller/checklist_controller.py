"""
Checklist Controller

Business logic for checklist generation.
"""

from typing import Dict
from ..models.checklist_model import ChecklistModel, ChecklistCategory
from ls_dyna_md import LSDynaParser


class ChecklistController:
    """Controller for checklist generation operations."""
    
    # 9大类关键字分类定义
    KEYWORD_CATEGORIES = {
        "控制与求解器设置": [
            "CONTROL_TERMINATION", "CONTROL_TIMESTEP", "CONTROL_HOURGLASS",
            "CONTROL_ENERGY", "CONTROL_BULK_VISCOSITY", "CONTROL_CONTACT",
            "CONTROL_SOLUTION", "CONTROL_ACCURACY", "CONTROL_OUTPUT",
            "CONTROL_IMPLICIT", "CONTROL_DYNAMIC_RELAXATION", "CONTROL_SHELL"
        ],
        "边界条件与载荷": [
            "BOUNDARY_PRESCRIBED_MOTION", "BOUNDARY_SPC", "BOUNDARY_SPC_SET",
            "LOAD_NODE", "LOAD_BODY", "LOAD_SEGMENT", "LOAD_BEAM",
            "INITIAL_VELOCITY", "INITIAL_VELOCITY_GENERATION"
        ],
        "材料定义": [
            "MAT_", "MAT_PIECEWISE_LINEAR_PLASTICITY", "MAT_ELASTIC",
            "MAT_SPOTWELD", "MAT_RIGID", "MAT_FU_CHANG_FOAM"
        ],
        "接触定义": [
            "CONTACT_", "CONTACT_AUTOMATIC", "CONTACT_TIED",
            "CONTACT_NODES_TO_SURFACE", "CONTACT_SINGLE_SURFACE"
        ],
        "网格数据": [
            "NODE", "ELEMENT_SHELL", "ELEMENT_SOLID", "ELEMENT_BEAM",
            "ELEMENT_DISCRETE", "ELEMENT_MASS", "ELEMENT_SEATBELT"
        ],
        "截面定义": [
            "SECTION_SHELL", "SECTION_SOLID", "SECTION_BEAM",
            "SECTION_DISCRETE", "SECTION_TSHELL"
        ],
        "连接与约束": [
            "CONSTRAINED_", "CONSTRAINED_INTERPOLATION_SPOTWELD",
            "CONSTRAINED_NODAL_RIGID_BODY", "CONSTRAINED_JOINT",
            "CONSTRAINED_RIGID_BODIES", "CONSTRAINED_EXTRA_NODES",
            "JOINT_", "RIGID_BODY"
        ],
        "输出设置": [
            "DATABASE_", "DATABASE_BINARY_D3PLOT", "DATABASE_GLSTAT",
            "DATABASE_HISTORY_NODE", "DATABASE_CROSS_SECTION",
            "DATABASE_EXTENT_BINARY", "DATABASE_NODOUT"
        ],
        "其他关键字": []  # 其他未分类的关键字
    }
    
    def __init__(self):
        """Initialize checklist controller."""
        pass
    
    def generate_checklist(self, parser: LSDynaParser) -> ChecklistModel:
        """Generate checklist from parser data.
        
        Args:
            parser: LSDynaParser instance
            
        Returns:
            ChecklistModel instance
        """
        checklist = ChecklistModel()
        
        # Get all keywords from parser
        keywords = parser.keywords
        
        # Categorize keywords
        categorized = self._categorize_keywords(keywords)
        
        # Create categories
        for cat_name, cat_keywords in categorized.items():
            category = ChecklistCategory(name=cat_name)
            
            for kw_name, kw_count in cat_keywords:
                category.keywords.append({
                    'name': kw_name,
                    'count': kw_count,
                    'has': True
                })
                category.total_count += kw_count
            
            category.has_content = len(category.keywords) > 0
            checklist.categories[cat_name] = category
        
        # Calculate statistics
        checklist.statistics = {
            'total_keywords': checklist.get_total_keywords(),
            'categories_with_content': checklist.get_has_content_count(),
            'total_categories': len(checklist.categories)
        }
        
        return checklist
    
    def _categorize_keywords(self, keywords: Dict[str, int]) -> Dict[str, list]:
        """Categorize keywords into 9 categories.
        
        Args:
            keywords: Dictionary of keyword names and counts
            
        Returns:
            Dictionary mapping category names to lists of (keyword, count) tuples
        """
        categorized = {cat_name: [] for cat_name in self.KEYWORD_CATEGORIES.keys()}
        other_keywords = []
        
        for kw_name, kw_count in keywords.items():
            categorized_flag = False
            
            # Check each category
            for cat_name, cat_keywords in self.KEYWORD_CATEGORIES.items():
                if cat_name == "其他关键字":
                    continue
                
                # Check if keyword matches any pattern in this category
                for pattern in cat_keywords:
                    if pattern.endswith("_"):
                        # Prefix match (e.g., "MAT_", "CONTACT_")
                        if kw_name.startswith(pattern):
                            categorized[cat_name].append((kw_name, kw_count))
                            categorized_flag = True
                            break
                    else:
                        # Exact match
                        if kw_name == pattern:
                            categorized[cat_name].append((kw_name, kw_count))
                            categorized_flag = True
                            break
                
                if categorized_flag:
                    break
            
            # If not categorized, add to "其他关键字"
            if not categorized_flag:
                other_keywords.append((kw_name, kw_count))
        
        categorized["其他关键字"] = other_keywords
        
        return categorized
