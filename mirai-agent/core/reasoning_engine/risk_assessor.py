#!/usr/bin/env python3
"""
🧠 Risk Assessor - Steps 31-40
Подраздел 1.4: Risk Assessment

Features:
- Risk Categories Definition (Step 31)
- Risk Probability Estimation (Step 32)
- Risk Impact Assessment (Step 33)
- Risk Matrix Construction (Step 34)
- Mitigation Strategies (Step 35)
- Safety Constraints (Step 36)
- Pre/Post Action Checks (Steps 37-38)
- Rollback Planning (Step 39)
- Risk Acceptance Decision (Step 40)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class RiskCategory(Enum):
    """Step 31: Risk Categories"""
    SYSTEM = "system"
    DATA = "data"
    USER = "user"
    SECURITY = "security"
    PERFORMANCE = "performance"


class RiskLevel(Enum):
    """Risk severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class RiskProbability(Enum):
    """Step 32: Risk probability levels"""
    LOW = "low"  # 1-25%
    MEDIUM = "medium"  # 26-75%
    HIGH = "high"  # 76-100%


class RiskImpact(Enum):
    """Step 33: Risk impact levels"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


@dataclass
class Risk:
    """Risk definition"""
    category: RiskCategory
    description: str
    probability: RiskProbability
    impact: RiskImpact
    mitigation: str = ""
    severity: RiskLevel = RiskLevel.MEDIUM
    
    def to_dict(self) -> Dict:
        return {
            "category": self.category.value,
            "description": self.description,
            "probability": self.probability.value,
            "impact": self.impact.value,
            "mitigation": self.mitigation,
            "severity": self.severity.value
        }


@dataclass
class SafetyConstraints:
    """Step 36: Safety Constraints Definition"""
    max_memory_mb: int = 500
    max_cpu_percent: float = 80.0
    timeout_seconds: int = 60
    max_retries: int = 3
    require_confirmation: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "max_memory_mb": self.max_memory_mb,
            "max_cpu_percent": self.max_cpu_percent,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "require_confirmation": self.require_confirmation
        }


@dataclass
class RollbackPlan:
    """Step 39: Rollback Plan"""
    action_id: str
    rollback_steps: List[str] = field(default_factory=list)
    rollback_data: Dict[str, Any] = field(default_factory=dict)
    can_rollback: bool = True
    estimated_rollback_time: float = 0.0  # seconds
    
    def to_dict(self) -> Dict:
        return {
            "action_id": self.action_id,
            "rollback_steps": self.rollback_steps,
            "rollback_data": self.rollback_data,
            "can_rollback": self.can_rollback,
            "estimated_rollback_time": self.estimated_rollback_time
        }


class RiskAssessor:
    """
    🧠 Risk Assessment System
    
    Implements Steps 31-40: Risk Assessment subsystem
    """
    
    def __init__(self):
        self.risk_history: List[Risk] = []
        self.accepted_risks: List[Risk] = []
        
        # Risk matrix (Step 34): probability x impact
        self.risk_matrix = self._construct_risk_matrix()
        
        logger.info("✅ Risk Assessor initialized")
    
    def _construct_risk_matrix(self) -> Dict[str, Dict[str, RiskLevel]]:
        """
        Step 34: Risk Matrix Construction
        - Combine probability x impact
        - Create 5x5 matrix
        """
        matrix = {
            # Probability: LOW
            "low": {
                "minor": RiskLevel.MINIMAL,
                "moderate": RiskLevel.LOW,
                "severe": RiskLevel.MEDIUM,
                "critical": RiskLevel.HIGH
            },
            # Probability: MEDIUM
            "medium": {
                "minor": RiskLevel.LOW,
                "moderate": RiskLevel.MEDIUM,
                "severe": RiskLevel.HIGH,
                "critical": RiskLevel.CRITICAL
            },
            # Probability: HIGH
            "high": {
                "minor": RiskLevel.MEDIUM,
                "moderate": RiskLevel.HIGH,
                "severe": RiskLevel.CRITICAL,
                "critical": RiskLevel.CRITICAL
            }
        }
        
        return matrix
    
    def categorize_risks(self, action: Dict) -> List[Risk]:
        """
        Step 31: Risk Categories Definition
        - For each action determine which risks apply
        """
        risks = []
        action_type = action.get("type", "unknown")
        
        # System risks
        if action_type in ["run_command", "execute_code", "shutdown", "restart"]:
            risks.append(Risk(
                category=RiskCategory.SYSTEM,
                description="Action may affect system stability",
                probability=RiskProbability.MEDIUM,
                impact=RiskImpact.SEVERE
            ))
        
        # Data risks
        if action_type in ["delete", "overwrite", "format"]:
            risks.append(Risk(
                category=RiskCategory.DATA,
                description="Action may cause data loss",
                probability=RiskProbability.HIGH,
                impact=RiskImpact.CRITICAL
            ))
        
        # User risks
        if action_type in ["send_email", "post_message", "make_payment"]:
            risks.append(Risk(
                category=RiskCategory.USER,
                description="Action may affect user reputation or finances",
                probability=RiskProbability.MEDIUM,
                impact=RiskImpact.SEVERE
            ))
        
        # Security risks
        if action_type in ["download", "execute_script", "modify_permissions"]:
            risks.append(Risk(
                category=RiskCategory.SECURITY,
                description="Action may introduce security vulnerabilities",
                probability=RiskProbability.MEDIUM,
                impact=RiskImpact.SEVERE
            ))
        
        # Performance risks
        if action.get("resource_impact", 0) > 0.7:
            risks.append(Risk(
                category=RiskCategory.PERFORMANCE,
                description="Action requires significant resources",
                probability=RiskProbability.HIGH,
                impact=RiskImpact.MODERATE
            ))
        
        return risks
    
    def estimate_risk_probability(self, risk: Risk, historical_data: List[Dict]) -> RiskProbability:
        """
        Step 32: Risk Probability Estimation
        - What's the probability that risk will occur?
        - Low (1-25%), Medium (26-75%), High (76-100%)
        """
        # Check historical occurrences
        if historical_data:
            occurrences = sum(1 for event in historical_data 
                            if event.get("risk_occurred", False))
            rate = occurrences / len(historical_data)
            
            if rate > 0.75:
                return RiskProbability.HIGH
            elif rate > 0.25:
                return RiskProbability.MEDIUM
            else:
                return RiskProbability.LOW
        
        # Default based on risk category
        high_prob_categories = [RiskCategory.PERFORMANCE]
        if risk.category in high_prob_categories:
            return RiskProbability.HIGH
        
        return risk.probability
    
    def assess_risk_impact(self, risk: Risk) -> RiskImpact:
        """
        Step 33: Risk Impact Assessment
        - If risk occurs, what will be the damage?
        - Minor, Moderate, Severe, Critical
        """
        # Critical impacts
        if risk.category in [RiskCategory.DATA, RiskCategory.SECURITY]:
            return RiskImpact.CRITICAL
        
        # Severe impacts
        if risk.category in [RiskCategory.SYSTEM, RiskCategory.USER]:
            return RiskImpact.SEVERE
        
        # Moderate impacts
        if risk.category == RiskCategory.PERFORMANCE:
            return RiskImpact.MODERATE
        
        return risk.impact
    
    def calculate_risk_severity(self, risk: Risk) -> RiskLevel:
        """
        Step 34: Use risk matrix to calculate severity
        """
        prob = risk.probability.value
        impact = risk.impact.value
        
        return self.risk_matrix.get(prob, {}).get(impact, RiskLevel.MEDIUM)
    
    def develop_mitigation_strategies(self, risks: List[Risk]) -> List[Risk]:
        """
        Step 35: Risk Mitigation Strategies
        - For each High/Critical risk define mitigation
        - Preventive measures
        - Detective measures
        - Corrective measures
        """
        for risk in risks:
            # Update severity based on matrix
            risk.severity = self.calculate_risk_severity(risk)
            
            # Develop mitigation for high/critical risks
            if risk.severity in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                mitigation_strategies = {
                    RiskCategory.SYSTEM: "Run in sandbox, set resource limits, enable monitoring",
                    RiskCategory.DATA: "Create backup before action, enable version control",
                    RiskCategory.USER: "Request user confirmation, provide preview",
                    RiskCategory.SECURITY: "Run security scan, validate inputs, use encryption",
                    RiskCategory.PERFORMANCE: "Limit execution time, monitor resources, throttle requests"
                }
                
                risk.mitigation = mitigation_strategies.get(
                    risk.category,
                    "Monitor action closely, prepare rollback"
                )
        
        self.risk_history.extend(risks)
        return risks
    
    def define_safety_constraints(self, action: Dict) -> SafetyConstraints:
        """
        Step 36: Safety Constraints Definition
        - Set safety constraints for action
        - Max memory usage, timeout, etc.
        """
        action_type = action.get("type", "unknown")
        
        # Different constraints for different action types
        if action_type in ["execute_code", "run_command"]:
            return SafetyConstraints(
                max_memory_mb=1000,
                max_cpu_percent=70.0,
                timeout_seconds=30,
                max_retries=2,
                require_confirmation=True
            )
        
        elif action_type in ["delete", "overwrite"]:
            return SafetyConstraints(
                max_memory_mb=100,
                max_cpu_percent=50.0,
                timeout_seconds=10,
                max_retries=0,
                require_confirmation=True
            )
        
        else:
            return SafetyConstraints(
                max_memory_mb=500,
                max_cpu_percent=60.0,
                timeout_seconds=60,
                max_retries=3,
                require_confirmation=False
            )
    
    def perform_pre_action_checks(self, action: Dict, context: Dict) -> Dict[str, Any]:
        """
        Step 37: Pre-Action Checks
        - Before executing action, what to check?
        - Is system stable? Has enough resources?
        """
        checks = {
            "system_stable": True,
            "resources_available": True,
            "dependencies_met": True,
            "all_passed": True,
            "checks": []
        }
        
        # System stability check
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > 90:
            checks["system_stable"] = False
            checks["checks"].append("CPU usage too high")
        
        if memory_percent > 90:
            checks["system_stable"] = False
            checks["checks"].append("Memory usage too high")
        
        # Resource availability check
        constraints = self.define_safety_constraints(action)
        if memory_percent + (constraints.max_memory_mb / 1024 / 16) > 95:  # Rough estimate
            checks["resources_available"] = False
            checks["checks"].append("Insufficient memory available")
        
        # Dependencies check
        dependencies = action.get("dependencies", [])
        if dependencies:
            # Check if dependencies are met (simplified)
            completed_actions = context.get("completed_actions", [])
            for dep in dependencies:
                if dep not in completed_actions:
                    checks["dependencies_met"] = False
                    checks["checks"].append(f"Dependency not met: {dep}")
        
        checks["all_passed"] = (
            checks["system_stable"] and 
            checks["resources_available"] and 
            checks["dependencies_met"]
        )
        
        return checks
    
    def perform_post_action_verification(self, action: Dict, result: Dict) -> Dict[str, Any]:
        """
        Step 38: Post-Action Verification
        - After action, what to check?
        - Did it succeed? Any side effects?
        """
        verification = {
            "success": result.get("success", False),
            "side_effects_detected": False,
            "system_stable": True,
            "verification_passed": True,
            "issues": []
        }
        
        # Check for errors in result
        if result.get("error"):
            verification["success"] = False
            verification["issues"].append(f"Error: {result['error']}")
        
        # Check system stability after action
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        if cpu_percent > 95:
            verification["system_stable"] = False
            verification["issues"].append("System under heavy load after action")
        
        # Check for unexpected side effects
        expected_changes = action.get("expected_changes", [])
        actual_changes = result.get("changes", [])
        
        unexpected = [c for c in actual_changes if c not in expected_changes]
        if unexpected:
            verification["side_effects_detected"] = True
            verification["issues"].append(f"Unexpected changes: {unexpected}")
        
        verification["verification_passed"] = (
            verification["success"] and 
            verification["system_stable"] and 
            not verification["side_effects_detected"]
        )
        
        return verification
    
    def plan_rollback(self, action: Dict) -> RollbackPlan:
        """
        Step 39: Rollback Planning
        - If something goes wrong, how to rollback?
        - For each action, is there a rollback plan?
        """
        action_type = action.get("type", "unknown")
        action_id = action.get("id", "unknown")
        
        # Irreversible actions
        if action_type in ["delete", "send_email", "post_message"]:
            return RollbackPlan(
                action_id=action_id,
                can_rollback=False,
                rollback_steps=["Action is irreversible"],
                estimated_rollback_time=0.0
            )
        
        # Easy rollback actions
        if action_type in ["click", "type"]:
            return RollbackPlan(
                action_id=action_id,
                can_rollback=True,
                rollback_steps=["Press Ctrl+Z", "Or navigate back"],
                estimated_rollback_time=1.0
            )
        
        # File operations
        if action_type in ["write_file", "modify_file"]:
            return RollbackPlan(
                action_id=action_id,
                can_rollback=True,
                rollback_steps=[
                    "Restore from backup",
                    "Or revert to previous version"
                ],
                rollback_data={"backup_path": action.get("backup_path")},
                estimated_rollback_time=5.0
            )
        
        # Default rollback
        return RollbackPlan(
            action_id=action_id,
            can_rollback=True,
            rollback_steps=["Undo action", "Restore previous state"],
            estimated_rollback_time=10.0
        )
    
    def accept_or_reject_risks(self, risk_assessment: Dict) -> bool:
        """
        Step 40: Risk Acceptance Decision
        - Is agent ready to accept remaining risks?
        - If no - choose another action
        - If yes - proceed
        """
        risks = risk_assessment.get("risks", [])
        
        # Reject if any CRITICAL risks without mitigation
        for risk in risks:
            if isinstance(risk, Risk):
                if risk.severity == RiskLevel.CRITICAL and not risk.mitigation:
                    logger.warning(f"❌ Rejecting due to unmitigated critical risk: {risk.description}")
                    return False
        
        # Reject if too many HIGH risks
        high_risks = [r for r in risks if isinstance(r, Risk) and r.severity == RiskLevel.HIGH]
        if len(high_risks) > 3:
            logger.warning(f"❌ Rejecting due to too many high risks: {len(high_risks)}")
            return False
        
        # Accept if all risks are mitigated or low/medium
        logger.info(f"✅ Accepting risks: {len(risks)} total risks identified")
        self.accepted_risks.extend([r for r in risks if isinstance(r, Risk)])
        return True
    
    def assess_action(self, action: Dict, context: Dict) -> Dict:
        """
        Complete risk assessment for an action
        
        Returns:
            Risk assessment with all components
        """
        logger.info(f"🔍 Assessing risks for action: {action.get('type', 'unknown')}")
        
        # Steps 31-34: Identify and categorize risks
        risks = self.categorize_risks(action)
        risks = self.develop_mitigation_strategies(risks)
        
        # Step 36: Define safety constraints
        constraints = self.define_safety_constraints(action)
        
        # Step 37: Pre-action checks
        pre_checks = self.perform_pre_action_checks(action, context)
        
        # Step 39: Rollback planning
        rollback = self.plan_rollback(action)
        
        # Create assessment
        assessment = {
            "action_id": action.get("id", "unknown"),
            "risks": risks,
            "total_risks": len(risks),
            "critical_risks": len([r for r in risks if r.severity == RiskLevel.CRITICAL]),
            "high_risks": len([r for r in risks if r.severity == RiskLevel.HIGH]),
            "constraints": constraints.to_dict(),
            "pre_checks": pre_checks,
            "rollback_plan": rollback.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 40: Accept or reject
        assessment["accepted"] = self.accept_or_reject_risks(assessment)
        
        return assessment
