import os
from datetime import datetime

class RequirementsWriter:
    def __init__(self, parser):
        self.unknown = parser.unknown_keywords
        self.filepath = parser.filepath
        
    def generate_requirements(self, output_dir):
        if not self.unknown:
            return None
            
        filename = os.path.basename(self.filepath)
        base = os.path.splitext(filename)[0]
        req_filename = f"{base}_AI_REQ.md"
        output_path = os.path.join(output_dir, req_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# AI Coding Requirement: Unhandled LS-Dyna Keywords\n\n")
            f.write(f"**Source File:** `{filename}`\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("> **Instruction for AI Agent:**\n")
            f.write("> The following keywords were found in the input file but are not yet supported by the parser.\n")
            f.write("> Please use the provided snippets to implement parsing logic in `ls_dyna_md/parser.py` and documentation logic in `ls_dyna_md/writers/detailed_writer.py`.\n\n")
            
            for i, (kw, data) in enumerate(sorted(self.unknown.items()), 1):
                f.write(f"## {i}. `*{kw}`\n")
                f.write(f"- **Found at Line:** {data['line']}\n")
                f.write(f"- **Context Snippet:**\n")
                f.write("```lsdyna\n")
                for l in data['snippet']:
                    f.write(l + "\n")
                f.write("```\n")
                f.write(f"- **Implementation Task:**\n")
                f.write(f"  1. Add `elif current_keyword == '{kw}':` block in `parser.py`.\n")
                f.write(f"  2. Extract relevant parameters based on LS-Dyna manual.\n")
                f.write(f"  3. Add a corresponding `_write_{kw.lower()}` method in `detailed_writer.py`.\n")
                f.write(f"  4. Add description to `utils/supported_commands.py`.\n\n")
                
        return output_path
