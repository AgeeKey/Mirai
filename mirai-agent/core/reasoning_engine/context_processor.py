#!/usr/bin/env python3
"""
🧠 Context Processor - Steps 56-70
Подраздел 2.2: Application State Tracking

Features:
- Application Registry (Step 56)
- Application State Machine (Step 57)
- Chrome Profile Tracking (Step 58)
- Window Hierarchy Tracking (Step 59)
- UI Element State (Step 60)
- Dialog & Popup Tracking (Step 61)
- File System Monitoring (Step 62)
- Network State Monitoring (Step 63)
- System Resource Monitoring (Step 64)
- Performance Metrics (Step 65)
"""

import logging
import psutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from enum import Enum
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


class ApplicationStatus(Enum):
    """Step 57: Application State Machine states"""
    NOT_RUNNING = "not_running"
    STARTING = "starting"
    READY = "ready"
    LOADING = "loading"
    ERROR = "error"
    CRASHED = "crashed"


@dataclass
class AppRegistry:
    """
    Step 56: Application Registry
    - List of all known applications
    - Characteristics for each
    """
    name: str
    executable: str
    typical_startup_time: float = 5.0  # seconds
    typical_memory_mb: int = 200
    typical_cpu_percent: float = 10.0
    known_states: List[str] = field(default_factory=list)
    file_extensions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "executable": self.executable,
            "typical_startup_time": self.typical_startup_time,
            "typical_memory_mb": self.typical_memory_mb,
            "typical_cpu_percent": self.typical_cpu_percent,
            "known_states": self.known_states,
            "file_extensions": self.file_extensions
        }


@dataclass
class UIElementState:
    """
    Step 60: UI Element State
    - For each UI element know its state
    """
    element_id: str
    element_type: str  # button, input, select, etc.
    enabled: bool = True
    visible: bool = True
    focused: bool = False
    coordinates: tuple = field(default_factory=lambda: (0, 0))
    size: tuple = field(default_factory=lambda: (0, 0))
    label: str = ""
    value: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        d = {
            "id": self.element_id,
            "type": self.element_type,
            "enabled": self.enabled,
            "visible": self.visible,
            "focused": self.focused,
            "coordinates": self.coordinates,
            "size": self.size,
            "label": self.label,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }
        return d


@dataclass
class ApplicationState:
    """Application state tracking"""
    app_name: str
    status: ApplicationStatus = ApplicationStatus.NOT_RUNNING
    pid: Optional[int] = None
    window_title: str = ""
    memory_mb: float = 0.0
    cpu_percent: float = 0.0
    startup_time: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    ui_elements: List[UIElementState] = field(default_factory=list)
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "app_name": self.app_name,
            "status": self.status.value,
            "pid": self.pid,
            "window_title": self.window_title,
            "memory_mb": self.memory_mb,
            "cpu_percent": self.cpu_percent,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
            "ui_elements_count": len(self.ui_elements),
            "error_message": self.error_message
        }


@dataclass
class DialogInfo:
    """Step 61: Dialog & Popup information"""
    dialog_type: str  # alert, confirm, prompt, custom
    title: str
    message: str
    buttons: List[str] = field(default_factory=list)
    default_button: Optional[str] = None
    can_dismiss: bool = True
    timestamp: datetime = field(default_factory=datetime.now)


class ContextProcessor:
    """
    🧠 Context Processing System
    
    Implements Steps 56-70: Application State Tracking
    """
    
    def __init__(self):
        # Step 56: Application Registry
        self.app_registry: Dict[str, AppRegistry] = self._init_app_registry()
        
        # Step 57: Application states
        self.app_states: Dict[str, ApplicationState] = {}
        
        # Step 58: Chrome profiles
        self.chrome_profiles: Dict[str, Dict] = {}
        self.current_chrome_profile: Optional[str] = None
        
        # Step 59: Window hierarchy
        self.window_hierarchy: Dict[int, List[int]] = {}  # parent_id: [child_ids]
        self.focused_window: Optional[int] = None
        
        # Step 61: Dialogs and popups
        self.active_dialogs: List[DialogInfo] = []
        
        # Step 62: File system monitoring
        self.recent_files: List[Dict] = []
        self.current_directory: str = "~"
        
        # Step 63: Network state
        self.network_state: Dict[str, Any] = {"connected": False}
        
        # Step 64: System resources
        self.resource_state: Dict[str, float] = {}
        
        # Step 65: Performance metrics
        self.performance_metrics: Dict[str, Dict] = defaultdict(dict)
        
        # Step 67: Error logs
        self.error_logs: List[Dict] = []
        
        logger.info("✅ Context Processor initialized")
    
    def _init_app_registry(self) -> Dict[str, AppRegistry]:
        """Initialize known applications registry"""
        apps = {
            "chrome": AppRegistry(
                name="Chrome",
                executable="chrome.exe",
                typical_startup_time=3.0,
                typical_memory_mb=300,
                typical_cpu_percent=15.0,
                known_states=["not_running", "starting", "ready", "loading"],
                file_extensions=[".html", ".htm"]
            ),
            "firefox": AppRegistry(
                name="Firefox",
                executable="firefox.exe",
                typical_startup_time=4.0,
                typical_memory_mb=350,
                typical_cpu_percent=12.0,
                known_states=["not_running", "starting", "ready"],
                file_extensions=[".html", ".htm"]
            ),
            "vscode": AppRegistry(
                name="VSCode",
                executable="code.exe",
                typical_startup_time=5.0,
                typical_memory_mb=400,
                typical_cpu_percent=8.0,
                known_states=["not_running", "ready"],
                file_extensions=[".py", ".js", ".ts", ".json"]
            ),
            "notepad": AppRegistry(
                name="Notepad",
                executable="notepad.exe",
                typical_startup_time=1.0,
                typical_memory_mb=50,
                typical_cpu_percent=2.0,
                known_states=["ready"],
                file_extensions=[".txt"]
            )
        }
        
        return apps
    
    # ═══════════════════════════════════════════════════════════════
    # Application State Management (Steps 56-60)
    # ═══════════════════════════════════════════════════════════════
    
    def get_application_state(self, app_name: str) -> Optional[ApplicationState]:
        """Get current state of application"""
        return self.app_states.get(app_name)
    
    def update_application_state(self, app_name: str, **kwargs) -> ApplicationState:
        """
        Step 57: Update application state
        - Track state transitions
        """
        if app_name not in self.app_states:
            self.app_states[app_name] = ApplicationState(app_name=app_name)
        
        state = self.app_states[app_name]
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        
        logger.debug(f"Updated {app_name} state: {state.status.value}")
        return state
    
    def transition_app_state(self, app_name: str, new_status: ApplicationStatus):
        """
        Step 57: Application State Machine
        - Manage state transitions
        """
        state = self.app_states.get(app_name)
        if not state:
            state = ApplicationState(app_name=app_name)
            self.app_states[app_name] = state
        
        old_status = state.status
        state.status = new_status
        
        # Special handling for state transitions
        if new_status == ApplicationStatus.STARTING:
            state.startup_time = datetime.now()
        
        logger.info(f"🔄 {app_name}: {old_status.value} → {new_status.value}")
    
    def detect_running_applications(self) -> List[str]:
        """Detect currently running applications"""
        running_apps = []
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                proc_name = proc.info['name'].lower()
                
                # Check against registry
                for app_id, app_info in self.app_registry.items():
                    if app_info.executable.lower() in proc_name:
                        running_apps.append(app_id)
                        
                        # Update state
                        if app_id not in self.app_states or self.app_states[app_id].status == ApplicationStatus.NOT_RUNNING:
                            self.update_application_state(
                                app_id,
                                status=ApplicationStatus.READY,
                                pid=proc.info['pid']
                            )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return list(set(running_apps))
    
    # ═══════════════════════════════════════════════════════════════
    # Chrome Profile Tracking (Step 58)
    # ═══════════════════════════════════════════════════════════════
    
    def track_chrome_profile(self, profile_name: str, preferences: Optional[Dict] = None):
        """
        Step 58: Chrome Profile Tracking
        - Which Chrome profile is active?
        - History of selected profiles
        - Preferences for each profile
        """
        if profile_name not in self.chrome_profiles:
            self.chrome_profiles[profile_name] = {
                "name": profile_name,
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None,
                "preferences": preferences or {}
            }
        
        profile = self.chrome_profiles[profile_name]
        profile["usage_count"] += 1
        profile["last_used"] = datetime.now().isoformat()
        
        self.current_chrome_profile = profile_name
        logger.info(f"📊 Chrome profile tracked: {profile_name}")
    
    def get_preferred_chrome_profile(self, context: Optional[str] = None) -> Optional[str]:
        """Get most suitable Chrome profile for context"""
        if not self.chrome_profiles:
            return None
        
        # Return most frequently used profile
        profiles = sorted(
            self.chrome_profiles.items(),
            key=lambda x: x[1]["usage_count"],
            reverse=True
        )
        
        return profiles[0][0] if profiles else None
    
    # ═══════════════════════════════════════════════════════════════
    # Window & UI Management (Steps 59-61)
    # ═══════════════════════════════════════════════════════════════
    
    def track_window_hierarchy(self, window_id: int, parent_id: Optional[int] = None):
        """
        Step 59: Window Hierarchy Tracking
        - Which windows are open?
        - Which window is focused?
        - Parent-child hierarchy
        """
        if parent_id is not None:
            if parent_id not in self.window_hierarchy:
                self.window_hierarchy[parent_id] = []
            if window_id not in self.window_hierarchy[parent_id]:
                self.window_hierarchy[parent_id].append(window_id)
    
    def set_focused_window(self, window_id: int):
        """Track which window is focused"""
        self.focused_window = window_id
        logger.debug(f"Focus changed to window: {window_id}")
    
    def update_ui_element_state(self, app_name: str, element: UIElementState):
        """
        Step 60: UI Element State
        - Track state of UI elements
        """
        state = self.app_states.get(app_name)
        if not state:
            state = ApplicationState(app_name=app_name)
            self.app_states[app_name] = state
        
        # Update or add element
        existing = next((e for e in state.ui_elements if e.element_id == element.element_id), None)
        if existing:
            state.ui_elements.remove(existing)
        state.ui_elements.append(element)
    
    def track_dialog(self, dialog: DialogInfo):
        """
        Step 61: Dialog & Popup Tracking
        - What dialogs/popups are open?
        - Type, content, buttons
        - How to close them?
        """
        self.active_dialogs.append(dialog)
        logger.info(f"📋 Dialog tracked: {dialog.dialog_type} - {dialog.title}")
    
    def dismiss_dialog(self, dialog_title: str) -> bool:
        """Dismiss a dialog"""
        for dialog in self.active_dialogs:
            if dialog.title == dialog_title:
                if dialog.can_dismiss:
                    self.active_dialogs.remove(dialog)
                    logger.info(f"✅ Dialog dismissed: {dialog_title}")
                    return True
        return False
    
    # ═══════════════════════════════════════════════════════════════
    # System Monitoring (Steps 62-65)
    # ═══════════════════════════════════════════════════════════════
    
    def monitor_file_system(self, filepath: str, action: str):
        """
        Step 62: File System Monitoring
        - Recently opened files
        - Current directory in file explorer
        - Paths to project files
        """
        self.recent_files.append({
            "filepath": filepath,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 100 files
        if len(self.recent_files) > 100:
            self.recent_files = self.recent_files[-100:]
        
        # Update current directory if opening file
        if action == "open":
            import os
            self.current_directory = os.path.dirname(filepath)
    
    def check_network_state(self) -> Dict:
        """
        Step 63: Network State Monitoring
        - Internet connection available?
        - What's the speed?
        - Which sites are accessible?
        """
        try:
            import socket
            
            # Try to connect to common DNS
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            connected = True
        except OSError:
            connected = False
        
        self.network_state = {
            "connected": connected,
            "checked_at": datetime.now().isoformat()
        }
        
        return self.network_state
    
    def monitor_system_resources(self) -> Dict:
        """
        Step 64: System Resource Monitoring
        - CPU usage, Memory, Disk, GPU
        - Per application breakdown
        """
        self.resource_state = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
            "disk_percent": psutil.disk_usage('/').percent,
            "timestamp": datetime.now().isoformat()
        }
        
        # Per-application resources
        for app_name, state in self.app_states.items():
            if state.pid:
                try:
                    proc = psutil.Process(state.pid)
                    state.memory_mb = proc.memory_info().rss / 1024 / 1024
                    state.cpu_percent = proc.cpu_percent(interval=0.1)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        return self.resource_state
    
    def track_performance_metrics(self, app_name: str, metric_name: str, value: float):
        """
        Step 65: Performance Metrics
        - For each application:
        - Startup time, response time, crash frequency
        """
        if app_name not in self.performance_metrics:
            self.performance_metrics[app_name] = {}
        
        if metric_name not in self.performance_metrics[app_name]:
            self.performance_metrics[app_name][metric_name] = []
        
        self.performance_metrics[app_name][metric_name].append({
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 100 measurements
        if len(self.performance_metrics[app_name][metric_name]) > 100:
            self.performance_metrics[app_name][metric_name] = self.performance_metrics[app_name][metric_name][-100:]
    
    def get_app_performance(self, app_name: str) -> Dict:
        """Get performance summary for application"""
        metrics = self.performance_metrics.get(app_name, {})
        
        summary = {}
        for metric_name, measurements in metrics.items():
            if measurements:
                values = [m["value"] for m in measurements]
                summary[metric_name] = {
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values)
                }
        
        return summary
    
    # ═══════════════════════════════════════════════════════════════
    # Error & State Management (Steps 66-70)
    # ═══════════════════════════════════════════════════════════════
    
    def log_error(self, app_name: str, error_message: str, screenshot_path: Optional[str] = None):
        """
        Step 67: Error Log Aggregation
        - All errors that occurred
        - Error message, timestamp, app, screenshot
        """
        error = {
            "app_name": app_name,
            "error_message": error_message,
            "screenshot_path": screenshot_path,
            "timestamp": datetime.now().isoformat()
        }
        
        self.error_logs.append(error)
        
        # Update app state
        if app_name in self.app_states:
            self.app_states[app_name].status = ApplicationStatus.ERROR
            self.app_states[app_name].error_message = error_message
        
        logger.error(f"❌ Error logged for {app_name}: {error_message}")
    
    def check_state_consistency(self) -> Dict:
        """
        Step 68: State Consistency Checking
        - Verify all states are consistent
        - If app crashed but status says READY - fix
        - Synchronize with reality
        """
        inconsistencies = []
        
        # Check each application state
        for app_name, state in self.app_states.items():
            if state.pid:
                try:
                    # Check if process exists
                    proc = psutil.Process(state.pid)
                    if not proc.is_running():
                        # Inconsistency: state says running but process doesn't exist
                        inconsistencies.append({
                            "app": app_name,
                            "issue": "Process not running but state says it is",
                            "action": "Update status to NOT_RUNNING"
                        })
                        state.status = ApplicationStatus.NOT_RUNNING
                        state.pid = None
                except psutil.NoSuchProcess:
                    inconsistencies.append({
                        "app": app_name,
                        "issue": "Process doesn't exist",
                        "action": "Update status to CRASHED"
                    })
                    state.status = ApplicationStatus.CRASHED
                    state.pid = None
        
        if inconsistencies:
            logger.warning(f"⚠️ Found {len(inconsistencies)} state inconsistencies")
        
        return {
            "consistent": len(inconsistencies) == 0,
            "inconsistencies": inconsistencies,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_state_diff(self, old_state: Dict, new_state: Dict) -> Dict:
        """
        Step 69: State Diff Calculation
        - What changed since last check?
        - Diff between old state and new state
        """
        diff = {
            "added": [],
            "removed": [],
            "modified": []
        }
        
        old_apps = set(old_state.get("applications", {}).keys())
        new_apps = set(new_state.get("applications", {}).keys())
        
        diff["added"] = list(new_apps - old_apps)
        diff["removed"] = list(old_apps - new_apps)
        
        # Check modified
        for app in old_apps & new_apps:
            old_app_state = old_state["applications"][app]
            new_app_state = new_state["applications"][app]
            
            if old_app_state != new_app_state:
                diff["modified"].append({
                    "app": app,
                    "old": old_app_state,
                    "new": new_app_state
                })
        
        return diff
    
    def create_state_snapshot(self) -> Dict:
        """
        Step 70: State Snapshot
        - Save current state snapshot
        - For rollback capability
        """
        snapshot = {
            "applications": {
                app_name: state.to_dict()
                for app_name, state in self.app_states.items()
            },
            "chrome_profiles": self.chrome_profiles,
            "current_chrome_profile": self.current_chrome_profile,
            "active_dialogs": len(self.active_dialogs),
            "resource_state": self.resource_state,
            "network_state": self.network_state,
            "timestamp": datetime.now().isoformat()
        }
        
        return snapshot
    
    def restore_snapshot(self, snapshot: Dict):
        """
        Step 70: Restore from Snapshot
        - Restore previous state
        """
        # Restore application states
        for app_name, state_dict in snapshot.get("applications", {}).items():
            state = ApplicationState(app_name=app_name)
            for key, value in state_dict.items():
                if hasattr(state, key) and key != "ui_elements":
                    setattr(state, key, value)
            self.app_states[app_name] = state
        
        # Restore chrome profiles
        self.chrome_profiles = snapshot.get("chrome_profiles", {})
        self.current_chrome_profile = snapshot.get("current_chrome_profile")
        
        logger.info(f"♻️ State restored from snapshot: {snapshot.get('timestamp')}")
    
    def get_full_context(self) -> Dict:
        """Get complete context for decision making"""
        self.check_state_consistency()
        self.monitor_system_resources()
        
        context = {
            "applications": {
                app_name: state.to_dict()
                for app_name, state in self.app_states.items()
            },
            "running_apps": self.detect_running_applications(),
            "focused_window": self.focused_window,
            "active_dialogs": len(self.active_dialogs),
            "chrome_profile": self.current_chrome_profile,
            "current_directory": self.current_directory,
            "network_connected": self.network_state.get("connected", False),
            "resources": self.resource_state,
            "recent_errors": len(self.error_logs),
            "timestamp": datetime.now().isoformat()
        }
        
        return context
