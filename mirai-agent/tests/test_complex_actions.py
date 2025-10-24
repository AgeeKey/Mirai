#!/usr/bin/env python3
"""
🧪 Tests for Section 3: Complex Actions (Browser & File System)
Comprehensive tests for steps 71-110
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.action_execution import (
    # Browser Actions
    URLNavigator,
    PageLoadWaiter,
    FormInteractor,
    FormSubmitter,
    LinkClicker,
    NewTabHandler,
    JavaScriptPopupHandler,
    AuthenticationHandler,
    ElementSelector,
    AJAXHandler,
    
    # File System Actions
    FileOpener,
    FileSaver,
    FileDeleter,
    FileMover,
    FileCopier,
    DirectoryLister,
    DirectoryCreator,
    CapCutVideoImporter,
    CapCutVideoEditor,
    CapCutVideoExporter,
    VSCodeFileOpener,
    VSCodeCodeEditor,
    VSCodeCodeRunner,
    ChromeProfileSelector,
    AppActionDispatcher,
)


def test_url_navigator():
    """Test 1: URL Navigation - Шаг 71"""
    print("\n🧪 TEST 1: URL Navigator")
    print("="*60)
    
    navigator = URLNavigator()
    assert navigator is not None
    
    # Test navigation
    success = navigator.navigate("https://example.com")
    assert success
    assert navigator.get_current_url() == "https://example.com"
    
    print("✅ URL navigation работает")
    return True


def test_form_interaction():
    """Test 2: Form Interaction - Шаги 75-77"""
    print("\n🧪 TEST 2: Form Interaction")
    print("="*60)
    
    # Test form filling
    form = FormInteractor()
    fields = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'secret123'
    }
    
    success = form.fill_form(fields)
    assert success
    
    # Test dropdown
    success = form.select_dropdown('country', 'USA')
    assert success
    
    # Test checkbox
    success = form.check_checkbox('terms', True)
    assert success
    
    # Test form submission
    submitter = FormSubmitter()
    success = submitter.submit()
    assert success
    
    print("✅ Form interaction работает")
    return True


def test_javascript_popups():
    """Test 3: JavaScript Popup Handling - Шаг 80"""
    print("\n🧪 TEST 3: JavaScript Popups")
    print("="*60)
    
    handler = JavaScriptPopupHandler()
    
    # Test alert
    success = handler.handle_alert(accept=True)
    assert success
    
    # Test confirm
    success = handler.handle_confirm(accept=True)
    assert success
    
    # Test prompt
    success = handler.handle_prompt("test input", accept=True)
    assert success
    
    print("✅ JavaScript popup handling работает")
    return True


def test_new_tab_handling():
    """Test 4: New Tab Handling - Шаг 79"""
    print("\n🧪 TEST 4: New Tab Handling")
    print("="*60)
    
    handler = NewTabHandler()
    
    # Test tab detection
    success = handler.detect_new_tab()
    assert success
    
    # Test tab switching
    success = handler.switch_to_tab(1)
    assert success
    assert handler.current_tab == 1
    
    # Test tab closing
    success = handler.close_tab(1)
    assert success
    
    print("✅ Tab handling работает")
    return True


def test_authentication():
    """Test 5: Authentication - Шаг 90"""
    print("\n🧪 TEST 5: Authentication")
    print("="*60)
    
    auth = AuthenticationHandler()
    
    # Test login
    success = auth.login("user123", "password")
    assert success
    
    # Test auth check
    is_authenticated = auth.check_authenticated()
    assert isinstance(is_authenticated, bool)
    
    # Test logout
    success = auth.logout()
    assert success
    
    print("✅ Authentication работает")
    return True


def test_file_operations():
    """Test 6: File Operations - Шаги 91-97"""
    print("\n🧪 TEST 6: File Operations")
    print("="*60)
    
    # Test file opening
    opener = FileOpener()
    success = opener.open_file("/path/to/file.txt")
    assert success
    
    # Test file saving
    saver = FileSaver()
    success = saver.save_file("/path/to/output.txt")
    assert success
    
    # Test file deletion
    deleter = FileDeleter()
    success = deleter.delete_file("/path/to/temp.txt", to_trash=True)
    assert success
    
    # Test file moving
    mover = FileMover()
    success = mover.move_file("/path/from.txt", "/path/to.txt")
    assert success
    
    # Test file copying
    copier = FileCopier()
    success = copier.copy_file("/path/source.txt", "/path/dest.txt")
    assert success
    
    print("✅ File operations работают")
    return True


def test_directory_operations():
    """Test 7: Directory Operations - Шаги 98-100"""
    print("\n🧪 TEST 7: Directory Operations")
    print("="*60)
    
    # Test directory listing
    lister = DirectoryLister()
    files = lister.list_files("/path/to/dir")
    assert isinstance(files, list)
    
    # Test directory creation
    creator = DirectoryCreator()
    success = creator.create_directory("/path/to/new_folder")
    assert success
    
    print("✅ Directory operations работают")
    return True


def test_capcut_actions():
    """Test 8: CapCut Actions - Шаги 101-103"""
    print("\n🧪 TEST 8: CapCut Video Editing")
    print("="*60)
    
    # Test video import
    importer = CapCutVideoImporter()
    success = importer.import_video("video.mp4")
    assert success
    
    # Test video editing
    editor = CapCutVideoEditor()
    success = editor.cut_video(0, 10)
    assert success
    
    success = editor.add_effect("blur")
    assert success
    
    success = editor.add_transition("fade")
    assert success
    
    # Test video export
    exporter = CapCutVideoExporter()
    success = exporter.export_video("output.mp4", quality="1080p")
    assert success
    
    print("✅ CapCut operations работают")
    return True


def test_vscode_actions():
    """Test 9: VSCode Actions - Шаги 104-106"""
    print("\n🧪 TEST 9: VSCode Integration")
    print("="*60)
    
    # Test file opening
    opener = VSCodeFileOpener()
    success = opener.open_file("main.py")
    assert success
    
    success = opener.open_folder("/project")
    assert success
    
    # Test code editing
    editor = VSCodeCodeEditor()
    success = editor.insert_text(10, "print('Hello')")
    assert success
    
    success = editor.format_document()
    assert success
    
    # Test code running
    runner = VSCodeCodeRunner()
    success = runner.run_code("python")
    assert success
    
    success = runner.debug_code()
    assert success
    
    print("✅ VSCode operations работают")
    return True


def test_chrome_actions():
    """Test 10: Chrome Actions - Шаги 107-108"""
    print("\n🧪 TEST 10: Chrome Integration")
    print("="*60)
    
    # Test profile selection
    profile_selector = ChromeProfileSelector()
    success = profile_selector.select_profile("Work")
    assert success
    
    print("✅ Chrome operations работают")
    return True


def test_app_dispatcher():
    """Test 11: App Action Dispatcher - Шаг 110"""
    print("\n🧪 TEST 11: App Action Dispatcher")
    print("="*60)
    
    dispatcher = AppActionDispatcher()
    assert dispatcher is not None
    
    # Test dispatching to different apps
    success = dispatcher.dispatch("capcut", "import", video="test.mp4")
    assert success
    
    success = dispatcher.dispatch("vscode", "run", language="python")
    assert success
    
    success = dispatcher.dispatch("chrome", "profile", name="Work")
    assert success
    
    print("✅ App dispatcher работает")
    return True


def test_ajax_and_dynamic_content():
    """Test 12: AJAX and Dynamic Content - Шаги 86-89"""
    print("\n🧪 TEST 12: AJAX and Dynamic Content")
    print("="*60)
    
    # Test AJAX handling
    ajax_handler = AJAXHandler()
    success = ajax_handler.wait_for_ajax(timeout=10)
    assert success
    
    # Test element selection
    selector = ElementSelector()
    elements = selector.find_by_css(".button")
    assert isinstance(elements, list)
    
    elements = selector.find_by_text("Submit")
    assert isinstance(elements, list)
    
    print("✅ AJAX and dynamic content handling работает")
    return True


def run_all_tests():
    """Запустить все тесты Section 3"""
    print("\n" + "="*70)
    print("🚀 SECTION 3: COMPLEX ACTIONS - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {}
    
    tests = [
        ("URL Navigator", test_url_navigator),
        ("Form Interaction", test_form_interaction),
        ("JavaScript Popups", test_javascript_popups),
        ("New Tab Handling", test_new_tab_handling),
        ("Authentication", test_authentication),
        ("File Operations", test_file_operations),
        ("Directory Operations", test_directory_operations),
        ("CapCut Actions", test_capcut_actions),
        ("VSCode Actions", test_vscode_actions),
        ("Chrome Actions", test_chrome_actions),
        ("App Dispatcher", test_app_dispatcher),
        ("AJAX & Dynamic Content", test_ajax_and_dynamic_content),
    ]
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Итоги
    print("\n" + "="*70)
    print("📊 TEST SUMMARY - SECTION 3")
    print("="*70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*70)
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"Results: {passed}/{total} tests passed ({success_rate:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL SECTION 3 TESTS PASSED!")
        print("✅ Browser Automation - Complete")
        print("✅ File System Operations - Complete")
        print("✅ Application-Specific Actions - Complete")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
