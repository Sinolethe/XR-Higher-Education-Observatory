
XR Higher Education Observatory
Codebook v1.0

Version: 1.0
Project: XR Higher Education Observatory
Author: Mei Xu
Institution: University of Bern

1. Purpose 目的

The XR Higher Education Observatory is an open Digital Humanities research platform for documenting and comparing Extended Reality (XR) projects in higher education.XR高等教育观察站是一个开放的数字人文研究平台，用于记录和比较高等教育领域的扩展现实（XR）项目。

The purpose of this codebook is to ensure that all projects are coded according to transparent, reproducible, and consistent criteria. It defines the unit of analysis, controlled vocabulary, coding rules, evidence requirements, and the variables used for the XR Epistemic Research Index (XREI).本编码手册旨在确保所有项目均按照透明、可复现且一致的标准进行编码。它定义了分析单元、受控词汇表、编码规则、证据要求以及用于XR知识研究指数（XREI）的变量。

2. Unit of Analysis 分析单元

The unit of analysis is one individual XR project conducted by a higher education institution.

A project may belong to one of the following categories:

Research
Teaching
Outreach
Infrastructure

Each project receives one unique project_id.

Example

University	             Project	Record
Universität Bielefeld     eTaRDiS	Yes

3. Inclusion Criteria  纳入标准

A project is included only if all four conditions are fulfilled.

Criterion	        Requirement
Institution	University or higher education institution
Verification	Publicly documented (paper, website, or official video)
Technology	VR, AR, MR, or Spatial Computing
Context	        Higher education, research, or scholarly knowledge production 背景：高等教育、研究或学术知识生产

Projects outside higher education are excluded.

4. Controlled Vocabulary    受控词汇表
   4.1 XR Type
   Value	Description
   VR	        Virtual Reality
   AR	        Augmented Reality
   MR	        Mixed Reality
   XR	        Extended Reality
   Spatial Computing	Context-aware spatial computing systems   空间计算 上下文感知空间计算系统
   4.2 Platform
   Value	Description
   Quest	Meta Quest devices
   HoloLens	Microsoft Mixed Reality
   PCVR	SteamVR / desktop VR
   WebXR	Browser-based XR
   Mobile AR	Smartphone or tablet AR

Only one primary platform should be selected. 只能选择一个主要平台。

4.3 Data Foundation 数据基础

Multiple values are allowed. 允许多个值。

Tag	                        Description
Knowledge Graph	Semantic knowledge graph
LOD	                        Linked Open Data
Wikidata	                Wikidata integration
DBpedia	                DBpedia dataset
3D Scan	                Three-dimensional scanning
DICOM	                Medical imaging  医学影像
GIS	                        Geographic information   地理信息
BIM	                        Building Information Model   建筑信息模型
Point Cloud	        Point cloud data   点云数据
Motion Capture	Motion capture data    运动捕捉数据


4.4 Technical Features   技术特性

Multiple tags may be assigned.

Examples:

Neo4j   一种高性能的**图数据库**，用“节点、边和属性”来存储数据，非常适合处理社交网络、推荐系统、知识图谱等具有复杂关联关系的数据。
Unity    实时3D互动内容创作引擎之一。
Unreal  由Epic Games开发的顶尖3D游戏引擎。
OpenXR 由Khronos Group主导的开放式XR（VR/AR/MR）跨平台标准。它的作用是让开发者写一次代码，就能在Oculus、HTC Vive、微软HoloLens等不同品牌的硬件设备上运行
Eye Tracking  眼球追踪
Hand Tracking  手势识别/手部追踪
LiDAR  激光
IIIF       国际图像互操作框架：一套用于在网络上高保真、跨平台发布和查看数字图像（如古籍、艺术品、历史地图）的国际标准协议


5. Coding Rules 编码规则

The following variables describe the epistemic characteristics of each XR project. 以下变量描述了每个 XR 项目的认知特征

5.1 Primary Function 主要功能

Select one primary function.

Value	        Definition
Visualisation	Presenting information visually            可视化：以视觉方式呈现信息
Exploration	Navigating knowledge spaces              探索：导航知识空间
Collaboration	Multi-user knowledge interaction         协作：多人知识交互
Simulation	Simulating processes or environments  模拟：模拟过程或环境


5.2 Spatial Navigation 空间导航

Question

Can users intentionally navigate within a three-dimensional knowledge space? 用户能否在三维知识空间中进行自主导航？

Code	Rule
1	Free movement, teleportation, walking, or flying  自由移动、瞬间移动、行走或飞行
0	No spatial navigation; only object viewing            无空间导航；仅查看对象


5.3 Embodied Interaction 具身交互

Question

Does bodily movement directly contribute to knowledge interaction?  身体运动是否直接参与知识交互？

Code	Examples
1	Hand tracking, gesture interaction, controller manipulation   手部追踪、手势交互、控制器操作
0	Mouse clicks or passive viewing only                                       仅鼠标点击或被动查看


5.4 Multi Perspective 多视角

Question

Can users investigate knowledge objects from multiple spatial or conceptual perspectives?  用户能否从多个空间或概念视角研究知识对象？

Code	Rule
1	Multiple viewpoints or knowledge layers  多个视角或知识层
0	Fixed perspective only                               仅固定视角


5.5 User Generated Content   用户生成内容

Question

Can users create or modify knowledge objects?  用户能否创建或修改知识对象？

Code	Rule
1	Annotation, editing, or creating content   注释、编辑或创建内容
0	Read-only environment                             只读环境


5.6 Collaborative Space  协作空间

Question

Can multiple users interact simultaneously within the same XR environment?  多个用户能否在同一 XR 环境中同时交互？

Code	Rule
1	Shared multi-user XR  共享的多用户 XR
0	Single-user only          仅限单用户


6. Accessibility Coding  可访问性

Accessibility is treated as an independent analytical dimension.  可访问性被视为一个独立的分析维度。

Variable	True                 if...
multilingual_support	Two or more interface languages   两种或多种界面语言
controller_free	Hand tracking or controller-free interaction   手部追踪或无需控制器的交互
cybersickness_mitigation	Comfort mode or teleport locomotion  舒适模式或瞬移移动
remote_access	Can be used without XR headset    无需 XR 头显即可使用
cultural_inclusivity	Explicit multilingual or cross-cultural design  明确的多语言或跨文化设计

Unknown values should be recorded as NULL, not False.  未知值应记录为 NULL，而非 False。



7. Evidence Rules 证据规则

Every coding decision must be supported by at least one documented source.  每个编码决策都必须至少有一个文档来源支持。

Evidence hierarchy 证据层级
Level	Source
1	Peer-reviewed publication 同行评审出版物
2	Official project website      项目官方网站
3	Technical documentation  技术文档
4	Official demonstration video  官方演示视频

Each evidence record should contain:   每条证据记录应包含：

source title   来源标题
quotation or evidence summary  引文或证据摘要
URL
access date   访问日期

No variable may be coded solely from personal assumptions.  任何变量的编码均不得仅基于个人假设。

Appendix A: Example (eTaRDiS)   附录 A：示例 (eTaRDiS)
Variable	Value
Primary Function	Exploration
Spatial Navigation	        1
Embodied Interaction	1
Multi Perspective	        1
User Generated Content	0
Collaborative Space	0

This example serves only as a demonstration of the coding procedure. Final values must always be justified by documented evidence. 此示例仅用于演示编码流程。最终值必须始终以文档证据为依据。
