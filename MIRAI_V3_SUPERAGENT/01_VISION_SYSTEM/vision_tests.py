#!/usr/bin/env python3
"""
PHASE 1: Vision System Test Suite
=================================

Comprehensive tests for all vision system components.
Includes unit tests, integration tests, and mock tests.

Author: MIRAI AI Agent
Version: 1.0.0
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from io import BytesIO

import numpy as np
from PIL import Image

# Import vision system components
from vision_complete import (
    VisionConfig,
    VisionLogger,
    VisionCache,
    VisionDatabase,
    VisionInitializer,
    ScreenCaptureManager,
    GPT4VisionAnalyzer,
    ScreenAnalyzer,
    ElementDetector,
    ProblemDetector,
    VisionOrchestrator,
    VisionError,
    ScreenshotError,
    GPT4VisionError
)


# ============================================================================
# Test Utilities
# ============================================================================

def create_test_image(width: int = 800, height: int = 600) -> Image.Image:
    """Create a test image for testing."""
    # Create a simple test image with some patterns
    img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    # Add some structure (a rectangle)
    img_array[100:200, 100:300] = [255, 0, 0]  # Red rectangle
    img_array[300:400, 400:600] = [0, 255, 0]  # Green rectangle
    
    return Image.fromarray(img_array, 'RGB')


# ============================================================================
# Test Vision Configuration
# ============================================================================

class TestVisionConfig(unittest.TestCase):
    """Test vision configuration class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = VisionConfig()
        
        self.assertEqual(config.screenshot_resolution, (1920, 1080))
        self.assertEqual(config.screenshot_quality, 95)
        self.assertEqual(config.gpt4_model, "gpt-4o-mini")
        self.assertEqual(config.max_retries, 3)
        self.assertTrue(config.cache_enabled)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = VisionConfig(
            screenshot_quality=80,
            gpt4_model="gpt-4o",
            max_retries=5
        )
        
        self.assertEqual(config.screenshot_quality, 80)
        self.assertEqual(config.gpt4_model, "gpt-4o")
        self.assertEqual(config.max_retries, 5)


# ============================================================================
# Test Vision Logger
# ============================================================================

class TestVisionLogger(unittest.TestCase):
    """Test vision logging system."""
    
    def setUp(self):
        """Set up test logger."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.logger = VisionLogger(log_file=self.log_file)
    
    def tearDown(self):
        """Clean up test files."""
        shutil.rmtree(self.temp_dir)
    
    def test_logger_initialization(self):
        """Test logger initializes correctly."""
        self.assertIsNotNone(self.logger.logger)
        self.assertEqual(self.logger.log_file, self.log_file)
    
    def test_logging_methods(self):
        """Test all logging methods."""
        self.logger.info("Test info")
        self.logger.debug("Test debug")
        self.logger.warning("Test warning")
        self.logger.error("Test error")
        
        # Check log file was created
        self.assertTrue(os.path.exists(self.log_file))
    
    def test_log_file_content(self):
        """Test log file contains messages."""
        test_message = "Test log message"
        self.logger.info(test_message)
        
        with open(self.log_file, 'r') as f:
            content = f.read()
            self.assertIn(test_message, content)


# ============================================================================
# Test Vision Cache
# ============================================================================

class TestVisionCache(unittest.TestCase):
    """Test vision caching system."""
    
    def setUp(self):
        """Set up test cache."""
        self.cache = VisionCache(ttl=1)  # 1 second TTL for testing
    
    def test_cache_set_get(self):
        """Test basic cache operations."""
        self.cache.set("test_key", "test_value")
        value = self.cache.get("test_key")
        
        self.assertEqual(value, "test_value")
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        value = self.cache.get("nonexistent_key")
        self.assertIsNone(value)
    
    def test_cache_expiration(self):
        """Test cache expiration."""
        import time
        
        self.cache.set("test_key", "test_value", ttl=0.5)
        
        # Should be available immediately
        value = self.cache.get("test_key")
        self.assertEqual(value, "test_value")
        
        # Wait for expiration
        time.sleep(0.6)
        
        # Should be expired
        value = self.cache.get("test_key")
        self.assertIsNone(value)
    
    def test_cache_clear(self):
        """Test cache clear."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.cache.clear()
        
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))


# ============================================================================
# Test Vision Database
# ============================================================================

class TestVisionDatabase(unittest.TestCase):
    """Test vision database system."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.db = VisionDatabase(self.db_path)
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close()
        shutil.rmtree(self.temp_dir)
    
    def test_database_creation(self):
        """Test database file is created."""
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_store_screenshot(self):
        """Test storing screenshot metadata."""
        screenshot_id = self.db.store_screenshot(
            file_path="/test/screenshot.png",
            width=1920,
            height=1080,
            format="PNG",
            size_bytes=123456,
            checksum="abc123"
        )
        
        self.assertIsNotNone(screenshot_id)
        self.assertGreater(screenshot_id, 0)
    
    def test_tables_exist(self):
        """Test all required tables exist."""
        cursor = self.db.conn.cursor()
        
        # Check screenshots table
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='screenshots'"
        )
        self.assertIsNotNone(cursor.fetchone())
        
        # Check analysis_results table
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_results'"
        )
        self.assertIsNotNone(cursor.fetchone())
        
        # Check detected_elements table
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='detected_elements'"
        )
        self.assertIsNotNone(cursor.fetchone())


# ============================================================================
# Test Vision Initializer
# ============================================================================

class TestVisionInitializer(unittest.TestCase):
    """Test vision system initialization."""
    
    def setUp(self):
        """Set up test initializer."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = VisionConfig(output_dir=self.temp_dir)
        self.initializer = VisionInitializer(self.config)
    
    def tearDown(self):
        """Clean up test files."""
        if self.initializer.db:
            self.initializer.db.close()
        shutil.rmtree(self.temp_dir)
    
    def test_initializer_setup(self):
        """Test complete initialization."""
        self.initializer.setup()
        
        self.assertIsNotNone(self.initializer.logger)
        self.assertIsNotNone(self.initializer.db)
        self.assertIsNotNone(self.initializer.directories)
        self.assertIsNotNone(self.initializer.gpu_info)
    
    def test_directory_creation(self):
        """Test output directories are created."""
        self.initializer.setup()
        
        # Check all directories exist
        for name, path in self.initializer.directories.items():
            self.assertTrue(path.exists(), f"Directory {name} should exist")


# ============================================================================
# Test Screenshot Capture Manager
# ============================================================================

class TestScreenCaptureManager(unittest.TestCase):
    """Test screenshot capture system."""
    
    def setUp(self):
        """Set up test capture manager."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = VisionConfig(output_dir=self.temp_dir)
        self.logger = VisionLogger()
        self.db = VisionDatabase(os.path.join(self.temp_dir, "test.db"))
        self.capture_manager = ScreenCaptureManager(
            self.config,
            self.logger,
            self.db
        )
    
    def tearDown(self):
        """Clean up test files."""
        self.db.close()
        shutil.rmtree(self.temp_dir)
    
    def test_pil_to_numpy_conversion(self):
        """Test PIL to numpy conversion."""
        test_image = create_test_image()
        img_array = self.capture_manager.pil_to_numpy(test_image)
        
        self.assertIsInstance(img_array, np.ndarray)
        self.assertEqual(len(img_array.shape), 3)
        self.assertEqual(img_array.shape[2], 3)  # BGR channels
    
    def test_numpy_to_pil_conversion(self):
        """Test numpy to PIL conversion."""
        test_image = create_test_image()
        img_array = self.capture_manager.pil_to_numpy(test_image)
        pil_image = self.capture_manager.numpy_to_pil(img_array)
        
        self.assertIsInstance(pil_image, Image.Image)
        self.assertEqual(pil_image.width, test_image.width)
        self.assertEqual(pil_image.height, test_image.height)
    
    def test_compress_screenshot(self):
        """Test screenshot compression."""
        test_image = create_test_image()
        buffer, size = self.capture_manager.compress_screenshot(test_image, quality=85)
        
        self.assertIsInstance(buffer, BytesIO)
        self.assertGreater(size, 0)
    
    def test_save_screenshot(self):
        """Test saving screenshot to disk."""
        test_image = create_test_image()
        filepath = self.capture_manager.save_screenshot(test_image)
        
        self.assertTrue(os.path.exists(filepath))
        self.assertGreater(os.path.getsize(filepath), 0)
    
    def test_encode_to_base64(self):
        """Test base64 encoding."""
        test_image = create_test_image()
        base64_str = self.capture_manager.encode_to_base64(test_image)
        
        self.assertIsInstance(base64_str, str)
        self.assertGreater(len(base64_str), 0)
    
    def test_create_thumbnail(self):
        """Test thumbnail creation."""
        test_image = create_test_image()
        thumbnail = self.capture_manager.create_thumbnail(test_image, size=(100, 100))
        
        self.assertIsInstance(thumbnail, Image.Image)
        self.assertLessEqual(thumbnail.width, 100)
        self.assertLessEqual(thumbnail.height, 100)


# ============================================================================
# Test GPT-4 Vision Analyzer
# ============================================================================

class TestGPT4VisionAnalyzer(unittest.TestCase):
    """Test GPT-4 Vision integration."""
    
    def setUp(self):
        """Set up test analyzer with mock client."""
        self.config = VisionConfig()
        self.logger = VisionLogger()
        self.cache = VisionCache()
        
        # Create mock OpenAI client
        self.mock_client = MagicMock()
        self.analyzer = GPT4VisionAnalyzer(
            self.mock_client,
            self.config,
            self.logger,
            self.cache
        )
    
    def test_analyze_image_with_mock(self):
        """Test image analysis with mocked API."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            'description': 'Test screenshot',
            'elements': ['button', 'text field'],
            'problems': [],
            'recommendations': ['Click the button']
        })
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test analysis
        test_image = create_test_image()
        result = self.analyzer.analyze_image(test_image)
        
        self.assertIsInstance(result, dict)
        self.assertIn('description', result)
        self.assertIn('elements', result)
        self.assertIn('processing_time', result)
    
    def test_analyze_image_caching(self):
        """Test that results are cached."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"description": "Test"}'
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # First call
        test_image = create_test_image()
        result1 = self.analyzer.analyze_image(test_image)
        
        # Second call should use cache
        result2 = self.analyzer.analyze_image(test_image)
        
        # API should only be called once
        self.assertEqual(
            self.mock_client.chat.completions.create.call_count,
            1
        )


# ============================================================================
# Test Screen Analyzer
# ============================================================================

class TestScreenAnalyzer(unittest.TestCase):
    """Test screen analysis system."""
    
    def setUp(self):
        """Set up test analyzer."""
        self.config = VisionConfig()
        self.logger = VisionLogger()
        self.analyzer = ScreenAnalyzer(self.config, self.logger)
    
    def test_analyze_screen(self):
        """Test complete screen analysis."""
        test_image = create_test_image()
        result = self.analyzer.analyze_screen(test_image)
        
        self.assertIsInstance(result, dict)
        self.assertIn('dimensions', result)
        self.assertIn('color_info', result)
        self.assertIn('text_regions', result)
        self.assertIn('layout', result)
    
    def test_color_analysis(self):
        """Test color scheme analysis."""
        test_image = create_test_image()
        img_array = np.array(test_image)
        color_info = self.analyzer._analyze_colors(img_array)
        
        self.assertIn('average_color', color_info)
        self.assertIn('brightness', color_info)
        self.assertIn('theme', color_info)
        self.assertIn(color_info['theme'], ['dark', 'light'])


# ============================================================================
# Test Element Detector
# ============================================================================

class TestElementDetector(unittest.TestCase):
    """Test UI element detection."""
    
    def setUp(self):
        """Set up test detector."""
        self.config = VisionConfig()
        self.logger = VisionLogger()
        self.detector = ElementDetector(self.config, self.logger)
    
    def test_detect_all_elements(self):
        """Test complete element detection."""
        test_image = create_test_image()
        elements = self.detector.detect_all_elements(test_image)
        
        self.assertIsInstance(elements, list)
        # May or may not find elements in random image, just check it runs
    
    def test_element_structure(self):
        """Test detected elements have correct structure."""
        test_image = create_test_image(width=1000, height=800)
        elements = self.detector.detect_all_elements(test_image)
        
        for element in elements:
            self.assertIn('type', element)
            self.assertIn('x', element)
            self.assertIn('y', element)
            self.assertIn('width', element)
            self.assertIn('height', element)
            self.assertIn('confidence', element)


# ============================================================================
# Test Problem Detector
# ============================================================================

class TestProblemDetector(unittest.TestCase):
    """Test problem detection system."""
    
    def setUp(self):
        """Set up test detector."""
        self.config = VisionConfig()
        self.logger = VisionLogger()
        self.detector = ProblemDetector(self.config, self.logger)
    
    def test_detect_problems(self):
        """Test problem detection."""
        test_image = create_test_image()
        problems = self.detector.detect_problems(test_image)
        
        self.assertIsInstance(problems, list)
    
    def test_detect_problems_with_gpt4_analysis(self):
        """Test problem detection with GPT-4 analysis."""
        test_image = create_test_image()
        gpt4_analysis = {
            'problems': ['Ad detected', 'Popup window']
        }
        
        problems = self.detector.detect_problems(test_image, gpt4_analysis)
        
        self.assertIsInstance(problems, list)
        self.assertGreaterEqual(len(problems), 2)  # At least the GPT-4 problems


# ============================================================================
# Test Vision Orchestrator
# ============================================================================

class TestVisionOrchestrator(unittest.TestCase):
    """Test complete vision system orchestration."""
    
    def setUp(self):
        """Set up test orchestrator."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = VisionConfig(output_dir=self.temp_dir)
        
        # Don't use real OpenAI API in tests
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}, clear=False):
            self.orchestrator = VisionOrchestrator(config=self.config)
    
    def tearDown(self):
        """Clean up test files."""
        self.orchestrator.cleanup()
        shutil.rmtree(self.temp_dir)
    
    @patch('pyautogui.screenshot')
    def test_run_complete_vision(self, mock_screenshot):
        """Test complete vision pipeline."""
        # Mock screenshot capture
        mock_screenshot.return_value = create_test_image()
        
        result = self.orchestrator.run_complete_vision(save_screenshot=False)
        
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('timestamp', result)
        self.assertIn('processing_time', result)
        self.assertIn('screenshot', result)
        self.assertIn('screen_analysis', result)
        self.assertIn('elements', result)
        self.assertIn('problems', result)
        self.assertIn('summary', result)
    
    @patch('pyautogui.screenshot')
    def test_cognitive_loop(self, mock_screenshot):
        """Test cognitive loop execution."""
        # Mock screenshot capture
        mock_screenshot.return_value = create_test_image()
        
        results = self.orchestrator.cognitive_loop(iterations=2, interval=0.1)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        
        for result in results:
            self.assertIn('success', result)


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = VisionConfig(output_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up integration test files."""
        shutil.rmtree(self.temp_dir)
    
    @patch('pyautogui.screenshot')
    def test_end_to_end_workflow(self, mock_screenshot):
        """Test complete end-to-end workflow."""
        # Mock screenshot
        mock_screenshot.return_value = create_test_image()
        
        # Initialize system without OpenAI key
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}, clear=False):
            orchestrator = VisionOrchestrator(config=self.config)
        
        # Run analysis
        result = orchestrator.run_complete_vision(save_screenshot=True)
        
        # Verify results
        self.assertTrue(result['success'])
        self.assertGreater(result['summary']['total_elements'], 0)
        
        # Verify screenshot was saved
        if result['screenshot']['filepath']:
            self.assertTrue(os.path.exists(result['screenshot']['filepath']))
        
        # Cleanup
        orchestrator.cleanup()


# ============================================================================
# Test Runner
# ============================================================================

def run_tests():
    """Run all tests."""
    import json
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestVisionConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestVisionLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestVisionCache))
    suite.addTests(loader.loadTestsFromTestCase(TestVisionDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestVisionInitializer))
    suite.addTests(loader.loadTestsFromTestCase(TestScreenCaptureManager))
    suite.addTests(loader.loadTestsFromTestCase(TestGPT4VisionAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestScreenAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestElementDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestProblemDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestVisionOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("🧪 TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
