#!/usr/bin/env python3
"""
🧠 Decision Maker - Steps 1-40
РАЗДЕЛ 1: DECISION MAKING FOUNDATION

Подсистемы:
1.1: Situation Analysis (Steps 1-10)
1.2: Multi-Factor Evaluation (Steps 11-20)
1.3: Prioritization & Ranking (Steps 21-30)
1.4: Risk Assessment (Steps 31-40)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import json

logger = logging.getLogger(__name__)


class ActionPriority(Enum):
    """Приоритет действия"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


@dataclass
class Action:
    """Действие которое может выполнить агент"""
    id: str
    name: str
    description: str
    action_type: str  # "click", "type", "navigate", etc.
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Evaluation scores (Steps 11-20)
    effectiveness_score: float = 0.0  # Step 11
    safety_score: float = 0.0  # Step 12
    time_complexity: float = 0.0  # Step 13 (seconds)
    resource_impact: float = 0.0  # Step 14 (0-1 scale)
    
    # Dependencies and conflicts (Steps 15-16)
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    
    # Alternatives and reversibility (Steps 17-18)
    alternatives: List[str] = field(default_factory=list)
    reversible: bool = True
    
    # Side effects and confidence (Steps 19-20)
    side_effects: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    # Priority and ranking (Steps 21-30)
    priority: ActionPriority = ActionPriority.MEDIUM
    rank: float = 0.0
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DecisionParameters:
    """Параметры для принятия решения"""
    visual_context: Dict[str, Any] = field(default_factory=dict)
    application_state: Dict[str, Any] = field(default_factory=dict)
    user_intent: str = ""
    available_actions: List[Action] = field(default_factory=list)
    context_window: List[Dict] = field(default_factory=list)
    risks: List[Dict] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    historical_patterns: List[Dict] = field(default_factory=list)


class DecisionMaker:
    """
    🧠 Decision Making Foundation
    
    Implements Steps 1-40 of Phase 2 Reasoning Engine:
    - Situation Analysis (1-10)
    - Multi-Factor Evaluation (11-20)
    - Prioritization & Ranking (21-30)
    - Risk Assessment (31-40)
    """
    
    def __init__(self, vision_system=None, memory_manager=None):
        """
        Step 1: Initialize Decision Maker
        - Load models GPT-4o
        - Initialize context memory
        - Prepare decision parameters
        """
        self.vision_system = vision_system
        self.memory_manager = memory_manager
        self.decision_history: List[Dict] = []
        self.context_memory: List[Dict] = []
        self.max_context_tokens = 8000  # Step 6: Context window limit
        
        # Weights for weighted analysis (Step 22)
        self.factor_weights = {
            "effectiveness": 0.3,
            "safety": 0.3,
            "speed": 0.2,
            "resources": 0.2
        }
        
        logger.info("✅ Decision Maker initialized")
    
    # ═══════════════════════════════════════════════════════════════
    # Subsection 1.1: Situation Analysis (Steps 1-10)
    # ═══════════════════════════════════════════════════════════════
    
    def get_visual_context(self) -> Dict[str, Any]:
        """
        Step 2: Capture Visual Context
        - Get latest screenshot from Vision System
        - Parse Vision Analysis result
        - Extract screen element information
        """
        if not self.vision_system:
            return {"elements": [], "status": "no_vision_system"}
        
        try:
            # Get current screen analysis
            screenshot_analysis = self.vision_system.analyze_current_screen()
            return {
                "elements": screenshot_analysis.get("elements", []),
                "application": screenshot_analysis.get("application", "unknown"),
                "status": screenshot_analysis.get("status", "ready"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get visual context: {e}")
            return {"elements": [], "status": "error", "error": str(e)}
    
    def analyze_application_state(self, visual_context: Dict) -> Dict[str, Any]:
        """
        Step 3: Analyze Application State
        - Determine which application is active
        - Check state (loading, ready, error)
        - Update Application State in memory
        """
        app_name = visual_context.get("application", "unknown")
        status = visual_context.get("status", "unknown")
        
        state = {
            "application": app_name,
            "status": status,
            "is_ready": status == "ready",
            "is_loading": status == "loading",
            "is_error": status == "error",
            "timestamp": datetime.now().isoformat()
        }
        
        # Update memory
        if self.memory_manager:
            try:
                self.memory_manager.store_application_state(state)
            except Exception as e:
                logger.warning(f"Could not store app state: {e}")
        
        return state
    
    def extract_user_intent(self, task: str) -> Dict[str, Any]:
        """
        Step 4: Extract User Intent
        - Understand user's goal from high-level task
        - Break down into sub-goals
        - Determine priority
        """
        # Simple intent extraction (can be enhanced with GPT-4)
        intent = {
            "main_goal": task,
            "sub_goals": self._decompose_task(task),
            "priority": self._determine_priority(task),
            "estimated_steps": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        intent["estimated_steps"] = len(intent["sub_goals"])
        return intent
    
    def _decompose_task(self, task: str) -> List[str]:
        """Helper: Decompose task into sub-goals"""
        # Basic decomposition (can be enhanced)
        keywords = {
            "search": ["open browser", "navigate to search", "enter query", "get results"],
            "open": ["locate application", "launch application", "wait for ready"],
            "type": ["find text field", "click field", "enter text"],
            "click": ["locate element", "move to element", "click element"]
        }
        
        task_lower = task.lower()
        for key, steps in keywords.items():
            if key in task_lower:
                return steps
        
        return [task]  # Default: single step
    
    def _determine_priority(self, task: str) -> ActionPriority:
        """Helper: Determine task priority"""
        urgent_keywords = ["urgent", "critical", "immediate", "now", "asap"]
        high_keywords = ["important", "priority", "soon"]
        
        task_lower = task.lower()
        if any(kw in task_lower for kw in urgent_keywords):
            return ActionPriority.CRITICAL
        elif any(kw in task_lower for kw in high_keywords):
            return ActionPriority.HIGH
        else:
            return ActionPriority.MEDIUM
    
    def get_available_actions(self, visual_context: Dict) -> List[Action]:
        """
        Step 5: Analyze Available Actions
        - Based on Vision data determine possible actions
        - Create list of available buttons, fields, options
        """
        actions = []
        elements = visual_context.get("elements", [])
        
        for idx, element in enumerate(elements):
            element_type = element.get("type", "unknown")
            
            # Generate action based on element type
            if element_type == "button":
                actions.append(Action(
                    id=f"click_button_{idx}",
                    name=f"Click {element.get('label', 'button')}",
                    description=f"Click on button: {element.get('label', 'unknown')}",
                    action_type="click",
                    parameters={"element": element, "coordinates": element.get("coordinates")}
                ))
            elif element_type == "input":
                actions.append(Action(
                    id=f"type_input_{idx}",
                    name=f"Type in {element.get('label', 'input field')}",
                    description=f"Enter text in: {element.get('label', 'unknown')}",
                    action_type="type",
                    parameters={"element": element, "coordinates": element.get("coordinates")}
                ))
        
        logger.info(f"Found {len(actions)} available actions")
        return actions
    
    def manage_context_window(self, full_context: List[Dict]) -> List[Dict]:
        """
        Step 6: Context Window Management
        - Select relevant parts from memory
        - Limit context for GPT-4o (max 8k tokens)
        - Prioritize recent events
        """
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        def estimate_tokens(context: List[Dict]) -> int:
            total_chars = sum(len(json.dumps(item)) for item in context)
            return total_chars // 4
        
        # Start with recent events
        relevant_context = []
        for item in reversed(full_context):
            relevant_context.insert(0, item)
            if estimate_tokens(relevant_context) > self.max_context_tokens:
                relevant_context.pop(0)
                break
        
        logger.info(f"Context window: {len(relevant_context)} items, ~{estimate_tokens(relevant_context)} tokens")
        return relevant_context
    
    def identify_risks(self, action: Action, context: Dict) -> List[Dict]:
        """
        Step 7: Risk Identification
        - Identify potential risks
        - Classify by severity
        - Prepare mitigation strategies
        """
        risks = []
        
        # System stability risk
        if action.action_type in ["run_command", "execute_code"]:
            risks.append({
                "type": "system_stability",
                "severity": "high",
                "description": "Command execution might affect system stability",
                "mitigation": "Run in sandboxed environment, set timeout"
            })
        
        # Data loss risk
        if action.action_type in ["delete", "overwrite"]:
            risks.append({
                "type": "data_loss",
                "severity": "critical",
                "description": "Action may delete or overwrite data",
                "mitigation": "Create backup before action, confirm with user"
            })
        
        # Resource exhaustion
        if action.resource_impact > 0.7:
            risks.append({
                "type": "resource_exhaustion",
                "severity": "medium",
                "description": "Action requires significant resources",
                "mitigation": "Check available resources, limit execution time"
            })
        
        return risks
    
    def check_constraints(self) -> Dict[str, Any]:
        """
        Step 8: Constraint Checking
        - Check system constraints (RAM, CPU, disk)
        - Check action limits
        - Check timeouts
        """
        import psutil
        
        constraints = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "cpu_available": psutil.cpu_percent(interval=0.1) < 80,
            "memory_available": psutil.virtual_memory().percent < 85,
            "disk_available": psutil.disk_usage('/').percent < 90,
            "timestamp": datetime.now().isoformat()
        }
        
        constraints["all_ok"] = all([
            constraints["cpu_available"],
            constraints["memory_available"],
            constraints["disk_available"]
        ])
        
        return constraints
    
    def find_historical_patterns(self, current_situation: Dict) -> List[Dict]:
        """
        Step 9: Historical Pattern Matching
        - Find similar situations in history
        - Extract what worked before
        - Determine what didn't work
        """
        if not self.memory_manager:
            return []
        
        patterns = []
        try:
            # Search for similar past situations
            similar_events = self.memory_manager.find_similar_situations(
                current_situation, limit=5
            )
            
            for event in similar_events:
                patterns.append({
                    "situation": event.get("situation"),
                    "action_taken": event.get("action"),
                    "result": event.get("result"),
                    "success": event.get("success", False),
                    "timestamp": event.get("timestamp")
                })
        except Exception as e:
            logger.warning(f"Pattern matching failed: {e}")
        
        return patterns
    
    def prepare_decision_parameters(
        self, 
        task: str, 
        visual_context: Optional[Dict] = None
    ) -> DecisionParameters:
        """
        Step 10: Prepare Decision Parameters
        - Collect all data for decision making
        - Create structured input for GPT-4o
        """
        # Get all necessary context
        if visual_context is None:
            visual_context = self.get_visual_context()
        
        app_state = self.analyze_application_state(visual_context)
        user_intent = self.extract_user_intent(task)
        available_actions = self.get_available_actions(visual_context)
        context_window = self.manage_context_window(self.context_memory)
        constraints = self.check_constraints()
        
        # Create decision parameters
        params = DecisionParameters(
            visual_context=visual_context,
            application_state=app_state,
            user_intent=user_intent["main_goal"],
            available_actions=available_actions,
            context_window=context_window,
            constraints=constraints,
            historical_patterns=self.find_historical_patterns({
                "task": task,
                "application": app_state.get("application")
            })
        )
        
        logger.info(f"✅ Decision parameters prepared: {len(available_actions)} actions available")
        return params
    
    # ═══════════════════════════════════════════════════════════════
    # Subsection 1.2: Multi-Factor Evaluation (Steps 11-20)
    # ═══════════════════════════════════════════════════════════════
    
    def score_effectiveness(self, action: Action, context: Dict) -> float:
        """
        Step 11: Effectiveness Scoring
        - For each action estimate success probability
        - Use historical data
        - Consider complexity
        """
        score = 0.5  # Base score
        
        # Check historical success rate
        if self.memory_manager:
            history = self.memory_manager.get_action_history(action.action_type)
            if history:
                success_rate = sum(1 for h in history if h.get("success")) / len(history)
                score = success_rate
        
        # Adjust for complexity
        param_count = len(action.parameters)
        if param_count > 5:
            score *= 0.8  # Complex actions less likely to succeed
        
        # Adjust for dependencies
        if action.dependencies:
            score *= 0.9  # Dependencies reduce effectiveness
        
        return min(1.0, max(0.0, score))
    
    def assess_safety(self, action: Action) -> float:
        """
        Step 12: Safety Assessment
        - Evaluate how safe the action is
        - Can it break the system?
        - Is there rollback capability?
        """
        safety = 1.0  # Default: safe
        
        # Dangerous action types
        dangerous_types = ["delete", "format", "shutdown", "kill_process"]
        if action.action_type in dangerous_types:
            safety = 0.3
        
        # Reduce safety if not reversible
        if not action.reversible:
            safety *= 0.7
        
        # Increase safety if has alternatives
        if action.alternatives:
            safety = min(1.0, safety * 1.2)
        
        return min(1.0, max(0.0, safety))
    
    def estimate_time_complexity(self, action: Action) -> float:
        """
        Step 13: Time Complexity Analysis
        - How long will the action take?
        - Does it fit within deadline?
        - Need optimization?
        """
        # Base time estimates (seconds)
        time_estimates = {
            "click": 0.5,
            "type": 2.0,
            "navigate": 3.0,
            "search": 5.0,
            "run_command": 10.0,
            "execute_code": 15.0
        }
        
        base_time = time_estimates.get(action.action_type, 5.0)
        
        # Adjust for complexity
        param_count = len(action.parameters)
        adjusted_time = base_time * (1 + param_count * 0.1)
        
        return adjusted_time
    
    def assess_resource_impact(self, action: Action) -> float:
        """
        Step 14: Resource Impact Assessment
        - How much memory/CPU will it require?
        - Are there sufficient resources?
        - Need to free resources?
        """
        # Resource impact scale: 0.0 (none) to 1.0 (maximum)
        impact_map = {
            "click": 0.1,
            "type": 0.1,
            "navigate": 0.3,
            "search": 0.4,
            "run_command": 0.6,
            "execute_code": 0.8,
            "open_application": 0.5
        }
        
        return impact_map.get(action.action_type, 0.3)
    
    def check_dependencies(self, action: Action, all_actions: List[Action]) -> List[str]:
        """
        Step 15: Dependency Checking
        - What other actions must be done first?
        - Any circular dependencies?
        - Correct order?
        """
        dependencies = []
        
        # Example: typing requires field to be focused (clicked first)
        if action.action_type == "type":
            # Look for click action on same element
            for other in all_actions:
                if (other.action_type == "click" and 
                    other.parameters.get("element") == action.parameters.get("element")):
                    dependencies.append(other.id)
        
        return dependencies
    
    def detect_conflicts(self, action: Action, planned_actions: List[Action]) -> List[str]:
        """
        Step 16: Conflict Detection
        - Are there conflicts with other actions?
        - Could action interfere with another?
        - Need synchronization?
        """
        conflicts = []
        
        # Check for resource conflicts
        for other in planned_actions:
            # Same element conflict
            if (action.parameters.get("element") == other.parameters.get("element") and
                action.id != other.id):
                conflicts.append(other.id)
        
        return conflicts
    
    def generate_alternatives(self, action: Action) -> List[str]:
        """
        Step 17: Alternative Options Generation
        - Find alternatives for each action
        - Minimum 3 options
        - Evaluate pros/cons
        """
        alternatives = []
        
        # Type alternatives
        if action.action_type == "type":
            alternatives.extend([
                "use_clipboard_paste",
                "use_keyboard_shortcuts",
                "use_autocomplete"
            ])
        
        # Click alternatives
        elif action.action_type == "click":
            alternatives.extend([
                "use_keyboard_enter",
                "use_keyboard_shortcut",
                "double_click"
            ])
        
        # Navigation alternatives
        elif action.action_type == "navigate":
            alternatives.extend([
                "use_url_bar",
                "use_bookmarks",
                "use_history"
            ])
        
        return alternatives[:3]  # Minimum 3
    
    def analyze_reversibility(self, action: Action) -> Tuple[bool, str]:
        """
        Step 18: Reversibility Analysis
        - Can the action be undone?
        - How difficult to rollback?
        - Any side effects?
        """
        # Irreversible actions
        irreversible = ["delete", "format", "send_email", "post_message"]
        if action.action_type in irreversible:
            return False, "Cannot undo this action"
        
        # Easily reversible
        reversible = ["click", "type", "navigate"]
        if action.action_type in reversible:
            return True, "Easy to undo (Ctrl+Z or back button)"
        
        # Moderately reversible
        return True, "Can be undone but requires multiple steps"
    
    def predict_side_effects(self, action: Action) -> List[str]:
        """
        Step 19: Side Effects Prediction
        - What side effects might occur?
        - How will they affect the system?
        - Need protection?
        """
        side_effects = []
        
        # Navigation side effects
        if action.action_type == "navigate":
            side_effects.extend([
                "May trigger page load",
                "Might show popups/ads",
                "Could lose current form data"
            ])
        
        # Code execution side effects
        if action.action_type in ["run_command", "execute_code"]:
            side_effects.extend([
                "May affect system state",
                "Could create files/processes",
                "Might consume significant resources"
            ])
        
        return side_effects
    
    def calculate_confidence(self, action: Action, all_factors: Dict) -> float:
        """
        Step 20: Decision Confidence Calculation
        - Based on all factors calculate confidence
        - Percentage probability of success
        - Need additional verification?
        """
        # Weighted combination of factors
        effectiveness = all_factors.get("effectiveness", 0.5)
        safety = all_factors.get("safety", 0.5)
        
        # Start with effectiveness
        confidence = effectiveness
        
        # Safety factor
        confidence *= safety
        
        # Reduce if has unresolved dependencies
        if action.dependencies:
            confidence *= 0.8
        
        # Reduce if has conflicts
        if action.conflicts:
            confidence *= 0.7
        
        # Increase if has successful history
        if all_factors.get("historical_success", 0) > 0.7:
            confidence = min(1.0, confidence * 1.2)
        
        return min(1.0, max(0.0, confidence))
    
    # ═══════════════════════════════════════════════════════════════
    # Subsection 1.3: Prioritization & Ranking (Steps 21-30)
    # ═══════════════════════════════════════════════════════════════
    
    def evaluate_actions(self, actions: List[Action], context: Dict) -> List[Action]:
        """
        Evaluate all actions with multi-factor analysis (Steps 11-20)
        """
        for action in actions:
            # Score all factors
            factors = {
                "effectiveness": self.score_effectiveness(action, context),
                "safety": self.assess_safety(action),
                "time": self.estimate_time_complexity(action),
                "resources": self.assess_resource_impact(action)
            }
            
            # Store scores
            action.effectiveness_score = factors["effectiveness"]
            action.safety_score = factors["safety"]
            action.time_complexity = factors["time"]
            action.resource_impact = factors["resources"]
            
            # Dependencies and conflicts
            action.dependencies = self.check_dependencies(action, actions)
            action.conflicts = self.detect_conflicts(action, actions)
            
            # Alternatives and reversibility
            action.alternatives = self.generate_alternatives(action)
            action.reversible, _ = self.analyze_reversibility(action)
            
            # Side effects and confidence
            action.side_effects = self.predict_side_effects(action)
            action.confidence = self.calculate_confidence(action, factors)
        
        return actions
    
    def rank_actions(self, actions: List[Action]) -> List[Action]:
        """
        Step 21-25: Action Priority Scoring and Ranking
        - Rank actions by priority
        - Apply weighted factor analysis
        - Pareto optimization
        """
        for action in actions:
            # Weighted score (Step 22)
            weighted_score = (
                action.effectiveness_score * self.factor_weights["effectiveness"] +
                action.safety_score * self.factor_weights["safety"] +
                (1.0 - action.time_complexity / 60.0) * self.factor_weights["speed"] +  # Normalize time
                (1.0 - action.resource_impact) * self.factor_weights["resources"]
            )
            
            action.rank = weighted_score
        
        # Sort by rank (highest first)
        ranked = sorted(actions, key=lambda a: a.rank, reverse=True)
        
        logger.info(f"Ranked {len(ranked)} actions")
        return ranked
    
    def select_top_actions(self, ranked_actions: List[Action], top_k: int = 3) -> List[Action]:
        """
        Step 26: Top Actions Selection
        - Select top-k actions for GPT-4o
        - Prepare detailed description of each
        """
        top_actions = ranked_actions[:top_k]
        
        logger.info(f"Selected top {len(top_actions)} actions:")
        for idx, action in enumerate(top_actions, 1):
            logger.info(f"  {idx}. {action.name} (rank: {action.rank:.3f}, confidence: {action.confidence:.3f})")
        
        return top_actions
    
    def prepare_fallback_actions(self, top_actions: List[Action]) -> Dict[str, List[str]]:
        """
        Step 27: Fallback Actions Preparation
        - If top-1 fails, what to do?
        - Prepare fallback for top-2 and top-3
        """
        fallback_plan = {}
        
        for idx, action in enumerate(top_actions):
            fallback_plan[action.id] = action.alternatives[:2] if action.alternatives else []
        
        return fallback_plan
    
    def define_emergency_actions(self) -> List[Dict]:
        """
        Step 28: Emergency Actions Definition
        - If nothing works, what's the emergency plan?
        - How to stop the agent?
        - How to recover?
        """
        emergency_actions = [
            {
                "name": "stop_all_actions",
                "description": "Stop all running actions immediately",
                "trigger": "critical_error"
            },
            {
                "name": "restore_last_state",
                "description": "Restore to last known good state",
                "trigger": "multiple_failures"
            },
            {
                "name": "request_human_help",
                "description": "Alert user for manual intervention",
                "trigger": "unable_to_proceed"
            }
        ]
        
        return emergency_actions
    
    def prepare_gpt4o_input(self, top_actions: List[Action], context: DecisionParameters) -> Dict:
        """
        Step 30: Prepare GPT-4o Decision Input
        - Form final input for model
        - Structured JSON/Markdown
        - Contains top-3 actions with metadata
        """
        input_data = {
            "task": context.user_intent,
            "application_state": context.application_state,
            "visual_context": {
                "application": context.visual_context.get("application"),
                "status": context.visual_context.get("status"),
                "element_count": len(context.visual_context.get("elements", []))
            },
            "constraints": context.constraints,
            "top_actions": [
                {
                    "id": action.id,
                    "name": action.name,
                    "description": action.description,
                    "type": action.action_type,
                    "rank": action.rank,
                    "confidence": action.confidence,
                    "effectiveness": action.effectiveness_score,
                    "safety": action.safety_score,
                    "time_estimate": action.time_complexity,
                    "reversible": action.reversible,
                    "alternatives": action.alternatives,
                    "side_effects": action.side_effects
                }
                for action in top_actions
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return input_data
    
    # ═══════════════════════════════════════════════════════════════
    # Main Decision Making Flow
    # ═══════════════════════════════════════════════════════════════
    
    def make_decision(self, task: str, visual_context: Optional[Dict] = None) -> Dict:
        """
        Complete decision making process (Steps 1-30)
        
        Returns:
            Decision with selected action and metadata
        """
        logger.info(f"🧠 Making decision for task: {task}")
        
        # Step 10: Prepare all parameters
        params = self.prepare_decision_parameters(task, visual_context)
        
        # Steps 11-20: Evaluate all actions
        evaluated_actions = self.evaluate_actions(params.available_actions, {
            "visual": params.visual_context,
            "app_state": params.application_state
        })
        
        # Steps 21-26: Rank and select top actions
        ranked_actions = self.rank_actions(evaluated_actions)
        top_actions = self.select_top_actions(ranked_actions, top_k=3)
        
        # Steps 27-28: Prepare fallbacks and emergency plan
        fallback_plan = self.prepare_fallback_actions(top_actions)
        emergency_plan = self.define_emergency_actions()
        
        # Step 30: Prepare final decision
        decision = {
            "task": task,
            "selected_action": top_actions[0] if top_actions else None,
            "alternative_actions": top_actions[1:] if len(top_actions) > 1 else [],
            "fallback_plan": fallback_plan,
            "emergency_plan": emergency_plan,
            "confidence": top_actions[0].confidence if top_actions else 0.0,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "total_actions_evaluated": len(params.available_actions),
                "constraints_ok": params.constraints.get("all_ok", False),
                "visual_elements": len(params.visual_context.get("elements", []))
            }
        }
        
        # Store in history
        self.decision_history.append(decision)
        
        logger.info(f"✅ Decision made: {decision['selected_action'].name if decision['selected_action'] else 'No action'}")
        return decision
