"""
Test script for minimal file processing

This script tests the core functionality without GUI.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui_app.controller.file_controller import FileController
from gui_app.controller.document_controller import DocumentController
from gui_app.controller.checklist_controller import ChecklistController

def test_minimal_file():
    """Test processing the smallest key file."""
    # Find the smallest file
    input_dir = "Input"
    files = []
    for f in os.listdir(input_dir):
        if f.endswith('.key'):
            filepath = os.path.join(input_dir, f)
            size = os.path.getsize(filepath)
            files.append((filepath, size))
    
    if not files:
        print("No .key files found in Input directory")
        return False
    
    # Sort by size and get smallest
    files.sort(key=lambda x: x[1])
    smallest_file = files[0][0]
    print(f"Testing with smallest file: {os.path.basename(smallest_file)} ({files[0][1] / (1024*1024):.2f} MB)")
    
    try:
        # Create controllers
        file_controller = FileController()
        doc_controller = DocumentController()
        checklist_controller = ChecklistController()
        
        # Create file model
        file_model = file_controller.create_file_model(smallest_file)
        print(f"File model created: {file_model.name}")
        print(f"Status: {file_model.status.value}")
        
        # Parse file
        print("\nParsing file...")
        parser = file_controller.parse_file(file_model)
        if not parser:
            print(f"ERROR: Failed to parse file: {file_model.error_message}")
            return False
        
        print(f"Parsed successfully. Found {len(parser.keywords)} keywords")
        
        # Generate documents
        print("\nGenerating documents...")
        results = doc_controller.generate_documents(parser, file_model, force=False)
        if not results['success']:
            print(f"ERROR: Failed to generate documents: {results.get('error')}")
            return False
        
        print(f"Documents generated successfully:")
        if results.get('docs_path'):
            print(f"  - {results['docs_path']}")
        if results.get('overview_path'):
            print(f"  - {results['overview_path']}")
        if results.get('requirements_path'):
            print(f"  - {results['requirements_path']}")
        
        # Generate checklist
        print("\nGenerating checklist...")
        checklist = checklist_controller.generate_checklist(parser)
        print(f"Checklist generated: {len(checklist.categories)} categories")
        print(f"Total keywords: {checklist.get_total_keywords()}")
        print(f"Categories with content: {checklist.get_has_content_count()}")
        
        # Print category summary
        print("\nCategory summary:")
        for cat_name, category in checklist.categories.items():
            if category.has_content:
                print(f"  {cat_name}: {category.total_count} keywords")
        
        print("\n[SUCCESS] All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_minimal_file()
    sys.exit(0 if success else 1)
