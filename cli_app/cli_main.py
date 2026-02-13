"""
CLI Application Main Logic

This module contains the main business logic for the CLI application.
The entry point (cli_app/main.py) imports and calls functions from here.
"""

import sys
import os
import glob
import time

from ls_dyna_md import __version__, LSDynaParser, DetailedWriter, OverviewWriter
from ls_dyna_md.writers.capability_writer import CapabilityWriter
from ls_dyna_md.writers.requirements_writer import RequirementsWriter

INPUT_DIR = "Input"
OUTPUT_DIR = "Output"
DOCS_DIR = "ls_dyna_md/docs"  # For SUPPORTED_COMMANDS.md (auto-generated)


def ensure_io_dirs():
    """Ensure standard Input/Output directories exist."""
    # Get project root directory (parent of cli_app)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, INPUT_DIR)
    output_path = os.path.join(base_dir, OUTPUT_DIR)
    docs_path = os.path.join(base_dir, DOCS_DIR)
    
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"Created standard input directory: {input_path}")
        print("Please place your .key files here.")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created standard output directory: {output_path}")

    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        print(f"Created documentation directory: {docs_path}")

    return input_path, output_path, docs_path


def process_file(filepath, output_base_dir):
    """Process a single LS-Dyna key file and generate documentation."""
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")
    
    start_time = time.time()
    
    try:
        # 1. Parse
        parser = LSDynaParser(filepath)
        parser.parse()
    except Exception as e:
        print(f"[ERROR] Error parsing {filename}: {e}")
        return False

    base_name = os.path.splitext(filename)[0]
    docs_path = os.path.join(output_base_dir, f"{base_name}_docs.md")
    overview_path = os.path.join(output_base_dir, f"{base_name}_overview.md")

    # 2. Generate Documentation
    try:
        print("  Generating Detailed Documentation...")
        writer = DetailedWriter(parser)
        writer.generate_markdown(docs_path)

        print("  Generating Engineering Overview...")
        overview = OverviewWriter(parser)
        overview.generate_overview(overview_path)
        
        elapsed = time.time() - start_time
        print(f"[SUCCESS] Success! ({elapsed:.2f}s)")
        print(f"  -> {docs_path}")
        print(f"  -> {overview_path}")
        
        # 3. Check for Requirements
        req_writer = RequirementsWriter(parser)
        req_path = req_writer.generate_requirements(output_base_dir)
        if req_path:
            print(f"  [WARNING] Generated AI Requirements: {req_path}")
            
        return True

    except Exception as e:
        print(f"[ERROR] Error generating docs for {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for CLI application."""
    print(f"==================================================")
    print(f"   LS-Dyna Documentation Generator v{__version__}")
    print(f"==================================================")
    
    input_dir, output_dir, docs_dir = ensure_io_dirs()
    
    # Generate capabilities doc at start
    cap_writer = CapabilityWriter()
    cap_writer.generate_doc(docs_dir)
    
    # Check for force flag
    force_mode = "--force" in sys.argv
    
    # Mode 1: Process specific file argument (if provided and not a flag)
    # Mode 2: Batch process Input/ directory (default)
    
    target_files = []
    
    # Simple arg parsing ignoring flags
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    
    if args:
        arg_path = args[0]
        if os.path.isfile(arg_path):
            target_files.append(arg_path)
        elif os.path.isdir(arg_path):
            # If user points to a directory, scan it
            target_files.extend(glob.glob(os.path.join(arg_path, "*.key")))
            target_files.extend(glob.glob(os.path.join(arg_path, "*.k")))
        else:
            # Maybe filename inside Input dir
            potential_path = os.path.join(input_dir, arg_path)
            if os.path.exists(potential_path):
                target_files.append(potential_path)
            else:
                print(f"Error: File not found: {arg_path}")
                return
    else:
        # Default: Scan Input dir
        print(f"Scanning directory: {input_dir}")
        target_files.extend(glob.glob(os.path.join(input_dir, "*.key")))
        target_files.extend(glob.glob(os.path.join(input_dir, "*.k")))

    if not target_files:
        print(f"No LS-Dyna keyword files (*.key, *.k) found in {input_dir}")
        print("Please place your input files in the 'Input' folder.")
        return

    print(f"Found {len(target_files)} files to check.")
    
    success_count = 0
    skipped_count = 0
    
    for f in target_files:
        filename = os.path.basename(f)
        base_name = os.path.splitext(filename)[0]
        
        # Check expected outputs
        docs_path = os.path.join(output_dir, f"{base_name}_docs.md")
        overview_path = os.path.join(output_dir, f"{base_name}_overview.md")
        
        if os.path.exists(docs_path) and os.path.exists(overview_path) and not force_mode:
            print(f"[SKIP] Skipping {filename} (Output exists)")
            skipped_count += 1
            continue
            
        if process_file(f, output_dir):
            success_count += 1
            
    print(f"\nProcessing complete:")
    print(f"  [SUCCESS] Processed: {success_count}")
    print(f"  [SKIP] Skipped:   {skipped_count}")
    print(f"  [ERROR] Failed:    {len(target_files) - success_count - skipped_count}")
