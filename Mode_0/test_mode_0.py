import sys
import os
# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now imports will work
from mode_0.config.config_manager import ConfigManager
# Other imports...
import unittest
import sys
import os
import time
import json
import logging
import importlib
import inspect
import sqlite3
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path
from io import StringIO
from datetime import datetime, timedelta
from contextlib import redirect_stdout, redirect_stderr

def find_module_path():
    """Find the mode_0 module path regardless of current directory"""
    # Start with current directory
    current = Path(os.getcwd())
    
    # Strategy 1: Check if we're in the Module_0_Git directory with Mode_0 subdirectory
    mode_0_dir = current / "Mode_0" / "mode_0"
    if mode_0_dir.exists():
        return str(current / "Mode_0")
        
    # Strategy 2: Check if we're already in the Mode_0 directory
    if (current / "mode_0").exists():
        return str(current)
        
    # Strategy 3: Check parent directory
    parent = current.parent
    if (parent / "Mode_0" / "mode_0").exists():
        return str(parent / "Mode_0")
        
    # Strategy 4: Search up to 3 levels up for Mode_0/mode_0
    for _ in range(3):
        current = current.parent
        if (current / "Mode_0" / "mode_0").exists():
            return str(current / "Mode_0")
    
    # Final diagnostic info if module not found
    return None

# Find and add the module path
module_path = find_module_path()
if module_path:
    sys.path.insert(0, module_path)
    print(f"Added module path: {module_path}")
else:
    print("ERROR: Could not locate the Mode_0/mode_0 module directory.")
    print(f"Current directory: {os.getcwd()}")
    print(f"sys.path: {sys.path}")

class TestReport:
    """Generates and formats test reports"""
    
    def __init__(self):
        self.results = {
            "start_time": time.time(),
            "end_time": None,
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "modules": {},
            "failures": [],
            "errors": []
        }
        self.current_module = None
        
        # ASCII alternatives to Unicode symbols for Windows
        self.PASS_SYMBOL = "PASS" 
        self.FAIL_SYMBOL = "FAIL"
        self.WARN_SYMBOL = "WARN"
    
    def start_module(self, module_name):
        """Record the start of a module test"""
        self.current_module = module_name
        if module_name not in self.results["modules"]:
            self.results["modules"][module_name] = {
                "tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "functions_tested": [],
                "issues": []
            }
    
    def add_function_tested(self, function_name):
        """Record a tested function"""
        if function_name not in self.results["modules"][self.current_module]["functions_tested"]:
            self.results["modules"][self.current_module]["functions_tested"].append(function_name)
    
    def add_test_result(self, test_name, result, error=None):
        """Add test result to the report"""
        self.results["total_tests"] += 1
        self.results["modules"][self.current_module]["tests"] += 1
        
        if result == "pass":
            self.results["passed"] += 1
            self.results["modules"][self.current_module]["passed"] += 1
        elif result == "fail":
            self.results["failed"] += 1
            self.results["modules"][self.current_module]["failed"] += 1
            self.results["failures"].append({
                "module": self.current_module,
                "test": test_name,
                "error": str(error)
            })
        elif result == "error":
            self.results["errors"] += 1
            self.results["modules"][self.current_module]["errors"] += 1
            self.results["errors"].append({
                "module": self.current_module,
                "test": test_name,
                "error": str(error)
            })
        elif result == "skip":
            self.results["skipped"] += 1
            self.results["modules"][self.current_module]["skipped"] += 1
    
    def add_issue(self, issue):
        """Add potential issue to module report"""
        self.results["modules"][self.current_module]["issues"].append(issue)
    
    def finalize(self):
        """Finalize the report"""
        self.results["end_time"] = time.time()
        self.results["duration"] = self.results["end_time"] - self.results["start_time"]
    
    def generate_report(self):
        """Generate formatted report"""
        self.finalize()
        
        # Build report
        report = []
        report.append("=" * 80)
        report.append(f"MODE_0 BOT TEST REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("TEST SUMMARY")
        report.append("-" * 80)
        report.append(f"Duration: {self.results['duration']:.2f} seconds")
        report.append(f"Total Tests: {self.results['total_tests']}")
        report.append(f"Passed: {self.results['passed']} ({(self.results['passed'] / self.results['total_tests'] * 100) if self.results['total_tests'] else 0:.1f}%)")
        report.append(f"Failed: {self.results['failed']}")
        report.append(f"Errors: {self.results['errors']}")
        report.append(f"Skipped: {self.results['skipped']}")
        report.append("")
        
        # Overall assessment
        total_issues = sum(len(module_data["issues"]) for module_data in self.results["modules"].values())
        if self.results["failed"] == 0 and self.results["errors"] == 0 and total_issues == 0:
            report.append(f"{self.PASS_SYMBOL} OVERALL ASSESSMENT: All tests passed. No issues detected.")
        elif self.results["failed"] > 0 or self.results["errors"] > 0:
            report.append(f"{self.FAIL_SYMBOL} OVERALL ASSESSMENT: Tests failed. See details below.")
        else:
            report.append(f"{self.WARN_SYMBOL} OVERALL ASSESSMENT: Tests passed but potential issues detected. See details below.")
        report.append("")
        
        # Module breakdown
        report.append("MODULE BREAKDOWN")
        report.append("-" * 80)
        for module, data in self.results["modules"].items():
            success_rate = (data['passed'] / data['tests'] * 100) if data['tests'] else 0
            status = self.PASS_SYMBOL if data['failed'] == 0 and data['errors'] == 0 else self.FAIL_SYMBOL
            
            report.append(f"{status} Module: {module}")
            report.append(f"  Tests: {data['tests']} (Passed: {data['passed']}, Failed: {data['failed']}, Errors: {data['errors']}, Skipped: {data['skipped']})")
            report.append(f"  Success Rate: {success_rate:.1f}%")
            
            if data["functions_tested"]:
                report.append("  Functions tested:")
                for func in sorted(data["functions_tested"]):
                    report.append(f"    - {func}")
            else:
                report.append("  No functions explicitly tested.")
            
            if data["issues"]:
                report.append("  Potential issues:")
                for issue in data["issues"]:
                    report.append(f"    - {self.WARN_SYMBOL} {issue}")
            
            report.append("")
        
        # Failures and errors
        if self.results["failures"]:
            report.append("FAILURES")
            report.append("-" * 80)
            for failure in self.results["failures"]:
                report.append(f"Module: {failure['module']}")
                report.append(f"Test: {failure['test']}")
                report.append(f"Error: {failure['error']}")
                report.append("")
        
        if self.results["errors"]:
            report.append("ERRORS")
            report.append("-" * 80)
            for error in self.results["errors"]:
                report.append(f"Module: {error['module']}")
                report.append(f"Test: {error['test']}")
                report.append(f"Error: {error['error']}")
                report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 80)
        if self.results["failed"] > 0 or self.results["errors"] > 0:
            report.append("- Fix failing tests and errors before deployment")
        
        # Add module-specific recommendations
        for module, data in self.results["modules"].items():
            if data["issues"]:
                for issue in data["issues"]:
                    if "placeholder" in issue.lower():
                        report.append(f"- Implement {module}: {issue}")
                    elif "not tested" in issue.lower():
                        report.append(f"- Add tests for {module}: {issue}")
        
        report.append("- Run this test suite regularly during development")
        report.append("- Consider adding more integration tests between components")
        report.append("")
        
        report.append("=" * 80)
        return "\n".join(report)

# Base test class with common functionality
class Mode0TestCase(unittest.TestCase):
    """Base test class for all Mode_0 test cases"""
    
    def setUp(self):
        self.report = test_report
    
    def run_async(self, coro):
        """Run async coroutine in test"""
        return asyncio.run(coro)

# Test case for config manager
class TestConfigManager(Mode0TestCase):
    """Test the configuration manager"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("ConfigManager")
        
        # Create test config
        self.test_config = {
            "test": {
                "value1": "test1",
                "value2": "test2",
                "nested": {
                    "value": "nested_value"
                }
            }
        }
        
        # Create temp config file
        self.config_path = "temp_test_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(self.test_config, f)
    
    def tearDown(self):
        # Clean up
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
    
    def test_load_config(self):
        """Test config loading"""
        self.report.add_function_tested("load_config")
        try:
            from mode_0.config.config_manager import ConfigManager
            config = ConfigManager(self.config_path)
            self.assertEqual(config.config, self.test_config)
            self.report.add_test_result("test_load_config", "pass")
        except Exception as e:
            self.report.add_test_result("test_load_config", "fail", e)
            raise
    
    def test_get_config_value(self):
        """Test getting config values with dot notation"""
        self.report.add_function_tested("get")
        try:
            from mode_0.config.config_manager import ConfigManager
            config = ConfigManager(self.config_path)
            self.assertEqual(config.get("test.value1"), "test1")
            self.assertEqual(config.get("test.nested.value"), "nested_value")
            self.assertEqual(config.get("nonexistent"), None)
            self.assertEqual(config.get("nonexistent", "default"), "default")
            self.report.add_test_result("test_get_config_value", "pass")
        except Exception as e:
            self.report.add_test_result("test_get_config_value", "fail", e)
            raise
    
    def test_set_config_value(self):
        """Test setting config values with dot notation"""
        self.report.add_function_tested("set")
        try:
            from mode_0.config.config_manager import ConfigManager
            config = ConfigManager(self.config_path)
            config.set("test.value1", "updated")
            self.assertEqual(config.get("test.value1"), "updated")
            
            config.set("test.new_value", "new")
            self.assertEqual(config.get("test.new_value"), "new")
            
            config.set("new_section.value", "value")
            self.assertEqual(config.get("new_section.value"), "value")
            
            self.report.add_test_result("test_set_config_value", "pass")
        except Exception as e:
            self.report.add_test_result("test_set_config_value", "fail", e)
            raise
    
    def test_save_config(self):
        """Test saving config to file"""
        self.report.add_function_tested("save")
        try:
            from mode_0.config.config_manager import ConfigManager
            config = ConfigManager(self.config_path)
            config.set("test.value1", "saved_value")
            config.save()
            
            # Load again to verify
            new_config = ConfigManager(self.config_path)
            self.assertEqual(new_config.get("test.value1"), "saved_value")
            
            self.report.add_test_result("test_save_config", "pass")
        except Exception as e:
            self.report.add_test_result("test_save_config", "fail", e)
            raise
    
    def test_handle_missing_config(self):
        """Test handling of missing config file"""
        self.report.add_function_tested("load_config")
        try:
            from mode_0.config.config_manager import ConfigManager
            # Non-existent path
            config = ConfigManager("nonexistent_config.json")
            self.assertEqual(config.config, {})
            self.report.add_test_result("test_handle_missing_config", "pass")
        except Exception as e:
            self.report.add_test_result("test_handle_missing_config", "fail", e)
            raise

# Test case for database manager
class TestDatabaseManager(Mode0TestCase):
    """Test the database manager"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("DatabaseManager")
        
        # Set up in-memory database
        self.db_path = ":memory:"
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_setup_database(self, mock_sqlite):
        """Test database table setup"""
        self.report.add_function_tested("setup_database")
        try:
            # Configure mock
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_sqlite.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Test
            from mode_0.database.db_manager import DatabaseManager
            db = DatabaseManager(self.db_path)
            
            # Verify
            self.assertEqual(mock_cursor.execute.call_count, 3)  # Three tables
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            self.report.add_test_result("test_setup_database", "pass")
        except Exception as e:
            self.report.add_test_result("test_setup_database", "fail", e)
            raise
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_add_or_update_user(self, mock_sqlite):
        """Test adding and updating users"""
        self.report.add_function_tested("add_or_update_user")
        try:
            # Configure mock
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_sqlite.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # New user scenario
            mock_cursor.fetchone.return_value = None
            
            # Test adding new user
            from mode_0.database.db_manager import DatabaseManager
            db = DatabaseManager(self.db_path)
            self.run_async(db.add_or_update_user("user123", "testuser", "TestUser"))
            
            # Should call INSERT for new user
            execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
            self.assertTrue(any('INSERT INTO users' in call for call in execute_calls))
            
            # Reset mocks
            mock_cursor.reset_mock()
            mock_conn.reset_mock()
            
            # Existing user scenario
            mock_cursor.fetchone.return_value = ("user123", "old_name", "OldName", "2023-01-01", "2023-01-01", 1, "{}")
            
            # Test updating existing user
            self.run_async(db.add_or_update_user("user123", "testuser", "TestUser"))
            
            # Should call UPDATE for existing user
            execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
            self.assertTrue(any('UPDATE users' in call for call in execute_calls))
            
            self.report.add_test_result("test_add_or_update_user", "pass")
        except Exception as e:
            self.report.add_test_result("test_add_or_update_user", "fail", e)
            raise
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_add_message(self, mock_sqlite):
        """Test adding messages to the database"""
        self.report.add_function_tested("add_message")
        try:
            # Configure mock
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_sqlite.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Test
            from mode_0.database.db_manager import DatabaseManager
            db = DatabaseManager(self.db_path)
            self.run_async(db.add_message("user123", "Test message", "test_channel"))
            
            # Verify
            execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
            self.assertTrue(any('INSERT INTO messages' in call for call in execute_calls))
            
            self.report.add_test_result("test_add_message", "pass")
        except Exception as e:
            self.report.add_test_result("test_add_message", "fail", e)
            raise
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_get_user_profile(self, mock_sqlite):
        """Test retrieving user profile"""
        self.report.add_function_tested("get_user_profile")
        try:
            # Configure mock
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_sqlite.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # User exists
            mock_cursor.fetchone.return_value = ('{"interests": ["music"]}',)
            
            # Test
            from mode_0.database.db_manager import DatabaseManager
            db = DatabaseManager(self.db_path)
            profile = self.run_async(db.get_user_profile("user123"))
            
            # Verify
            self.assertEqual(profile, {"interests": ["music"]})
            mock_cursor.execute.assert_called_with('SELECT profile FROM users WHERE user_id = ?', ("user123",))
            
            # User doesn't exist
            mock_cursor.fetchone.return_value = None
            profile = self.run_async(db.get_user_profile("nonexistent"))
            self.assertEqual(profile, {})
            
            self.report.add_test_result("test_get_user_profile", "pass")
        except Exception as e:
            self.report.add_test_result("test_get_user_profile", "fail", e)
            raise
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_update_user_profile(self, mock_sqlite):
        """Test updating user profile"""
        self.report.add_function_tested("update_user_profile")
        try:
            # Configure mock
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_sqlite.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Test
            from mode_0.database.db_manager import DatabaseManager
            db = DatabaseManager(self.db_path)
            test_profile = {"interests": ["music", "gaming"], "mood": "happy"}
            self.run_async(db.update_user_profile("user123", test_profile))
            
            # Verify
            execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
            self.assertTrue(any('UPDATE users' in call for call in execute_calls))
            
            self.report.add_test_result("test_update_user_profile", "pass")
        except Exception as e:
            self.report.add_test_result("test_update_user_profile", "fail", e)
            raise

# Test case for persona system
class TestPersonaSystem(Mode0TestCase):
    """Test the persona system"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("PersonaSystem")
        
        # Mock database
        self.mock_db = MagicMock()
        
        # Test responses
        self.test_responses = {
            "greetings": ["Hey there, {username}!", "Hello, {username}!"],
            "generic_responses": ["That's interesting, {username}!", "Cool, {username}!"],
            "question_responses": ["Good question, {username}!", "Let me think, {username}..."],
            "conversation_starters": ["Test starter 1", "Test starter 2"]
        }
        
        # Test config
        self.test_config = {
            "base_personality": {
                "friendly": 0.8,
                "humor": 0.7
            },
            "learning_rate": 0.05
        }
    
    @patch("builtins.open")
    def test_init_and_defaults(self, mock_open):
        """Test initialization and defaults"""
        self.report.add_function_tested("__init__")
        self.report.add_function_tested("_default_persona_config")
        self.report.add_function_tested("_default_responses")
        try:
            # Test with missing files
            mock_open.side_effect = FileNotFoundError
            
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            
            # Should use defaults
            self.assertIsNotNone(persona.config)
            self.assertIsNotNone(persona.responses)
            
            # Verify mood and learning rate
            self.assertEqual(persona.mood, "neutral")
            self.assertEqual(persona.learning_rate, 0.05)
            
            self.report.add_test_result("test_init_and_defaults", "pass")
        except Exception as e:
            self.report.add_test_result("test_init_and_defaults", "fail", e)
            raise
    
    @patch("builtins.open")
    def test_generate_greeting(self, mock_open):
        """Test greeting generation"""
        self.report.add_function_tested("generate_greeting")
        try:
            # Mock responses file
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.test_responses)
            
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            persona.responses = self.test_responses  # Override with our test responses
            
            # Test greeting
            greeting = self.run_async(persona.generate_greeting("testuser", "user123"))
            
            # Should format username
            self.assertIn("testuser", greeting)
            
            self.report.add_test_result("test_generate_greeting", "pass")
        except Exception as e:
            self.report.add_test_result("test_generate_greeting", "fail", e)
            raise
    
    @patch("builtins.open")
    def test_get_conversation_starter(self, mock_open):
        """Test conversation starter generation"""
        self.report.add_function_tested("get_conversation_starter")
        try:
            # Mock responses file
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.test_responses)
            
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            persona.responses = self.test_responses  # Override with our test responses
            
            # Test conversation starter
            starter = self.run_async(persona.get_conversation_starter())
            
            # Should use one of the starters
            self.assertTrue(starter in ["Test starter 1", "Test starter 2"])
            
            self.report.add_test_result("test_get_conversation_starter", "pass")
        except Exception as e:
            self.report.add_test_result("test_get_conversation_starter", "fail", e)
            raise
    
    @patch("builtins.open")
    def test_generate_response(self, mock_open):
        """Test response generation"""
        self.report.add_function_tested("generate_response")
        try:
            # Mock responses file
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.test_responses)
            
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            persona.responses = self.test_responses  # Override with our test responses
            
            # Mock message
            mock_message = MagicMock()
            mock_message.content = "Test message"
            mock_message.author = MagicMock()
            mock_message.author.display_name = "testuser"
            
            # Test response
            response = self.run_async(persona.generate_response(mock_message))
            
            # Should format username
            self.assertIn("testuser", response)
            
            self.report.add_test_result("test_generate_response", "pass")
        except Exception as e:
            self.report.add_test_result("test_generate_response", "fail", e)
            raise

# Test case for user profiler
class TestUserProfiler(Mode0TestCase):
    """Test the user profiler"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("UserProfiler")
        
        # Mock database
        self.mock_db = MagicMock()
        
        # Set up mock profile
        self.test_profile = {
            "first_seen": "2023-01-01T12:00:00",
            "visits": 1,
            "interests": ["music"],
            "conversations": []
        }
        
        # Configure mock get_user_profile
        self.mock_db.get_user_profile = AsyncMock(return_value=self.test_profile)
        self.mock_db.update_user_profile = AsyncMock()
    
    def test_get_user_profile(self):
        """Test getting user profile"""
        self.report.add_function_tested("get_user_profile")
        try:
            from mode_0.persona.user_profiler import UserProfiler
            profiler = UserProfiler(self.mock_db)
            
            profile = self.run_async(profiler.get_user_profile("user123"))
            
            # Verify
            self.assertEqual(profile, self.test_profile)
            self.mock_db.get_user_profile.assert_called_with("user123")
            
            self.report.add_test_result("test_get_user_profile", "pass")
        except Exception as e:
            self.report.add_test_result("test_get_user_profile", "fail", e)
            raise
    
    def test_update_profile(self):
        """Test updating user profile"""
        self.report.add_function_tested("update_profile")
        try:
            from mode_0.persona.user_profiler import UserProfiler
            profiler = UserProfiler(self.mock_db)
            
            # Mock message
            mock_message = MagicMock()
            mock_message.content = "Test message"
            
            # Test with existing profile
            updated_profile = self.run_async(profiler.update_profile("user123", mock_message))
            
            # Visits should increment
            self.assertEqual(updated_profile["visits"], 2)
            
            # Last seen should be updated
            self.assertIn("last_seen", updated_profile)
            
            # Database update should be called
            self.mock_db.update_user_profile.assert_called_with("user123", updated_profile)
            
            # Test with empty profile
            self.mock_db.get_user_profile = AsyncMock(return_value={})
            
            new_profile = self.run_async(profiler.update_profile("new_user", mock_message))
            
            # New profile should be initialized
            self.assertEqual(new_profile["visits"], 1)
            self.assertIn("first_seen", new_profile)
            self.assertIn("last_seen", new_profile)
            self.assertIn("interests", new_profile)
            self.assertIn("conversations", new_profile)
            
            self.report.add_test_result("test_update_profile", "pass")
        except Exception as e:
            self.report.add_test_result("test_update_profile", "fail", e)
            raise
    
    def test_analyze_message(self):
        """Test message analysis"""
        self.report.add_function_tested("analyze_message")
        try:
            from mode_0.persona.user_profiler import UserProfiler
            profiler = UserProfiler(self.mock_db)
            
            # Mock message
            mock_message = MagicMock()
            mock_message.content = "Test message about music and DJs"
            
            analysis = self.run_async(profiler.analyze_message(mock_message))
            
            # Current implementation returns empty dict
            self.assertEqual(analysis, {})
            self.report.add_issue("analyze_message is a placeholder that returns empty dict")
            
            self.report.add_test_result("test_analyze_message", "pass")
        except Exception as e:
            self.report.add_test_result("test_analyze_message", "fail", e)
            raise

# Test case for StreamElements manager
class TestStreamElementsManager(Mode0TestCase):
    """Test the StreamElements manager"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("StreamElementsManager")
        
        # Test credentials
        self.jwt_token = "test_jwt_token"
        self.channel_id = "test_channel_id"
    
    def test_initialization(self):
        """Test initialization"""
        self.report.add_function_tested("__init__")
        try:
            from mode_0.streamelements.se_manager import StreamElementsManager
            se_manager = StreamElementsManager(self.jwt_token, self.channel_id)
            
            # Verify headers
            self.assertEqual(se_manager.jwt_token, self.jwt_token)
            self.assertEqual(se_manager.channel_id, self.channel_id)
            self.assertEqual(se_manager.headers, {
                'Authorization': f'Bearer {self.jwt_token}',
                'Content-Type': 'application/json'
            })
            
            # Verify URLs
            self.assertEqual(se_manager.base_url, "https://api.streamelements.com/kappa/v2")
            self.assertEqual(se_manager.ws_url, "wss://realtime.streamelements.com/socket.io")
            
            # Verify initial state
            self.assertFalse(se_manager.connected)
            self.assertIsNone(se_manager.ws)
            self.assertEqual(se_manager.commands, {})
            self.assertEqual(se_manager.games, {
                "solo": [],
                "group": [],
                "duel": []
            })
            
            self.report.add_test_result("test_initialization", "pass")
        except Exception as e:
            self.report.add_test_result("test_initialization", "fail", e)
            raise
    
    def test_connect(self):
        """Test connecting to StreamElements API"""
        self.report.add_function_tested("connect")
        try:
            from mode_0.streamelements.se_manager import StreamElementsManager
            
            # Create instance with mock methods
            se_manager = StreamElementsManager(self.jwt_token, self.channel_id)
            se_manager.fetch_commands = AsyncMock()
            se_manager.fetch_games = AsyncMock()
            se_manager.connect_websocket = AsyncMock()
            
            # Test connect
            self.run_async(se_manager.connect())
            
            # Verify methods were called
            se_manager.fetch_commands.assert_called_once()
            se_manager.fetch_games.assert_called_once()
            se_manager.connect_websocket.assert_called_once()
            
            self.report.add_test_result("test_connect", "pass")
            self.report.add_issue("fetch_commands, fetch_games, and connect_websocket methods are placeholders")
        except Exception as e:
            self.report.add_test_result("test_connect", "fail", e)
            raise

# Test case for StreamElements events
class TestStreamElementsEvents(Mode0TestCase):
    """Test the StreamElements events handler"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("StreamElementsEvents")
        
        # Mock bot
        self.mock_bot = MagicMock()
    
    def test_initialization(self):
        """Test initialization"""
        self.report.add_function_tested("__init__")
        try:
            from mode_0.streamelements.se_events import StreamElementsEvents
            events = StreamElementsEvents(self.mock_bot)
            
            # Verify bot reference
            self.assertEqual(events.bot, self.mock_bot)
            
            self.report.add_test_result("test_initialization", "pass")
        except Exception as e:
            self.report.add_test_result("test_initialization", "fail", e)
            raise
    
    def test_handle_event(self):
        """Test event handling"""
        self.report.add_function_tested("handle_event")
        self.report.add_function_tested("handle_follow")
        self.report.add_function_tested("handle_subscription")
        self.report.add_function_tested("handle_tip")
        self.report.add_function_tested("handle_host")
        self.report.add_function_tested("handle_raid")
        self.report.add_function_tested("handle_redemption")
        try:
            from mode_0.streamelements.se_events import StreamElementsEvents
            
            # Create instance with mock methods
            events = StreamElementsEvents(self.mock_bot)
            events.handle_follow = AsyncMock()
            events.handle_subscription = AsyncMock()
            events.handle_tip = AsyncMock()
            events.handle_host = AsyncMock()
            events.handle_raid = AsyncMock()
            events.handle_redemption = AsyncMock()
            
            # Test different event types
            event_types = [
                {"type": "follower-latest", "handler": events.handle_follow},
                {"type": "subscriber-latest", "handler": events.handle_subscription},
                {"type": "tip-latest", "handler": events.handle_tip},
                {"type": "host-latest", "handler": events.handle_host},
                {"type": "raid-latest", "handler": events.handle_raid},
                {"type": "redemption-latest", "handler": events.handle_redemption}
            ]
            
            for event in event_types:
                event_data = {"type": event["type"], "data": "test_data"}
                self.run_async(events.handle_event(event_data))
                event["handler"].assert_called_with(event_data)
            
            # Test unknown event type
            event_data = {"type": "unknown-event", "data": "test_data"}
            self.run_async(events.handle_event(event_data))
            
            self.report.add_test_result("test_handle_event", "pass")
            self.report.add_issue("Event handler methods are placeholders")
        except Exception as e:
            self.report.add_test_result("test_handle_event", "fail", e)
            raise

# Test case for utils.helpers
class TestHelpers(Mode0TestCase):
    """Test the utility helper functions"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("Helpers")
    
    def test_get_random_delay(self):
        """Test random delay generator"""
        self.report.add_function_tested("get_random_delay")
        try:
            from mode_0.utils.helpers import get_random_delay
            
            # Test with default parameters
            delay = get_random_delay()
            self.assertTrue(1 <= delay <= 3)
            
            # Test with custom parameters
            delay = get_random_delay(5, 10)
            self.assertTrue(5 <= delay <= 10)
            
            self.report.add_test_result("test_get_random_delay", "pass")
        except Exception as e:
            self.report.add_test_result("test_get_random_delay", "fail", e)
            raise
    
    def test_format_duration(self):
        """Test duration formatting"""
        self.report.add_function_tested("format_duration")
        try:
            from mode_0.utils.helpers import format_duration
            
            # Test various durations
            test_cases = [
                (30, "30 seconds"),
                (60, "1 minute"),
                (120, "2 minutes"),
                (3600, "1 hour"),
                (7200, "2 hours"),
                (86400, "1 day"),
                (172800, "2 days")
            ]
            
            for seconds, expected in test_cases:
                self.assertEqual(format_duration(seconds), expected)
            
            self.report.add_test_result("test_format_duration", "pass")
        except Exception as e:
            self.report.add_test_result("test_format_duration", "fail", e)
            raise
    
    def test_calculate_time_since(self):
        """Test time since calculation"""
        self.report.add_function_tested("calculate_time_since")
        try:
            from mode_0.utils.helpers import calculate_time_since
            from datetime import datetime, timedelta
            
            now = datetime.now()
            
            # Test various time differences
            test_cases = [
                (now - timedelta(seconds=30), "just now"),
                (now - timedelta(minutes=5), "5 minutes ago"),
                (now - timedelta(hours=2), "2 hours ago"),
                (now - timedelta(days=3), "3 days ago"),
                (now - timedelta(days=14), "2 weeks ago"),
                (now - timedelta(days=60), "2 months ago")
            ]
            
            for timestamp, expected in test_cases:
                result = calculate_time_since(timestamp)
                self.assertEqual(result, expected)
            
            # Test with ISO format string
            result = calculate_time_since((now - timedelta(minutes=10)).isoformat())
            self.assertEqual(result, "10 minutes ago")
            
            self.report.add_test_result("test_calculate_time_since", "pass")
        except Exception as e:
            self.report.add_test_result("test_calculate_time_since", "fail", e)
            raise

# Test case for logger
class TestLogger(Mode0TestCase):
    """Test the logging system"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("Logger")
    
    @patch("mode_0.utils.logger.os")
    @patch("mode_0.utils.logger.logging")
    @patch("mode_0.utils.logger.colorlog")
    def test_setup_logger(self, mock_colorlog, mock_logging, mock_os):
        """Test logger setup"""
        self.report.add_function_tested("setup_logger")
        try:
            # Configure mocks
            mock_logger = MagicMock()
            mock_logging.getLogger.return_value = mock_logger
            mock_console_handler = MagicMock()
            mock_colorlog.StreamHandler.return_value = mock_console_handler
            mock_file_handler = MagicMock()
            mock_logging.FileHandler.return_value = mock_file_handler
            
            # Test
            from mode_0.utils.logger import setup_logger
            logger = setup_logger()
            
            # Verify
            mock_os.makedirs.assert_called_with("logs", exist_ok=True)
            mock_logging.getLogger.assert_called_with("mode_0")
            mock_logger.setLevel.assert_called_once()
            mock_logger.addHandler.assert_any_call(mock_console_handler)
            mock_logger.addHandler.assert_any_call(mock_file_handler)
            
            self.report.add_test_result("test_setup_logger", "pass")
        except Exception as e:
            self.report.add_test_result("test_setup_logger", "fail", e)
            raise

# Test case for bot commands
class TestCommands(Mode0TestCase):
    """Test bot commands"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("Commands")
        
        # Mock bot and context
        self.mock_bot = MagicMock()
        self.mock_ctx = MagicMock()
        self.mock_ctx.author.name = "testuser"
        self.mock_ctx.send = AsyncMock()
    
    def test_basic_commands(self):
        """Test basic bot commands"""
        self.report.add_function_tested("help_command")
        self.report.add_function_tested("about_command")
        self.report.add_function_tested("socials_command")
        try:
            from mode_0.core.commands import BasicCommands
            
            # Initialize commands
            commands = BasicCommands(self.mock_bot)
            
            # Test help command
            self.run_async(commands.help_command(self.mock_ctx))
            self.mock_ctx.send.assert_called_with(f"@{self.mock_ctx.author.name} Available commands: !help, !about, !socials")
            
            # Reset mock
            self.mock_ctx.send.reset_mock()
            
            # Test about command
            self.run_async(commands.about_command(self.mock_ctx))
            self.mock_ctx.send.assert_called_with(f"@{self.mock_ctx.author.name} I'm Mode_0, a custom bot for DJ Qwazi905's channel!")
            
            # Reset mock
            self.mock_ctx.send.reset_mock()
            
            # Test socials command
            self.run_async(commands.socials_command(self.mock_ctx))
            self.mock_ctx.send.assert_called_with(f"@{self.mock_ctx.author.name} Follow DJ Qwazi905 on: Twitch: twitch.tv/Qwazi905 | Twitter: x.com/Qwazi905 | SoundCloud: soundcloud.com/qwaziqwazi905")
            
            self.report.add_test_result("test_basic_commands", "pass")
        except Exception as e:
            self.report.add_test_result("test_basic_commands", "fail", e)
            raise
    
    def test_admin_commands(self):
        """Test admin commands"""
        self.report.add_function_tested("mode_command")
        self.report.add_function_tested("_is_admin")
        try:
            from mode_0.core.commands import AdminCommands
            
            # Initialize commands with mock bot
            commands = AdminCommands(self.mock_bot)
            
            # Mock the _is_admin method
            commands._is_admin = AsyncMock(return_value=True)
            
            # Mock persona.get_current_mode
            self.mock_bot.persona.get_current_mode.return_value = "normal"
            
            # Test botmode command without args (get current mode)
            self.run_async(commands.mode_command(self.mock_ctx))
            self.mock_ctx.send.assert_called_with(f"@{self.mock_ctx.author.name} Current bot mode: normal")
            
            # Reset mock
            self.mock_ctx.send.reset_mock()
            
            # Test botmode command with args (set mode)
            self.run_async(commands.mode_command(self.mock_ctx, "party"))
            self.mock_ctx.send.assert_called_with(f"@{self.mock_ctx.author.name} Bot mode changed to: party")
            
            # Test non-admin case
            commands._is_admin = AsyncMock(return_value=False)
            self.mock_ctx.send.reset_mock()
            
            self.run_async(commands.mode_command(self.mock_ctx, "party"))
            self.mock_ctx.send.assert_not_called()
            
            self.report.add_test_result("test_admin_commands", "pass")
            self.report.add_issue("_is_admin method is a placeholder that always returns False")
        except Exception as e:
            self.report.add_test_result("test_admin_commands", "fail", e)
            raise

# Test case for core bot
class TestBot(Mode0TestCase):
    """Test the core bot functionality"""
    
    def setUp(self):
        super().setUp()
        self.report.start_module("Bot")
        
        # Create patches
        self.patches = [
            patch("mode_0.core.bot.commands.Bot.__init__", return_value=None),
            patch("mode_0.core.bot.setup_logger"),
            patch("mode_0.core.bot.ConfigManager"),
            patch("mode_0.core.bot.DatabaseManager"),
            patch("mode_0.core.bot.PersonaSystem"),
            patch("mode_0.core.bot.StreamElementsManager"),
            patch("mode_0.core.bot.asyncio.Queue")
        ]
        
        # Start all patches
        for p in self.patches:
            p.start()
    
    def tearDown(self):
        # Stop all patches
        for p in self.patches:
            p.stop()
    
    def test_initialization(self):
        """Test bot initialization"""
        self.report.add_function_tested("__init__")
        try:
            from mode_0.core.bot import Mode0Bot
            
            # Create bot instance
            bot = Mode0Bot()
            
            # Check that the bot was initialized properly
            from mode_0.core.bot import setup_logger
            from mode_0.core.bot import ConfigManager
            from mode_0.core.bot import DatabaseManager
            from mode_0.core.bot import PersonaSystem
            from mode_0.core.bot import StreamElementsManager
            
            setup_logger.assert_called_once()
            ConfigManager.assert_called_once()
            DatabaseManager.assert_called_once()
            PersonaSystem.assert_called_once()
            StreamElementsManager.assert_called_once()
            
            self.report.add_test_result("test_initialization", "pass")
        except Exception as e:
            self.report.add_test_result("test_initialization", "fail", e)
            raise
    
    @patch("mode_0.core.bot.Mode0Bot.handle_commands")
    def test_event_message(self, mock_handle_commands):
        """Test message event handling"""
        self.report.add_function_tested("event_message")
        try:
            from mode_0.core.bot import Mode0Bot
            
            # Create bot instance with mock queue
            bot = Mode0Bot()
            bot.nick = "testbot"
            bot.message_queue = AsyncMock()
            bot.message_queue.put = AsyncMock()
            mock_handle_commands.side_effect = AsyncMock()
            
            # Test message from another user
            mock_message = MagicMock()
            mock_message.author = MagicMock()
            mock_message.author.name = "testuser"
            
            self.run_async(bot.event_message(mock_message))
            
            # Should process commands and queue message
            mock_handle_commands.assert_called_once_with(mock_message)
            bot.message_queue.put.assert_called_once_with(mock_message)
            
            # Reset mocks
            mock_handle_commands.reset_mock()
            bot.message_queue.put.reset_mock()
            
            # Test message from bot itself
            mock_message = MagicMock()
            mock_message.author = MagicMock()
            mock_message.author.name = "testbot"
            
            self.run_async(bot.event_message(mock_message))
            
            # Should ignore bot's own messages
            mock_handle_commands.assert_not_called()
            bot.message_queue.put.assert_not_called()
            
            self.report.add_test_result("test_event_message", "pass")
        except Exception as e:
            self.report.add_test_result("test_event_message", "fail", e)
            raise
    
    def test_event_ready(self):
        """Test ready event handling"""
        self.report.add_function_tested("event_ready")
        try:
            from mode_0.core.bot import Mode0Bot
            
            # Create bot instance
            bot = Mode0Bot()
            bot.nick = "testbot"
            bot.initial_channels = ["channel1", "channel2"]
            bot.se_manager = MagicMock()
            bot.se_manager.connect = AsyncMock()
            
            self.run_async(bot.event_ready())
            
            # Should connect to StreamElements
            bot.se_manager.connect.assert_called_once()
            
            self.report.add_test_result("test_event_ready", "pass")
        except Exception as e:
            self.report.add_test_result("test_event_ready", "fail", e)
            raise
    
    def test_process_message_queue(self):
        """Test message queue processing"""
        self.report.add_function_tested("_process_message_queue")
        try:
            from mode_0.core.bot import Mode0Bot
            
            # Create bot instance with mock queue
            bot = Mode0Bot()
            
            # Create async mock queue
            queue_items = [MagicMock() for _ in range(3)]
            
            # Configure mock queue behavior
            async def mock_get():
                if queue_items:
                    return queue_items.pop(0)
                else:
                    # Raise exception to stop the infinite loop
                    raise Exception("Empty queue")
            
            bot.message_queue = MagicMock()
            bot.message_queue.get = AsyncMock(side_effect=mock_get)
            bot.message_queue.task_done = MagicMock()
            
            # Test process_message_queue
            with self.assertRaises(Exception):
                self.run_async(bot._process_message_queue())
            
            # Should call task_done for each item
            self.assertEqual(bot.message_queue.task_done.call_count, 3)
            
            self.report.add_test_result("test_process_message_queue", "pass")
            self.report.add_issue("_process_message_queue has placeholder implementation")
        except Exception as e:
            self.report.add_test_result("test_process_message_queue", "fail", e)
            raise
    
    def test_idle_chat_initiator(self):
        """Test idle chat initiator"""
        self.report.add_function_tested("_idle_chat_initiator")
        try:
            from mode_0.core.bot import Mode0Bot
            
            # Create bot instance
            bot = Mode0Bot()
            
            # Test short run of idle_chat_initiator (will be a placeholder)
            # We'll use a mock to generate an exception to break out of the infinite loop
            bot.config.get = MagicMock(side_effect=Exception("Test exit"))
            
            with self.assertRaises(Exception):
                self.run_async(bot._idle_chat_initiator())
            
            self.report.add_test_result("test_idle_chat_initiator", "pass")
            self.report.add_issue("_idle_chat_initiator has placeholder implementation")
        except Exception as e:
            self.report.add_test_result("test_idle_chat_initiator", "fail", e)
            raise

# Main test runner
def run_tests():
    """Run all test cases and generate report"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestConfigManager,
        TestDatabaseManager,
        TestPersonaSystem,
        TestUserProfiler,
        TestStreamElementsManager,
        TestStreamElementsEvents,
        TestHelpers,
        TestLogger,
        TestCommands,
        TestBot
    ]
    
    # Check if mode_0 module is importable before running tests
    try:
        importlib.import_module('mode_0')
        print("Successfully imported mode_0 module")
    except ImportError as e:
        print(f"\nERROR: Cannot import 'mode_0' module: {e}")
        print(f"Module search path: {sys.path}")
        print(f"Current directory: {os.getcwd()}")
        print("\nPlease ensure the Mode_0 directory is correctly located and accessible.")
        return f"Import error: {str(e)}"
    
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        test_suite.addTests(tests)
    
    # Run tests with custom test runner that suppresses output
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        unittest.TextTestRunner(verbosity=0).run(test_suite)
    
    # Generate report
    return test_report.generate_report()

# Set up global test report
test_report = TestReport()

if __name__ == "__main__":
    # Print header
    print("=" * 80)
    print("MODE_0 BOT TEST SUITE")
    print("=" * 80)
    print("Running comprehensive tests...")
    
    # Run tests and generate report
    report = run_tests()
    
    # Print report
    print("\n" + report)
    
    # Write report to file
    report_path = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nTest report saved to: {report_path}")
