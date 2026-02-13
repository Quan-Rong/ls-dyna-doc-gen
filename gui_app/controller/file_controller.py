"""
File Controller

Business logic for file processing.
"""

import os
from typing import List, Optional
from ..models.file_model import FileModel, FileStatus
from ..utils.path_utils import get_project_root
from ls_dyna_md import LSDynaParser


class FileController:
    """Controller for file processing operations."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """Initialize file controller.
        
        Args:
            output_dir: Output directory for generated documents (default: project_root/Output)
        """
        project_root = get_project_root()
        self.output_dir = output_dir or os.path.join(project_root, "Output")
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_file_model(self, filepath: str) -> FileModel:
        """Create a FileModel from file path.
        
        Args:
            filepath: Path to the .key file
            
        Returns:
            FileModel instance
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_model = FileModel(path=filepath)
        
        # Check if already processed
        if file_model.check_output_exists(self.output_dir):
            file_model.status = FileStatus.PROCESSED
        
        return file_model
    
    def check_file_status(self, file_model: FileModel) -> FileStatus:
        """Check and update file processing status.
        
        Args:
            file_model: FileModel instance
            
        Returns:
            Updated FileStatus
        """
        if file_model.check_output_exists(self.output_dir):
            file_model.status = FileStatus.PROCESSED
        else:
            file_model.status = FileStatus.UNPROCESSED
        
        return file_model.status
    
    def parse_file(self, file_model: FileModel, update_status: bool = False) -> Optional[LSDynaParser]:
        """Parse a .key file.
        
        Args:
            file_model: FileModel instance
            update_status: Whether to update file status during parsing
            
        Returns:
            LSDynaParser instance if successful, None otherwise
        """
        try:
            if update_status:
                file_model.status = FileStatus.PROCESSING
            parser = LSDynaParser(file_model.path)
            parser.parse()
            return parser
        except Exception as e:
            if update_status:
                file_model.status = FileStatus.ERROR
                file_model.error_message = str(e)
            return None
