# Supported LS-Dyna Commands

> **Generated:** 2026-02-13 01:24:59

This document lists all LS-Dyna keywords currently supported by the parser.
It serves as a reference for users and a capability matrix for AI development.

| Command | Function | Parameters | Example |
|---|---|---|---|
| `*CONSTRAINED_INTERPOLATION_SPOTWELD` | SPR: 插值点焊，更真实的焊点连接。 | **NodeID**: 焊核节点<br>**PID1/PID2**: 被连接部件 | <small>*CONSTRAINED_INTERPOLATION_SPOTWELD<br>20001, 1, 100, 101</small> |
| `*CONSTRAINED_JOINT_***` | 定义运动副连接 (REVOLUTE, SPHERICAL 等)。 | **N1, N2**: 定义关节的节点对 | <small>*CONSTRAINED_JOINT_SPHERICAL<br>5001, 5002</small> |
| `*CONSTRAINED_NODAL_RIGID_BODY` | CNRB: 将一组节点变为刚体。 | **PID**: Part ID (Created)<br>**NSID**: Node Set ID | <small>*CONSTRAINED_NODAL_RIGID_BODY<br>9001, 0, 10</small> |
| `*CONTACT_***` | 定义接触可以处理 AUTOMATIC, TIED, NODES_TO_SURFACE 等类型。 | **SSID/MSID**: Slave/Master IDs<br>**SST/MST**: ID Type (Part/Set) | <small>*CONTACT_AUTOMATIC_SINGLE_SURFACE<br>0, 0, 0, 0</small> |
| `*DAMPING_***` | 定义系统的能量耗散（阻尼）。 | **LCD**: Load Curve ID for damping factor | <small>*DAMPING_GLOBAL<br>0, 10.0</small> |
| `*DATABASE_***` | 控制输出文件的频率 (如 `DATABASE_BINARY_D3PLOT`, `DATABASE_GLSTAT`)。 | **DT**: 输出时间间隔<br>**BINARY**: 输出格式标志 | <small>*DATABASE_BINARY_D3PLOT<br>0.005</small> |
| `*DEFINE_CURVE` | 定义 XY 曲线数据。 | **LCID**: Curve ID | <small>*DEFINE_CURVE<br>10, 0, 0, 0, 0<br>0.0, 0.0</small> |
| `*DEFINE_TRANSFORMATION` | 定义几何变换（平移、旋转、缩放），通常配合 INCLUDE_TRANSFORM 使用。 | **TRANID**: Transform ID<br>**Option**: ROTATE/TRANSL/SCALE | <small>*DEFINE_TRANSFORMATION<br>100<br>ROTATE, 1.0, 0.0, 0.0, 45.0</small> |
| `*ELEMENT_***` | 通用单元定义 (DISCRETE, MASS, SEATBELT 等)。 | Standard Element Format | <small>*ELEMENT_DISCRETE<br>8001, 1005, 501, 502</small> |
| `*ELEMENT_BEAM` | 定义梁单元 (1D)。常用于焊点或结构梁。 | **EID**: Element ID<br>**PID**: Part ID<br>**N1, N2**: Node IDs | <small>*ELEMENT_BEAM<br>7001, 1002, 401, 402</small> |
| `*ELEMENT_SHELL` | 定义壳单元。 | **EID**: Element ID<br>**PID**: Part ID<br>**N1-N4**: Node IDs | <small>*ELEMENT_SHELL<br>5001, 1001, 201, 202, 203, 204</small> |
| `*ELEMENT_SOLID` | 定义实体单元。 | **EID**: Element ID<br>**PID**: Part ID<br>**N1-N8**: Node IDs | <small>*ELEMENT_SOLID<br>6001, 1001, 301, 302, 303, 304, 305, 306, 307, 308</small> |
| `*INCLUDE` | 引入外部文件。Parser 支持 `INCLUDE` 和 `INCLUDE_TRANSFORM`。 | **FILENAME**: 文件路径<br>**TRANID**: 变换 ID (Optional) | <small>*INCLUDE_TRANSFORM<br>submodels/engine.k<br>$ tranid<br>200</small> |
| `*INITIAL_VELOCITY` | 定义节点或刚体的初始速度场。 | **VX, VY, VZ**: 平动速度<br>**WXR, WYR, WZR**: 转动速度 | <small>*INITIAL_VELOCITY<br>15.6, 0.0, 0.0, 0.0, 0.0, 0.0</small> |
| `*MAT_***` | 定义材料本构 (e.g., PLASTICITY, ELASTIC, SPOTWELD)。 | **MID**: Material ID<br>**RO, E, PR**: 基础力学参数 | <small>*MAT_PIECEWISE_LINEAR_PLASTICITY<br>50, 7.85e-9, 2.1e5, 0.3</small> |
| `*NODE` | 定义有限元节点。 | **NID**: Node ID<br>**X, Y, Z**: 坐标 | <small>*NODE<br>10023, 120.5, 30.0, -10.0</small> |
| `*PARAMETER` | 定义参数变量（R型或I型），可在其他关键字中通过 &name 引用。 | **Name**: 变量名<br>**Value**: 数值 | <small>*PARAMETER<br>R thick, 1.25<br>R velocity, 15.6</small> |
| `*PART` | 定义部件。支持 `PART`, `PART_COMPOSITE`, `PART_CONTACT`。 | **PID**: Part ID<br>**SECID**: Section ID<br>**MID**: Material ID | <small>*PART<br>Bumper Beam<br>1001, 20, 50</small> |
| `*SECTION_***` | 定义单元属性截面 (SHELL, SOLID, BEAM, DISCRETE)。 | **SECID**: Section ID<br>**ELFORM**: 单元积分算法 | <small>*SECTION_SHELL<br>20, 16, 0.0, 0.0, 0.0</small> |
| `*SET_***` | 定义集合 (NODE_LIST, PART_LIST, SEGMENT)。 | **SID**: Set ID<br>**DA1-4**: Solver attributes | <small>*SET_PART_LIST<br>10, 0.0, 0.0, 0.0, 0.0<br>1001, 1002, 1003</small> |
| `*TITLE` | 设置模型的全局标题，通常显示在 d3plot 的第一帧。 | Title String | <small>*TITLE<br>Ford Taurus Crash Model v1.0</small> |
