"""
Integration test for config scenarios
Tests various configuration edge cases
"""
import sys
import os
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.config_manager import ConfigManager

def test_valid_config():
    """Test loading valid configuration"""
    config = ConfigManager()
    
    assert config.get("version") is not None
    assert config.get("database.path") is not None
    assert config.get("logging.level") is not None
    
    print("✅ Valid config loads correctly")

def test_missing_key_with_default():
    """Test accessing missing key with default value"""
    config = ConfigManager()
    
    value = config.get("nonexistent.key", default="default_value")
    assert value == "default_value"
    
    print("✅ Missing key returns default")

def test_custom_config_file():
    """Test loading from custom config file"""
    # Create temporary config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        custom_config = {
            "version": "test.1.0",
            "custom_key": "custom_value"
        }
        json.dump(custom_config, f)
        temp_path = f.name
    
    try:
        # Load custom config
        config = ConfigManager(config_path=temp_path)
        
        assert config.get("version") == "test.1.0"
        assert config.get("custom_key") == "custom_value"
        
        print("✅ Custom config file loads correctly")
    finally:
        os.unlink(temp_path)

def test_config_update():
    """Test updating configuration"""
    config = ConfigManager()
    
    # Set a value
    config.set("test.key", "test_value")
    
    # Retrieve it
    value = config.get("test.key")
    assert value == "test_value"
    
    print("✅ Config update works")

if __name__ == "__main__":
    print("🧪 Testing Config Scenarios...")
    test_valid_config()
    test_missing_key_with_default()
    test_custom_config_file()
    test_config_update()
    print("🎉 All config tests passed!")
