#!/usr/bin/env python3
"""
🧠 Preference Manager - Steps 71-90
Подраздел 2.3: User Preferences & Patterns

Features:
- Preference Learning (Step 71)
- Work Pattern Analysis (Step 72)
- Application Usage Patterns (Step 73)
- Search Query Patterns (Step 74)
- File Access Patterns (Step 75)
- UI Interaction Patterns (Step 76)
- Error Recovery Preferences (Step 77)
- Decision-Making Preferences (Step 78)
- Time Preferences (Step 79)
- Confidence Calibration (Step 80)
"""

import logging
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, time
from typing import Any, Dict, List, Optional
from pathlib import Path
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    """
    Step 81: Preference Personalization
    - All preferences combined in Profile
    - Each user has own Profile
    - Agent adapts to profile
    """
    user_id: str
    
    # Step 71: Browser and tool preferences
    preferred_browser: str = "chrome"
    preferred_profile: Optional[str] = None
    preferred_search_language: str = "en"
    
    # Step 72: Work patterns
    work_hours_start: time = time(9, 0)
    work_hours_end: time = time(17, 0)
    works_weekends: bool = False
    active_days: List[str] = field(default_factory=lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    
    # Step 73: Application usage
    app_sequence: List[str] = field(default_factory=list)
    frequently_used_apps: Dict[str, int] = field(default_factory=dict)
    
    # Step 74: Search patterns
    search_categories: Dict[str, int] = field(default_factory=dict)
    favorite_websites: List[str] = field(default_factory=list)
    
    # Step 75: File access patterns
    common_directories: List[str] = field(default_factory=list)
    common_file_extensions: List[str] = field(default_factory=list)
    
    # Step 76: UI interaction patterns
    click_speed: str = "normal"  # slow, normal, fast
    prefers_keyboard: bool = False
    click_pattern: str = "center"  # corners, center, mixed
    
    # Step 77: Error recovery
    error_recovery_style: str = "conservative"  # aggressive, conservative
    preferred_undo_method: str = "ctrl_z"  # ctrl_z, menu, reload
    
    # Step 78: Decision making
    risk_tolerance: str = "medium"  # low, medium, high
    decision_speed: str = "balanced"  # fast, balanced, careful
    
    # Step 79: Time preferences
    acceptable_deadline: int = 60  # seconds
    patience_level: str = "patient"  # impatient, patient, very_patient
    
    # Step 80: Confidence calibration
    confidence_threshold: float = 0.7  # Require confirmation if below this
    auto_execute_threshold: float = 0.9  # Auto-execute if above this
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    total_interactions: int = 0
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["last_updated"] = self.last_updated.isoformat()
        d["work_hours_start"] = self.work_hours_start.isoformat()
        d["work_hours_end"] = self.work_hours_end.isoformat()
        return d
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Load profile from dict"""
        # Convert datetime strings
        if "created_at" in data:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data:
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        if "work_hours_start" in data:
            data["work_hours_start"] = time.fromisoformat(data["work_hours_start"])
        if "work_hours_end" in data:
            data["work_hours_end"] = time.fromisoformat(data["work_hours_end"])
        
        return cls(**data)


class PreferenceManager:
    """
    🧠 User Preferences & Patterns Manager
    
    Implements Steps 71-90: Learning and adapting to user preferences
    """
    
    def __init__(self, user_id: str, data_dir: Optional[Path] = None):
        self.user_id = user_id
        
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data" / "preferences"
        
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_path = self.data_dir / f"{user_id}_profile.json"
        
        # Load or create profile
        self.profile = self._load_profile()
        
        # Pattern tracking
        self.interaction_history: List[Dict] = []
        self.app_usage_log: List[Dict] = []
        self.search_history: List[Dict] = []
        self.file_access_log: List[Dict] = []
        
        logger.info(f"✅ Preference Manager initialized for user: {user_id}")
    
    def _load_profile(self) -> UserProfile:
        """Load user profile from disk"""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    data = json.load(f)
                    return UserProfile.from_dict(data)
            except Exception as e:
                logger.warning(f"Failed to load profile: {e}, creating new one")
        
        return UserProfile(user_id=self.user_id)
    
    def _save_profile(self):
        """Save user profile to disk"""
        try:
            self.profile.last_updated = datetime.now()
            with open(self.profile_path, 'w') as f:
                json.dump(self.profile.to_dict(), f, indent=2)
            logger.debug(f"Profile saved for {self.user_id}")
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # Preference Learning (Steps 71-80)
    # ═══════════════════════════════════════════════════════════════
    
    def learn_browser_preference(self, browser: str, profile: Optional[str] = None):
        """
        Step 71: Preference Learning
        - Which browser does user prefer?
        - Which profile for which work?
        """
        self.profile.preferred_browser = browser
        if profile:
            self.profile.preferred_profile = profile
        
        self._save_profile()
        logger.info(f"📚 Learned browser preference: {browser} (profile: {profile})")
    
    def analyze_work_patterns(self) -> Dict:
        """
        Step 72: Work Pattern Analysis
        - When does user work? 9am-5pm?
        - Active on weekends?
        - When do they rest?
        """
        # Analyze from interaction history
        if not self.interaction_history:
            return {"status": "insufficient_data"}
        
        hours_active = defaultdict(int)
        days_active = defaultdict(int)
        
        for interaction in self.interaction_history:
            dt = datetime.fromisoformat(interaction.get("timestamp", datetime.now().isoformat()))
            hours_active[dt.hour] += 1
            days_active[dt.strftime("%A")] += 1
        
        # Find peak hours
        if hours_active:
            peak_hour = max(hours_active.items(), key=lambda x: x[1])[0]
            # Estimate work hours (simplified)
            active_hours = [h for h, count in hours_active.items() if count > len(self.interaction_history) * 0.1]
            if active_hours:
                self.profile.work_hours_start = time(min(active_hours), 0)
                self.profile.work_hours_end = time(max(active_hours), 0)
        
        # Check weekend activity
        weekend_activity = days_active.get("Saturday", 0) + days_active.get("Sunday", 0)
        total_activity = sum(days_active.values())
        self.profile.works_weekends = (weekend_activity / total_activity > 0.2) if total_activity > 0 else False
        
        # Update active days
        self.profile.active_days = [day for day, count in days_active.items() if count > 0]
        
        self._save_profile()
        
        return {
            "work_hours": f"{self.profile.work_hours_start}-{self.profile.work_hours_end}",
            "works_weekends": self.profile.works_weekends,
            "active_days": self.profile.active_days,
            "peak_hour": peak_hour if hours_active else None
        }
    
    def identify_app_sequences(self) -> List[List[str]]:
        """
        Step 73: Application Usage Patterns
        - Which apps used in what order?
        - Chrome → VSCode → CapCut?
        - Typical sequence?
        """
        if len(self.app_usage_log) < 3:
            return []
        
        sequences = []
        current_sequence = []
        
        for log_entry in self.app_usage_log:
            app = log_entry.get("app_name")
            if app:
                if not current_sequence or current_sequence[-1] != app:
                    current_sequence.append(app)
                    
                    if len(current_sequence) >= 3:
                        sequences.append(current_sequence[:])
                        current_sequence = current_sequence[-2:]  # Keep last 2 for overlap
        
        # Find most common sequence
        if sequences:
            sequence_counter = Counter(tuple(seq) for seq in sequences)
            most_common = sequence_counter.most_common(1)[0][0]
            self.profile.app_sequence = list(most_common)
            self._save_profile()
        
        return sequences
    
    def track_search_patterns(self, query: str, category: Optional[str] = None):
        """
        Step 74: Search Query Patterns
        - What types of searches usually done?
        - Programming? News? Shopping?
        - Favorite sites?
        """
        self.search_history.append({
            "query": query,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update categories
        if category:
            self.profile.search_categories[category] = self.profile.search_categories.get(category, 0) + 1
        
        # Extract websites from queries (simplified)
        if "http" in query or "www." in query:
            # Very basic URL extraction
            words = query.split()
            for word in words:
                if "." in word and not word.startswith("."):
                    if word not in self.profile.favorite_websites:
                        self.profile.favorite_websites.append(word)
        
        self._save_profile()
    
    def track_file_access(self, filepath: str):
        """
        Step 75: File Access Patterns
        - Which files/folders frequently used?
        - ~/Desktop, ~/Documents, ~/Projects?
        - Typical file extensions?
        """
        self.file_access_log.append({
            "filepath": filepath,
            "timestamp": datetime.now().isoformat()
        })
        
        path = Path(filepath)
        
        # Track directory
        directory = str(path.parent)
        if directory not in self.profile.common_directories:
            self.profile.common_directories.append(directory)
        
        # Track extension
        if path.suffix and path.suffix not in self.profile.common_file_extensions:
            self.profile.common_file_extensions.append(path.suffix)
        
        # Keep only top 10 most common
        if len(self.profile.common_directories) > 10:
            self.profile.common_directories = self.profile.common_directories[-10:]
        
        self._save_profile()
    
    def analyze_click_patterns(self, click_data: List[Dict]) -> Dict:
        """
        Step 76: UI Interaction Patterns
        - How does user usually click? Fast or slow?
        - Prefers buttons or keyboard?
        - Click patterns (corners, center)?
        """
        if not click_data:
            return {"status": "no_data"}
        
        # Analyze click speed
        click_intervals = []
        for i in range(1, len(click_data)):
            prev_time = datetime.fromisoformat(click_data[i-1].get("timestamp", datetime.now().isoformat()))
            curr_time = datetime.fromisoformat(click_data[i].get("timestamp", datetime.now().isoformat()))
            interval = (curr_time - prev_time).total_seconds()
            if interval < 10:  # Only consider clicks within 10 seconds
                click_intervals.append(interval)
        
        if click_intervals:
            avg_interval = sum(click_intervals) / len(click_intervals)
            if avg_interval < 1.0:
                self.profile.click_speed = "fast"
            elif avg_interval > 3.0:
                self.profile.click_speed = "slow"
            else:
                self.profile.click_speed = "normal"
        
        # Analyze keyboard vs mouse preference
        keyboard_actions = sum(1 for c in click_data if c.get("type") == "keyboard")
        mouse_actions = sum(1 for c in click_data if c.get("type") == "mouse")
        self.profile.prefers_keyboard = keyboard_actions > mouse_actions
        
        # Analyze click positions (simplified)
        positions = [c.get("position", "center") for c in click_data if "position" in c]
        if positions:
            position_counter = Counter(positions)
            most_common_position = position_counter.most_common(1)[0][0]
            self.profile.click_pattern = most_common_position
        
        self._save_profile()
        
        return {
            "click_speed": self.profile.click_speed,
            "prefers_keyboard": self.profile.prefers_keyboard,
            "click_pattern": self.profile.click_pattern
        }
    
    def learn_error_recovery_preference(self, method: str):
        """
        Step 77: Error Recovery Preferences
        - How to rollback from errors?
        - Ctrl+Z? Undo menu? Reload?
        - Aggressive or conservative?
        """
        self.profile.preferred_undo_method = method
        
        # Infer recovery style from method
        aggressive_methods = ["reload", "restart", "force_quit"]
        if method in aggressive_methods:
            self.profile.error_recovery_style = "aggressive"
        else:
            self.profile.error_recovery_style = "conservative"
        
        self._save_profile()
    
    def learn_decision_preference(self, risk_level: str, decision_speed: str):
        """
        Step 78: Decision-Making Preferences
        - Prefer fast but risky?
        - Or slow but reliable?
        - Risk tolerance level?
        """
        self.profile.risk_tolerance = risk_level
        self.profile.decision_speed = decision_speed
        
        self._save_profile()
        logger.info(f"📚 Learned decision preference: risk={risk_level}, speed={decision_speed}")
    
    def learn_time_preference(self, deadline: int, patience: str):
        """
        Step 79: Time Preference
        - What deadline is usually acceptable?
        - Need fast (1-2 sec) or can wait (10+ sec)?
        - Patient user?
        """
        self.profile.acceptable_deadline = deadline
        self.profile.patience_level = patience
        
        self._save_profile()
    
    def calibrate_confidence(self, actual_outcomes: List[Dict]) -> Dict:
        """
        Step 80: Confidence Calibration
        - How confident should recommendations be?
        - If low confidence - ask for confirmation?
        - If high confidence - act autonomously?
        """
        if not actual_outcomes:
            return {"status": "no_data"}
        
        # Analyze success rate by confidence level
        confidence_buckets = {
            "low": [],
            "medium": [],
            "high": []
        }
        
        for outcome in actual_outcomes:
            confidence = outcome.get("confidence", 0.5)
            success = outcome.get("success", False)
            
            if confidence < 0.6:
                confidence_buckets["low"].append(success)
            elif confidence < 0.8:
                confidence_buckets["medium"].append(success)
            else:
                confidence_buckets["high"].append(success)
        
        # Calculate success rates
        calibration = {}
        for bucket, outcomes in confidence_buckets.items():
            if outcomes:
                success_rate = sum(outcomes) / len(outcomes)
                calibration[f"{bucket}_success_rate"] = success_rate
        
        # Adjust thresholds based on calibration
        high_success_rate = calibration.get("high_success_rate", 0.9)
        if high_success_rate > 0.95:
            self.profile.auto_execute_threshold = 0.85  # Lower threshold
        elif high_success_rate < 0.85:
            self.profile.auto_execute_threshold = 0.95  # Raise threshold
        
        self._save_profile()
        
        return calibration
    
    # ═══════════════════════════════════════════════════════════════
    # Additional Steps (81-90)
    # ═══════════════════════════════════════════════════════════════
    
    def record_interaction(self, interaction: Dict):
        """Record user interaction for pattern analysis"""
        interaction["timestamp"] = datetime.now().isoformat()
        self.interaction_history.append(interaction)
        self.profile.total_interactions += 1
        
        # Keep last 1000 interactions
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
    
    def record_app_usage(self, app_name: str, action: str):
        """Record application usage"""
        self.app_usage_log.append({
            "app_name": app_name,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update frequently used apps
        self.profile.frequently_used_apps[app_name] = self.profile.frequently_used_apps.get(app_name, 0) + 1
        self._save_profile()
    
    def get_recommendation(self, context: Dict) -> Dict:
        """
        Step 87: Pattern-Based Recommendations
        - Based on current context + patterns
        - Suggest most probable action
        - Probability > 80%?
        """
        recommendations = []
        
        # Recommend based on app sequence
        if context.get("last_apps"):
            last_apps = context["last_apps"]
            if self.profile.app_sequence and len(last_apps) >= 2:
                # Check if last apps match beginning of sequence
                if last_apps[-2:] == self.profile.app_sequence[:2]:
                    next_app = self.profile.app_sequence[2] if len(self.profile.app_sequence) > 2 else None
                    if next_app:
                        recommendations.append({
                            "type": "app",
                            "action": f"open_{next_app}",
                            "confidence": 0.85,
                            "reason": "follows typical app sequence"
                        })
        
        # Recommend based on time of day
        current_hour = datetime.now().hour
        if self.profile.work_hours_start.hour <= current_hour <= self.profile.work_hours_end.hour:
            recommendations.append({
                "type": "context",
                "suggestion": "work_mode",
                "confidence": 0.75,
                "reason": "within work hours"
            })
        
        return {
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    def detect_anomaly(self, current_behavior: Dict) -> Optional[Dict]:
        """
        Step 86: Anomaly Detection in Patterns
        - If behavior deviates from usual - notice
        - Maybe need help or something broken?
        """
        anomalies = []
        
        # Check if active during unusual hours
        current_hour = datetime.now().hour
        work_start = self.profile.work_hours_start.hour
        work_end = self.profile.work_hours_end.hour
        
        if current_hour < work_start - 2 or current_hour > work_end + 2:
            anomalies.append({
                "type": "time_anomaly",
                "description": "Active during unusual hours",
                "severity": "low"
            })
        
        # Check if using unusual app
        current_app = current_behavior.get("app")
        if current_app and current_app not in self.profile.frequently_used_apps:
            anomalies.append({
                "type": "app_anomaly",
                "description": f"Using unusual application: {current_app}",
                "severity": "medium"
            })
        
        return {"anomalies": anomalies} if anomalies else None
    
    def export_profile(self) -> Dict:
        """Export complete user profile"""
        return self.profile.to_dict()
    
    def import_profile(self, profile_data: Dict):
        """Import user profile"""
        self.profile = UserProfile.from_dict(profile_data)
        self._save_profile()
        logger.info(f"📥 Profile imported for {self.user_id}")
