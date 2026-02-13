from datetime import datetime
import os
from collections import defaultdict
from ..utils.descriptions import get_keyword_description

class DetailedWriter:
    def __init__(self, parser):
        self.parser = parser

    def __getattr__(self, name):
        return getattr(self.parser, name)

    def generate_markdown(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as md:
            # Header
            md.write(f"# \U0001f3d7\ufe0f LS-Dyna Model Analysis: {self.title}\n\n")
            md.write(f"**Filename:** `{self.filename}`  \n")
            md.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            md.write(f"**File Size:** {os.path.getsize(self.filepath) / (1024*1024):.2f} MB  \n")
            md.write("---\n\n")

            # Table of Contents
            md.write("## \U0001f4d1 Table of Contents\n\n")
            md.write("1. [\U0001f4c3 File Header Comments](#1--file-header-comments)\n")
            md.write("2. [\U0001f4cb Keyword Summary](#2--keyword-summary)\n")
            md.write("3. [\U0001f4c7 Model Metadata](#3--model-metadata)\n")
            md.write("4. [\U0001f4e6 Assembly & Includes](#4--assembly--includes)\n")
            md.write("5. [\U0001f4ca Mesh Statistics](#5--mesh-statistics)\n")
            md.write("6. [\U0001f4cd Node Definitions](#6--node-definitions)\n")
            md.write("7. [\U0001f3ed Parts Catalog](#7--parts-catalog)\n")
            md.write("8. [\U0001f9f1 Materials](#8--materials)\n")
            md.write("9. [\u2702\ufe0f Sections](#9--sections)\n")
            md.write("10. [\U0001f9e9 Elements](#10--elements)\n")
            md.write("11. [\U0001f91d Contacts](#11--contacts)\n")
            md.write("12. [\U0001f517 Constraints](#12--constraints)\n")
            md.write("13. [\U0001f4c2 Sets](#13--sets)\n")
            md.write("14. [\U0001f4c8 Curves](#14--curves)\n")
            md.write("15. [\u2699\ufe0f Parameters](#15--parameters)\n")
            md.write("16. [\U0001f30a Damping Definitions](#16--damping-definitions)\n")
            md.write("17. [\U0001f4be Database Output Controls](#17--database-output-controls)\n")
            md.write("18. [\U0001f3af Initial Conditions](#18--initial-conditions)\n")
            md.write("19. [\U0001f4ca Complete Keyword Statistics](#19--complete-keyword-statistics)\n\n")

            # 1. File Header Comments
            self._write_header_comments(md)
            
            # 2. Keyword Summary
            self._write_keyword_summary(md)
            
            # 3. Metadata
            self._write_metadata(md)
            
            # 4. Includes
            self._write_includes(md)
            
            # 5. Mesh Statistics
            self._write_mesh_statistics(md)
            
            # 6. Node Definitions
            self._write_node_definitions(md)
            
            # 7. Parts Catalog
            self._write_parts_catalog(md)
            
            # 8. Materials
            self._write_materials(md)
            
            # 9. Sections
            self._write_sections(md)
            
            # 10. Elements
            self._write_elements(md)
            
            # 11. Contacts
            self._write_contacts(md)
            
            # 12. Constraints
            self._write_constraints(md)
            
            # 13. Sets
            self._write_sets(md)
            
            # 14. Curves
            self._write_curves(md)
            
            # 15. Parameters
            self._write_parameters(md)
            
            # 16. Damping Definitions
            self._write_damping(md)
            
            # 17. Database Output Controls
            self._write_database_outputs(md)
            
            # 18. Initial Conditions
            self._write_initial_conditions(md)
            
            # 19. Complete Keyword Statistics
            self._write_complete_statistics(md)

    def _write_header_comments(self, md):
        md.write("## 1. \U0001f4c3 File Header Comments\n\n")
        md.write("> \u2139\ufe0f \u6587\u4ef6\u5934\u90e8\u6ce8\u91ca\u5305\u542b\u6a21\u578b\u5206\u7c7b\u3001\u7248\u672c\u548c\u5de5\u7a0b\u5143\u4fe1\u606f\u3002\n\n")
        
        if self.header_comments:
            header_data = []
            current_key = None
            current_value = []
            in_multiline = False
            
            for comment in self.header_comments:
                clean_comment = comment.lstrip("$").strip()
                
                if not clean_comment:
                    continue
                
                if "<<MULTI_LINE" in clean_comment:
                    in_multiline = True
                    if "=" in clean_comment:
                        parts = clean_comment.split("=", 1)
                        current_key = parts[0].strip()
                    continue
                
                if "MULTI_LINE>>" in clean_comment:
                    in_multiline = False
                    if current_key and current_value:
                        header_data.append((current_key, "<br>".join(current_value)))
                        current_key = None
                        current_value = []
                    continue
                
                if in_multiline:
                    current_value.append(clean_comment)
                    continue
                
                if "=" in clean_comment:
                    parts = clean_comment.split("=", 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    header_data.append((key, value))
                else:
                    header_data.append(("Comment", clean_comment))
            
            md.write("| Property | Value |\n")
            md.write("|---|---|\n")
            for key, value in header_data:
                if len(str(value)) > 200:
                    value = str(value)[:197] + "..."
                md.write(f"| **{key}** | {value} |\n")
        else:
            md.write("*No header comments found.*\n")
        md.write("\n")

    def _write_keyword_summary(self, md):
        """写入关键字统计摘要（第2章）。
        
        遍历所有解析到的关键字，按出现次数降序排列，
        并附上每个关键字的物理含义描述。
        """
        md.write("## 2. \U0001f4cb Keyword Summary\n\n")
        md.write("> \U0001f4ca \u6a21\u578b\u4e2d\u4f7f\u7528\u7684\u6240\u6709 LS-DYNA \u5173\u952e\u5b57\u53ca\u5176\u51fa\u73b0\u6b21\u6570\u3002\n\n")
        
        md.write("| Keyword | Count | Description |\n")
        md.write("|---|---|---|\n")
        
        sorted_keywords = sorted(self.keywords.items(), key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords:
            desc = get_keyword_description(keyword)
            md.write(f"| `*{keyword}` | {count:,} | {desc} |\n")
        md.write("\n")

    def _write_metadata(self, md):
        md.write("## 3. \U0001f4c7 Model Metadata\n\n")
        if self.metadata:
            md.write("| Property | Value |\n")
            md.write("|---|---|\n")
            for key, value in self.metadata.items():
                if len(str(value)) > 100:
                    value = str(value)[:97] + "..."
                md.write(f"| `{key}` | {value} |\n")
        else:
            md.write("*\u2139\ufe0f \u672a\u5728\u6587\u4ef6\u4e2d\u68c0\u6d4b\u5230\u5143\u6570\u636e\u3002*\n")
        md.write("\n")

    def _write_includes(self, md):
        md.write("## 4. \U0001f4e6 Assembly & Includes\n")
        md.write(f"**Total Included Files:** {len(self.includes)}\n\n")
        if self.includes:
            md.write("| # | Type | Filename | Transform ID |\n")
            md.write("|---|---|---|---|\n")
            for idx, inc in enumerate(self.includes, 1):
                trans_info = inc.get('trans_id', '-') or '-'
                md.write(f"| {idx} | **{inc['type']}** | `{inc['filename']}` | {trans_info} |\n")
        else:
            md.write("*\U0001f4e6 \u8fd9\u662f\u4e00\u4e2a\u72ec\u7acb\u7684\u7ec4\u4ef6\u6587\u4ef6\uff0c\u4e0d\u5305\u542b Include \u6587\u4ef6\u3002*\n")
        md.write("\n")

    def _write_mesh_statistics(self, md):
        md.write("## 5. \U0001f4ca Mesh Statistics\n\n")
        
        total_elements = sum(elem_data["count"] for elem_data in self.elements.values())
        
        md.write("| Entity Type | Count |\n")
        md.write("|---|---|\n")
        md.write(f"| **Nodes** | {self.node_count:,} |\n")
        md.write(f"| **Total Elements** | {total_elements:,} |\n")
        
        for elem_type, elem_data in sorted(self.elements.items()):
            md.write(f"| - {elem_type} Elements | {elem_data['count']:,} |\n")
        
        md.write(f"| **Total Parts** | {len(self.parts):,} |\n")
        md.write(f"| **Unique Section IDs** | {len(self.unique_secids):,} |\n")
        md.write(f"| **Unique Material IDs** | {len(self.unique_mids):,} |\n")
        md.write("\n")

    def _write_node_definitions(self, md):
        md.write("## 6. \U0001f4cd Node Definitions\n\n")
        md.write(f"**Total Nodes:** {self.node_count:,}\n\n")
        
        if self.node_ranges:
            # 按节点数量排序，取前10个主要号段
            sorted_ranges = sorted(self.node_ranges, key=lambda x: x[2], reverse=True)[:10]
            
            md.write("### Major Node Ranges (Top 10 by count)\n\n")
            md.write("| Range # | Start Node ID | End Node ID | Count |\n")
            md.write("|---|---|---|---|\n")
            for idx, (start, end, count) in enumerate(sorted_ranges, 1):
                md.write(f"| {idx} | {start:,} | {end:,} | {count:,} |\n")
            
            if len(self.node_ranges) > 10:
                md.write(f"\n*... and {len(self.node_ranges) - 10} more node ranges*\n")
        else:
            md.write("*No node range information available.*\n")
        md.write("\n")

    def _write_parts_catalog(self, md):
        md.write("## 7. \U0001f3ed Parts Catalog\n\n")
        md.write(f"> \U0001f9e9 **\u603b\u90e8\u4ef6\u6570:** {len(self.parts)}\n\n")
        
        if self.parts:
            parts_by_type = defaultdict(list)
            for part in self.parts:
                parts_by_type[part['type']].append(part)
            
            for part_type, parts_list in sorted(parts_by_type.items()):
                md.write(f"### {part_type} ({len(parts_list)} parts)\n\n")
                
                # 添加格式说明
                if part_type == "PART_COMPOSITE":
                    md.write("**Format:** `*PART_COMPOSITE`\n")
                    md.write("```\n")
                    md.write("PID    SECID  MID    ...\n")
                    md.write("```\n")
                    md.write("**Description:** Composite material parts with multiple layers. ")
                    md.write("These parts typically use glass fiber reinforced plastics (e.g., GB215HP) ")
                    md.write("with layered construction for structural components.\n\n")
                
                md.write("| PID | Title | Section ID | Material ID |\n")
                md.write("|---|---|---|---|\n")
                for part in parts_list[:30]:
                    pid = part.get('pid', '-')
                    secid = part.get('secid', '-')
                    mid = part.get('mid', '-')
                    title = part.get('title', 'Untitled')
                    md.write(f"| {pid} | {title} | {secid} | {mid} |\n")
                
                if len(parts_list) > 30:
                    md.write(f"*... and {len(parts_list) - 30} more parts (省略)*\n")
                md.write("\n")
        else:
            md.write("*No parts defined in this file.*\n\n")

    def _write_materials(self, md):
        md.write("## 8. \U0001f9f1 Materials\n\n")
        md.write(f"> \U0001f52c **\u603b\u6750\u6599\u6570:** {len(self.materials)}\n\n")
        
        if self.materials:
            mats_by_type = defaultdict(list)
            for mat in self.materials:
                mats_by_type[mat['type']].append(mat)
            
            for mat_type, mats_list in sorted(mats_by_type.items()):
                md.write(f"### {mat_type}\n\n")
                
                # 命令解释
                md.write(f"**Description:** Material model `{mat_type}` defines material properties for structural analysis.\n\n")
                
                # Format 展示
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("*" + mat_type + "\n")
                md.write("TITLE\n")
                md.write("MID  RO  E  PR  SIGY  ETAN  ...\n")
                md.write("(Additional property lines)\n")
                md.write("```\n\n")
                
                # 参数说明
                md.write("**Parameters:**\n")
                md.write("- MID: Material ID\n")
                md.write("- RO: Mass density\n")
                md.write("- E: Young's modulus\n")
                md.write("- PR: Poisson's ratio\n")
                md.write("- Additional parameters vary by material type\n\n")
                
                # 表格列出前30项
                md.write(f"**Material List ({len(mats_list)} total):**\n\n")
                md.write("| # | Material Title | Properties (first 3 lines) |\n")
                md.write("|---|---|---|\n")
                
                for idx, mat in enumerate(mats_list[:30], 1):
                    title = mat.get('title', 'Untitled')
                    props_str = " / ".join(mat['properties'][:3]) if mat['properties'] else "N/A"
                    if len(props_str) > 100:
                        props_str = props_str[:97] + "..."
                    md.write(f"| {idx} | {title} | `{props_str}` |\n")
                
                if len(mats_list) > 30:
                    md.write(f"\n*... and {len(mats_list) - 30} more materials (省略)*\n")
                md.write("\n")
        else:
            md.write("*\U0001f9f1 \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u6750\u6599\uff08\u53ef\u80fd\u5728\u4e3b\u6a21\u578b\u6216\u5176\u4ed6 Include \u6587\u4ef6\u4e2d\u5b9a\u4e49\uff09\u3002*\n\n")

    def _write_sections(self, md):
        md.write("## 9. \u2702\ufe0f Sections\n\n")
        md.write(f"> \U0001f4d0 **\u603b\u622a\u9762\u6570:** {len(self.sections)}\n\n")
        
        if self.sections:
            secs_by_type = defaultdict(list)
            for sec in self.sections:
                secs_by_type[sec['type']].append(sec)
            
            for sec_type, secs_list in sorted(secs_by_type.items()):
                md.write(f"### {sec_type}\n\n")
                
                # 命令解释
                if "SHELL" in sec_type:
                    md.write("**Description:** Shell section properties define element formulation, thickness, and integration points for shell elements. ")
                    md.write("Linked to PART via SECID. For PART_CONTACT, defines contact surface properties.\n\n")
                elif "BEAM" in sec_type:
                    md.write("**Description:** Beam section properties define cross-sectional geometry and integration scheme for beam elements.\n\n")
                elif "SOLID" in sec_type:
                    md.write("**Description:** Solid section properties define element formulation for solid elements.\n\n")
                else:
                    md.write(f"**Description:** Section properties for `{sec_type}`.\n\n")
                
                # Format 展示
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("*" + sec_type + "\n")
                md.write("TITLE\n")
                if "SHELL" in sec_type:
                    md.write("SECID  ELFORM  SHRF  NIP  PROPT  QR/IRID  ICOMP\n")
                    md.write("T1     T2      T3    T4   NLOC   MAREA    IDOF\n")
                elif "BEAM" in sec_type:
                    md.write("SECID  ELFORM  SHRF  QR/IRID  CST  SCOOR\n")
                    md.write("(Cross-section parameters)\n")
                elif "SOLID" in sec_type:
                    md.write("SECID  ELFORM\n")
                md.write("```\n\n")
                
                # 参数说明
                md.write("**Parameters:**\n")
                if "SHELL" in sec_type:
                    md.write("- SECID: Section ID (links to PART)\n")
                    md.write("- ELFORM: Element formulation (2=Belytschko-Tsay, etc.)\n")
                    md.write("- SHRF: Shear correction factor\n")
                    md.write("- NIP: Number of integration points through thickness\n")
                    md.write("- T1-T4: Thickness at nodes 1-4\n\n")
                elif "BEAM" in sec_type:
                    md.write("- SECID: Section ID (links to PART)\n")
                    md.write("- ELFORM: Element formulation\n")
                    md.write("- Cross-section geometry parameters\n\n")
                elif "SOLID" in sec_type:
                    md.write("- SECID: Section ID (links to PART)\n")
                    md.write("- ELFORM: Element formulation\n\n")
                
                # 表格列出前30项
                md.write(f"**Section List ({len(secs_list)} total):**\n\n")
                md.write("| # | Section Title | Properties (first 2 lines) |\n")
                md.write("|---|---|---|\n")
                
                for idx, sec in enumerate(secs_list[:30], 1):
                    title = sec.get('title', 'Untitled')
                    props_str = " / ".join(sec['properties'][:2]) if sec['properties'] else "N/A"
                    if len(props_str) > 100:
                        props_str = props_str[:97] + "..."
                    md.write(f"| {idx} | {title} | `{props_str}` |\n")
                
                if len(secs_list) > 30:
                    md.write(f"\n*... and {len(secs_list) - 30} more sections (省略)*\n")
                md.write("\n")
        else:
            md.write("*\u2702\ufe0f \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u622a\u9762\u5c5e\u6027\u3002*\n\n")

    def _write_elements(self, md):
        md.write("## 10. \U0001f9e9 Elements\n\n")
        
        for elem_type, elem_data in sorted(self.elements.items()):
            md.write(f"### ELEMENT_{elem_type}\n")
            md.write(f"**Total Count:** {elem_data['count']:,}\n\n")
            
            # 添加格式说明
            if elem_type == "BEAM":
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  PID  N1  N2  N3  RT1  RT2  LOCAL\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- PID: Part ID (links to material and section)\n")
                md.write("- N1, N2: Node IDs defining the beam axis\n")
                md.write("- N3: Third node for orientation (0 = automatic)\n\n")
                
                # 统计涉及的材料
                beam_pids = set()
                for sample in elem_data['samples']:
                    parts = sample.split()
                    if len(parts) >= 2:
                        beam_pids.add(parts[1])
                md.write(f"**Unique Part IDs used:** {len(beam_pids)}\n\n")
            
            elif elem_type == "BEAM_ORIENTATION":
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  PID  N1  N2\n")
                md.write("VX   VY   VZ\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- PID: Part ID\n")
                md.write("- N1, N2: Node IDs\n")
                md.write("- VX, VY, VZ: Orientation vector components\n\n")
            
            elif elem_type == "SHELL":
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  PID  N1  N2  N3  N4\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- PID: Part ID\n")
                md.write("- N1-N4: Node IDs (N4=0 for triangular elements)\n\n")
            
            elif elem_type == "SHELL_THICKNESS":
                md.write("**Description:** Shell elements with variable thickness defined at each node. ")
                md.write("Used when thickness varies across the element for more accurate structural response.\n\n")
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  PID  N1  N2  N3  N4\n")
                md.write("THIC1  THIC2  THIC3  THIC4\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- PID: Part ID\n")
                md.write("- N1-N4: Node IDs\n")
                md.write("- THIC1-THIC4: Shell thickness at each node\n\n")
            
            elif elem_type == "SOLID":
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  PID  N1  N2  N3  N4  N5  N6  N7  N8\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- PID: Part ID\n")
                md.write("- N1-N8: Node IDs (hex), N1-N4 for tet\n\n")
            
            elif elem_type == "MASS":
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("EID  NID  MASS  PID\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- EID: Element ID\n")
                md.write("- NID: Node ID where mass is applied\n")
                md.write("- MASS: Lumped mass value\n")
                md.write("- PID: Part ID for output grouping\n\n")
            
            elif elem_type == "SEATBELT_ACCELEROMETER":
                md.write("**Description:** Defines an accelerometer element for seatbelt system. ")
                md.write("Used in occupant safety simulations to trigger seatbelt retractor locking mechanisms.\n\n")
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("SBACID  N1  N2  N3  IGRAV  ICOORD  RADIUS\n")
                md.write("```\n")
                md.write("**Parameters:**\n")
                md.write("- SBACID: Seatbelt accelerometer ID\n")
                md.write("- N1, N2, N3: Nodes defining the accelerometer coordinate system\n")
                md.write("- IGRAV: Gravity vector flag\n")
                md.write("- ICOORD: Coordinate system flag\n\n")
            
            if elem_data['samples']:
                md.write("**Sample Elements (first 30):**\n\n")
                md.write("| # | Element Data |\n")
                md.write("|---|---|\n")
                for idx, sample in enumerate(elem_data['samples'][:30], 1):
                    md.write(f"| {idx} | `{sample}` |\n")
                
                if elem_data['count'] > 30:
                    md.write(f"\n*... and {elem_data['count'] - 30} more elements (省略)*\n")
            md.write("\n")

    def _write_contacts(self, md):
        md.write("## 11. \U0001f91d Contacts\n\n")
        md.write(f"> \U0001f517 **\u603b\u63a5\u89e6\u5b9a\u4e49\u6570:** {len(self.contacts)}\n\n")
        
        if self.contacts:
            contacts_by_type = defaultdict(list)
            for contact in self.contacts:
                contacts_by_type[contact['type']].append(contact)
            
            for contact_type, contacts_list in sorted(contacts_by_type.items()):
                md.write(f"### {contact_type}\n\n")
                
                # 命令解释
                md.write(f"**Description:** Contact definition `{contact_type}` establishes interaction between surfaces or parts.\n\n")
                
                # Format 展示
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("*" + contact_type + "\n")
                md.write("TITLE\n")
                md.write("SSID  MSID  SSTYP  MSTYP  SBOXID  MBOXID  SPR  MPR  ...\n")
                md.write("FS    FD    DC     VC     VDC     PENCHK  BT   DT   ...\n")
                md.write("```\n\n")
                
                # 参数说明
                md.write("**Parameters:**\n")
                md.write("- SSID: Slave segment/part set ID\n")
                md.write("- MSID: Master segment/part set ID\n")
                md.write("- FS: Static coefficient of friction\n")
                md.write("- FD: Dynamic coefficient of friction\n")
                md.write("- Additional parameters control contact behavior\n\n")
                
                # 表格列出前30项
                md.write(f"**Contact List ({len(contacts_list)} total):**\n\n")
                md.write("| # | Contact Title | SSID | MSID |\n")
                md.write("|---|---|---|---|\n")
                
                for idx, contact in enumerate(contacts_list[:30], 1):
                    title = contact.get('title', 'Untitled')
                    ssid = contact.get('ssid', '-')
                    msid = contact.get('msid', '-')
                    md.write(f"| {idx} | {title} | {ssid} | {msid} |\n")
                
                if len(contacts_list) > 30:
                    md.write(f"\n*... and {len(contacts_list) - 30} more contacts (省略)*\n")
                md.write("\n")
        else:
            md.write("*\U0001f91d \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u63a5\u89e6\u5173\u7cfb\uff08\u53ef\u80fd\u5728\u4e3b\u6a21\u578b\u4e2d\u5b9a\u4e49\uff09\u3002*\n\n")

    def _write_constraints(self, md):
        md.write("## 12. \U0001f517 Constraints\n\n")
        md.write(f"> \U0001f527 **\u603b\u7ea6\u675f\u6570:** {len(self.constraints)}\n\n")
        
        # Rigid Bodies
        if self.rigid_bodies:
            md.write("### CONSTRAINED_NODAL_RIGID_BODY\n\n")
            md.write("**Description:** Defines a set of nodes as a rigid body that moves as a single entity.\n\n")
            md.write("**Format:**\n")
            md.write("```\n")
            md.write("PID  CID  NSID  PNODE  IPRT  DRFLAG  RRFLAG\n")
            md.write("```\n\n")
            md.write("**Parameters:**\n")
            md.write("- PID: Part ID for the rigid body\n")
            md.write("- NSID: Node Set ID containing all rigid body nodes\n")
            md.write("- PNODE: Primary node (0 = auto-calculated center of mass)\n")
            md.write("- DRFLAG: Translational constraint flag (0 = free)\n")
            md.write("- RRFLAG: Rotational constraint flag (0 = free)\n\n")
            md.write("**Interpretation:** All nodes in the node set maintain their relative positions ")
            md.write("and move together as a rigid body. The primary node (or center of mass if PNODE=0) ")
            md.write("serves as the reference point for the rigid body motion.\n\n")
            
            md.write("| # | PID | NSID | PNODE | DRFLAG | RRFLAG |\n")
            md.write("|---|---|---|---|---|---|\n")
            for idx, rb in enumerate(self.rigid_bodies[:30], 1):
                data = rb.get('data', [])
                if len(data) >= 5:
                    md.write(f"| {idx} | {data[0]} | {data[2] if len(data) > 2 else '-'} | {data[3] if len(data) > 3 else '0'} | {data[4] if len(data) > 4 else '0'} | {data[5] if len(data) > 5 else '0'} |\n")
            
            if len(self.rigid_bodies) > 30:
                md.write(f"\n*... and {len(self.rigid_bodies) - 30} more (省略)*\n")
            md.write("\n")
        
        # Joints
        if self.joints:
            md.write("### CONSTRAINED_JOINT_REVOLUTE_ID\n\n")
            md.write("**Description:** Defines a revolute (hinge) joint between two parts.\n\n")
            md.write("**Format:**\n")
            md.write("```\n")
            md.write("JID  N1  N2  N3  N4  ...\n")
            md.write("```\n\n")
            md.write("**Parameters:**\n")
            md.write("- JID: Joint ID\n")
            md.write("- N1, N2: Nodes defining the rotation axis\n")
            md.write("- N3, N4: Additional constraint nodes\n\n")
            
            md.write("| # | Joint ID | Node 1 | Node 2 | Node 3 | Node 4 |\n")
            md.write("|---|---|---|---|---|---|\n")
            for idx, joint in enumerate(self.joints[:30], 1):
                data = joint.get('data', [])
                jid = data[0] if len(data) > 0 else '-'
                n1 = data[1] if len(data) > 1 else '-'
                n2 = data[2] if len(data) > 2 else '-'
                n3 = data[3] if len(data) > 3 else '-'
                n4 = data[4] if len(data) > 4 else '-'
                md.write(f"| {idx} | {jid} | {n1} | {n2} | {n3} | {n4} |\n")
            
            if len(self.joints) > 30:
                md.write(f"\n*... and {len(self.joints) - 30} more (省略)*\n")
            md.write("\n")

    def _write_sets(self, md):
        md.write("## 13. \U0001f4c2 Sets\n\n")
        md.write(f"> \U0001f4c1 **\u603b\u96c6\u5408\u6570:** {len(self.sets)}\n\n")
        
        if self.sets:
            sets_by_type = defaultdict(list)
            for s in self.sets:
                sets_by_type[s['type']].append(s)
            
            # 首先显示统计摘要
            md.write("### Set Statistics Summary\n\n")
            md.write("| Set Type | Count | Description |\n")
            md.write("|---|---|---|\n")
            for set_type, sets_list in sorted(sets_by_type.items()):
                if "NODE" in set_type:
                    desc = "Node sets"
                elif "PART" in set_type:
                    desc = "Part sets"
                elif "SHELL" in set_type:
                    desc = "Shell element sets"
                else:
                    desc = "Other sets"
                md.write(f"| `*{set_type}` | {len(sets_list)} | {desc} |\n")
            md.write("\n")
            
            # 然后详细列出每种类型
            for set_type, sets_list in sorted(sets_by_type.items()):
                md.write(f"### {set_type}\n\n")
                
                # 命令解释
                if "NODE" in set_type:
                    md.write("**Description:** Each entry defines a node set that groups nodes for boundary conditions, output requests, or contact definitions. ")
                    md.write("Each title represents one individual node set.\n\n")
                elif "PART" in set_type:
                    md.write("**Description:** Each entry defines a part set that groups parts for contact, output, or material assignment. ")
                    md.write("Each title represents one individual part set.\n\n")
                elif "SHELL" in set_type:
                    md.write("**Description:** Each entry defines a shell element set that groups shell elements for specific operations. ")
                    md.write("Each title represents one individual shell element set.\n\n")
                else:
                    md.write(f"**Description:** Set definition for `{set_type}`. Each title represents one individual set.\n\n")
                
                # Format 展示
                md.write("**Format:**\n")
                md.write("```\n")
                md.write("*" + set_type + "\n")
                if "TITLE" in set_type:
                    md.write("TITLE\n")
                md.write("SID  ...\n")
                md.write("(List of IDs)\n")
                md.write("```\n\n")
                
                # 参数说明
                md.write("**Parameters:**\n")
                md.write("- SID: Set ID (unique identifier)\n")
                if "NODE" in set_type:
                    md.write("- List of node IDs belonging to this set\n\n")
                elif "PART" in set_type:
                    md.write("- List of part IDs belonging to this set\n\n")
                else:
                    md.write("- List of element IDs belonging to this set\n\n")
                
                # 表格列出前30项
                md.write(f"**Individual Sets ({len(sets_list)} total):**\n\n")
                md.write("| # | Set ID/Title | Type |\n")
                md.write("|---|---|---|\n")
                
                for idx, s in enumerate(sets_list[:30], 1):
                    title = s.get('title', 'Untitled')
                    set_type_short = "Node Set" if "NODE" in set_type else ("Part Set" if "PART" in set_type else "Element Set")
                    md.write(f"| {idx} | {title} | {set_type_short} |\n")
                
                if len(sets_list) > 30:
                    md.write(f"\n*... and {len(sets_list) - 30} more sets (省略)*\n")
                md.write("\n")
        else:
            md.write("*\U0001f4c2 \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u96c6\u5408\u3002*\n\n")

    def _write_curves(self, md):
        md.write("## 14. \U0001f4c8 Curves\n\n")
        md.write(f"> \U0001f4c9 **\u603b\u66f2\u7ebf\u6570:** {len(self.curves)}\n\n")
        
        if self.curves:
            for idx, curve in enumerate(self.curves[:50], 1):
                md.write(f"{idx}. {curve['title']}\n")
            
            if len(self.curves) > 50:
                md.write(f"*... and {len(self.curves) - 50} more curves (省略)*\n")
            md.write("\n")
        else:
            md.write("*\U0001f4c8 \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u8f7d\u8377\u66f2\u7ebf\u3002*\n\n")

    def _write_parameters(self, md):
        md.write("## 15. \u2699\ufe0f Parameters\n\n")
        md.write(f"> \U0001f4dd **\u603b\u53c2\u6570\u6570:** {len(self.parameters)}\n\n")
        
        if self.parameters:
            md.write("| Parameter Name | Value |\n")
            md.write("|---|---|\n")
            for name, value in sorted(self.parameters.items()):
                md.write(f"| `{name}` | `{value}` |\n")
        else:
            md.write("*\u2699\ufe0f \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u5168\u5c40\u53c2\u6570\u3002*\n")
        md.write("\n")

    def _write_damping(self, md):
        """写入阻尼定义章节（第16章）。
        
        DAMPING_PART_STIFFNESS 为特定部件施加刚度比例阻尼，
        控制高频振荡，物理上等效于 Rayleigh 阻尼的刚度项。
        """
        md.write("## 16. \U0001f30a Damping Definitions\n\n")
        md.write(f"> \U0001f4a7 **\u603b\u963b\u5c3c\u5b9a\u4e49\u6570:** {len(self.damping)}\n\n")
        
        if self.damping:
            damp_by_type = defaultdict(list)
            for d in self.damping:
                damp_by_type[d['type']].append(d)
            
            for damp_type, damp_list in sorted(damp_by_type.items()):
                md.write(f"### {damp_type}\n\n")
                
                if "PART_STIFFNESS" in damp_type:
                    md.write("**Description:** Applies stiffness-proportional damping to specific parts. ")
                    md.write("This is the stiffness term of Rayleigh damping (C = β·K), ")
                    md.write("effective at suppressing high-frequency oscillations in explicit dynamics.\n\n")
                    md.write("**Format:**\n")
                    md.write("```\n")
                    md.write("*DAMPING_PART_STIFFNESS\n")
                    md.write("PID  COEF\n")
                    md.write("```\n\n")
                    md.write("**Parameters:**\n")
                    md.write("- PID: Part ID to apply damping\n")
                    md.write("- COEF: Damping coefficient (β)\n\n")
                else:
                    md.write(f"**Description:** Damping definition `{damp_type}`.\n\n")
                
                md.write(f"**Damping List ({len(damp_list)} total):**\n\n")
                md.write("| # | Data |\n")
                md.write("|---|---|\n")
                for idx, d in enumerate(damp_list[:30], 1):
                    data_str = " / ".join(d['data'][:2]) if d['data'] else "N/A"
                    if len(data_str) > 100:
                        data_str = data_str[:97] + "..."
                    md.write(f"| {idx} | `{data_str}` |\n")
                md.write("\n")
        else:
            md.write("*\U0001f30a \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u963b\u5c3c\u3002*\n\n")

    def _write_database_outputs(self, md):
        """写入数据库输出控制章节（第17章）。
        
        DATABASE 关键字控制求解过程中的数据输出，
        包括截面力输出、节点历史输出等后处理所需数据。
        """
        md.write("## 17. \U0001f4be Database Output Controls\n\n")
        md.write(f"> \U0001f4bf **\u603b\u6570\u636e\u5e93\u8f93\u51fa\u5b9a\u4e49\u6570:** {len(self.database_outputs)}\n\n")
        
        if self.database_outputs:
            db_by_type = defaultdict(list)
            for db in self.database_outputs:
                db_by_type[db['type']].append(db)
            
            for db_type, db_list in sorted(db_by_type.items()):
                md.write(f"### {db_type}\n\n")
                
                if "CROSS_SECTION_PLANE" in db_type:
                    md.write("**Description:** Defines a cross-section plane for measuring resultant forces and moments. ")
                    md.write("Used for barrier force output, section force analysis, and structural load paths.\n\n")
                    md.write("**Format:**\n")
                    md.write("```\n")
                    md.write("*DATABASE_CROSS_SECTION_PLANE_ID\n")
                    md.write("CSID  TITLE\n")
                    md.write("XCT  YCT  ZCT  XCH  YCH  ZCH\n")
                    md.write("XHH  YHH  ZHH  LENL  LENM  ID  ITYPE\n")
                    md.write("```\n\n")
                    md.write("**Parameters:**\n")
                    md.write("- CSID: Cross-section ID\n")
                    md.write("- XCT,YCT,ZCT: Tail coordinates of section normal vector\n")
                    md.write("- XCH,YCH,ZCH: Head coordinates of section normal vector\n")
                    md.write("- LENL,LENM: Section plane dimensions\n\n")
                elif "HISTORY_NODE" in db_type:
                    md.write("**Description:** Specifies nodes for time-history output (d3thdt). ")
                    md.write("Displacement, velocity, and acceleration of these nodes are recorded for post-processing.\n\n")
                    md.write("**Format:**\n")
                    md.write("```\n")
                    md.write("*DATABASE_HISTORY_NODE\n")
                    md.write("ID1  ID2  ID3  ID4  ID5  ID6  ID7  ID8\n")
                    md.write("```\n\n")
                    md.write("**Parameters:**\n")
                    md.write("- IDn: Node IDs for history output\n\n")
                else:
                    md.write(f"**Description:** Database output definition `{db_type}`.\n\n")
                
                md.write(f"**Output Definitions ({len(db_list)} total):**\n\n")
                md.write("| # | Data (first 2 lines) |\n")
                md.write("|---|---|\n")
                for idx, db in enumerate(db_list[:30], 1):
                    data_str = " / ".join(db['data'][:2]) if db['data'] else "N/A"
                    if len(data_str) > 100:
                        data_str = data_str[:97] + "..."
                    md.write(f"| {idx} | `{data_str}` |\n")
                md.write("\n")
        else:
            md.write("*\U0001f4be \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u6570\u636e\u5e93\u8f93\u51fa\u63a7\u5236\u3002*\n\n")

    def _write_initial_conditions(self, md):
        """写入初始条件章节（第18章）。
        
        INITIAL_ 关键字定义模型的初始状态，
        如梁单元初始轴力（螺栓预紧力）、初始速度等。
        """
        md.write("## 18. \U0001f3af Initial Conditions\n\n")
        md.write(f"> \U0001f680 **\u603b\u521d\u59cb\u6761\u4ef6\u5b9a\u4e49\u6570:** {len(self.initial_conditions)}\n\n")
        
        if self.initial_conditions:
            init_by_type = defaultdict(list)
            for ic in self.initial_conditions:
                init_by_type[ic['type']].append(ic)
            
            for init_type, init_list in sorted(init_by_type.items()):
                md.write(f"### {init_type}\n\n")
                
                if "AXIAL_FORCE_BEAM" in init_type:
                    md.write("**Description:** Defines initial axial force in beam elements. ")
                    md.write("Commonly used for bolt preload simulation - the beam element starts with a pre-defined tension force ")
                    md.write("to represent the clamping force of a bolted joint.\n\n")
                    md.write("**Format:**\n")
                    md.write("```\n")
                    md.write("*INITIAL_AXIAL_FORCE_BEAM\n")
                    md.write("EID  FORCE\n")
                    md.write("```\n\n")
                    md.write("**Parameters:**\n")
                    md.write("- EID: Beam element ID\n")
                    md.write("- FORCE: Initial axial force value (positive = tension)\n\n")
                elif "STRESS_SHELL" in init_type:
                    md.write("**Description:** Defines initial stress state in shell elements. ")
                    md.write("Commonly used to map residual stresses from metal forming simulations (stamping) ")
                    md.write("into the crash model, improving prediction accuracy for energy absorption.\n\n")
                    md.write("**Format:**\n")
                    md.write("```\n")
                    md.write("*INITIAL_STRESS_SHELL\n")
                    md.write("EID  NPLANE  NTHICK  NHISV  LARGE\n")
                    md.write("T  SIGXX  SIGYY  SIGZZ  SIGXY  SIGYZ  SIGZX  EPS\n")
                    md.write("```\n\n")
                    md.write("**Parameters:**\n")
                    md.write("- EID: Shell element ID\n")
                    md.write("- NPLANE: Number of in-plane integration points\n")
                    md.write("- NTHICK: Number of through-thickness integration points\n")
                    md.write("- SIGXX, SIGYY, SIGZZ: Normal stress components\n")
                    md.write("- SIGXY, SIGYZ, SIGZX: Shear stress components\n")
                    md.write("- EPS: Effective plastic strain\n\n")
                else:
                    md.write(f"**Description:** Initial condition definition `{init_type}`.\n\n")
                
                md.write(f"**Initial Condition List ({len(init_list)} total):**\n\n")
                md.write("| # | Data (first 2 lines) |\n")
                md.write("|---|---|\n")
                for idx, ic in enumerate(init_list[:30], 1):
                    data_str = " / ".join(ic['data'][:2]) if ic['data'] else "N/A"
                    if len(data_str) > 100:
                        data_str = data_str[:97] + "..."
                    md.write(f"| {idx} | `{data_str}` |\n")
                md.write("\n")
        else:
            md.write("*\U0001f3af \u672c\u6587\u4ef6\u672a\u5b9a\u4e49\u521d\u59cb\u6761\u4ef6\u3002*\n\n")

    def _write_complete_statistics(self, md):
        md.write("## 19. \U0001f4ca Complete Keyword Statistics\n\n")
        md.write("> \U0001f4cb \u6240\u6709\u5173\u952e\u5b57\u7684\u5b8c\u6574\u7edf\u8ba1\uff08\u6309\u51fa\u73b0\u6b21\u6570\u964d\u5e8f\uff09\u3002\n\n")
        md.write("| Keyword | Count |\n")
        md.write("|---|---|\n")
        sorted_keywords = sorted(self.keywords.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_keywords:
            md.write(f"| `*{k}` | {v:,} |\n")

    # =========================================================================
    # Overview 文件生成 (高级工程分析摘要)
    # =========================================================================
