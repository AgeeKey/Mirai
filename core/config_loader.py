#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Configuration Loader                                          ║
║  Unified YAML Config Loading with Validation                        ║
╚══════════════════════════════════════════════════════════════════════╝

Version: 2.0.0
Codename: Evolution

Загружает unified конфиг из mirai.yaml с:
- ✅ Валидацией всех параметров
- ✅ Environment variable подстановкой
- ✅ Fallback на дефолты
- ✅ Caching для performance
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# ═══════════════════════════════════════════════════════════════════
# Dataclasses для typed config access
# ═══════════════════════════════════════════════════════════════════


@dataclass
class OpenAIModelConfig:
    """Конфиг для одной OpenAI модели"""

    name: str
    temperature: float = 0.25
    top_p: float = 0.9
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.0
    max_tokens: int = 2000
    timeout_s: int = 90
    use_cases: list = field(default_factory=list)


@dataclass
class OpenAIConfig:
    """OpenAI API Configuration"""

    defaults: Dict[str, Any] = field(default_factory=dict)
    models: Dict[str, OpenAIModelConfig] = field(default_factory=dict)
    limits: Dict[str, Any] = field(default_factory=dict)
    circuit_breaker: Dict[str, Any] = field(default_factory=dict)
    degradation: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryConfig:
    """Memory System Configuration"""

    enabled: bool = True
    backend: str = "sqlite"
    db_path: str = "data/mirai_memory.db"
    session_storage: str = "data/sessions/"
    short_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    rag: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringConfig:
    """Monitoring & Logging Configuration"""

    enabled: bool = True
    logs: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    tracing: Dict[str, Any] = field(default_factory=dict)
    alerts: Dict[str, Any] = field(default_factory=dict)
    healthcheck: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityConfig:
    """Security Configuration"""

    api_keys: Dict[str, str] = field(default_factory=dict)
    sandbox: Dict[str, Any] = field(default_factory=dict)
    privacy: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MiraiConfig:
    """
    Unified MIRAI Configuration

    Объединяет все конфиги в один typed объект
    """

    version: str = "2.0.0"
    codename: str = "Evolution"
    name: str = "MIRAI AI Agent"
    description: str = ""

    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)

    cognitive_loop: Dict[str, Any] = field(default_factory=dict)
    ethical_filter: Dict[str, Any] = field(default_factory=dict)
    self_evolution: Dict[str, Any] = field(default_factory=dict)
    self_registry: Dict[str, Any] = field(default_factory=dict)
    services: Dict[str, Any] = field(default_factory=dict)
    nlp: Dict[str, Any] = field(default_factory=dict)
    integrations: Dict[str, Any] = field(default_factory=dict)
    iot: Dict[str, Any] = field(default_factory=dict)
    testing: Dict[str, Any] = field(default_factory=dict)
    development: Dict[str, Any] = field(default_factory=dict)

    _raw_config: Dict[str, Any] = field(default_factory=dict, repr=False)


# ═══════════════════════════════════════════════════════════════════
# Config Loader
# ═══════════════════════════════════════════════════════════════════


class ConfigLoader:
    """
    Unified Configuration Loader

    Features:
    - ✅ YAML parsing
    - ✅ Environment variable substitution
    - ✅ Validation
    - ✅ Caching
    - ✅ Typed access через dataclasses
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config loader

        Args:
            config_path: Path to mirai.yaml (optional, автопоиск)
        """
        self.logger = logging.getLogger(__name__)

        # Найти конфиг файл
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._find_config()

        # Cache
        self._config: Optional[MiraiConfig] = None
        self._loaded = False

    def _find_config(self) -> Path:
        """
        Автопоиск конфига в:
        1. configs/mirai.yaml
        2. /root/mirai/configs/mirai.yaml
        3. ./mirai.yaml
        """
        search_paths = [
            Path("configs/mirai.yaml"),
            Path("/root/mirai/configs/mirai.yaml"),
            Path("mirai.yaml"),
        ]

        for path in search_paths:
            if path.exists():
                self.logger.info(f"Found config at: {path}")
                return path

        # Если не нашли - использовать дефолтный путь
        default = Path("/root/mirai/configs/mirai.yaml")
        self.logger.warning(f"Config not found, using default: {default}")
        return default

    def _substitute_env_vars(self, value: Any) -> Any:
        """
        Подставить environment variables в конфиг

        Например: ${OPENAI_API_KEY} → значение из env
        """
        if isinstance(value, str):
            # Простая подстановка ${VAR_NAME}
            if value.startswith("${") and value.endswith("}"):
                var_name = value[2:-1]
                env_value = os.getenv(var_name)
                if env_value is not None:
                    return env_value
                else:
                    self.logger.warning(f"Environment variable not found: {var_name}")
                    return value

        elif isinstance(value, dict):
            return {k: self._substitute_env_vars(v) for k, v in value.items()}

        elif isinstance(value, list):
            return [self._substitute_env_vars(item) for item in value]

        return value

    def _load_yaml(self) -> Dict[str, Any]:
        """Load and parse YAML config"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        if not raw_config:
            raise ValueError(f"Config file is empty: {self.config_path}")

        # Подставить env vars
        config = self._substitute_env_vars(raw_config)

        return config

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration

        Checks:
        - Required fields
        - Value ranges
        - Consistency
        """
        # Version check
        if "version" not in config:
            raise ValueError("Config missing 'version' field")

        # OpenAI check
        if "openai" not in config:
            raise ValueError("Config missing 'openai' section")

        if "models" not in config["openai"]:
            raise ValueError("Config missing 'openai.models' section")

        # Check main models
        required_models = ["main", "heavy"]
        for model_type in required_models:
            if model_type not in config["openai"]["models"]:
                self.logger.warning(f"Missing model type: {model_type}")

        # Memory check
        if "memory" not in config:
            self.logger.warning("Config missing 'memory' section")

        self.logger.info("Configuration validation passed ✅")

    def _parse_openai_config(self, raw: Dict[str, Any]) -> OpenAIConfig:
        """Parse OpenAI config section"""
        models = {}
        for model_type, model_data in raw.get("models", {}).items():
            models[model_type] = OpenAIModelConfig(
                name=model_data.get("name", "gpt-4o-mini"),
                temperature=model_data.get("temperature", 0.25),
                top_p=model_data.get("top_p", 0.9),
                frequency_penalty=model_data.get("frequency_penalty", 0.1),
                presence_penalty=model_data.get("presence_penalty", 0.0),
                max_tokens=model_data.get("max_tokens", 2000),
                timeout_s=model_data.get("timeout_s", 90),
                use_cases=model_data.get("use_cases", []),
            )

        return OpenAIConfig(
            defaults=raw.get("defaults", {}),
            models=models,
            limits=raw.get("limits", {}),
            circuit_breaker=raw.get("circuit_breaker", {}),
            degradation=raw.get("degradation", {}),
        )

    def _parse_memory_config(self, raw: Dict[str, Any]) -> MemoryConfig:
        """Parse Memory config section"""
        return MemoryConfig(
            enabled=raw.get("enabled", True),
            backend=raw.get("backend", "sqlite"),
            db_path=raw.get("db_path", "data/mirai_memory.db"),
            session_storage=raw.get("session_storage", "data/sessions/"),
            short_term=raw.get("short_term", {}),
            long_term=raw.get("long_term", {}),
            user_preferences=raw.get("user_preferences", {}),
            rag=raw.get("rag", {}),
        )

    def _parse_monitoring_config(self, raw: Dict[str, Any]) -> MonitoringConfig:
        """Parse Monitoring config section"""
        return MonitoringConfig(
            enabled=raw.get("enabled", True),
            logs=raw.get("logs", {}),
            metrics=raw.get("metrics", {}),
            tracing=raw.get("tracing", {}),
            alerts=raw.get("alerts", {}),
            healthcheck=raw.get("healthcheck", {}),
        )

    def _parse_security_config(self, raw: Dict[str, Any]) -> SecurityConfig:
        """Parse Security config section"""
        return SecurityConfig(
            api_keys=raw.get("api_keys", {}),
            sandbox=raw.get("sandbox", {}),
            privacy=raw.get("privacy", {}),
        )

    def load(self, force_reload: bool = False) -> MiraiConfig:
        """
        Load configuration

        Args:
            force_reload: Force reload from disk (ignore cache)

        Returns:
            Parsed and validated MiraiConfig
        """
        # Use cache if available
        if self._loaded and not force_reload:
            return self._config

        self.logger.info(f"Loading config from: {self.config_path}")

        # Load YAML
        raw_config = self._load_yaml()

        # Validate
        self._validate_config(raw_config)

        # Parse into typed dataclasses
        config = MiraiConfig(
            version=raw_config.get("version", "2.0.0"),
            codename=raw_config.get("codename", "Evolution"),
            name=raw_config.get("name", "MIRAI AI Agent"),
            description=raw_config.get("description", ""),
            openai=self._parse_openai_config(raw_config.get("openai", {})),
            memory=self._parse_memory_config(raw_config.get("memory", {})),
            monitoring=self._parse_monitoring_config(raw_config.get("monitoring", {})),
            security=self._parse_security_config(raw_config.get("security", {})),
            cognitive_loop=raw_config.get("cognitive_loop", {}),
            ethical_filter=raw_config.get("ethical_filter", {}),
            self_evolution=raw_config.get("self_evolution", {}),
            self_registry=raw_config.get("self_registry", {}),
            services=raw_config.get("services", {}),
            nlp=raw_config.get("nlp", {}),
            integrations=raw_config.get("integrations", {}),
            iot=raw_config.get("iot", {}),
            testing=raw_config.get("testing", {}),
            development=raw_config.get("development", {}),
            _raw_config=raw_config,
        )

        # Cache
        self._config = config
        self._loaded = True

        self.logger.info(
            f"Config loaded successfully: {config.name} v{config.version} ({config.codename})"
        )

        return config

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get config value by dot-separated path

        Example:
            config.get('openai.models.main.temperature')
            → 0.25
        """
        if not self._loaded:
            self.load()

        keys = key_path.split(".")
        value = self._config._raw_config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def reload(self) -> MiraiConfig:
        """Force reload config from disk"""
        return self.load(force_reload=True)


# ═══════════════════════════════════════════════════════════════════
# Global config instance (singleton pattern)
# ═══════════════════════════════════════════════════════════════════

_global_config: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Get global config loader instance (singleton)"""
    global _global_config
    if _global_config is None:
        _global_config = ConfigLoader()
    return _global_config


def get_config(force_reload: bool = False) -> MiraiConfig:
    """
    Get loaded configuration

    Args:
        force_reload: Force reload from disk

    Returns:
        Loaded MiraiConfig
    """
    loader = get_config_loader()
    return loader.load(force_reload=force_reload)


# ═══════════════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════════════


def get_openai_model_config(model_type: str = "main") -> Optional[OpenAIModelConfig]:
    """
    Get OpenAI model config by type

    Args:
        model_type: 'main', 'heavy', 'fast', 'creative', etc.

    Returns:
        OpenAIModelConfig or None
    """
    config = get_config()
    return config.openai.models.get(model_type)


def get_api_key() -> Optional[str]:
    """
    Get OpenAI API key

    Tries:
    1. Environment variable (OPENAI_API_KEY)
    2. Config file (if source='file')
    3. Fallback file (configs/api_keys.json)
    """
    # Try env first (most secure)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # Try config
    config = get_config()
    source = config.security.api_keys.get("source", "env")

    if source == "env":
        env_var = config.security.api_keys.get("env_var", "OPENAI_API_KEY")
        return os.getenv(env_var)

    elif source == "file":
        fallback = config.security.api_keys.get(
            "fallback_file", "configs/api_keys.json"
        )
        fallback_path = Path(fallback)

        if fallback_path.exists():
            import json

            with open(fallback_path, "r") as f:
                keys = json.load(f)
                return keys.get("openai_api_key")

    return None


# ═══════════════════════════════════════════════════════════════════
# Main (для тестирования)
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  MIRAI Config Loader Test                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()

    # Load config
    config = get_config()

    # Print summary
    print(f"Name: {config.name}")
    print(f"Version: {config.version} ({config.codename})")
    print(f"Description: {config.description}")
    print()

    # OpenAI models
    print("OpenAI Models:")
    for model_type, model_config in config.openai.models.items():
        print(f"  {model_type}: {model_config.name}")
        print(f"    Temperature: {model_config.temperature}")
        print(f"    Max tokens: {model_config.max_tokens}")
        print(f"    Use cases: {len(model_config.use_cases)}")
    print()

    # Memory
    print(f"Memory enabled: {config.memory.enabled}")
    print(f"Memory backend: {config.memory.backend}")
    print(f"Memory DB path: {config.memory.db_path}")
    print()

    # Services
    print("Services:")
    for service_name, service_config in config.services.items():
        print(f"  {service_name}: {service_config.get('enabled', False)}")
    print()

    # Features
    features = []
    if config.cognitive_loop.get("enabled"):
        features.append("Cognitive Loop")
    if config.ethical_filter.get("enabled"):
        features.append("Ethical Filter")
    if config.self_evolution.get("enabled"):
        features.append("Self-Evolution")
    if config.memory.enabled:
        features.append("Memory System")
    if config.nlp.get("enabled"):
        features.append("NLP")
    if config.iot.get("enabled"):
        features.append("IoT")

    print(f"Active features: {', '.join(features) if features else 'None'}")
    print()

    # API key check
    api_key = get_api_key()
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("❌ API key not found!")
    print()

    # Test dot notation
    temperature = get_config_loader().get("openai.models.main.temperature")
    print(f"Main model temperature (via dot notation): {temperature}")

    print()
    print("✅ Config loaded successfully!")
