"""
Document Controller

Business logic for document generation.
"""

import os
from typing import Optional
from ..models.file_model import FileModel
from ..models.document_model import DocumentModel, DocumentType
from ..utils.path_utils import get_project_root
from ls_dyna_md import DetailedWriter, OverviewWriter
from ls_dyna_md.writers.capability_writer import CapabilityWriter
from ls_dyna_md.writers.requirements_writer import RequirementsWriter


class DocumentController:
    """Controller for document generation operations."""
    
    def __init__(self, output_dir: Optional[str] = None, docs_dir: Optional[str] = None):
        """Initialize document controller.
        
        Args:
            output_dir: Output directory for generated documents (default: project_root/Output)
            docs_dir: Documentation directory for capability doc (default: project_root/ls_dyna_md/docs)
        """
        project_root = get_project_root()
        self.output_dir = output_dir or os.path.join(project_root, "Output")
        self.docs_dir = docs_dir or os.path.join(project_root, "ls_dyna_md", "docs")
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Ensure output directories exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
    
    def generate_documents(self, parser, file_model: FileModel, force: bool = False) -> dict:
        """Generate all documents for a parsed file.
        
        Args:
            parser: LSDynaParser instance
            file_model: FileModel instance
            force: Force regeneration even if files exist
            
        Returns:
            Dictionary with document paths and success status
        """
        base_name = os.path.splitext(file_model.name)[0]
        results = {
            'success': False,
            'docs_path': None,
            'overview_path': None,
            'requirements_path': None,
            'error': None
        }
        
        try:
            # Ensure output directory exists
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            # Generate detailed documentation
            docs_path = os.path.join(self.output_dir, f"{base_name}_docs.md")
            if force or not os.path.exists(docs_path):
                writer = DetailedWriter(parser)
                writer.generate_markdown(docs_path)
                print(f"Generated docs: {docs_path}")
            else:
                print(f"Docs already exists, skipping: {docs_path}")
            results['docs_path'] = docs_path
            
            # Generate overview documentation
            overview_path = os.path.join(self.output_dir, f"{base_name}_overview.md")
            if force or not os.path.exists(overview_path):
                overview = OverviewWriter(parser)
                overview.generate_overview(overview_path)
                print(f"Generated overview: {overview_path}")
            else:
                print(f"Overview already exists, skipping: {overview_path}")
            results['overview_path'] = overview_path
            
            # Generate requirements if needed
            req_writer = RequirementsWriter(parser)
            req_path = req_writer.generate_requirements(self.output_dir)
            if req_path:
                results['requirements_path'] = req_path
                print(f"Generated requirements: {req_path}")
            
            # Verify files were created
            if not os.path.exists(docs_path):
                raise FileNotFoundError(f"Failed to create docs file: {docs_path}")
            if not os.path.exists(overview_path):
                raise FileNotFoundError(f"Failed to create overview file: {overview_path}")
            
            results['success'] = True
            return results
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Error generating documents: {e}")
            import traceback
            traceback.print_exc()
            return results
    
    def generate_capability_doc(self):
        """Generate capability documentation (SUPPORTED_COMMANDS.md).
        
        This should be called once at application start.
        """
        cap_writer = CapabilityWriter()
        cap_writer.generate_doc(self.docs_dir)
    
    def load_document(self, file_path: str, doc_type: DocumentType) -> Optional[DocumentModel]:
        """Load a document from file.
        
        Args:
            file_path: Path to the document file
            doc_type: Type of document
            
        Returns:
            DocumentModel instance if successful, None otherwise
        """
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc_model = DocumentModel(
                file_path=file_path,
                doc_type=doc_type,
                content=content
            )
            doc_model.metadata['file_size'] = os.path.getsize(file_path)
            return doc_model
        except Exception as e:
            return None
