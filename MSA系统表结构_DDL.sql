-- =====================================================================
-- MSA 管理系统 数据库建表脚本（Oracle）
-- 依据：MSA系统表结构.xlsx（基础数据表 / 业务数据表 两 Sheet）
-- 用途：供 erwin Data Modeler 反向工程（Reverse Engineer）生成 ER 模型 / ER1 文件
-- 说明：
--   1) QMS_MM_MASTER / QMSA_instGroups / syses_userid / QMSAPlan 为已有表，
--      此处按文档字段全集输出 CREATE TABLE 供建模参考；实际库变更请用 ALTER。
--   2) 字段注释已包含字段说明与枚举取值（页面口径）。
-- =====================================================================

-- ---------------------------------------------------
-- 表：QMS_MM_MASTER
-- ---------------------------------------------------
CREATE TABLE QMS_MM_MASTER (
  MiId  VARCHAR2(32) NOT NULL,
  ManageNo  VARCHAR2(64),
  Type  VARCHAR2(32),
  Name  VARCHAR2(128),
  Brand  VARCHAR2(64),
  Model  VARCHAR2(64),
  Fn  VARCHAR2(64),
  MeasureRange  VARCHAR2(128),
  Resolution  VARCHAR2(64),
  AbcType  VARCHAR2(32),
  UseDeptId  VARCHAR2(32),
  ProductLine  VARCHAR2(64),
  Process  VARCHAR2(64),
  StorePos  VARCHAR2(128),
  CheckItem  VARCHAR2(256),
  Status  VARCHAR2(12),
  ReceiveUserId  VARCHAR2(32),
  EntryTime  VARCHAR2(12),
  CalibTime  VARCHAR2(12),
  NextCalibTime  VARCHAR2(12),
  CheckCycle  VARCHAR2(4),
  CheckOrg  VARCHAR2(128),
  CheckResult  VARCHAR2(12),
  MsaResult  VARCHAR2(12),
  ReportNo  VARCHAR2(64),
  PerCheckMark  VARCHAR2(12),
  SealTime  VARCHAR2(12),
  SealReason  VARCHAR2(512),
  SealUserId  VARCHAR2(32),
  SealPos  VARCHAR2(128),
  UnsealTime  VARCHAR2(12),
  UnsealUserId  VARCHAR2(32),
  UnsealReason  VARCHAR2(512),
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(12),
  UpdateMan  VARCHAR2(32),
  UpdateTime  VARCHAR2(12),
  CalDur  VARCHAR2(10),
  CalMeth  VARCHAR2(32),
  MinTol  VARCHAR2(32),
  MeetTenth  VARCHAR2(32),
  ServLife  VARCHAR2(32),
  Warranty  VARCHAR2(12),
  LineCode  VARCHAR2(32),
  FirstIcDate  VARCHAR2(12),
  HalfIcDate  VARCHAR2(12),
  Unit  VARCHAR2(2),
  CalCycle  INT,
  IsMsa  VARCHAR2(1),
  LastMsaTime  VARCHAR2(14),
  LastMsaAnalyst  VARCHAR2(32),
  LastMsaConclusion  VARCHAR2(2),
  GroupId  VARCHAR2(20),
  Remark  VARCHAR2(512),
  CONSTRAINT PK_QMS_MM_MASTER PRIMARY KEY (MiId),
  CONSTRAINT FK_QMS_MM_MASTER_GroupId FOREIGN KEY (GroupId) REFERENCES QMSA_instGroups(GroupId)
);

COMMENT ON TABLE QMS_MM_MASTER IS 'QMS_MM_MASTER';
COMMENT ON COLUMN QMS_MM_MASTER.MiId IS '计量器具ID';
COMMENT ON COLUMN QMS_MM_MASTER.ManageNo IS '管理编号';
COMMENT ON COLUMN QMS_MM_MASTER.Type IS '器具类型；枚举：卡尺、千分尺、指示表、塞规/环规、扭力扳手、压力表、天平、温度计、三坐标测量机、其他（页面器具类型下拉）';
COMMENT ON COLUMN QMS_MM_MASTER.Name IS '计量器具名称';
COMMENT ON COLUMN QMS_MM_MASTER.Brand IS '厂商品牌';
COMMENT ON COLUMN QMS_MM_MASTER.Model IS '型号';
COMMENT ON COLUMN QMS_MM_MASTER.Fn IS '出厂编号';
COMMENT ON COLUMN QMS_MM_MASTER.MeasureRange IS '测量范围';
COMMENT ON COLUMN QMS_MM_MASTER.Resolution IS '分辨率/分辨力';
COMMENT ON COLUMN QMS_MM_MASTER.AbcType IS '类别；枚举：长度、力学、热学、电磁、时间频率、化学、声学、光学、其他（页面「类别」下拉；与 ER 的 A/B/C 分类口径不同，以页面为准）';
COMMENT ON COLUMN QMS_MM_MASTER.UseDeptId IS '使用部门ID';
COMMENT ON COLUMN QMS_MM_MASTER.ProductLine IS '生产线';
COMMENT ON COLUMN QMS_MM_MASTER.Process IS '工序';
COMMENT ON COLUMN QMS_MM_MASTER.StorePos IS '存放位置';
COMMENT ON COLUMN QMS_MM_MASTER.CheckItem IS '检测项目';
COMMENT ON COLUMN QMS_MM_MASTER.Status IS '状态；枚举：在用、待校准、送检中、封存、停用、报废（页面器具状态）';
COMMENT ON COLUMN QMS_MM_MASTER.ReceiveUserId IS '领用人ID';
COMMENT ON COLUMN QMS_MM_MASTER.EntryTime IS '入账时间';
COMMENT ON COLUMN QMS_MM_MASTER.CalibTime IS '校准时间';
COMMENT ON COLUMN QMS_MM_MASTER.NextCalibTime IS '下次校准时间';
COMMENT ON COLUMN QMS_MM_MASTER.CheckCycle IS '校准周期(月)';
COMMENT ON COLUMN QMS_MM_MASTER.CheckOrg IS '校准机构';
COMMENT ON COLUMN QMS_MM_MASTER.CheckResult IS '校准结果；枚举：合格、限用、不合格';
COMMENT ON COLUMN QMS_MM_MASTER.MsaResult IS 'MSA结果';
COMMENT ON COLUMN QMS_MM_MASTER.ReportNo IS '报告编号';
COMMENT ON COLUMN QMS_MM_MASTER.PerCheckMark IS '是否期间检查；枚举：是、否';
COMMENT ON COLUMN QMS_MM_MASTER.SealTime IS '封存时间';
COMMENT ON COLUMN QMS_MM_MASTER.SealReason IS '封存原因';
COMMENT ON COLUMN QMS_MM_MASTER.SealUserId IS '封存人ID';
COMMENT ON COLUMN QMS_MM_MASTER.SealPos IS '封存位置';
COMMENT ON COLUMN QMS_MM_MASTER.UnsealTime IS '启封时间';
COMMENT ON COLUMN QMS_MM_MASTER.UnsealUserId IS '启封申请人ID';
COMMENT ON COLUMN QMS_MM_MASTER.UnsealReason IS '启封原因';
COMMENT ON COLUMN QMS_MM_MASTER.CreateMan IS '创建人';
COMMENT ON COLUMN QMS_MM_MASTER.CreateTime IS '创建时间';
COMMENT ON COLUMN QMS_MM_MASTER.UpdateMan IS '更新人';
COMMENT ON COLUMN QMS_MM_MASTER.UpdateTime IS '更新时间';
COMMENT ON COLUMN QMS_MM_MASTER.CalDur IS '计量用时';
COMMENT ON COLUMN QMS_MM_MASTER.CalMeth IS '校准方式；枚举：外校、内校';
COMMENT ON COLUMN QMS_MM_MASTER.MinTol IS '工位最小公差带';
COMMENT ON COLUMN QMS_MM_MASTER.MeetTenth IS '是否满足1/10；枚举：是、否';
COMMENT ON COLUMN QMS_MM_MASTER.ServLife IS '使用寿命';
COMMENT ON COLUMN QMS_MM_MASTER.Warranty IS '质保期';
COMMENT ON COLUMN QMS_MM_MASTER.LineCode IS '线别';
COMMENT ON COLUMN QMS_MM_MASTER.FirstIcDate IS '校准后首次短期核查完成日期';
COMMENT ON COLUMN QMS_MM_MASTER.HalfIcDate IS '半周期月度核查完成日期';
COMMENT ON COLUMN QMS_MM_MASTER.Unit IS '周期单位；★新增（MSA扩展）：';
COMMENT ON COLUMN QMS_MM_MASTER.CalCycle IS '提醒周期；★新增（MSA扩展）：';
COMMENT ON COLUMN QMS_MM_MASTER.IsMsa IS '是否做MSA；枚举：1=是/0=否；★新增（MSA扩展）：1=是/0=否；计划创建/台账生成前置判定';
COMMENT ON COLUMN QMS_MM_MASTER.LastMsaTime IS '上次MSA时间';
COMMENT ON COLUMN QMS_MM_MASTER.LastMsaAnalyst IS '上次MSA分析人';
COMMENT ON COLUMN QMS_MM_MASTER.LastMsaConclusion IS '上次MSA结论';
COMMENT ON COLUMN QMS_MM_MASTER.GroupId IS '所属器具组；★新增（MSA扩展）：所属器具组编号，标记该器具属于哪个器具组（关联 instGroups.id）';
COMMENT ON COLUMN QMS_MM_MASTER.Remark IS '备注';

-- ---------------------------------------------------
-- 表：QMSA_instGroups
-- ---------------------------------------------------
CREATE TABLE QMSA_instGroups (
  GroupId  VARCHAR2(20) NOT NULL,
  GroupName  VARCHAR2(100),
  GroupType  VARCHAR2(10) NOT NULL,
  Dept  VARCHAR2(100),
  Editor  VARCHAR2(50) NOT NULL,
  EditorDate  VARCHAR2(14) NOT NULL,
  CalCycle  INT,
  Unit  VARCHAR2(2),
  RemindAdvance  INT,
  NextPlanDate  DATE,
  NextRemind  DATE,
  LastPlanDate  VARCHAR2(14),
  LastMsaTime  VARCHAR2(14),
  LastMsaAnalyst  VARCHAR2(32),
  LastMsaConclusion  VARCHAR2(2),
  Remark  VARCHAR2(200),
  CONSTRAINT PK_QMSA_instGroups PRIMARY KEY (GroupId)
);

COMMENT ON TABLE QMSA_instGroups IS 'QMSA_instGroups';
COMMENT ON COLUMN QMSA_instGroups.GroupId IS '组编号';
COMMENT ON COLUMN QMSA_instGroups.GroupName IS '组名称';
COMMENT ON COLUMN QMSA_instGroups.GroupType IS '组类型；枚举：INST(测量器具组)、IQC(检验组)、IPQC(巡检组)、FQC(终检组)、GPR(动总GPR)；仅 INST 为器具组，按器具创建 MSA 选 INST，按人员创建 MSA 选人员组';
COMMENT ON COLUMN QMSA_instGroups.Dept IS '部门';
COMMENT ON COLUMN QMSA_instGroups.Editor IS '维护人';
COMMENT ON COLUMN QMSA_instGroups.EditorDate IS '维护时间';
COMMENT ON COLUMN QMSA_instGroups.CalCycle IS '提醒周期';
COMMENT ON COLUMN QMSA_instGroups.Unit IS '周期单位';
COMMENT ON COLUMN QMSA_instGroups.RemindAdvance IS '提前提醒天数';
COMMENT ON COLUMN QMSA_instGroups.NextPlanDate IS '下次计划日期';
COMMENT ON COLUMN QMSA_instGroups.NextRemind IS '下次提醒日期';
COMMENT ON COLUMN QMSA_instGroups.LastPlanDate IS '上次计划日期';
COMMENT ON COLUMN QMSA_instGroups.LastMsaTime IS '上次MSA时间';
COMMENT ON COLUMN QMSA_instGroups.LastMsaAnalyst IS '上次MSA分析人';
COMMENT ON COLUMN QMSA_instGroups.LastMsaConclusion IS '上次MSA结论';
COMMENT ON COLUMN QMSA_instGroups.Remark IS '说明';

-- ---------------------------------------------------
-- 表：syses_userid
-- ---------------------------------------------------
CREATE TABLE syses_userid (
  LastMsaTime  VARCHAR2(14),
  LastMsaAnalyst  VARCHAR2(32),
  LastMsaConclusion  VARCHAR2(2),
);

COMMENT ON TABLE syses_userid IS 'syses_userid';
COMMENT ON COLUMN syses_userid.LastMsaTime IS '上次MSA时间';
COMMENT ON COLUMN syses_userid.LastMsaAnalyst IS '上次MSA分析人';
COMMENT ON COLUMN syses_userid.LastMsaConclusion IS '上次MSA结论';

-- ---------------------------------------------------
-- 表：QMSA_calibrations
-- ---------------------------------------------------
CREATE TABLE QMSA_calibrations (
  CalibrationsId  VARCHAR2(20) NOT NULL,
  MsaNo  VARCHAR2(20) NOT NULL,
  TargetNo  VARCHAR2(64),
  OperateTime  VARCHAR2(14),
  Analyst  VARCHAR2(32),
  InputMan  VARCHAR2(32),
  Conclusion  VARCHAR2(2),
  CONSTRAINT PK_QMSA_calibrations PRIMARY KEY (CalibrationsId, MsaNo)
);

COMMENT ON TABLE QMSA_calibrations IS 'QMSA_calibrations';
COMMENT ON COLUMN QMSA_calibrations.CalibrationsId IS '记录编号';
COMMENT ON COLUMN QMSA_calibrations.MsaNo IS 'MSA计划号';
COMMENT ON COLUMN QMSA_calibrations.TargetNo IS '器具/人员编号';
COMMENT ON COLUMN QMSA_calibrations.OperateTime IS '操作时间';
COMMENT ON COLUMN QMSA_calibrations.Analyst IS '分析人';
COMMENT ON COLUMN QMSA_calibrations.InputMan IS '操作人';
COMMENT ON COLUMN QMSA_calibrations.Conclusion IS '结论';

-- ---------------------------------------------------
-- 表：QMSA_characteristics
-- ---------------------------------------------------
CREATE TABLE QMSA_characteristics (
  QualZoneNo  VARCHAR2(20) NOT NULL,
  PlanZoneNo  VARCHAR2(20) NOT NULL,
  CharNo  VARCHAR2(64) NOT NULL,
  Name  VARCHAR2(200) NOT NULL,
  Type  VARCHAR2(4) NOT NULL,
  InspStage  VARCHAR2(14) NOT NULL,
  CompNo  VARCHAR2(50) NOT NULL,
  ProcessCode  VARCHAR2(100),
  Category  VARCHAR2(1) NOT NULL,
  InspMethod  VARCHAR2(64),
  Unit  VARCHAR2(20),
  StdVal  NUMBER(18,6),
  Usl  NUMBER(18,6),
  Lsl  NUMBER(18,6),
  Status  VARCHAR2(1),
  ExportNo  VARCHAR2(64),
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSA_characteristics PRIMARY KEY (QualZoneNo, PlanZoneNo, CharNo)
);

COMMENT ON TABLE QMSA_characteristics IS 'QMSA_characteristics';
COMMENT ON COLUMN QMSA_characteristics.QualZoneNo IS '质检区划（工厂）';
COMMENT ON COLUMN QMSA_characteristics.PlanZoneNo IS '车间';
COMMENT ON COLUMN QMSA_characteristics.CharNo IS '特性编号';
COMMENT ON COLUMN QMSA_characteristics.Name IS '特性名称';
COMMENT ON COLUMN QMSA_characteristics.Type IS '特性级别；枚举：SC(关键特性)、CC(重要特性)、普通(一般特性)';
COMMENT ON COLUMN QMSA_characteristics.InspStage IS '检验阶段；待定项，需找时阳阳确认';
COMMENT ON COLUMN QMSA_characteristics.CompNo IS '零件号';
COMMENT ON COLUMN QMSA_characteristics.ProcessCode IS '工序编码；待定项，需找时阳阳/用户确认，用编号还是名称';
COMMENT ON COLUMN QMSA_characteristics.Category IS '数据类型；枚举：计量型、计数型';
COMMENT ON COLUMN QMSA_characteristics.InspMethod IS '检验方法';
COMMENT ON COLUMN QMSA_characteristics.Unit IS '单位';
COMMENT ON COLUMN QMSA_characteristics.StdVal IS '标准值';
COMMENT ON COLUMN QMSA_characteristics.Usl IS '上限';
COMMENT ON COLUMN QMSA_characteristics.Lsl IS '下限';
COMMENT ON COLUMN QMSA_characteristics.Status IS '状态；枚举：启用、停用';
COMMENT ON COLUMN QMSA_characteristics.ExportNo IS '导出编号';
COMMENT ON COLUMN QMSA_characteristics.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_characteristics.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_standards
-- ---------------------------------------------------
CREATE TABLE QMSA_standards (
  StandardsId  VARCHAR2(20) NOT NULL,
  QualZoneNo  VARCHAR2(20) NOT NULL,
  PlanZoneNo  VARCHAR2(20) NOT NULL,
  CharNo  VARCHAR2(64),
  InspMethod  VARCHAR2(14),
  AnalyzeType  VARCHAR2(8) NOT NULL,
  InstIds  VARCHAR2(500),
  MaxOperatorCount  INT,
  MinOperatorCount  INT,
  MaxTrialCount  INT,
  MinTrialCount  INT,
  MaxSampleCount  INT,
  MinSampleCount  INT,
  Basis  VARCHAR2(200),
  Status  VARCHAR2(2) NOT NULL,
  CreateMan  VARCHAR2(32) NOT NULL,
  CreateTime  VARCHAR2(14) NOT NULL,
  Remark  VARCHAR2(200),
  CONSTRAINT PK_QMSA_standards PRIMARY KEY (StandardsId)
);

COMMENT ON TABLE QMSA_standards IS 'QMSA_standards';
COMMENT ON COLUMN QMSA_standards.StandardsId IS '标准编号';
COMMENT ON COLUMN QMSA_standards.QualZoneNo IS '质检区划（工厂）';
COMMENT ON COLUMN QMSA_standards.PlanZoneNo IS '车间';
COMMENT ON COLUMN QMSA_standards.CharNo IS '特性编号';
COMMENT ON COLUMN QMSA_standards.InspMethod IS '检验方法；待定项，需找时阳阳确认';
COMMENT ON COLUMN QMSA_standards.AnalyzeType IS '分析类型；枚举：GRR、KAPPA、线性、偏倚、稳定性、CGCGK(Cg/Cgk)、分辨力';
COMMENT ON COLUMN QMSA_standards.InstIds IS '适用器具；待定项，需找时阳阳确认';
COMMENT ON COLUMN QMSA_standards.MaxOperatorCount IS '测量人数上限';
COMMENT ON COLUMN QMSA_standards.MinOperatorCount IS '测量人数下限';
COMMENT ON COLUMN QMSA_standards.MaxTrialCount IS '测量次数上限';
COMMENT ON COLUMN QMSA_standards.MinTrialCount IS '测量次数下限';
COMMENT ON COLUMN QMSA_standards.MaxSampleCount IS '样本数量上限';
COMMENT ON COLUMN QMSA_standards.MinSampleCount IS '样本数量下限';
COMMENT ON COLUMN QMSA_standards.Basis IS '校验标准';
COMMENT ON COLUMN QMSA_standards.Status IS '状态；枚举：启用、停用';
COMMENT ON COLUMN QMSA_standards.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_standards.CreateTime IS '创建时间';
COMMENT ON COLUMN QMSA_standards.Remark IS '备注';

-- ---------------------------------------------------
-- 表：QMSA_anMethods
-- ---------------------------------------------------
CREATE TABLE QMSA_anMethods (
  AnalyzeType  VARCHAR2(20) NOT NULL,
  AnalyzeName  VARCHAR2(50) NOT NULL,
  NeedSample  VARCHAR2(1) NOT NULL,
  MethodGroup  VARCHAR2(8) NOT NULL,
  MaxOperatorCount  INT,
  MinOperatorCount  INT,
  MaxTrialCount  INT,
  MinTrialCount  INT,
  MaxSampleCount  INT,
  MinSampleCount  INT,
  DefaultSampleCount  INT,
  DefaultTrialCount  INT,
  DefaultOperatorCount  INT,
  DefaultType  VARCHAR2(1) NOT NULL,
  Status  VARCHAR2(1) NOT NULL,
  Remark  VARCHAR2(200),
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSA_anMethods PRIMARY KEY (AnalyzeType)
);

COMMENT ON TABLE QMSA_anMethods IS 'QMSA_anMethods';
COMMENT ON COLUMN QMSA_anMethods.AnalyzeType IS '分析类型；枚举：GRR(重复性+再现性)、KAPPA(计数型一致性)、LINEAR(线性)、BIAS(偏倚性)、STABILITY(稳定性)、CGCGK(Cg/Cgk Type1)、RES(分辨力)';
COMMENT ON COLUMN QMSA_anMethods.AnalyzeName IS '类型名称';
COMMENT ON COLUMN QMSA_anMethods.NeedSample IS '是否取样；枚举：1=是/0=否（RES 分辨力不取样）；1=是/0=否（RES 分辨力不取样），
待定项：不同工厂在取样规则上是否有差异，如果有差异，方法名称就不存，只存代码，';
COMMENT ON COLUMN QMSA_anMethods.MethodGroup IS '方法组';
COMMENT ON COLUMN QMSA_anMethods.MaxOperatorCount IS '测量人数上限';
COMMENT ON COLUMN QMSA_anMethods.MinOperatorCount IS '测量人数下限';
COMMENT ON COLUMN QMSA_anMethods.MaxTrialCount IS '测量次数上限';
COMMENT ON COLUMN QMSA_anMethods.MinTrialCount IS '测量次数下限';
COMMENT ON COLUMN QMSA_anMethods.MaxSampleCount IS '样本数量上限';
COMMENT ON COLUMN QMSA_anMethods.MinSampleCount IS '样本数量下限';
COMMENT ON COLUMN QMSA_anMethods.DefaultSampleCount IS '默认样品数';
COMMENT ON COLUMN QMSA_anMethods.DefaultTrialCount IS '默认次数';
COMMENT ON COLUMN QMSA_anMethods.DefaultOperatorCount IS '默认人数';
COMMENT ON COLUMN QMSA_anMethods.DefaultType IS '数据类型；枚举：计量型、计数型';
COMMENT ON COLUMN QMSA_anMethods.Status IS '状态；枚举：启用、停用';
COMMENT ON COLUMN QMSA_anMethods.Remark IS '备注';
COMMENT ON COLUMN QMSA_anMethods.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_anMethods.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_judgeRules
-- ---------------------------------------------------
CREATE TABLE QMSA_judgeRules (
  RuleNo  VARCHAR2(20) NOT NULL,
  AnalyzeType  VARCHAR2(20) NOT NULL,
  ParamValue  VARCHAR2(200),
  JudgeCondition  VARCHAR2(200),
  Verdict  VARCHAR2(50) NOT NULL,
  Remark  VARCHAR2(200),
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSA_judgeRules PRIMARY KEY (RuleNo),
  CONSTRAINT FK_QMSA_judgeRules_AnalyzeType FOREIGN KEY (AnalyzeType) REFERENCES QMSA_anMethods(AnalyzeType)
);

COMMENT ON TABLE QMSA_judgeRules IS 'QMSA_judgeRules';
COMMENT ON COLUMN QMSA_judgeRules.RuleNo IS '规则编号';
COMMENT ON COLUMN QMSA_judgeRules.AnalyzeType IS '分析类型';
COMMENT ON COLUMN QMSA_judgeRules.ParamValue IS '参数值';
COMMENT ON COLUMN QMSA_judgeRules.JudgeCondition IS '判定条件';
COMMENT ON COLUMN QMSA_judgeRules.Verdict IS '判定结论；枚举：可接受、有条件接受、不可接受（页面判定结论下拉）';
COMMENT ON COLUMN QMSA_judgeRules.Remark IS '备注';
COMMENT ON COLUMN QMSA_judgeRules.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_judgeRules.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_calParams
-- ---------------------------------------------------
CREATE TABLE QMSA_calParams (
  AnalyzeType  VARCHAR2(20) NOT NULL,
  ParamNo  VARCHAR2(50),
  Name  VARCHAR2(100) NOT NULL,
  Value  NUMBER(18,6) NOT NULL,
  ParamType  VARCHAR2(2),
  Remark  VARCHAR2(200),
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(14),,
  CONSTRAINT FK_QMSA_calParams_AnalyzeType FOREIGN KEY (AnalyzeType) REFERENCES QMSA_anMethods(AnalyzeType)
);

COMMENT ON TABLE QMSA_calParams IS 'QMSA_calParams';
COMMENT ON COLUMN QMSA_calParams.AnalyzeType IS '分析类型';
COMMENT ON COLUMN QMSA_calParams.ParamNo IS '参数编号';
COMMENT ON COLUMN QMSA_calParams.Name IS '参数名称';
COMMENT ON COLUMN QMSA_calParams.Value IS '参数值';
COMMENT ON COLUMN QMSA_calParams.ParamType IS '类型';
COMMENT ON COLUMN QMSA_calParams.Remark IS '备注';
COMMENT ON COLUMN QMSA_calParams.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_calParams.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_SampleLib
-- ---------------------------------------------------
CREATE TABLE QMSA_SampleLib (
  SampleId  VARCHAR2(32) NOT NULL,
  SampleName  VARCHAR2(128) NOT NULL,
  SampleType  VARCHAR2(2) NOT NULL,
  CompNo  VARCHAR2(32),
  Qctqp  VARCHAR2(200),
  Verdict  VARCHAR2(1),
  Subplant  VARCHAR2(10),
  RefValue  VARCHAR2(10) NOT NULL,
  Unit  VARCHAR2(14),
  ExpireDate  DATE,
  QualZoneNo  VARCHAR2(32) NOT NULL,
  PlanZoneNo  VARCHAR2(32) NOT NULL,
  Status  VARCHAR2(2) NOT NULL,
  CreateMan  VARCHAR2(32) NOT NULL,
  CreateTime  VARCHAR2(14) NOT NULL,
  Remark  VARCHAR2(500),
  CONSTRAINT PK_QMSA_SampleLib PRIMARY KEY (SampleId),
  CONSTRAINT FK_QMSA_SampleLib_Qctqp FOREIGN KEY (Qctqp) REFERENCES QMSA_characteristics(CharNo)
);

COMMENT ON TABLE QMSA_SampleLib IS 'QMSA_SampleLib';
COMMENT ON COLUMN QMSA_SampleLib.SampleId IS '样本编号';
COMMENT ON COLUMN QMSA_SampleLib.SampleName IS '样本名称';
COMMENT ON COLUMN QMSA_SampleLib.SampleType IS '样本类型；枚举：标准件、生产件';
COMMENT ON COLUMN QMSA_SampleLib.CompNo IS '零件号';
COMMENT ON COLUMN QMSA_SampleLib.Qctqp IS '被测项目';
COMMENT ON COLUMN QMSA_SampleLib.Verdict IS '判定状态；枚举：合格、不合格';
COMMENT ON COLUMN QMSA_SampleLib.Subplant IS '标准值';
COMMENT ON COLUMN QMSA_SampleLib.RefValue IS '真值';
COMMENT ON COLUMN QMSA_SampleLib.Unit IS '单位';
COMMENT ON COLUMN QMSA_SampleLib.ExpireDate IS '有效期至';
COMMENT ON COLUMN QMSA_SampleLib.QualZoneNo IS '工厂';
COMMENT ON COLUMN QMSA_SampleLib.PlanZoneNo IS '车间';
COMMENT ON COLUMN QMSA_SampleLib.Status IS '状态；枚举：启用、停用';
COMMENT ON COLUMN QMSA_SampleLib.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_SampleLib.CreateTime IS '创建时间';
COMMENT ON COLUMN QMSA_SampleLib.Remark IS '备注';

-- ---------------------------------------------------
-- 表：QMSA_Samplepersonnel
-- ---------------------------------------------------
CREATE TABLE QMSA_Samplepersonnel (
  SamplingPlanNo  VARCHAR2(32) NOT NULL,
  MsaNo  VARCHAR2(18) NOT NULL,
  InputMan  VARCHAR2(10) NOT NULL,
  CreateMan  VARCHAR2(32),
  CreateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSA_Samplepersonnel PRIMARY KEY (SamplingPlanNo, MsaNo, InputMan)
);

COMMENT ON TABLE QMSA_Samplepersonnel IS 'QMSA_Samplepersonnel';
COMMENT ON COLUMN QMSA_Samplepersonnel.SamplingPlanNo IS '采样计划号';
COMMENT ON COLUMN QMSA_Samplepersonnel.MsaNo IS 'MSA计划号';
COMMENT ON COLUMN QMSA_Samplepersonnel.InputMan IS '操作人';
COMMENT ON COLUMN QMSA_Samplepersonnel.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_Samplepersonnel.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_AnalysisSamples
-- ---------------------------------------------------
CREATE TABLE QMSA_AnalysisSamples (
  SamplingPlanNo  VARCHAR2(32) NOT NULL,
  MsaNo  VARCHAR2(18) NOT NULL,
  SampleId  VARCHAR2(32) NOT NULL,
  SampleName  VARCHAR2(128),
  CompNo  VARCHAR2(32),
  CONSTRAINT PK_QMSA_AnalysisSamples PRIMARY KEY (SamplingPlanNo, MsaNo)
);

COMMENT ON TABLE QMSA_AnalysisSamples IS 'QMSA_AnalysisSamples';
COMMENT ON COLUMN QMSA_AnalysisSamples.SamplingPlanNo IS '采样计划号';
COMMENT ON COLUMN QMSA_AnalysisSamples.MsaNo IS 'MSA计划号';
COMMENT ON COLUMN QMSA_AnalysisSamples.SampleId IS '样本编号';
COMMENT ON COLUMN QMSA_AnalysisSamples.SampleName IS '样本名称';
COMMENT ON COLUMN QMSA_AnalysisSamples.CompNo IS '零件号';

-- ---------------------------------------------------
-- 表：QMSAPlan
-- ---------------------------------------------------
CREATE TABLE QMSAPlan (
  MsaNo  VARCHAR2(18) NOT NULL,
  CheckItemNo  VARCHAR2(18),
  AnalBillNo  VARCHAR2(18),
  MacNo  VARCHAR2(32),
  MacName  VARCHAR2(128),
  GroupId  VARCHAR2(20),
  Qctq  VARCHAR2(200),
  QualZoneNo  VARCHAR2(4),
  PlanZoneNo  VARCHAR2(32),
  CompNo  VARCHAR2(32),
  Model  VARCHAR2(32),
  ATVNo  VARCHAR2(18),
  PlanTime  VARCHAR2(8),
  FactTime  VARCHAR2(14),
  ExeStatus  VARCHAR2(2),
  ObServer  VARCHAR2(20),
  InputMan  VARCHAR2(20),
  InputTime  VARCHAR2(14),
  PlanType  VARCHAR2(20) NOT NULL,
  TaskSource  VARCHAR2(1),
  Owner  VARCHAR2(32) NOT NULL,
  Result  VARCHAR2(100),
  Remark  VARCHAR2(500),
  CONSTRAINT PK_QMSAPlan PRIMARY KEY (MsaNo),
  CONSTRAINT FK_QMSAPlan_CheckItemNo FOREIGN KEY (CheckItemNo) REFERENCES QMSACheckItem(MSACheckItemNoP),
  CONSTRAINT FK_QMSAPlan_MacNo FOREIGN KEY (MacNo) REFERENCES QMS_MM_MASTER(MIID),
  CONSTRAINT FK_QMSAPlan_GroupId FOREIGN KEY (GroupId) REFERENCES QMSA_instGroups(GroupId)
);

COMMENT ON TABLE QMSAPlan IS 'QMSAPlan';
COMMENT ON COLUMN QMSAPlan.MsaNo IS '计划编号；★ER1；如 MSAP-2026-001';
COMMENT ON COLUMN QMSAPlan.CheckItemNo IS '检验项目编号(删除？）；★ER1';
COMMENT ON COLUMN QMSAPlan.AnalBillNo IS '分析单号；★ER1；计划下分析单';
COMMENT ON COLUMN QMSAPlan.MacNo IS '量具编号；★ER1；器具MSA必填';
COMMENT ON COLUMN QMSAPlan.MacName IS '量具名称；★ER1；冗余展示';
COMMENT ON COLUMN QMSAPlan.GroupId IS '器具组；★ER1；冗余展示';
COMMENT ON COLUMN QMSAPlan.Qctq IS '测量对象（被测项目）；★ER1；如：轴径 φ50±0.05';
COMMENT ON COLUMN QMSAPlan.QualZoneNo IS '工厂；★ER1；工厂/区划带出';
COMMENT ON COLUMN QMSAPlan.PlanZoneNo IS '车间；★ER1；创建弹窗质检区划改车间下拉';
COMMENT ON COLUMN QMSAPlan.CompNo IS '零件号；★ER1';
COMMENT ON COLUMN QMSAPlan.Model IS '型号；★ER1';
COMMENT ON COLUMN QMSAPlan.ATVNo IS '工序号；★ER1';
COMMENT ON COLUMN QMSAPlan.PlanTime IS '计划止日期；★ER1；YYYYMMDD';
COMMENT ON COLUMN QMSAPlan.FactTime IS '执行日期；★ER1';
COMMENT ON COLUMN QMSAPlan.ExeStatus IS '执行状态；枚举：0=未执行/1=执行中/2=已完成（对应页面 待开始/进行中/已完成 三档归集）；★ER1；0/1/2 见枚举';
COMMENT ON COLUMN QMSAPlan.ObServer IS '分析人；★ER1；前端=分析人，创建弹窗单选下拉';
COMMENT ON COLUMN QMSAPlan.InputMan IS '操作人；★ER1';
COMMENT ON COLUMN QMSAPlan.InputTime IS '操作时间；★ER1';
COMMENT ON COLUMN QMSAPlan.PlanType IS '计划类型；枚举：器具MSA、人员MSA；★新增：器具MSA/人员MSA；按人创建=人员MSA，
待定项：和时洋洋/业务确认还要不要';
COMMENT ON COLUMN QMSAPlan.TaskSource IS '任务来源；枚举：周期任务、临时任务（触发来源：周期复评/新过程→周期任务，顾客审核整改/手动→临时任务）';
COMMENT ON COLUMN QMSAPlan.Owner IS '责任人；★新增：创建弹窗责任人下拉（必填）';
COMMENT ON COLUMN QMSAPlan.Result IS '判定结果；枚举：可接受、有条件接受、不可接受（多记录取最差；无结论为待采集）；★新增：可接受/有条件接受/不可接受；多记录取最差';
COMMENT ON COLUMN QMSAPlan.Remark IS '备注；★新增';

-- ---------------------------------------------------
-- 表：QMSARegister
-- ---------------------------------------------------
CREATE TABLE QMSARegister (
  LedgerNo  VARCHAR2(18) NOT NULL,
  LedgerType  VARCHAR2(10) NOT NULL,
  Qctq  VARCHAR2(200),
  MacNo  VARCHAR2(32),
  MacName  VARCHAR2(128),
  QcName  VARCHAR2(4),
  ExeStatus  VARCHAR2(2),
  PlanZoneNo  VARCHAR2(32),
  DeptNo  VARCHAR2(32),
  Describe  VARCHAR2(200),
  CompNo  VARCHAR2(32),
  CompName  VARCHAR2(18),
  AtvNo  VARCHAR2(18),
  QcType  VARCHAR2(18),
  StdVal  VARCHAR2(500),
  Usl  VARCHAR2(20),
  Lsl  VARCHAR2(20),
  TlValue  VARCHAR2(20),
  QualZoneNo  VARCHAR2(4),
  FlType  VARCHAR2(1),
  AnalyzeType  VARCHAR2(10),
  AnalyzeGroup  VARCHAR2(18),
  NewQc  VARCHAR2(10),
  Ppap  VARCHAR2(10),
  PreventMeasure  VARCHAR2(300),
  AnalysisType  VARCHAR2(20),
  MsaNo  VARCHAR2(18),
  TrialCount  VARCHAR2(4),
  OperatorCount  VARCHAR2(4),
  SampleCapacity  VARCHAR2(20),
  AnalyzeTime  VARCHAR2(14),
  ObServer  VARCHAR2(20),
  InputTime  VARCHAR2(14),
  InputMan  VARCHAR2(18),
  Conclusion  VARCHAR2(18),
  RowTimestamp  VARCHAR2(17),
  RowUniqueId  VARCHAR2(20),
  RowCruxTmsp  VARCHAR2(90),
  RowToHisMark  VARCHAR2(1),
  RowToHisTmsp  VARCHAR2(17),
  RowExtend  VARCHAR2(4000),
  AuditSponsor  VARCHAR2(32),
  AuditApplyTime  VARCHAR2(14),
  CgCgkStatus  VARCHAR2(2),
  BiasStatus  VARCHAR2(2),
  LinearityStatus  VARCHAR2(2),
  StabilityStatus  VARCHAR2(2),
  RepeatabilityStatus  VARCHAR2(2),
  ReproducibilityStatus  VARCHAR2(2),
  KappaStatus  VARCHAR2(2),
  ResolutionStatus  VARCHAR2(2),
  SamplingPlanNum  VARCHAR2(32) NOT NULL,
  AuditConfirm  VARCHAR2(32),
  CfmTime  VARCHAR2(14),
  ConfirmStatus  VARCHAR2(10) NOT NULL,
  AuditStatus  VARCHAR2(20) NOT NULL,
  Reviewer  VARCHAR2(50),
  ReviewTime  VARCHAR2(14),
  Approver  VARCHAR2(50),
  ApproveDate  VARCHAR2(14),
  ImportFile  VARCHAR2(200),
  Remark  VARCHAR2(500),
  CreateMan  VARCHAR2(50),
  CreateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSARegister PRIMARY KEY (LedgerNo, SamplingPlanNum)
);

COMMENT ON TABLE QMSARegister IS 'QMSARegister';
COMMENT ON COLUMN QMSARegister.LedgerNo IS '台账编号';
COMMENT ON COLUMN QMSARegister.LedgerType IS '台账类型；枚举：GRR、KAPPA、线性/偏倚、稳定性、Cg/Cgk';
COMMENT ON COLUMN QMSARegister.Qctq IS '测量对象';
COMMENT ON COLUMN QMSARegister.MacNo IS '量具编号';
COMMENT ON COLUMN QMSARegister.MacName IS '量具名称';
COMMENT ON COLUMN QMSARegister.QcName IS '结构类型；枚举：交叉、嵌套、扩展（GRR 分析时填写）';
COMMENT ON COLUMN QMSARegister.ExeStatus IS '执行状态';
COMMENT ON COLUMN QMSARegister.PlanZoneNo IS '车间';
COMMENT ON COLUMN QMSARegister.DeptNo IS '部门';
COMMENT ON COLUMN QMSARegister.Describe IS '描述';
COMMENT ON COLUMN QMSARegister.CompNo IS '零件号';
COMMENT ON COLUMN QMSARegister.CompName IS '零件名称';
COMMENT ON COLUMN QMSARegister.AtvNo IS '工序号';
COMMENT ON COLUMN QMSARegister.QcType IS '质量特性（需确认是否保留，与被测项目重叠）';
COMMENT ON COLUMN QMSARegister.StdVal IS '标准值';
COMMENT ON COLUMN QMSARegister.Usl IS '上限';
COMMENT ON COLUMN QMSARegister.Lsl IS '下限';
COMMENT ON COLUMN QMSARegister.TlValue IS '公差值';
COMMENT ON COLUMN QMSARegister.QualZoneNo IS '质检区划';
COMMENT ON COLUMN QMSARegister.FlType IS 'FL类型';
COMMENT ON COLUMN QMSARegister.AnalyzeType IS '分析类型';
COMMENT ON COLUMN QMSARegister.AnalyzeGroup IS '分析组';
COMMENT ON COLUMN QMSARegister.NewQc IS '新QC工程表';
COMMENT ON COLUMN QMSARegister.Ppap IS 'PPAP标识';
COMMENT ON COLUMN QMSARegister.PreventMeasure IS '预防措施';
COMMENT ON COLUMN QMSARegister.AnalysisType IS '分析方法类型';
COMMENT ON COLUMN QMSARegister.MsaNo IS 'MSA计划编号';
COMMENT ON COLUMN QMSARegister.TrialCount IS '测量次数';
COMMENT ON COLUMN QMSARegister.OperatorCount IS '测量人数';
COMMENT ON COLUMN QMSARegister.SampleCapacity IS '样本数量';
COMMENT ON COLUMN QMSARegister.AnalyzeTime IS '分析时间';
COMMENT ON COLUMN QMSARegister.ObServer IS '分析人';
COMMENT ON COLUMN QMSARegister.InputTime IS '操作时间';
COMMENT ON COLUMN QMSARegister.InputMan IS '操作人';
COMMENT ON COLUMN QMSARegister.Conclusion IS '结论；枚举：可接受、有条件接受、不可接受';
COMMENT ON COLUMN QMSARegister.RowTimestamp IS '时间戳';
COMMENT ON COLUMN QMSARegister.RowUniqueId IS '唯一ID';
COMMENT ON COLUMN QMSARegister.RowCruxTmsp IS '关键时间戳';
COMMENT ON COLUMN QMSARegister.RowToHisMark IS '转历史标记';
COMMENT ON COLUMN QMSARegister.RowToHisTmsp IS '转历史时间戳';
COMMENT ON COLUMN QMSARegister.RowExtend IS '扩展字段';
COMMENT ON COLUMN QMSARegister.AuditSponsor IS '审核发起人';
COMMENT ON COLUMN QMSARegister.AuditApplyTime IS '发起时间';
COMMENT ON COLUMN QMSARegister.CgCgkStatus IS 'CG/CGK状态；枚举：不做、未做、通过、不通过、有条件接受（页面维度状态标识）';
COMMENT ON COLUMN QMSARegister.BiasStatus IS '偏移状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.LinearityStatus IS '线性状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.StabilityStatus IS '稳定性状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.RepeatabilityStatus IS '重复性状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.ReproducibilityStatus IS '再现性状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.KappaStatus IS 'KAPPA状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.ResolutionStatus IS '分辨力状态；枚举：不做、未做、通过、不通过、有条件接受';
COMMENT ON COLUMN QMSARegister.SamplingPlanNum IS '采样计划号';
COMMENT ON COLUMN QMSARegister.AuditConfirm IS '审核确认人';
COMMENT ON COLUMN QMSARegister.CfmTime IS '确认时间';
COMMENT ON COLUMN QMSARegister.ConfirmStatus IS '确认状态；枚举：已确认、未确认（approver 或 approveDate 有值=已确认）；已确认/未确认；approver 或 approveDate 有值=已确认';
COMMENT ON COLUMN QMSARegister.AuditStatus IS '审核状态；枚举：待采集、待分析、待审核、已批准、需整改、已闭环、已关闭';
COMMENT ON COLUMN QMSARegister.Reviewer IS '审核人（确认是否需要';
COMMENT ON COLUMN QMSARegister.ReviewTime IS '审核时间';
COMMENT ON COLUMN QMSARegister.Approver IS '批准人；确认操作写入';
COMMENT ON COLUMN QMSARegister.ApproveDate IS '批准日期';
COMMENT ON COLUMN QMSARegister.ImportFile IS '导入文件';
COMMENT ON COLUMN QMSARegister.Remark IS '备注';
COMMENT ON COLUMN QMSARegister.CreateMan IS '创建人';
COMMENT ON COLUMN QMSARegister.CreateTime IS '创建时间';

-- ---------------------------------------------------
-- 表：QMSA_SamplingPlan
-- ---------------------------------------------------
CREATE TABLE QMSA_SamplingPlan (
  SamplingPlanNO  VARCHAR2(50) NOT NULL,
  SampleId  VARCHAR2(50) NOT NULL,
  InputMan  VARCHAR2(50) NOT NULL,
  LedgerNo  VARCHAR2(50),
  MsaNo  VARCHAR2(50) NOT NULL,
  InspectItemNo  VARCHAR2(50),
  ManageNo  VARCHAR2(50),
  MeasureValue1  NUMBER(16,6),
  MeasureValue2  NUMBER(16,6),
  MeasureValue3  NUMBER(16,6),
  MeasureValue4  NUMBER(16,6),
  MeasureValue5  NUMBER(16,6),
  MeasureValue6  NUMBER(16,6),
  MeasureValue7  NUMBER(16,6),
  MeasureValue8  NUMBER(16,6),
  MeasureValue9  NUMBER(16,6),
  MeasureValue10  NUMBER(16,6),
  CreateMan  VARCHAR2(50),
  CreateTime  VARCHAR2(14),
  UpdateMan  VARCHAR2(50),
  UpdateTime  VARCHAR2(14),
  CONSTRAINT PK_QMSA_SamplingPlan PRIMARY KEY (SamplingPlanNO, SampleId, InputMan)
);

COMMENT ON TABLE QMSA_SamplingPlan IS 'QMSA_SamplingPlan';
COMMENT ON COLUMN QMSA_SamplingPlan.SamplingPlanNO IS '采样计划号';
COMMENT ON COLUMN QMSA_SamplingPlan.SampleId IS '样本编号';
COMMENT ON COLUMN QMSA_SamplingPlan.InputMan IS '操作人';
COMMENT ON COLUMN QMSA_SamplingPlan.LedgerNo IS '台账编号';
COMMENT ON COLUMN QMSA_SamplingPlan.MsaNo IS 'MSA计划号';
COMMENT ON COLUMN QMSA_SamplingPlan.InspectItemNo IS '检验项目号';
COMMENT ON COLUMN QMSA_SamplingPlan.ManageNo IS '管理编号';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue1 IS '测量值1';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue2 IS '测量值2';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue3 IS '测量值3';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue4 IS '测量值4';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue5 IS '测量值5';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue6 IS '测量值6';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue7 IS '测量值7';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue8 IS '测量值8';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue9 IS '测量值9';
COMMENT ON COLUMN QMSA_SamplingPlan.MeasureValue10 IS '测量值10';
COMMENT ON COLUMN QMSA_SamplingPlan.CreateMan IS '创建人';
COMMENT ON COLUMN QMSA_SamplingPlan.CreateTime IS '创建时间';
COMMENT ON COLUMN QMSA_SamplingPlan.UpdateMan IS '更新人';
COMMENT ON COLUMN QMSA_SamplingPlan.UpdateTime IS '更新时间';
