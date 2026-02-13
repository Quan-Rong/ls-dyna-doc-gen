import os
import re
import sys
from datetime import datetime
from collections import defaultdict

class LSDynaParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.work_dir = os.path.dirname(filepath)
        
        # Data storage
        self.title = "Unknown Title"
        self.includes = []
        self.parameters = {}
        self.keywords = {}
        self.unknown_keywords = {}  # Store unhandled keywords for AI analysis
        self.transformations = {}
        self.hierarchy_comments = []
        self.metadata = {}
        self.header_comments = []
        
        # Detailed entity storage
        self.parts = []
        self.materials = []
        self.sections = []
        self.contacts = []
        self.sets = []
        self.constraints = []
        self.curves = []
        self.nodes = []  # Store node ranges
        self.elements = defaultdict(list)  # {type: [element_data]}
        self.joints = []  # Joint definitions
        self.rigid_bodies = []  # Rigid body definitions
        self.spotweld_constraints = []  # CONSTRAINED_INTERPOLATION_SPOTWELD
        self.damping = []  # DAMPING_ definitions
        self.database_outputs = []  # DATABASE_ output controls
        self.initial_conditions = []  # INITIAL_ conditions
        
        # Statistics
        self.node_count = 0
        self.node_ranges = []  # [(start, end, count)]
        self.unique_secids = set()
        self.unique_mids = set()
        
        # Regex patterns
        self.re_keyword = re.compile(r'^\*([A-Za-z0-9_]+)(.*)')
        self.re_param = re.compile(r'^\s*[RI]\s+([A-Za-z0-9_]+)\s+([0-9\.\-\+eE]+)')
        self.re_component = re.compile(r'^\$\s*components\.component\[.*')

    def parse(self):
        if not os.path.exists(self.filepath):
            print(f"Error: File not found - {self.filepath}")
            return

        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        current_keyword = None
        current_title = None
        i = 0
        in_header = True
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 1. 处理注释
            if line.startswith("$"):
                if in_header:
                    self.header_comments.append(line)
                
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) >= 2:
                        key = parts[0].strip().lstrip("$").strip()
                        value = parts[1].strip()
                        self.metadata[key] = value
                        if "definition.label" in key:
                            self.title = value
                
                if self.re_component.match(line):
                    self.hierarchy_comments.append(line.lstrip("$").strip())
                i += 1
                continue

            # 2. 处理关键字
            if line.startswith("*"):
                in_header = False
                
                if line.startswith("*END"):
                    break
                    
                match = self.re_keyword.match(line)
                if match:
                    current_keyword = match.group(1).upper()
                    keyword_suffix = match.group(2).strip()
                    
                    # 提取 TITLE 后缀
                    if "_TITLE" in current_keyword or keyword_suffix:
                        if i + 1 < len(lines):
                            next_line = lines[i+1].strip()
                            if next_line and not next_line.startswith("*") and not next_line.startswith("$"):
                                current_title = next_line
                    
                    self.keywords[current_keyword] = self.keywords.get(current_keyword, 0) + 1
                    
                    # === 详细解析各类实体 ===
                    
                    # TITLE
                    if current_keyword == "TITLE":
                        if i + 1 < len(lines):
                            self.title = lines[i+1].strip()
                        i += 2
                        continue

                    # PARAMETER
                    elif current_keyword.startswith("PARAMETER"):
                        j = i + 1
                        while j < len(lines) and not lines[j].startswith("*"):
                            p_line = lines[j].strip()
                            if not p_line.startswith("$"):
                                p_match = self.re_param.match(p_line)
                                if p_match:
                                    self.parameters[p_match.group(1)] = p_match.group(2)
                            j += 1
                        i = j
                        continue

                    # PART
                    elif current_keyword in ["PART", "PART_COMPOSITE", "PART_CONTACT"]:
                        part_data = {"type": current_keyword, "title": "Untitled"}
                        j = i + 1
                        
                        # 读取标题行
                        if j < len(lines):
                            title_line = lines[j].strip()
                            if title_line and not title_line.startswith("*") and not title_line.startswith("$"):
                                part_data["title"] = title_line
                                j += 1
                        
                        # 跳过注释行
                        while j < len(lines) and lines[j].strip().startswith("$"):
                            j += 1
                        
                        # 读取 PART 数据行
                        if j < len(lines):
                            data_line = lines[j].strip()
                            if not data_line.startswith("*") and not data_line.startswith("$"):
                                parts = data_line.split()
                                if len(parts) >= 3:
                                    part_data["pid"] = parts[0]
                                    part_data["secid"] = parts[1]
                                    part_data["mid"] = parts[2]
                                    
                                    # 收集唯一的 SECID 和 MID
                                    self.unique_secids.add(parts[1])
                                    self.unique_mids.add(parts[2])
                        
                        self.parts.append(part_data)
                        current_title = None

                    # MATERIAL
                    elif current_keyword.startswith("MAT_"):
                        mat_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "properties": []
                        }
                        j = i + 1
                        if current_title:
                            j += 1
                        
                        # 读取材料数据
                        line_count = 0
                        while j < len(lines) and line_count < 5:
                            data_line = lines[j].strip()
                            if data_line.startswith("*"):
                                break
                            if data_line and not data_line.startswith("$"):
                                mat_data["properties"].append(data_line)
                                line_count += 1
                            j += 1
                        
                        self.materials.append(mat_data)
                        current_title = None

                    # SECTION
                    elif current_keyword.startswith("SECTION_"):
                        sec_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "properties": []
                        }
                        j = i + 1
                        if current_title:
                            j += 1
                        
                        # 读取截面数据
                        line_count = 0
                        while j < len(lines) and line_count < 10:
                            data_line = lines[j].strip()
                            if data_line.startswith("*"):
                                break
                            if data_line and not data_line.startswith("$"):
                                sec_data["properties"].append(data_line)
                                line_count += 1
                            j += 1
                        
                        self.sections.append(sec_data)
                        current_title = None

                    # CONTACT
                    elif current_keyword.startswith("CONTACT_"):
                        contact_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled"
                        }
                        # 提取 SSID 和 MSID
                        j = i + 1
                        if current_title:
                            j += 1
                        while j < len(lines) and lines[j].strip().startswith("$"):
                            j += 1
                        if j < len(lines):
                            data_line = lines[j].strip()
                            if not data_line.startswith("*") and not data_line.startswith("$"):
                                parts = data_line.split()
                                if len(parts) >= 2:
                                    contact_data["ssid"] = parts[0]
                                    contact_data["msid"] = parts[1]
                        self.contacts.append(contact_data)
                        current_title = None

                    # SET
                    elif current_keyword.startswith("SET_"):
                        set_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled"
                        }
                        # 提取 SID
                        j = i + 1
                        if current_title:
                            j += 1
                        while j < len(lines) and lines[j].strip().startswith("$"):
                            j += 1
                        if j < len(lines):
                            data_line = lines[j].strip()
                            if not data_line.startswith("*") and not data_line.startswith("$"):
                                parts = data_line.split()
                                if parts:
                                    set_data["sid"] = parts[0]
                        self.sets.append(set_data)
                        current_title = None

                    # CONSTRAINED
                    elif current_keyword.startswith("CONSTRAINED_"):
                        constraint_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "data": []
                        }
                        
                        # 特殊处理 JOINT 和 RIGID_BODY
                        if "JOINT" in current_keyword:
                            j = i + 1
                            while j < len(lines) and lines[j].strip().startswith("$"):
                                j += 1
                            if j < len(lines):
                                data_line = lines[j].strip()
                                if not data_line.startswith("*"):
                                    constraint_data["data"] = data_line.split()
                            self.joints.append(constraint_data)
                        elif "RIGID_BODY" in current_keyword:
                            j = i + 1
                            while j < len(lines) and lines[j].strip().startswith("$"):
                                j += 1
                            if j < len(lines):
                                data_line = lines[j].strip()
                                if not data_line.startswith("*"):
                                    constraint_data["data"] = data_line.split()
                            self.rigid_bodies.append(constraint_data)
                        elif "INTERPOLATION_SPOTWELD" in current_keyword:
                            # 解析焊点插值约束的详细数据
                            j = i + 1
                            while j < len(lines) and lines[j].strip().startswith("$"):
                                j += 1
                            if j < len(lines):
                                data_line = lines[j].strip()
                                if not data_line.startswith("*"):
                                    parts = data_line.split()
                                    if len(parts) >= 3:
                                        constraint_data["pid1"] = parts[0]
                                        constraint_data["pid2"] = parts[1]
                                        constraint_data["nsid"] = parts[2]
                                    if len(parts) >= 5:
                                        constraint_data["thick"] = parts[3]
                                        constraint_data["radius"] = parts[4]
                            self.spotweld_constraints.append(constraint_data)
                        
                        self.constraints.append(constraint_data)
                        current_title = None

                    # DEFINE_CURVE
                    elif current_keyword.startswith("DEFINE_CURVE"):
                        curve_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled"
                        }
                        self.curves.append(curve_data)
                        current_title = None

                    # NODE
                    elif current_keyword == "NODE":
                        j = i + 1
                        node_ids = []
                        while j < len(lines):
                            node_line = lines[j].strip()
                            if node_line.startswith("*"):
                                break
                            if node_line and not node_line.startswith("$"):
                                parts = node_line.split()
                                if parts:
                                    try:
                                        node_ids.append(int(parts[0]))
                                        self.node_count += 1
                                    except:
                                        pass
                            j += 1
                        
                        # 计算节点号段
                        if node_ids:
                            node_ids.sort()
                            ranges = []
                            start = node_ids[0]
                            prev = node_ids[0]
                            count = 1
                            
                            for nid in node_ids[1:]:
                                if nid == prev + 1:
                                    count += 1
                                    prev = nid
                                else:
                                    ranges.append((start, prev, count))
                                    start = nid
                                    prev = nid
                                    count = 1
                            ranges.append((start, prev, count))
                            self.node_ranges.extend(ranges)
                        
                        i = j
                        continue

                    # ELEMENT
                    elif current_keyword.startswith("ELEMENT_"):
                        elem_type = current_keyword.replace("ELEMENT_", "")
                        j = i + 1
                        elem_count = 0
                        elem_samples = []
                        
                        while j < len(lines):
                            elem_line = lines[j].strip()
                            if elem_line.startswith("*"):
                                break
                            if elem_line and not elem_line.startswith("$"):
                                if elem_count < 30:  # 只保存前30个样本
                                    elem_samples.append(elem_line)
                                elem_count += 1
                            j += 1
                        
                        self.elements[elem_type] = {
                            "count": elem_count,
                            "samples": elem_samples
                        }
                        i = j
                        continue

                    # INCLUDE
                    elif "INCLUDE" in current_keyword:
                        if i + 1 < len(lines):
                            inc_file = lines[i+1].strip()
                            if inc_file.startswith("$"):
                                i += 1
                                continue
                                
                            inc_type = "TRANSFORM" if "TRANSFORM" in current_keyword else "STANDARD"
                            trans_id = None
                            
                            if inc_type == "TRANSFORM":
                                for k in range(i+2, min(i+20, len(lines))):
                                    if lines[k].startswith("*"):
                                        break
                                    if "tranid" in lines[k].lower():
                                        parts = lines[k].split()
                                        if parts:
                                            trans_id = parts[-1]
                                        break
                            
                            self.includes.append({
                                "type": inc_type,
                                "filename": inc_file,
                                "trans_id": trans_id
                            })
                            
                            if inc_type == "TRANSFORM":
                                j = i + 2
                                while j < len(lines) and not lines[j].startswith("*") and (j - i < 20):
                                    j += 1
                                i = j
                            else:
                                i += 2
                        else:
                            i += 1
                        continue

                    # DEFINE_TRANSFORMATION
                    elif current_keyword.startswith("DEFINE_TRANSFORMATION"):
                        trans_id = "Unknown"
                        if i + 1 < len(lines) and not lines[i+1].startswith("*"):
                            parts = lines[i+1].split()
                            if parts:
                                trans_id = parts[0]
                        self.transformations[trans_id] = current_keyword

                    # DAMPING (阻尼定义)
                    elif current_keyword.startswith("DAMPING_"):
                        damp_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "data": []
                        }
                        j = i + 1
                        if current_title:
                            j += 1
                        line_count = 0
                        while j < len(lines) and line_count < 5:
                            data_line = lines[j].strip()
                            if data_line.startswith("*"):
                                break
                            if data_line and not data_line.startswith("$"):
                                damp_data["data"].append(data_line)
                                line_count += 1
                            j += 1
                        self.damping.append(damp_data)
                        current_title = None

                    # DATABASE (数据库输出控制)
                    elif current_keyword.startswith("DATABASE_"):
                        db_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "data": []
                        }
                        j = i + 1
                        if current_title:
                            j += 1
                        line_count = 0
                        while j < len(lines) and line_count < 10:
                            data_line = lines[j].strip()
                            if data_line.startswith("*"):
                                break
                            if data_line and not data_line.startswith("$"):
                                db_data["data"].append(data_line)
                                line_count += 1
                            j += 1
                        self.database_outputs.append(db_data)
                        current_title = None

                    # INITIAL (初始条件)
                    elif current_keyword.startswith("INITIAL_"):
                        init_data = {
                            "type": current_keyword,
                            "title": current_title or "Untitled",
                            "data": []
                        }
                        j = i + 1
                        if current_title:
                            j += 1
                        line_count = 0
                        while j < len(lines) and line_count < 10:
                            data_line = lines[j].strip()
                            if data_line.startswith("*"):
                                break
                            if data_line and not data_line.startswith("$"):
                                init_data["data"].append(data_line)
                                line_count += 1
                            j += 1
                        self.initial_conditions.append(init_data)
                        current_title = None

                    # UNKNOWN KEYWORDS Capture
                    else:
                        # print(f"DEBUG: Found unknown keyword: {current_keyword}")
                        if current_keyword not in self.unknown_keywords and not current_keyword.startswith("END"):
                            snippet = [line.strip()]
                            # Capture up to 5 lines of context
                            for k in range(1, 6):
                                if i + k < len(lines):
                                    next_l = lines[i+k].strip()
                                    if next_l.startswith("*"): break
                                    snippet.append(next_l)
                            self.unknown_keywords[current_keyword] = {
                                "line": i + 1,
                                "snippet": snippet
                            }
                        current_title = None
            
            i += 1

