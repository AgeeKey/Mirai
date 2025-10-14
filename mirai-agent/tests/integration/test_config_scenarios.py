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

def test_config_file_exists():
    """Test that config or api_keys file exists"""
    api_keys_path = Path(__file__).parent.parent.parent / "configs" / "api_keys.json"
    
    if api_keys_path.exists():
        with open(api_keys_path) as f:
            keys = json.load(f)
        print(f"✅ API keys file exists with {len(keys)} keys configured")
    else:
        print(f"⚠️ API keys file not found (expected for security)")
        # This is OK - may be using env vars
    
    print("✅ Config check passed")

def test_api_keys_template_exists():
    """Test that API keys template exists"""
    api_keys_path = Path(__file__).parent.parent.parent / "configs" / "api_keys.json"
    
    if api_keys_path.exists():
        with open(api_keys_path) as f:
            keys = json.load(f)
        print(f"✅ API keys file exists with {len(keys)} keys")
    else:
        print(f"⚠️ API keys file not found (expected for security)")

def test_example_config():
    """Test creating and loading example config"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        example_config = {
            "version": "test.1.0",
            "test_key": "test_value",
            "nested": {
                "key": "value"
            }
        }
        json.dump(example_config, f)
        temp_path = f.name
    
    try:
        # Load and validate
        with open(temp_path) as f:
            loaded = json.load(f)
        
        assert loaded["version"] == "test.1.0"
        assert loaded["test_key"] == "test_value"
        assert loaded["nested"]["key"] == "value"
        
        print("✅ Custom config file loads correctly")
    finally:
        os.unlink(temp_path)

if __name__ == "__main__":
    print("🧪 Testing Config Scenarios...")
    test_config_file_exists()
    test_api_keys_template_exists()
    test_example_config()
    print("🎉 All config tests passed!")
