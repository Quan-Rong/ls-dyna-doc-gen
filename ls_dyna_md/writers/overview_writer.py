from datetime import datetime
import os
from collections import defaultdict
from ..utils.engineering import (
    get_element_engineering_meaning,
    get_contact_engineering_meaning,
    get_initial_engineering_meaning
)

class OverviewWriter:
    def __init__(self, parser):
        self.parser = parser

    def __getattr__(self, name):
        return getattr(self.parser, name)

    def generate_overview(self, output_path):
        """生成模型工程分析摘要 (Overview)。
        
        不同于 generate_markdown() 输出的详细数据文档，
        Overview 文件从 CAE 工程师视角提供高层次物理分析：
        - 模型概览（尺寸、来源、用途）
        - 关键物理特征（单元类型分布及其工程含义）
        - 连接方式分析（焊点、胶粘、绑定接触）
        - 初始条件分析（成型映射、预紧力）
        - 潜在问题标记
        """
        total_elements = sum(elem_data["count"] for elem_data in self.elements.values())
        
        with open(output_path, 'w', encoding='utf-8') as md:
            # === 标题 ===
            md.write(f"# Model Overview: {self.title}\n\n")
            md.write(f"**Filename:** `{self.filename}`  \n")
            md.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            md.write("---\n\n")

            # === 1. 模型概览 ===
            md.write("## 📊 模型概览\n\n")
            md.write("| 属性 | 数值 |\n")
            md.write("|---|---|\n")
            md.write(f"| **模型名称** | {self.title} |\n")
            
            # 从 metadata 提取子模型类型
            sub_type = self.metadata.get('objectType', '')
            nid_detail = self.metadata.get('property.string.NID.detail', '')
            if sub_type and nid_detail:
                md.write(f"| **子模型类型** | {sub_type} - {nid_detail} |\n")
            elif sub_type:
                md.write(f"| **子模型类型** | {sub_type} |\n")
            
            # 项目/阶段
            phase = self.metadata.get('variant.phase.name', '')
            project = self.metadata.get('project.name', '')
            if phase:
                # 从项目路径中提取项目代号
                project_code = ''
                if project:
                    parts = project.strip('/').split('/')
                    for p in parts:
                        if len(p) >= 2 and p[0].isalpha() and any(c.isdigit() for c in p):
                            project_code = p
                            break
                if project_code:
                    md.write(f"| **项目** | {project_code} {phase} |\n")
                else:
                    md.write(f"| **阶段** | {phase} |\n")
            
            dept = self.metadata.get('department.name', '')
            if dept:
                md.write(f"| **部门** | {dept} |\n")
            
            desc = self.metadata.get('description', '')
            if desc:
                md.write(f"| **描述** | {desc} |\n")
                
            md.write(f"| **文件大小** | {os.path.getsize(self.filepath) / (1024*1024):.2f} MB |\n")
            md.write(f"| **节点数** | {self.node_count:,} |\n")
            md.write(f"| **总单元数** | {total_elements:,} |\n")
            md.write(f"| **部件数** | {len(self.parts):,} |\n")
            md.write(f"| **截面数** | {len(self.sections):,} |\n")
            if self.materials:
                md.write(f"| **材料数** | {len(self.materials):,} |\n")
            md.write("\n")

            # === 2. 关键物理特征 ===
            md.write("## 🔍 关键物理特征\n\n")
            
            # 单元类型分布
            md.write("### 单元类型分布\n\n")
            if self.elements:
                md.write("| 单元类型 | 数量 | 占比 | 工程含义 |\n")
                md.write("|---|---|---|---|\n")
                sorted_elems = sorted(self.elements.items(), key=lambda x: x[1]['count'], reverse=True)
                for elem_type, elem_data in sorted_elems:
                    count = elem_data['count']
                    pct = (count / total_elements * 100) if total_elements > 0 else 0
                    meaning = get_element_engineering_meaning(elem_type, count, total_elements)
                    md.write(f"| `ELEMENT_{elem_type}` | {count:,} | {pct:.1f}% | {meaning} |\n")
                md.write("\n")
                
                # 高级分析：成型映射检测
                has_thickness = "SHELL_THICKNESS" in self.elements
                has_stress = any("STRESS_SHELL" in ic.get('type', '') for ic in self.initial_conditions)
                
                if has_thickness and has_stress:
                    md.write("> 💡 **成型-碰撞耦合分析:** 本模型同时包含 `ELEMENT_SHELL_THICKNESS`（变厚度壳）和 `INITIAL_STRESS_SHELL`（初始应力），")
                    md.write("说明进行了**完整的冲压成型映射 (Forming Mapping)**。冲压后的减薄分布和残余应力被映射到碰撞模型中，")
                    md.write("这是高精度碰撞仿真的标志。\n\n")
                elif has_thickness:
                    md.write("> 💡 **厚度映射:** 本模型使用 `ELEMENT_SHELL_THICKNESS` 进行了厚度映射（冲压减薄），")
                    md.write("但未包含初始应力映射。\n\n")
            else:
                md.write("*未检测到单元定义。*\n\n")

            # === 3. 连接方式分析 ===
            md.write("### 连接方式分析\n\n")
            
            has_connections = False
            
            # 分析接触类型
            if self.contacts:
                has_connections = True
                contact_types = defaultdict(int)
                for c in self.contacts:
                    contact_types[c['type']] += 1
                
                md.write("| 连接类型 | 数量 | 工程含义 |\n")
                md.write("|---|---|---|\n")
                for ct, cnt in sorted(contact_types.items(), key=lambda x: x[1], reverse=True):
                    meaning = get_contact_engineering_meaning(ct)
                    md.write(f"| `{ct}` | {cnt} | {meaning} |\n")
                md.write("\n")
            
            # 焊点约束
            if self.spotweld_constraints:
                has_connections = True
                md.write(f"**焊点插值约束 (INTERPOLATION_SPOTWELD):** {len(self.spotweld_constraints)} 个\n\n")
                md.write("焊点连接使用网格无关的插值方法，通过 PID 对连接不同部件。\n\n")
            
            # 刚体约束/关节
            if self.constraints:
                has_connections = True
                constraint_types = defaultdict(int)
                for c in self.constraints:
                    constraint_types[c.get('type', 'Unknown')] += 1
                for ct, cnt in sorted(constraint_types.items()):
                    md.write(f"- **{ct}**: {cnt} 个\n")
                md.write("\n")
            
            if not has_connections:
                md.write("*本文件未定义独立的连接关系（可能在主模型或其他 Include 文件中定义）。*\n\n")

            # === 4. 初始条件 ===
            if self.initial_conditions:
                md.write("### 初始条件\n\n")
                init_types = defaultdict(int)
                for ic in self.initial_conditions:
                    init_types[ic['type']] += 1
                
                md.write("| 初始条件类型 | 数量 | 工程含义 |\n")
                md.write("|---|---|---|\n")
                for it, cnt in sorted(init_types.items()):
                    meaning = get_initial_engineering_meaning(it)
                    md.write(f"| `{it}` | {cnt} | {meaning} |\n")
                md.write("\n")

            # === 5. 阻尼配置 ===
            if self.damping:
                md.write("### 阻尼配置\n\n")
                md.write(f"共 {len(self.damping)} 个阻尼定义。")
                damp_types = defaultdict(int)
                for d in self.damping:
                    damp_types[d['type']] += 1
                for dt, cnt in sorted(damp_types.items()):
                    if "PART_STIFFNESS" in dt:
                        md.write(f"其中 {cnt} 个 `DAMPING_PART_STIFFNESS` 用于抑制高频振荡（Rayleigh 阻尼刚度项 C=β·K）。")
                md.write("\n\n")

            # === 6. 数据库输出 ===
            if self.database_outputs:
                md.write("### 数据库输出控制\n\n")
                db_types = defaultdict(int)
                for db in self.database_outputs:
                    db_types[db['type']] += 1
                for dt, cnt in sorted(db_types.items()):
                    if "CROSS_SECTION" in dt:
                        md.write(f"- **截面力输出** (`{dt}`): {cnt} 个截面，用于测量结构传力路径\n")
                    elif "HISTORY_NODE" in dt:
                        md.write(f"- **节点历史输出** (`{dt}`): {cnt} 个定义，记录关键节点的位移/速度/加速度\n")
                    else:
                        md.write(f"- `{dt}`: {cnt} 个\n")
                md.write("\n")

            # === 7. 材料与截面亮点 ===
            if self.sections:
                md.write("### 材料与截面亮点\n\n")
                
                # 检测特殊截面类型
                elform_usage = defaultdict(int)
                for section in self.sections:
                    for data_line in section.get('data', []):
                        parts = data_line.split()
                        if len(parts) >= 2:
                            try:
                                elform = int(parts[1])
                                elform_usage[elform] += 1
                            except (ValueError, IndexError):
                                pass
                            break
                
                if elform_usage:
                    md.write("**单元算法 (ELFORM) 使用分布:**\n\n")
                    md.write("| ELFORM | 数量 | 含义 |\n")
                    md.write("|---|---|---|\n")
                    elform_desc = {
                        1: "Hughes-Liu 壳（精确但较慢）",
                        2: "Belytschko-Tsay 壳（最快，需沙漏控制）",
                        3: "BCIZ 三角形壳",
                        4: "C0 三角形壳",
                        6: "S/R Hughes-Liu 壳",
                        7: "S/R co-rotational 壳",
                        10: "Belytschko-Wong-Chiang 壳",
                        16: "Fully Integrated 壳（无沙漏，适合吸能件）",
                        -16: "Fully Integrated 壳（无沙漏，带面内稳定）",
                        20: "Cohesive 实体（粘接层建模）",
                        1: "常应变实体（默认）",
                        -1: "Fully Integrated 实体",
                        -2: "Fully Integrated S/R 实体",
                    }
                    for ef, cnt in sorted(elform_usage.items()):
                        desc_text = elform_desc.get(ef, f"ELFORM={ef}")
                        md.write(f"| {ef} | {cnt} | {desc_text} |\n")
                    md.write("\n")
                    
                    # 特殊标注
                    if 20 in elform_usage:
                        md.write("> ⚠️ **Cohesive 单元 (ELFORM=20):** 检测到粘接层建模，通常用于结构胶 (Structural Adhesive) 连接。\n\n")
                    if 16 in elform_usage or -16 in elform_usage:
                        md.write("> ✅ **全积分单元 (ELFORM=16):** 用于关键吸能部件，避免沙漏模式，提高精度。\n\n")

            # === 8. 关键字概览 ===
            md.write("## 📋 关键字统计\n\n")
            md.write("| 关键字 | 数量 |\n")
            md.write("|---|---|\n")
            sorted_kw = sorted(self.keywords.items(), key=lambda x: x[1], reverse=True)
            for k, v in sorted_kw:
                md.write(f"| `*{k}` | {v:,} |\n")
            md.write("\n")

