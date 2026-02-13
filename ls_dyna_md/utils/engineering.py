"""Engineering analysis helpers for LS-DYNA models."""

def get_element_engineering_meaning(elem_type, count=0, total=0):
    """Interprets the engineering application of an element type."""
    meanings = {
        "SOLID": "实体单元（粘接层/铸件/厚板建模）",
        "SHELL": "标准壳单元（等厚度）",
        "SHELL_THICKNESS": "变厚度壳（冲压成型映射后的减薄分布）",
        "BEAM": "梁单元（焊点/螺栓/加强筋）",
        "BEAM_ORIENTATION": "带方向向量的梁单元",
        "MASS": "集中质量（配重/附加质量）",
        "SEATBELT_ACCELEROMETER": "安全带加速度计（乘员安全系统）",
    }
    return meanings.get(elem_type, "通用结构单元")

def get_contact_engineering_meaning(contact_type):
    """Interprets the engineering purpose of a contact definition."""
    if "FORCE_TRANSDUCER" in contact_type:
        return "力传感器接触（测量界面力，不影响物理行为）"
    if "TIED" in contact_type:
        if "SHELL_EDGE" in contact_type:
            return "壳边-面绑定接触（结构胶-钣金连接）"
        return "绑定接触（不可分离连接）"
    if "SINGLE_SURFACE" in contact_type:
        return "自接触（防止穿透）"
    if "SURFACE_TO_SURFACE" in contact_type:
        return "面-面接触（标准接触对）"
    return "通用接触定义"

def get_initial_engineering_meaning(initial_type):
    """Interprets the physical significance of an initial condition."""
    if "AXIAL_FORCE_BEAM" in initial_type:
        return "梁单元初始轴力 → 螺栓预紧力模拟"
    if "STRESS_SHELL" in initial_type:
        return "冲压残余应力映射 → 提高碰撞吸能预测精度"
    if "VELOCITY" in initial_type:
        return "初始速度场（碰撞初速度）"
    return "通用初始状态定义"
