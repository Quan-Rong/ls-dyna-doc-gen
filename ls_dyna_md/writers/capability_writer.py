import os
from datetime import datetime
from ..utils.supported_commands import SUPPORTED_COMMANDS_DATA

class CapabilityWriter:
    def generate_doc(self, output_dir):
        """Generates the SUPPORTED_COMMANDS.md file in the doc directory."""
        output_path = os.path.join(output_dir, "SUPPORTED_COMMANDS.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Supported LS-Dyna Commands\n\n")
            f.write(f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("This document lists all LS-Dyna keywords currently supported by the parser.\n")
            f.write("It serves as a reference for users and a capability matrix for AI development.\n\n")
            
            f.write("| Command | Function | Parameters | Example |\n")
            f.write("|---|---|---|---|\n")
            
            for cmd, info in sorted(SUPPORTED_COMMANDS_DATA.items()):
                # Format example for markdown table
                # We replace newlines with <br> to keep it compact but readable
                example = info['example'].replace('\n', '<br>')
                params = info['params']
                desc = info['desc']
                
                # Using <code> for command to make it pop
                cmd_str = f"`*{cmd}`"
                
                f.write(f"| {cmd_str} | {desc} | {params} | <small>{example}</small> |\n")
                
        return output_path
