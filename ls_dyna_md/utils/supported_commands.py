"""
Registry of LS-Dyna commands supported by the parser.
Includes descriptions, parameters, and examples for documentation generation.
Updated: 2026-02-12 (Comprehensive Scan)
"""

SUPPORTED_COMMANDS_DATA = {
    # --- Global & Control ---
    "TITLE": {
        "desc": "设置模型的全局标题，通常显示在 d3plot 的第一帧。",
        "params": "Title String",
        "example": "*TITLE\nFord Taurus Crash Model v1.0"
    },
    "PARAMETER": {
        "desc": "定义参数变量（R型或I型），可在其他关键字中通过 &name 引用。",
        "params": "**Name**: 变量名<br>**Value**: 数值",
        "example": "*PARAMETER\nR thick, 1.25\nR velocity, 15.6"
    },
    "INCLUDE": {
        "desc": "引入外部文件。Parser 支持 `INCLUDE` 和 `INCLUDE_TRANSFORM`。",
        "params": "**FILENAME**: 文件路径<br>**TRANID**: 变换 ID (Optional)",
        "example": "*INCLUDE_TRANSFORM\nsubmodels/engine.k\n$ tranid\n200"
    },
    "DEFINE_TRANSFORMATION": {
        "desc": "定义几何变换（平移、旋转、缩放），通常配合 INCLUDE_TRANSFORM 使用。",
        "params": "**TRANID**: Transform ID<br>**Option**: ROTATE/TRANSL/SCALE",
        "example": "*DEFINE_TRANSFORMATION\n100\nROTATE, 1.0, 0.0, 0.0, 45.0"
    },
    "DATABASE_***": {
        "desc": "控制输出文件的频率 (如 `DATABASE_BINARY_D3PLOT`, `DATABASE_GLSTAT`)。",
        "params": "**DT**: 输出时间间隔<br>**BINARY**: 输出格式标志",
        "example": "*DATABASE_BINARY_D3PLOT\n0.005"
    },
    "DAMPING_***": {
        "desc": "定义系统的能量耗散（阻尼）。",
        "params": "**LCD**: Load Curve ID for damping factor",
        "example": "*DAMPING_GLOBAL\n0, 10.0"
    },
    "INITIAL_VELOCITY": {
        "desc": "定义节点或刚体的初始速度场。",
        "params": "**VX, VY, VZ**: 平动速度<br>**WXR, WYR, WZR**: 转动速度",
        "example": "*INITIAL_VELOCITY\n15.6, 0.0, 0.0, 0.0, 0.0, 0.0"
    },

    # --- Components ---
    "PART": {
        "desc": "定义部件。支持 `PART`, `PART_COMPOSITE`, `PART_CONTACT`。",
        "params": "**PID**: Part ID<br>**SECID**: Section ID<br>**MID**: Material ID",
        "example": "*PART\nBumper Beam\n1001, 20, 50"
    },
    "SECTION_***": {
        "desc": "定义单元属性截面 (SHELL, SOLID, BEAM, DISCRETE)。",
        "params": "**SECID**: Section ID<br>**ELFORM**: 单元积分算法",
        "example": "*SECTION_SHELL\n20, 16, 0.0, 0.0, 0.0"
    },
    "MAT_***": {
        "desc": "定义材料本构 (e.g., PLASTICITY, ELASTIC, SPOTWELD)。",
        "params": "**MID**: Material ID<br>**RO, E, PR**: 基础力学参数",
        "example": "*MAT_PIECEWISE_LINEAR_PLASTICITY\n50, 7.85e-9, 2.1e5, 0.3"
    },

    # --- Mesh ---
    "NODE": {
        "desc": "定义有限元节点。",
        "params": "**NID**: Node ID<br>**X, Y, Z**: 坐标",
        "example": "*NODE\n10023, 120.5, 30.0, -10.0"
    },
    "ELEMENT_SHELL": {
        "desc": "定义壳单元。",
        "params": "**EID**: Element ID<br>**PID**: Part ID<br>**N1-N4**: Node IDs",
        "example": "*ELEMENT_SHELL\n5001, 1001, 201, 202, 203, 204"
    },
    "ELEMENT_SOLID": {
        "desc": "定义实体单元。",
        "params": "**EID**: Element ID<br>**PID**: Part ID<br>**N1-N8**: Node IDs",
        "example": "*ELEMENT_SOLID\n6001, 1001, 301, 302, 303, 304, 305, 306, 307, 308"
    },
    "ELEMENT_BEAM": {
        "desc": "定义梁单元 (1D)。常用于焊点或结构梁。",
        "params": "**EID**: Element ID<br>**PID**: Part ID<br>**N1, N2**: Node IDs",
        "example": "*ELEMENT_BEAM\n7001, 1002, 401, 402"
    },
    "ELEMENT_***": {
        "desc": "通用单元定义 (DISCRETE, MASS, SEATBELT 等)。",
        "params": "Standard Element Format",
        "example": "*ELEMENT_DISCRETE\n8001, 1005, 501, 502"
    },
    
    # --- Sets & Contacts ---
    "SET_***": {
        "desc": "定义集合 (NODE_LIST, PART_LIST, SEGMENT)。",
        "params": "**SID**: Set ID<br>**DA1-4**: Solver attributes",
        "example": "*SET_PART_LIST\n10, 0.0, 0.0, 0.0, 0.0\n1001, 1002, 1003"
    },
    "CONTACT_***": {
        "desc": "定义接触可以处理 AUTOMATIC, TIED, NODES_TO_SURFACE 等类型。",
        "params": "**SSID/MSID**: Slave/Master IDs<br>**SST/MST**: ID Type (Part/Set)",
        "example": "*CONTACT_AUTOMATIC_SINGLE_SURFACE\n0, 0, 0, 0"
    },

    # --- Constraints ---
    "CONSTRAINED_JOINT_***": {
        "desc": "定义运动副连接 (REVOLUTE, SPHERICAL 等)。",
        "params": "**N1, N2**: 定义关节的节点对",
        "example": "*CONSTRAINED_JOINT_SPHERICAL\n5001, 5002"
    },
    "CONSTRAINED_NODAL_RIGID_BODY": {
        "desc": "CNRB: 将一组节点变为刚体。",
        "params": "**PID**: Part ID (Created)<br>**NSID**: Node Set ID",
        "example": "*CONSTRAINED_NODAL_RIGID_BODY\n9001, 0, 10"
    },
    "CONSTRAINED_INTERPOLATION_SPOTWELD": {
        "desc": "SPR: 插值点焊，更真实的焊点连接。",
        "params": "**NodeID**: 焊核节点<br>**PID1/PID2**: 被连接部件",
        "example": "*CONSTRAINED_INTERPOLATION_SPOTWELD\n20001, 1, 100, 101"
    },

    # --- Data ---
    "DEFINE_CURVE": {
        "desc": "定义 XY 曲线数据。",
        "params": "**LCID**: Curve ID",
        "example": "*DEFINE_CURVE\n10, 0, 0, 0, 0\n0.0, 0.0"
    }
}
