
"""
Philips Healthcare — A2A + MCP Agentic Workflow Console
========================================================
A multi-agent orchestration platform using Agent-to-Agent (A2A) protocol
for inter-agent communication and Model Context Protocol (MCP) for
dynamic tool discovery and invocation.

Use Cases:
  1. MRI Performance Drift Investigation
  2. ECG AI-Assisted Report Automation
  3. Patient Monitoring Alert Triage

Built for The Mountain Path Academy
https://themountainpathacademy.com

Author: Prof. V. Ravichandran
"""

import streamlit as st
import time
import uuid
import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum

# ─────────────────────────────────────────────────────────────────────
# 0.  PAGE CONFIG + BRAND TOKENS
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Philips A2A+MCP Agentic Workflow",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Philips-inspired palette merged with Mountain Path tokens
PHILIPS_BLUE   = "#0B5ED7"
PHILIPS_DARK   = "#00205C"
PHILIPS_LIGHT  = "#E8F0FE"
GOLD           = "#FFD700"
MID_BLUE       = "#004d80"
CARD_BG        = "#112240"
TXT            = "#e6f1ff"
MUTED          = "#8892b0"
GREEN          = "#28a745"
RED            = "#dc3545"
LIGHT_BLUE     = "#ADD8E6"
ORANGE         = "#FF8C00"
BG_GRADIENT    = "linear-gradient(135deg,#0a1628,#0f2440,#14325a)"

# ─────────────────────────────────────────────────────────────────────
# 1.  CSS INJECTION
# ─────────────────────────────────────────────────────────────────────
st.html(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  /* ---------- global background & text ---------- */
  .stApp {{
    background: {BG_GRADIENT} !important;
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
    font-family: 'Inter', sans-serif !important;
  }}
  [data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0a1628 0%, #0d1d35 100%) !important;
    border-right: 1px solid rgba(11,94,215,0.25) !important;
  }}
  [data-testid="stSidebar"] * {{
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
  }}

  /* ---------- headings ---------- */
  h1, h2, h3, h4 {{
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
    font-family: 'Inter', sans-serif !important;
  }}
  h1 {{ font-weight: 800 !important; letter-spacing: -0.5px !important; }}

  /* ---------- inputs ---------- */
  .stTextInput input, .stSelectbox div[data-baseweb="select"],
  .stTextArea textarea {{
    background-color: rgba(14,36,64,0.85) !important;
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
    border: 1px solid rgba(11,94,215,0.35) !important;
    border-radius: 8px !important;
  }}
  .stTextInput label, .stSelectbox label, .stTextArea label {{
    color: {LIGHT_BLUE} !important;
    -webkit-text-fill-color: {LIGHT_BLUE} !important;
  }}

  /* ---------- buttons ---------- */
  .stButton > button {{
    background: linear-gradient(135deg, {PHILIPS_BLUE}, {MID_BLUE}) !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.25s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
  }}
  .stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(11,94,215,0.45) !important;
  }}

  /* ---------- tabs ---------- */
  .stTabs [data-baseweb="tab-list"] {{
    gap: 0 !important;
    background: transparent !important;
    border-bottom: 2px solid rgba(11,94,215,0.2) !important;
  }}
  .stTabs [data-baseweb="tab"] {{
    color: {MUTED} !important;
    -webkit-text-fill-color: {MUTED} !important;
    font-weight: 500 !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.4rem !important;
  }}
  .stTabs [aria-selected="true"] {{
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
    border-bottom: 3px solid {GOLD} !important;
  }}

  /* ---------- metrics ---------- */
  [data-testid="stMetric"] {{
    background: rgba(14,36,64,0.7) !important;
    border: 1px solid rgba(11,94,215,0.2) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
  }}
  [data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    -webkit-text-fill-color: {MUTED} !important;
  }}
  [data-testid="stMetricValue"] {{
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
    font-weight: 700 !important;
  }}

  /* ---------- expander ---------- */
  .streamlit-expanderHeader {{
    background: rgba(14,36,64,0.6) !important;
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
    border-radius: 8px !important;
  }}

  /* ---------- alerts ---------- */
  .stAlert {{ border-radius: 8px !important; }}

  /* ---------- JSON viewer ---------- */
  pre {{ background: #0a1628 !important; border-radius: 8px !important; }}

  /* ---------- scrollbar ---------- */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: #0a1628; }}
  ::-webkit-scrollbar-thumb {{ background: {PHILIPS_BLUE}; border-radius: 3px; }}
</style>
""")


# ─────────────────────────────────────────────────────────────────────
# 2.  DATA MODELS  (A2A-style schemas)
# ─────────────────────────────────────────────────────────────────────
class TaskStatus(Enum):
    PENDING   = "pending"
    PLANNING  = "planning"
    RUNNING   = "running"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED    = "failed"

@dataclass
class AgentCard:
    """A2A Agent Card — runtime capability advertisement."""
    agent_id: str
    name: str
    capabilities: List[str]
    description: str
    icon: str
    status: str = "online"

@dataclass
class MCPTool:
    """MCP Tool descriptor — discovered at runtime."""
    tool_id: str
    name: str
    description: str
    parameters: Dict[str, str]
    server: str

@dataclass
class TaskStep:
    step_id: str
    description: str
    required_capabilities: List[str]
    assigned_agent: Optional[str] = None
    status: str = "pending"
    mcp_tools_used: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    result_summary: str = ""
    start_time: Optional[str] = None
    end_time: Optional[str] = None

@dataclass
class WorkflowTask:
    task_id: str
    goal: str
    context: Dict[str, Any]
    status: str = "pending"
    steps: List[TaskStep] = field(default_factory=list)
    created_at: str = ""
    completed_at: str = ""
    review_result: str = ""


# ─────────────────────────────────────────────────────────────────────
# 3.  AGENT & MCP REGISTRIES  (simulated runtime discovery)
# ─────────────────────────────────────────────────────────────────────
AGENT_REGISTRY: List[AgentCard] = [
    AgentCard("orch-001", "Orchestrator",
              ["routing", "discovery", "aggregation"],
              "Master coordinator — discovers agents, routes tasks, aggregates results.",
              "🎯"),
    AgentCard("plan-001", "Strategic Planner",
              ["planning", "decomposition", "dependency_analysis"],
              "Breaks high-level goals into structured, dependency-aware step plans.",
              "🧠"),
    AgentCard("mri-exec-001", "MRI Analytics Executor",
              ["mri_logs", "signal_analysis", "gradient_monitoring", "drift_detection"],
              "Specialised executor for MRI telemetry, performance baselines & drift analytics.",
              "🔬"),
    AgentCard("ecg-exec-001", "ECG AI Executor",
              ["ecg_ai", "waveform_analysis", "arrhythmia_detection", "lef_detection"],
              "AI-powered ECG analysis — arrhythmia flagging, LEF detection, waveform interpretation.",
              "💓"),
    AgentCard("clinical-001", "Clinical Rules Engine",
              ["clinical_protocol", "clinical_rules", "compliance_check"],
              "Applies hospital-specific clinical protocols, regulatory constraints & compliance rules.",
              "📋"),
    AgentCard("field-001", "Field Service Coordinator",
              ["field_service_scheduling", "parts_inventory", "technician_dispatch"],
              "Schedules on-site service, checks parts availability, dispatches field engineers.",
              "🔧"),
    AgentCard("report-001", "Report Generator",
              ["report_generation", "document_formatting", "summary_generation"],
              "Produces structured clinical reports, executive summaries & audit-ready documents.",
              "📝"),
    AgentCard("alert-001", "Alert Router",
              ["alert_routing", "escalation", "notification"],
              "Routes urgent findings to appropriate clinician queues with priority triage.",
              "🚨"),
    AgentCard("review-001", "Quality Reviewer",
              ["review", "validation", "quality_assurance"],
              "Reviews all outputs for completeness, accuracy & compliance before delivery.",
              "✅"),
    AgentCard("monitor-001", "Patient Monitor Analyst",
              ["vitals_analysis", "trend_detection", "anomaly_detection"],
              "Analyses real-time patient vital signs, detects trends & anomalies from bedside monitors.",
              "📊"),
]

MCP_TOOL_REGISTRY: List[MCPTool] = [
    MCPTool("mcp-t01", "fetch_mri_telemetry",
            "Retrieve MRI performance telemetry from Philips IntelliSpace",
            {"device_id": "str", "time_window": "str"}, "philips-intellispace-mcp"),
    MCPTool("mcp-t02", "analyze_signal_stability",
            "Run signal stability analysis on MRI scan data",
            {"device_id": "str", "metrics": "list"}, "philips-analytics-mcp"),
    MCPTool("mcp-t03", "fetch_clinical_protocol",
            "Retrieve hospital-specific clinical protocols",
            {"hospital": "str", "modality": "str"}, "philips-protocol-mcp"),
    MCPTool("mcp-t04", "schedule_field_service",
            "Schedule field-service visit & check technician availability",
            {"device_id": "str", "priority": "str"}, "philips-service-mcp"),
    MCPTool("mcp-t05", "ingest_ecg_waveform",
            "Ingest 12-lead ECG waveform from Philips TC Series",
            {"ecg_id": "str", "hospital": "str"}, "philips-ecg-mcp"),
    MCPTool("mcp-t06", "run_cardiologs_ai",
            "Run Cardiologs AI arrhythmia detection on ECG",
            {"ecg_id": "str", "algorithms": "list"}, "philips-cardiologs-mcp"),
    MCPTool("mcp-t07", "run_anumana_lef",
            "Run Anumana AI for low ejection fraction detection",
            {"ecg_id": "str"}, "philips-anumana-mcp"),
    MCPTool("mcp-t08", "generate_clinical_report",
            "Generate structured clinical report document",
            {"findings": "dict", "template": "str"}, "philips-report-mcp"),
    MCPTool("mcp-t09", "route_alert",
            "Route urgent alerts to clinician queue",
            {"priority": "str", "department": "str"}, "philips-alert-mcp"),
    MCPTool("mcp-t10", "fetch_patient_vitals",
            "Fetch real-time vitals from IntelliVue monitors",
            {"patient_id": "str", "time_window": "str"}, "philips-intellivue-mcp"),
    MCPTool("mcp-t11", "check_parts_inventory",
            "Query spare parts inventory for a device type",
            {"device_type": "str", "part_code": "str"}, "philips-supply-mcp"),
    MCPTool("mcp-t12", "compliance_audit_check",
            "Validate actions against FDA/MDR regulatory requirements",
            {"action_type": "str", "device_class": "str"}, "philips-compliance-mcp"),
]

# ─────────────────────────────────────────────────────────────────────
# 4.  DYNAMIC PLANNER  (non-hardcoded task decomposition)
# ─────────────────────────────────────────────────────────────────────
def discover_agents(required_caps: List[str]) -> List[AgentCard]:
    """A2A Agent Discovery — find agents whose capabilities match requirements."""
    matches = []
    for agent in AGENT_REGISTRY:
        if any(cap in agent.capabilities for cap in required_caps):
            matches.append(agent)
    return matches

def discover_mcp_tools(capability: str) -> List[MCPTool]:
    """MCP Tool Discovery — list tools relevant to a capability."""
    keyword_map = {
        "mri_logs": ["mri", "telemetry"],
        "signal_analysis": ["signal", "stability", "analyze"],
        "drift_detection": ["signal", "analyze"],
        "gradient_monitoring": ["signal", "analyze"],
        "clinical_protocol": ["clinical", "protocol", "compliance"],
        "clinical_rules": ["clinical", "protocol", "compliance"],
        "compliance_check": ["compliance", "audit"],
        "field_service_scheduling": ["schedule", "field", "parts"],
        "parts_inventory": ["parts", "inventory"],
        "ecg_ai": ["ecg", "cardiologs", "anumana"],
        "waveform_analysis": ["ecg", "waveform", "ingest"],
        "arrhythmia_detection": ["cardiologs", "arrhythmia"],
        "lef_detection": ["anumana", "lef"],
        "report_generation": ["report", "generate"],
        "alert_routing": ["alert", "route"],
        "vitals_analysis": ["vitals", "patient"],
        "trend_detection": ["vitals", "patient"],
        "anomaly_detection": ["vitals", "patient"],
    }
    keywords = keyword_map.get(capability, [capability.split("_")[0]])
    return [t for t in MCP_TOOL_REGISTRY
            if any(kw in t.name.lower() or kw in t.description.lower() for kw in keywords)]

def choose_agent(agents: List[AgentCard], required_cap: str) -> Optional[AgentCard]:
    """Runtime agent selection — picks the best-fit agent for a capability."""
    for a in agents:
        if required_cap in a.capabilities:
            return a
    return agents[0] if agents else None


# ─────────────────────────────────────────────────────────────────────
# 5.  USE-CASE PLAN GENERATORS  (AI-driven, non-hardcoded planning)
# ─────────────────────────────────────────────────────────────────────
def plan_mri_drift(context: Dict[str, Any]) -> List[TaskStep]:
    """Planner Agent dynamically generates steps for MRI drift investigation."""
    device = context.get("device_id", "MRI-UNKNOWN")
    hospital = context.get("hospital", "Unknown Hospital")
    return [
        TaskStep(f"{device}.1", f"Fetch performance telemetry for {device} from {hospital} IntelliSpace",
                 ["mri_logs"]),
        TaskStep(f"{device}.2", f"Analyse signal stability, gradient performance & scan-time drift for {device}",
                 ["signal_analysis", "drift_detection"]),
        TaskStep(f"{device}.3", f"Retrieve clinical protocols & operational constraints for {hospital}",
                 ["clinical_protocol"]),
        TaskStep(f"{device}.4", f"Check spare-parts inventory for {device} components",
                 ["parts_inventory"]),
        TaskStep(f"{device}.5", f"Generate corrective action plan (remote diagnostic / recalibration / on-site service)",
                 ["field_service_scheduling", "clinical_protocol"]),
        TaskStep(f"{device}.6", f"Validate proposed actions against FDA/MDR compliance requirements",
                 ["compliance_check"]),
        TaskStep(f"{device}.7", f"Produce executive summary report & schedule field-service if needed",
                 ["report_generation", "field_service_scheduling"]),
    ]

def plan_ecg_report(context: Dict[str, Any]) -> List[TaskStep]:
    """Planner Agent dynamically generates steps for ECG report automation."""
    ecg_id = context.get("ecg_id", "ECG-UNKNOWN")
    patient = context.get("patient_id", "Patient-UNKNOWN")
    hospital = context.get("hospital", "Unknown Hospital")
    return [
        TaskStep(f"{ecg_id}.1", f"Ingest 12-lead ECG waveform & metadata for {ecg_id} from {hospital}",
                 ["waveform_analysis"]),
        TaskStep(f"{ecg_id}.2", f"Run Cardiologs AI arrhythmia detection on {ecg_id}",
                 ["arrhythmia_detection"]),
        TaskStep(f"{ecg_id}.3", f"Run Anumana AI for low ejection fraction (LEF) screening on {ecg_id}",
                 ["lef_detection"]),
        TaskStep(f"{ecg_id}.4", f"Apply {hospital} clinical rules & local protocol overrides",
                 ["clinical_rules"]),
        TaskStep(f"{ecg_id}.5", f"Draft preliminary ECG report for cardiologist review",
                 ["report_generation"]),
        TaskStep(f"{ecg_id}.6", f"Flag urgent findings & route to clinician queue",
                 ["alert_routing"]),
    ]

def plan_patient_monitoring(context: Dict[str, Any]) -> List[TaskStep]:
    """Planner Agent dynamically generates steps for patient monitoring alert triage."""
    patient = context.get("patient_id", "Patient-UNKNOWN")
    hospital = context.get("hospital", "Unknown Hospital")
    return [
        TaskStep(f"{patient}.1", f"Fetch real-time vitals from IntelliVue monitors for {patient}",
                 ["vitals_analysis"]),
        TaskStep(f"{patient}.2", f"Detect vital-sign trends & anomalies over last 4 hours",
                 ["trend_detection", "anomaly_detection"]),
        TaskStep(f"{patient}.3", f"Cross-reference anomalies with {hospital} clinical protocols",
                 ["clinical_rules"]),
        TaskStep(f"{patient}.4", f"Generate triage assessment & recommended interventions",
                 ["report_generation"]),
        TaskStep(f"{patient}.5", f"Route alerts based on severity — escalate critical findings",
                 ["alert_routing", "escalation"]),
    ]


# ─────────────────────────────────────────────────────────────────────
# 6.  SIMULATED EXECUTION ENGINE
# ─────────────────────────────────────────────────────────────────────
MRI_RESULTS = {
    "fetch_performance_logs": {
        "summary": "Retrieved 7-day telemetry — 847 scan sessions, 12.4 GB raw data ingested.",
        "artifacts": ["telemetry_raw_7d.parquet", "scan_session_log.csv"],
        "detail": {"sessions": 847, "data_size_gb": 12.4, "uptime_pct": 97.2}
    },
    "analyze_drift_trend": {
        "summary": "Signal stability degraded 4.2% vs baseline. Gradient coil temp trending +1.8°C/week. Scan-time drift: +0.3s avg per sequence.",
        "artifacts": ["drift_analysis_report.json", "trend_chart.png"],
        "detail": {"signal_drift_pct": -4.2, "gradient_temp_trend": "+1.8°C/week", "scan_time_drift_s": 0.3, "severity": "MEDIUM"}
    },
    "fetch_clinical_constraints": {
        "summary": "Hospital-X MRI protocol v4.2 loaded — 23 active constraints, 3 critical safety limits identified.",
        "artifacts": ["clinical_protocol_v4.2.json"],
        "detail": {"constraints": 23, "critical_limits": 3, "last_updated": "2026-03-15"}
    },
    "check_parts": {
        "summary": "Gradient coil cooling unit (GCC-450X) available in regional warehouse — ETA 2 business days.",
        "artifacts": ["parts_availability.json"],
        "detail": {"part": "GCC-450X", "available": True, "eta_days": 2, "warehouse": "EU-West"}
    },
    "corrective_plan": {
        "summary": "Recommended: Phase 1 — Remote recalibration (24h). Phase 2 — If drift persists, schedule on-site gradient coil service within 5 business days.",
        "artifacts": ["corrective_action_plan.pdf"],
        "detail": {"phase_1": "Remote recalibration", "phase_2": "On-site gradient service", "risk_level": "Medium"}
    },
    "compliance_check": {
        "summary": "All proposed actions validated against FDA 21 CFR Part 820 & EU MDR 2017/745. No regulatory gaps detected.",
        "artifacts": ["compliance_validation.pdf"],
        "detail": {"fda_compliant": True, "mdr_compliant": True, "gaps": 0}
    },
    "executive_report": {
        "summary": "Executive report generated. Field-service ticket FST-2026-0789 created for Phase 2 contingency. Estimated downtime: <4 hours.",
        "artifacts": ["executive_summary.pdf", "field_service_ticket_FST-2026-0789.json"],
        "detail": {"ticket_id": "FST-2026-0789", "estimated_downtime_hrs": 4}
    },
}

ECG_RESULTS = {
    "ingest_waveform": {
        "summary": "12-lead ECG waveform ingested — 10s recording at 500 Hz, all 12 leads quality-verified.",
        "artifacts": ["ecg_waveform_raw.hl7", "lead_quality_report.json"],
        "detail": {"leads": 12, "duration_s": 10, "sample_rate_hz": 500, "quality": "GOOD"}
    },
    "cardiologs_ai": {
        "summary": "Cardiologs AI detected: Atrial fibrillation (confidence 94.2%), PVC (confidence 87.5%). No ST elevation.",
        "artifacts": ["cardiologs_findings.json", "rhythm_strip_annotated.pdf"],
        "detail": {"afib": {"detected": True, "confidence": 94.2}, "pvc": {"detected": True, "confidence": 87.5}, "st_elevation": False}
    },
    "anumana_lef": {
        "summary": "Anumana LEF screening: Low ejection fraction probability 72.3% — FLAGGED for cardiology review.",
        "artifacts": ["anumana_lef_result.json"],
        "detail": {"lef_probability": 72.3, "flagged": True, "recommendation": "Echo follow-up recommended"}
    },
    "clinical_rules": {
        "summary": "Hospital-Y ECG Protocol v3 applied — 2 rules triggered: AFib pathway activation & LEF echo-referral.",
        "artifacts": ["rules_applied.json"],
        "detail": {"rules_triggered": 2, "pathways_activated": ["AFib", "LEF-Echo"]}
    },
    "report_draft": {
        "summary": "Preliminary ECG report drafted — AI-flagged AFib + suspected LEF. Ready for cardiologist sign-off.",
        "artifacts": ["preliminary_ecg_report.pdf", "ai_summary.txt"],
        "detail": {"status": "Draft", "requires_sign_off": True}
    },
    "alert_route": {
        "summary": "URGENT alert routed to Cardiology queue at Hospital-Y. Dr. Patel notified via pager + Philips IntelliSpace Portal.",
        "artifacts": ["alert_confirmation.json"],
        "detail": {"priority": "URGENT", "routed_to": "Cardiology", "clinician": "Dr. Patel"}
    },
}

MONITOR_RESULTS = {
    "fetch_vitals": {
        "summary": "4-hour vital signs retrieved — HR, SpO2, BP, RR, Temp from IntelliVue MX800. 14,400 data points.",
        "artifacts": ["vitals_4h.parquet", "vitals_summary.json"],
        "detail": {"data_points": 14400, "monitor": "IntelliVue MX800", "parameters": 5}
    },
    "trend_analysis": {
        "summary": "Trend alert: SpO2 declining 3.1%/hr over last 2 hours (96% → 89.8%). HR compensatory rise detected (+12 bpm).",
        "artifacts": ["trend_analysis.json", "trend_chart.png"],
        "detail": {"spo2_trend": "-3.1%/hr", "current_spo2": 89.8, "hr_rise": "+12 bpm", "severity": "HIGH"}
    },
    "cross_reference": {
        "summary": "Protocol match: Suspected respiratory deterioration pathway. Triggers early-warning score (EWS) = 7 (HIGH).",
        "artifacts": ["ews_calculation.json"],
        "detail": {"ews_score": 7, "pathway": "Respiratory Deterioration", "threshold_breach": True}
    },
    "triage_report": {
        "summary": "Triage assessment: HIGH priority. Recommended intervention — immediate respiratory assessment, ABG analysis, escalate to attending physician.",
        "artifacts": ["triage_assessment.pdf"],
        "detail": {"priority": "HIGH", "interventions": ["Respiratory assessment", "ABG analysis", "Physician escalation"]}
    },
    "alert_escalation": {
        "summary": "CRITICAL alert dispatched to ICU team & attending physician. Bedside alarm activated on IntelliVue MX800.",
        "artifacts": ["escalation_log.json"],
        "detail": {"level": "CRITICAL", "notified": ["ICU Team", "Attending Physician"], "bedside_alarm": True}
    },
}

def get_result_for_step(use_case: str, step_index: int) -> Dict:
    """Simulate MCP tool execution and return results."""
    if use_case == "MRI Performance Drift":
        keys = list(MRI_RESULTS.keys())
        return MRI_RESULTS.get(keys[min(step_index, len(keys)-1)], {})
    elif use_case == "ECG Report Automation":
        keys = list(ECG_RESULTS.keys())
        return ECG_RESULTS.get(keys[min(step_index, len(keys)-1)], {})
    else:
        keys = list(MONITOR_RESULTS.keys())
        return MONITOR_RESULTS.get(keys[min(step_index, len(keys)-1)], {})


# ─────────────────────────────────────────────────────────────────────
# 7.  HEADER BANNER
# ─────────────────────────────────────────────────────────────────────
st.html(f"""
<div style="
    background: linear-gradient(135deg, {PHILIPS_DARK}, #0B3D91, {PHILIPS_BLUE});
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    border: 1px solid rgba(11,94,215,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    user-select: none;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
        background:radial-gradient(circle, rgba(255,215,0,0.08) 0%, transparent 70%);
        border-radius:50%;"></div>
    <div style="position:absolute;bottom:-30px;left:20%;width:120px;height:120px;
        background:radial-gradient(circle, rgba(11,94,215,0.12) 0%, transparent 70%);
        border-radius:50%;"></div>
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
        <span style="font-size:36px;">🏥</span>
        <div>
            <span style="font-family:'Inter',sans-serif; font-size:28px; font-weight:800;
                color:white; -webkit-text-fill-color:white; letter-spacing:-0.5px;">
                Philips Healthcare
            </span>
            <span style="font-family:'Inter',sans-serif; font-size:28px; font-weight:300;
                color:{GOLD}; -webkit-text-fill-color:{GOLD}; margin-left:8px;">
                A2A + MCP
            </span>
        </div>
    </div>
    <p style="font-family:'Inter',sans-serif; font-size:14px; font-weight:400;
        color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; margin:4px 0 0 52px;
        letter-spacing:0.3px;">
        Multi-Agent Orchestration Console &nbsp;·&nbsp;
        Agent-to-Agent Protocol &nbsp;·&nbsp;
        Model Context Protocol &nbsp;·&nbsp;
        Dynamic Task Planning & Execution
    </p>
</div>
""")


# ─────────────────────────────────────────────────────────────────────
# 8.  SIDEBAR — USE CASE SELECTOR & AGENT REGISTRY
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.html(f"""
    <div style="text-align:center; padding:8px 0 16px; user-select:none;">
        <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
            color:{GOLD}; -webkit-text-fill-color:{GOLD};">
            ⚙️ Workflow Control
        </span>
    </div>
    """)

    use_case = st.selectbox(
        "Select Use Case",
        ["MRI Performance Drift", "ECG Report Automation", "Patient Monitoring Alert Triage"],
        key="use_case_select"
    )

    st.markdown("---")

    # Agent Registry display
    st.html(f"""
    <div style="user-select:none; margin-bottom:8px;">
        <span style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
            color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-transform:uppercase;
            letter-spacing:1px;">
            🤖 A2A Agent Registry ({len(AGENT_REGISTRY)} agents online)
        </span>
    </div>
    """)

    for agent in AGENT_REGISTRY:
        caps_str = ", ".join(agent.capabilities[:3])
        if len(agent.capabilities) > 3:
            caps_str += f" +{len(agent.capabilities)-3}"
        st.html(f"""
        <div style="background:rgba(14,36,64,0.6); border:1px solid rgba(11,94,215,0.2);
            border-radius:8px; padding:8px 12px; margin-bottom:6px; user-select:none;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:14px;">{agent.icon}</span>
                <span style="font-family:'Inter',sans-serif; font-size:12px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">{agent.name}</span>
                <span style="margin-left:auto; font-size:8px; background:{GREEN};
                    color:#fff; -webkit-text-fill-color:#fff; padding:1px 6px; border-radius:10px;
                    font-family:'Inter',sans-serif; font-weight:600;">ONLINE</span>
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:3px;">
                {caps_str}
            </div>
        </div>
        """)

    st.markdown("---")
    st.html(f"""
    <div style="user-select:none; margin-bottom:8px;">
        <span style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
            color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-transform:uppercase;
            letter-spacing:1px;">
            🔌 MCP Tool Servers ({len(MCP_TOOL_REGISTRY)} tools)
        </span>
    </div>
    """)
    servers = list(set(t.server for t in MCP_TOOL_REGISTRY))
    for srv in sorted(servers):
        tool_count = sum(1 for t in MCP_TOOL_REGISTRY if t.server == srv)
        st.html(f"""
        <div style="display:flex; align-items:center; gap:6px; padding:3px 0; user-select:none;">
            <span style="font-size:8px; color:{GREEN}; -webkit-text-fill-color:{GREEN};">●</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:10px;
                color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">{srv}</span>
            <span style="font-family:'Inter',sans-serif; font-size:9px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-left:auto;">
                {tool_count} tools</span>
        </div>
        """)


# ─────────────────────────────────────────────────────────────────────
# 9.  MAIN CONTENT — TABS
# ─────────────────────────────────────────────────────────────────────
tab_workflow, tab_architecture, tab_protocols = st.tabs([
    "🚀 Workflow Execution", "🏗️ Architecture & Design", "📡 Protocol Reference"
])

# ─────────── TAB 1: WORKFLOW EXECUTION ───────────
with tab_workflow:

    # ---------- Use-case specific input forms ----------
    if use_case == "MRI Performance Drift":
        st.html(f"""
        <div style="user-select:none; margin-bottom:16px;">
            <span style="font-family:'Inter',sans-serif; font-size:20px; font-weight:700;
                color:{TXT}; -webkit-text-fill-color:{TXT};">
                🔬 MRI Performance Drift Investigation
            </span>
            <p style="font-family:'Inter',sans-serif; font-size:13px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:4px;">
                Investigate scanner performance degradation, analyse telemetry, and generate corrective action plans.
            </p>
        </div>
        """)
        c1, c2, c3, c4 = st.columns(4)
        device_id = c1.text_input("Device ID", "MRI-2026-0789")
        hospital  = c2.text_input("Hospital", "Philips Memorial Hospital")
        alert_type = c3.selectbox("Alert Type", ["performance_drift", "gradient_fault", "cooling_anomaly"])
        priority  = c4.selectbox("Priority", ["low", "medium", "high"], index=1)
        context = {"device_id": device_id, "hospital": hospital,
                   "alert_type": alert_type, "priority": priority, "modality": "MRI"}

    elif use_case == "ECG Report Automation":
        st.html(f"""
        <div style="user-select:none; margin-bottom:16px;">
            <span style="font-family:'Inter',sans-serif; font-size:20px; font-weight:700;
                color:{TXT}; -webkit-text-fill-color:{TXT};">
                💓 ECG AI-Assisted Report Automation
            </span>
            <p style="font-family:'Inter',sans-serif; font-size:13px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:4px;">
                AI-powered ECG analysis with arrhythmia detection, LEF screening, and automated clinical reporting.
            </p>
        </div>
        """)
        c1, c2, c3, c4 = st.columns(4)
        ecg_id    = c1.text_input("ECG ID", "ECG-2026-0456")
        patient_id = c2.text_input("Patient ID", "PAT-1122")
        hospital  = c3.text_input("Hospital", "Philips Heart Center")
        priority  = c4.selectbox("Priority", ["routine", "urgent"], index=1)
        context = {"ecg_id": ecg_id, "patient_id": patient_id,
                   "hospital": hospital, "priority": priority, "modality": "ECG", "ecg_type": "resting_12_lead"}

    else:  # Patient Monitoring
        st.html(f"""
        <div style="user-select:none; margin-bottom:16px;">
            <span style="font-family:'Inter',sans-serif; font-size:20px; font-weight:700;
                color:{TXT}; -webkit-text-fill-color:{TXT};">
                📊 Patient Monitoring Alert Triage
            </span>
            <p style="font-family:'Inter',sans-serif; font-size:13px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:4px;">
                Real-time vital sign analysis, anomaly detection, and automated clinical escalation pathways.
            </p>
        </div>
        """)
        c1, c2, c3, c4 = st.columns(4)
        patient_id = c1.text_input("Patient ID", "PAT-5567")
        hospital   = c2.text_input("Hospital / Ward", "ICU-3, Philips General")
        monitor    = c3.selectbox("Monitor Type", ["IntelliVue MX800", "IntelliVue MX550", "IntelliVue X3"])
        window     = c4.selectbox("Analysis Window", ["1 hour", "2 hours", "4 hours", "8 hours"], index=2)
        context = {"patient_id": patient_id, "hospital": hospital,
                   "monitor_type": monitor, "time_window": window}

    # ---------- RUN BUTTON ----------
    run_clicked = st.button("▶  EXECUTE AGENT WORKFLOW", use_container_width=True)

    if run_clicked:
        st.markdown("---")
        workflow_id = f"WF-{uuid.uuid4().hex[:8].upper()}"
        ts_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ── Phase 1: Discovery ──
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border-left:4px solid {GOLD};
            border-radius:0 8px 8px 0; padding:12px 18px; margin-bottom:16px; user-select:none;">
            <span style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                color:{GOLD}; -webkit-text-fill-color:{GOLD};">
                PHASE 1 — A2A AGENT DISCOVERY
            </span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:11px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-left:12px;">
                Workflow {workflow_id} · {ts_now}
            </span>
        </div>
        """)
        orch_status = st.empty()
        orch_status.info("🎯 Orchestrator scanning A2A Agent Cards for available capabilities...")
        time.sleep(1.0)

        # Show discovered agents
        all_caps = set()
        if use_case == "MRI Performance Drift":
            all_caps = {"mri_logs", "signal_analysis", "drift_detection", "clinical_protocol",
                        "parts_inventory", "field_service_scheduling", "compliance_check",
                        "report_generation", "review"}
        elif use_case == "ECG Report Automation":
            all_caps = {"waveform_analysis", "arrhythmia_detection", "lef_detection",
                        "clinical_rules", "report_generation", "alert_routing", "review"}
        else:
            all_caps = {"vitals_analysis", "trend_detection", "anomaly_detection",
                        "clinical_rules", "report_generation", "alert_routing", "review"}

        discovered = discover_agents(list(all_caps))
        orch_status.success(f"✅ Discovered {len(discovered)} agents with matching capabilities via A2A Agent Cards.")

        # ── Phase 2: Planning ──
        time.sleep(0.5)
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border-left:4px solid {PHILIPS_BLUE};
            border-radius:0 8px 8px 0; padding:12px 18px; margin-bottom:16px; user-select:none;">
            <span style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                color:{PHILIPS_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">
                PHASE 2 — DYNAMIC TASK PLANNING
            </span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:11px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-left:12px;">
                Planner Agent decomposing goal into structured steps
            </span>
        </div>
        """)
        plan_status = st.empty()
        plan_status.info("🧠 Planner Agent analysing goal, discovering MCP tools, generating step plan...")
        time.sleep(1.2)

        # Generate plan
        if use_case == "MRI Performance Drift":
            steps = plan_mri_drift(context)
        elif use_case == "ECG Report Automation":
            steps = plan_ecg_report(context)
        else:
            steps = plan_patient_monitoring(context)

        plan_status.success(f"✅ Plan generated: {len(steps)} steps with dependency-aware execution order.")

        # Show plan overview
        with st.expander("📋 View Generated Plan", expanded=True):
            for i, step in enumerate(steps):
                agents_for_step = discover_agents(step.required_capabilities)
                assigned = choose_agent(agents_for_step, step.required_capabilities[0])
                step.assigned_agent = assigned.name if assigned else "Unassigned"
                tools = []
                for cap in step.required_capabilities:
                    tools.extend(discover_mcp_tools(cap))
                tool_names = list(set(t.name for t in tools))
                step.mcp_tools_used = tool_names

                st.html(f"""
                <div style="background:rgba(14,36,64,0.5); border:1px solid rgba(11,94,215,0.15);
                    border-radius:8px; padding:10px 14px; margin-bottom:6px; user-select:none;
                    display:flex; align-items:flex-start; gap:12px;">
                    <div style="min-width:28px; height:28px; background:{PHILIPS_BLUE};
                        border-radius:50%; display:flex; align-items:center; justify-content:center;
                        font-family:'Inter',sans-serif; font-size:12px; font-weight:700;
                        color:white; -webkit-text-fill-color:white;">{i+1}</div>
                    <div>
                        <div style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
                            color:{TXT}; -webkit-text-fill-color:{TXT};">{step.description}</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
                            color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:3px;">
                            Agent: {step.assigned_agent} &nbsp;·&nbsp;
                            MCP Tools: {', '.join(tool_names[:3])}{' +'+str(len(tool_names)-3) if len(tool_names)>3 else ''}
                        </div>
                    </div>
                </div>
                """)

        # ── Phase 3: Execution ──
        time.sleep(0.5)
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border-left:4px solid {GREEN};
            border-radius:0 8px 8px 0; padding:12px 18px; margin-bottom:16px; user-select:none;">
            <span style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                color:{GREEN}; -webkit-text-fill-color:{GREEN};">
                PHASE 3 — A2A TASK EXECUTION + MCP TOOL INVOCATION
            </span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:11px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-left:12px;">
                Executor agents calling MCP tools dynamically
            </span>
        </div>
        """)

        progress_bar = st.progress(0)
        execution_log = st.container()

        for i, step in enumerate(steps):
            result = get_result_for_step(use_case, i)
            step.status = "running"
            step.start_time = datetime.now().strftime("%H:%M:%S")

            with execution_log:
                step_col1, step_col2 = st.columns([3, 1])

                with step_col1:
                    st.html(f"""
                    <div style="background:rgba(14,36,64,0.6); border:1px solid rgba(40,167,69,0.3);
                        border-radius:10px; padding:14px 18px; margin-bottom:8px; user-select:none;">
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                            <span style="font-size:10px; background:{GREEN};
                                color:#fff; -webkit-text-fill-color:#fff; padding:2px 8px;
                                border-radius:10px; font-family:'Inter',sans-serif;
                                font-weight:700; text-transform:uppercase;">Step {i+1}/{len(steps)}</span>
                            <span style="font-family:'Inter',sans-serif; font-size:13px;
                                font-weight:600; color:{TXT}; -webkit-text-fill-color:{TXT};">
                                {step.description}
                            </span>
                        </div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:11px;
                            color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};
                            background:rgba(0,0,0,0.3); padding:8px 12px; border-radius:6px;
                            margin-top:6px; line-height:1.7;">
                            <span style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">▸ A2A</span> Task dispatched to <b>{step.assigned_agent}</b><br>
                            <span style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">▸ MCP</span> Tools invoked: {', '.join(step.mcp_tools_used[:3])}<br>
                            <span style="color:{GREEN}; -webkit-text-fill-color:{GREEN};">▸ Result:</span> {result.get('summary', 'Completed successfully.')}
                        </div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                            color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-top:6px;">
                            Artifacts: {', '.join(result.get('artifacts', []))}
                        </div>
                    </div>
                    """)

                with step_col2:
                    detail = result.get("detail", {})
                    if detail:
                        st.json(detail)

            step.status = "completed"
            step.end_time = datetime.now().strftime("%H:%M:%S")
            step.result_summary = result.get("summary", "")
            step.artifacts = result.get("artifacts", [])
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.8)

        # ── Phase 4: Review ──
        time.sleep(0.3)
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border-left:4px solid {GOLD};
            border-radius:0 8px 8px 0; padding:12px 18px; margin:16px 0; user-select:none;">
            <span style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                color:{GOLD}; -webkit-text-fill-color:{GOLD};">
                PHASE 4 — QUALITY REVIEW & VALIDATION
            </span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:11px;
                color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-left:12px;">
                Reviewer Agent validating all outputs
            </span>
        </div>
        """)
        review_status = st.empty()
        review_status.info("✅ Quality Reviewer verifying completeness, accuracy & compliance...")
        time.sleep(1.5)

        total_artifacts = sum(len(s.artifacts) for s in steps)
        review_status.success(
            f"✅ **Review APPROVED** — All {len(steps)} steps completed · {total_artifacts} artifacts generated · "
            f"No gaps detected · Workflow {workflow_id} finalised."
        )

        # ── Summary Dashboard ──
        st.markdown("---")
        st.html(f"""
        <div style="user-select:none; margin-bottom:16px;">
            <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
                color:{GOLD}; -webkit-text-fill-color:{GOLD};">
                📊 Workflow Execution Summary
            </span>
        </div>
        """)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Workflow ID", workflow_id)
        m2.metric("Steps Executed", len(steps))
        m3.metric("Artifacts Generated", total_artifacts)
        m4.metric("Status", "✅ APPROVED")

        # Task trace JSON
        with st.expander("🔍 Full Task Trace (A2A Artifacts)", expanded=False):
            trace = {
                "workflow_id": workflow_id,
                "use_case": use_case,
                "context": context,
                "timestamp": ts_now,
                "agents_involved": [s.assigned_agent for s in steps],
                "steps": [
                    {
                        "step_id": s.step_id,
                        "description": s.description,
                        "agent": s.assigned_agent,
                        "mcp_tools": s.mcp_tools_used,
                        "status": s.status,
                        "result": s.result_summary,
                        "artifacts": s.artifacts,
                    }
                    for s in steps
                ],
                "review": "APPROVED",
            }
            st.json(trace)


# ─────────── TAB 2: ARCHITECTURE ───────────
with tab_architecture:
    st.html(f"""
    <div style="user-select:none; margin-bottom:20px;">
        <span style="font-family:'Inter',sans-serif; font-size:22px; font-weight:700;
            color:{TXT}; -webkit-text-fill-color:{TXT};">
            System Architecture — A2A + MCP Agent Orchestration
        </span>
    </div>
    """)

    # Architecture Diagram as styled HTML
    st.html(f"""
    <div style="background:rgba(14,36,64,0.5); border:1px solid rgba(11,94,215,0.25);
        border-radius:14px; padding:28px; margin-bottom:24px; user-select:none;">

        <!-- Row 1: User & Orchestrator -->
        <div style="display:flex; justify-content:center; gap:40px; margin-bottom:28px; flex-wrap:wrap;">
            <div style="background:linear-gradient(135deg,#1a3a5c,#0d2440); border:2px solid {GOLD};
                border-radius:12px; padding:16px 24px; text-align:center; min-width:180px;">
                <div style="font-size:24px;">👤</div>
                <div style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD}; margin-top:4px;">User / Clinician</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">Streamlit UI · REST API</div>
            </div>
            <div style="display:flex; align-items:center;">
                <span style="font-family:'Inter',sans-serif; font-size:20px; color:{GOLD};
                    -webkit-text-fill-color:{GOLD};">→ Goal →</span>
            </div>
            <div style="background:linear-gradient(135deg,#1a3a5c,#0d2440); border:2px solid {PHILIPS_BLUE};
                border-radius:12px; padding:16px 24px; text-align:center; min-width:220px;">
                <div style="font-size:24px;">🎯</div>
                <div style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                    color:{TXT}; -webkit-text-fill-color:{TXT}; margin-top:4px;">Orchestrator Agent</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">
                    A2A Client/Server · Discovery · Routing</div>
            </div>
        </div>

        <!-- Arrow down -->
        <div style="text-align:center; margin-bottom:20px;">
            <span style="font-family:'Inter',sans-serif; font-size:16px; color:{PHILIPS_BLUE};
                -webkit-text-fill-color:{LIGHT_BLUE};">↓ &nbsp; A2A Task Dispatch &nbsp; ↓</span>
        </div>

        <!-- Row 2: Planner & Reviewer -->
        <div style="display:flex; justify-content:center; gap:30px; margin-bottom:28px; flex-wrap:wrap;">
            <div style="background:linear-gradient(135deg,#1a3a5c,#0d2440); border:1px solid rgba(11,94,215,0.4);
                border-radius:10px; padding:14px 20px; text-align:center; min-width:170px;">
                <div style="font-size:20px;">🧠</div>
                <div style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Planner Agent</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">
                    A2A Server + MCP Client<br>Goal → Structured Plan</div>
            </div>
            <div style="background:linear-gradient(135deg,#1a3a5c,#0d2440); border:1px solid rgba(11,94,215,0.4);
                border-radius:10px; padding:14px 20px; text-align:center; min-width:170px;">
                <div style="font-size:20px;">✅</div>
                <div style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Reviewer Agent</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">
                    A2A Server<br>Validates · Approves · Replans</div>
            </div>
        </div>

        <!-- Arrow down -->
        <div style="text-align:center; margin-bottom:20px;">
            <span style="font-family:'Inter',sans-serif; font-size:16px; color:{PHILIPS_BLUE};
                -webkit-text-fill-color:{LIGHT_BLUE};">↓ &nbsp; A2A Steps + MCP Tool Calls &nbsp; ↓</span>
        </div>

        <!-- Row 3: Executor Agents -->
        <div style="display:flex; justify-content:center; gap:16px; margin-bottom:28px; flex-wrap:wrap;">
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">🔬</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">MRI Executor</div>
            </div>
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">💓</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">ECG Executor</div>
            </div>
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">📋</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Clinical Rules</div>
            </div>
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">🔧</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Field Service</div>
            </div>
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">📝</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Report Gen</div>
            </div>
            <div style="background:rgba(14,36,64,0.8); border:1px solid rgba(40,167,69,0.3);
                border-radius:10px; padding:12px 16px; text-align:center; min-width:130px;">
                <div style="font-size:18px;">🚨</div>
                <div style="font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
                    color:{TXT}; -webkit-text-fill-color:{TXT};">Alert Router</div>
            </div>
        </div>

        <!-- Arrow down -->
        <div style="text-align:center; margin-bottom:20px;">
            <span style="font-family:'Inter',sans-serif; font-size:16px; color:{GREEN};
                -webkit-text-fill-color:{GREEN};">↓ &nbsp; MCP Tool Discovery & Invocation &nbsp; ↓</span>
        </div>

        <!-- Row 4: MCP Servers -->
        <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">IntelliSpace</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">Analytics</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">Cardiologs AI</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">IntelliVue</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">Service Mgmt</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
            <div style="background:rgba(0,32,92,0.6); border:1px solid rgba(255,215,0,0.3);
                border-radius:8px; padding:10px 14px; text-align:center; min-width:120px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:500;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">Compliance</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED};">MCP Server</div>
            </div>
        </div>
    </div>
    """)

    # Design principles
    st.html(f"""
    <div style="user-select:none; margin:20px 0 12px;">
        <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
            color:{GOLD}; -webkit-text-fill-color:{GOLD};">
            Why This Architecture Is Non-Hardcoded
        </span>
    </div>
    """)

    principles = [
        ("Runtime Agent Discovery", "Agents advertise capabilities via A2A Agent Cards. The orchestrator discovers and selects agents dynamically — no fixed routing tables.", "🔍"),
        ("Dynamic MCP Tool Binding", "Executors call MCP tool/list at runtime to discover available tools. New tools can be added to MCP servers without changing agent code.", "🔌"),
        ("Structured Task Schemas", "Every message follows a strict Task → TaskStatus → Artifact schema. The planner can generate any number of steps with arbitrary capabilities.", "📐"),
        ("Capability-Driven Routing", "Task assignment uses required_capabilities matching, not if/else branches. Adding a new agent with new capabilities immediately makes it available.", "🧭"),
        ("Data-Driven Planning", "The Planner Agent uses the goal + context + available capabilities to generate plans. Different goals produce different step sequences automatically.", "🧠"),
        ("Protocol-Driven Review", "The Reviewer Agent checks outputs against acceptance criteria defined in the plan schema, not hardcoded validation rules.", "✅"),
    ]

    cols = st.columns(2)
    for i, (title, desc, icon) in enumerate(principles):
        with cols[i % 2]:
            st.html(f"""
            <div style="background:rgba(14,36,64,0.5); border:1px solid rgba(11,94,215,0.2);
                border-radius:10px; padding:14px 18px; margin-bottom:10px; user-select:none;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                    <span style="font-size:18px;">{icon}</span>
                    <span style="font-family:'Inter',sans-serif; font-size:14px; font-weight:700;
                        color:{TXT}; -webkit-text-fill-color:{TXT};">{title}</span>
                </div>
                <div style="font-family:'Inter',sans-serif; font-size:12px;
                    color:{MUTED}; -webkit-text-fill-color:{MUTED}; line-height:1.6;">
                    {desc}
                </div>
            </div>
            """)


# ─────────── TAB 3: PROTOCOL REFERENCE ───────────
with tab_protocols:
    st.html(f"""
    <div style="user-select:none; margin-bottom:20px;">
        <span style="font-family:'Inter',sans-serif; font-size:22px; font-weight:700;
            color:{TXT}; -webkit-text-fill-color:{TXT};">
            Protocol Reference — A2A & MCP
        </span>
    </div>
    """)

    p1, p2 = st.columns(2)

    with p1:
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border:1px solid rgba(11,94,215,0.3);
            border-radius:12px; padding:20px 24px; user-select:none; height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="font-size:22px;">🤝</span>
                <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">A2A Protocol</span>
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
                color:{TXT}; -webkit-text-fill-color:{TXT}; margin-bottom:6px;">
                Agent-to-Agent Communication
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:12px; line-height:1.7;
                color:{MUTED}; -webkit-text-fill-color:{MUTED};">
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">Purpose:</b>
                Standardised inter-agent messaging for task coordination, status tracking, and artifact exchange.<br><br>
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">Key Concepts:</b><br>
                • <b>Agent Cards</b> — Runtime capability advertisement<br>
                • <b>Task Objects</b> — Structured goal + context + constraints<br>
                • <b>Task Status</b> — pending → running → completed/failed<br>
                • <b>Artifacts</b> — Typed output attachments<br>
                • <b>Task History</b> — Full audit trail of state transitions<br><br>
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">In This System:</b>
                A2A handles all agent discovery, task routing, status tracking, and result aggregation between Orchestrator, Planner, Executors, and Reviewer.
            </div>
        </div>
        """)

    with p2:
        st.html(f"""
        <div style="background:rgba(14,36,64,0.5); border:1px solid rgba(11,94,215,0.3);
            border-radius:12px; padding:20px 24px; user-select:none; height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="font-size:22px;">🔌</span>
                <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
                    color:{GOLD}; -webkit-text-fill-color:{GOLD};">MCP Protocol</span>
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:13px; font-weight:600;
                color:{TXT}; -webkit-text-fill-color:{TXT}; margin-bottom:6px;">
                Model Context Protocol — Tool Access
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:12px; line-height:1.7;
                color:{MUTED}; -webkit-text-fill-color:{MUTED};">
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">Purpose:</b>
                Standardised access to external tools, resources, and prompts — allowing agents to discover and invoke capabilities dynamically.<br><br>
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">Key Concepts:</b><br>
                • <b>Tools</b> — Callable functions (search, analyse, generate)<br>
                • <b>Resources</b> — Data sources (telemetry, protocols, records)<br>
                • <b>Prompts</b> — Reusable prompt templates<br>
                • <b>tool/list</b> — Runtime tool discovery endpoint<br>
                • <b>Transport</b> — stdio / HTTP / SSE<br><br>
                <b style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};">In This System:</b>
                MCP servers expose Philips-specific tools (IntelliSpace, Cardiologs AI, IntelliVue, Service Management). Executors discover tools at runtime via MCP, enabling zero-code tool swaps.
            </div>
        </div>
        """)

    # Data contract reference
    st.html(f"""
    <div style="user-select:none; margin:24px 0 12px;">
        <span style="font-family:'Inter',sans-serif; font-size:18px; font-weight:700;
            color:{GOLD}; -webkit-text-fill-color:{GOLD};">
            📐 Data Contracts
        </span>
    </div>
    """)

    with st.expander("Task Request Schema"):
        st.json({
            "task_id": "string — unique identifier",
            "goal": "string — natural language objective",
            "context": {"key": "value — domain-specific parameters"},
            "required_capabilities": ["list of capability strings"],
            "step": "string (optional) — specific step identifier",
            "plan_json": "string (optional) — serialised plan from planner"
        })

    with st.expander("Task Status Schema"):
        st.json({
            "task_id": "string — matches request",
            "status": "pending | planning | running | reviewing | completed | failed",
            "artifacts": ["list of output file references"],
            "metadata": {"agent": "executor name", "result": "summary string", "tool_trace": "MCP calls"}
        })

    with st.expander("MCP Tool Descriptor"):
        st.json({
            "tool_id": "string — unique tool identifier",
            "name": "string — callable function name",
            "description": "string — what the tool does",
            "parameters": {"param_name": "type — input schema"},
            "server": "string — MCP server hosting this tool"
        })


# ─────────────────────────────────────────────────────────────────────
# 10. FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.html(f"""
<div style="text-align:center; padding:16px 0 8px; user-select:none;">
    <div style="font-family:'Inter',sans-serif; font-size:14px; font-weight:600;
        color:{GOLD}; -webkit-text-fill-color:{GOLD}; margin-bottom:6px;">
        The Mountain Path Academy — World of Finance
    </div>
    <div style="font-family:'Inter',sans-serif; font-size:12px;
        color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-bottom:4px;">
        Prof. V. Ravichandran &nbsp;·&nbsp;
        Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore, Goa Institute of Management
    </div>
    <div style="margin-top:6px;">
        <a href="https://themountainpathacademy.com" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;
           font-family:'Inter',sans-serif; font-size:12px; font-weight:500;">
            🌐 themountainpathacademy.com
        </a>
        &nbsp;&nbsp;·&nbsp;&nbsp;
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;
           font-family:'Inter',sans-serif; font-size:12px; font-weight:500;">
            💼 LinkedIn
        </a>
        &nbsp;&nbsp;·&nbsp;&nbsp;
        <a href="https://github.com/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;
           font-family:'Inter',sans-serif; font-size:12px; font-weight:500;">
            💻 GitHub
        </a>
    </div>
</div>
""")
