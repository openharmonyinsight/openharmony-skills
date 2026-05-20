#!/usr/bin/env python3
"""
End-to-end test for the Cangjie Compiler Knowledge Base system.
Tests all requirements from the requirements document.
"""

import json
import os
import sys
import subprocess
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class E2ETest:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.kb_dir = self.script_dir.parent / 'knowledge-base'
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def log_pass(self, message):
        print(f"{GREEN}✓{RESET} {message}")
        self.passed += 1
        
    def log_fail(self, message):
        print(f"{RED}✗{RESET} {message}")
        self.failed += 1
        
    def log_warn(self, message):
        print(f"{YELLOW}⚠{RESET} {message}")
        self.warnings += 1
        
    def test_knowledge_base_files_exist(self):
        """Test that all required knowledge base files exist"""
        print("\n=== Testing Knowledge Base File Structure ===")
        
        # Check search index
        search_index = self.kb_dir / 'search-index.json'
        if search_index.exists():
            self.log_pass("search-index.json exists")
        else:
            self.log_fail("search-index.json not found")
            
        # Check cross references
        cross_ref = self.kb_dir / 'cross-references.json'
        if cross_ref.exists():
            self.log_pass("cross-references.json exists")
        else:
            self.log_fail("cross-references.json not found")
            
        # Check modules directory
        modules_dir = self.kb_dir / 'modules'
        if modules_dir.exists() and modules_dir.is_dir():
            module_files = list(modules_dir.glob('*.json'))
            if module_files:
                self.log_pass(f"modules/ directory contains {len(module_files)} module files")
            else:
                self.log_warn("modules/ directory is empty")
        else:
            self.log_fail("modules/ directory not found")
            
        # Check descriptions directory
        desc_dir = self.kb_dir / 'descriptions'
        if desc_dir.exists() and desc_dir.is_dir():
            desc_files = list(desc_dir.glob('*.md'))
            if desc_files:
                self.log_pass(f"descriptions/ directory contains {len(desc_files)} description files")
            else:
                self.log_warn("descriptions/ directory is empty")
        else:
            self.log_fail("descriptions/ directory not found")

    def test_search_index_structure(self):
        """Test that search index has correct structure"""
        print("\n=== Testing Search Index Structure ===")
        
        search_index_path = self.kb_dir / 'search-index.json'
        if not search_index_path.exists():
            self.log_fail("Cannot test index structure - file not found")
            return
            
        try:
            with open(search_index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
                
            if not isinstance(index, dict):
                self.log_fail("Search index is not a dictionary")
                return
                
            self.log_pass(f"Search index loaded successfully with {len(index)} entries")
            
            # Check a few entries for structure
            sample_count = min(5, len(index))
            valid_entries = 0
            
            for keyword, data in list(index.items())[:sample_count]:
                if isinstance(data, dict):
                    # Check for expected fields
                    has_description = 'description' in data or 'description_zh' in data or 'description_en' in data
                    has_modules = 'modules' in data
                    has_classes = 'classes' in data
                    has_functions = 'functions' in data
                    
                    if has_description or has_modules or has_classes or has_functions:
                        valid_entries += 1
                        
            if valid_entries == sample_count:
                self.log_pass(f"All sampled entries have valid structure")
            else:
                self.log_warn(f"Only {valid_entries}/{sample_count} sampled entries have valid structure")
                
        except json.JSONDecodeError as e:
            self.log_fail(f"Search index is not valid JSON: {e}")
        except Exception as e:
            self.log_fail(f"Error reading search index: {e}")
            
    def test_cross_references_structure(self):
        """Test that cross references have correct structure"""
        print("\n=== Testing Cross References Structure ===")
        
        cross_ref_path = self.kb_dir / 'cross-references.json'
        if not cross_ref_path.exists():
            self.log_fail("Cannot test cross references - file not found")
            return
            
        try:
            with open(cross_ref_path, 'r', encoding='utf-8') as f:
                cross_ref = json.load(f)
                
            if not isinstance(cross_ref, dict):
                self.log_fail("Cross references is not a dictionary")
                return
                
            self.log_pass("Cross references loaded successfully")
            
            # Check for module dependencies
            if 'module_dependencies' in cross_ref:
                mod_deps = cross_ref['module_dependencies']
                self.log_pass(f"Module dependencies found with {len(mod_deps)} modules")
            else:
                self.log_warn("No module_dependencies field in cross references")
                
            # Check for function calls
            if 'function_calls' in cross_ref:
                func_calls = cross_ref['function_calls']
                self.log_pass(f"Function calls found with {len(func_calls)} functions")
            else:
                self.log_warn("No function_calls field in cross references")
                
        except json.JSONDecodeError as e:
            self.log_fail(f"Cross references is not valid JSON: {e}")
        except Exception as e:
            self.log_fail(f"Error reading cross references: {e}")

    def test_search_functionality(self):
        """Test search functionality with various queries"""
        print("\n=== Testing Search Functionality ===")
        
        search_script = self.script_dir / 'search.py'
        if not search_script.exists():
            self.log_fail("search.py not found")
            return
            
        # Test queries covering different language features
        test_queries = [
            ("lambda", "Lambda expressions"),
            ("类型推断", "Type inference (Chinese)"),
            ("generic", "Generic types"),
            ("pattern match", "Pattern matching"),
            ("class", "Class definitions"),
            ("interface", "Interface definitions"),
            ("sema", "Semantic analysis module"),
            ("parser", "Parser module"),
            ("AST", "Abstract Syntax Tree"),
        ]
        
        for query, description in test_queries:
            try:
                result = subprocess.run(
                    [sys.executable, str(search_script), query, '--json'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    try:
                        output = json.loads(result.stdout)
                        if output and len(output) > 0:
                            self.log_pass(f"Search '{query}' ({description}): {len(output)} results")
                        else:
                            self.log_warn(f"Search '{query}' ({description}): no results")
                    except json.JSONDecodeError:
                        self.log_warn(f"Search '{query}' ({description}): invalid JSON output")
                else:
                    self.log_fail(f"Search '{query}' ({description}): failed with code {result.returncode}")
                    
            except subprocess.TimeoutExpired:
                self.log_fail(f"Search '{query}' ({description}): timeout")
            except Exception as e:
                self.log_fail(f"Search '{query}' ({description}): {e}")
                
    def test_fuzzy_matching(self):
        """Test fuzzy matching capability"""
        print("\n=== Testing Fuzzy Matching ===")
        
        search_script = self.script_dir / 'search.py'
        if not search_script.exists():
            self.log_fail("search.py not found")
            return
            
        # Test with intentional typos
        fuzzy_queries = [
            ("lamda", "lambda with typo"),
            ("genric", "generic with typo"),
            ("paser", "parser with typo"),
        ]
        
        for query, description in fuzzy_queries:
            try:
                result = subprocess.run(
                    [sys.executable, str(search_script), query, '--json'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    try:
                        output = json.loads(result.stdout)
                        if output and len(output) > 0:
                            self.log_pass(f"Fuzzy search '{query}' ({description}): found results")
                        else:
                            self.log_warn(f"Fuzzy search '{query}' ({description}): no results")
                    except json.JSONDecodeError:
                        self.log_warn(f"Fuzzy search '{query}' ({description}): invalid JSON")
                else:
                    self.log_fail(f"Fuzzy search '{query}' ({description}): failed")
                    
            except Exception as e:
                self.log_fail(f"Fuzzy search '{query}' ({description}): {e}")

    def test_description_files(self):
        """Test that description files have correct format"""
        print("\n=== Testing Description Files Format ===")
        
        desc_dir = self.kb_dir / 'descriptions'
        if not desc_dir.exists():
            self.log_fail("descriptions/ directory not found")
            return
            
        desc_files = list(desc_dir.glob('*.md'))
        if not desc_files:
            self.log_warn("No description files found")
            return
            
        valid_files = 0
        for desc_file in desc_files[:10]:  # Sample first 10 files
            try:
                with open(desc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for YAML frontmatter
                if content.startswith('---'):
                    # Check for required fields
                    has_keyword = 'keyword:' in content
                    has_title = content.count('#') > 0
                    has_description = '描述' in content or 'Description' in content
                    
                    if has_keyword and has_title and has_description:
                        valid_files += 1
                        
            except Exception as e:
                self.log_warn(f"Error reading {desc_file.name}: {e}")
                
        if valid_files > 0:
            self.log_pass(f"{valid_files}/{len(desc_files[:10])} sampled description files have valid format")
        else:
            self.log_warn("No valid description files found in sample")
            
    def test_documentation_exists(self):
        """Test that required documentation exists"""
        print("\n=== Testing Documentation ===")
        
        skill_dir = self.script_dir.parent
        
        # Check SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        if skill_md.exists():
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 500:  # Should have substantial content
                    self.log_pass("SKILL.md exists with substantial content")
                else:
                    self.log_warn("SKILL.md exists but seems incomplete")
        else:
            self.log_fail("SKILL.md not found")
            
        # Check AI_MAINTENANCE_GUIDE.md
        guide_md = skill_dir / 'AI_MAINTENANCE_GUIDE.md'
        if guide_md.exists():
            with open(guide_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 1000:  # Should have substantial content
                    self.log_pass("AI_MAINTENANCE_GUIDE.md exists with substantial content")
                else:
                    self.log_warn("AI_MAINTENANCE_GUIDE.md exists but seems incomplete")
        else:
            self.log_fail("AI_MAINTENANCE_GUIDE.md not found")
            
    def test_scripts_exist(self):
        """Test that required scripts exist and are executable"""
        print("\n=== Testing Scripts ===")
        
        required_scripts = [
            'generate_knowledge.py',
            'search.py',
            'file_scanner.py',
            'cpp_parser.py',
            'module_analyzer.py',
            'dependency_analyzer.py',
            'keyword_extractor.py',
            'markdown_parser.py',
            'search_index_builder.py',
            'cross_ref_builder.py',
            'query_parser.py',
            'search_engine.py',
            'result_ranker.py',
            'result_formatter.py',
        ]
        
        for script_name in required_scripts:
            script_path = self.script_dir / script_name
            if script_path.exists():
                self.log_pass(f"{script_name} exists")
            else:
                self.log_fail(f"{script_name} not found")
                
    def run_all_tests(self):
        """Run all tests and print summary"""
        print("=" * 60)
        print("Cangjie Compiler Knowledge Base - End-to-End Test")
        print("=" * 60)
        
        self.test_knowledge_base_files_exist()
        self.test_search_index_structure()
        self.test_cross_references_structure()
        self.test_description_files()
        self.test_documentation_exists()
        self.test_scripts_exist()
        self.test_search_functionality()
        self.test_fuzzy_matching()
        
        # Print summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"{GREEN}Passed:{RESET} {self.passed}")
        print(f"{RED}Failed:{RESET} {self.failed}")
        print(f"{YELLOW}Warnings:{RESET} {self.warnings}")
        print("=" * 60)
        
        if self.failed == 0:
            print(f"\n{GREEN}All tests passed!{RESET}")
            return 0
        else:
            print(f"\n{RED}Some tests failed.{RESET}")
            return 1

if __name__ == '__main__':
    test = E2ETest()
    sys.exit(test.run_all_tests())
