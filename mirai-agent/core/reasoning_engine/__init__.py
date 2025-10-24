#!/usr/bin/env python3
"""
🧠 MIRAI Phase 2: Reasoning Engine

Advanced decision-making and reasoning system for autonomous operation.

Components:
- DecisionMaker: Decision making foundation (Steps 1-40)
- ContextProcessor: Context processing (Steps 56-70)
- IntelligentPlanner: Intelligent planning (Steps 91-140)
- MemorySystem: Enhanced memory management (Steps 41-55)
- RiskAssessor: Risk assessment and mitigation (Steps 31-40)
- PreferenceManager: User preference learning (Steps 71-90)

Version: 2.0.0
Codename: REASONING
"""

from .decision_maker import DecisionMaker, Action, DecisionParameters, ActionPriority
from .context_processor import (
    ContextProcessor,
    ApplicationState,
    ApplicationStatus,
    UIElementState,
    AppRegistry,
)
from .intelligent_planner import (
    IntelligentPlanner,
    Task,
    TaskStatus,
    ExecutionPlan,
)
from .memory_system import (
    ShortTermMemory,
    LongTermMemory,
    SessionMemory,
    EventActionResult,
    MemoryContextIntegration,
)
from .risk_assessor import (
    RiskAssessor,
    Risk,
    RiskCategory,
    RiskLevel,
    RiskProbability,
    RiskImpact,
    SafetyConstraints,
    RollbackPlan,
)
from .preference_manager import PreferenceManager, UserProfile

__all__ = [
    # Decision Making
    "DecisionMaker",
    "Action",
    "DecisionParameters",
    "ActionPriority",
    # Context Processing
    "ContextProcessor",
    "ApplicationState",
    "ApplicationStatus",
    "UIElementState",
    "AppRegistry",
    # Intelligent Planning
    "IntelligentPlanner",
    "Task",
    "TaskStatus",
    "ExecutionPlan",
    # Memory System
    "ShortTermMemory",
    "LongTermMemory",
    "SessionMemory",
    "EventActionResult",
    "MemoryContextIntegration",
    # Risk Assessment
    "RiskAssessor",
    "Risk",
    "RiskCategory",
    "RiskLevel",
    "RiskProbability",
    "RiskImpact",
    "SafetyConstraints",
    "RollbackPlan",
    # Preferences
    "PreferenceManager",
    "UserProfile",
]

__version__ = "2.0.0"
