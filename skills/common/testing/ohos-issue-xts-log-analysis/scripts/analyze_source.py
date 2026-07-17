#!/usr/bin/env python3
"""
源码解析脚本 - 提取API到Domain链路

功能：
1. 解析 .ets 源码文件，提取 import 语句（@kit.X 和 @ohos.Y 语法）
2. 定位 it() 测试用例块
3. 提取失败断言行位置
4. 查询数据库获取 kit/module/subsystem/domain 映射
5. 输出 JSON 格式结果

用法：
    python3 analyze_source.py <file.ets>
    python3 analyze_source.py <directory>
    python3 analyze_source.py <file.ets> --format json
    python3 analyze_source.py <directory> --format summary
"""

import re
import os
import sys
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple


DB_PATH = os.path.join(os.path.dirname(__file__), '../data/xts_rules.db')

# 复用 map_domain 的固化映射（最稳定，字段名不可能脱节）
# analyze_source 的 domain 解析全部委托 map_domain，不再直接查 db
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from map_domain import map_sut, expand_kit
except ImportError:
    map_sut = None
    expand_kit = None


@dataclass
class ImportInfo:
    """import 语句信息"""
    raw_statement: str
    module_path: str
    import_type: str
    imported_names: List[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class TestCaseInfo:
    """测试用例信息"""
    name: str
    start_line: int
    end_line: int
    description: str = ""
    test_type: str = ""


@dataclass
class AssertLocation:
    """断言位置信息"""
    line_number: int
    column: int = 0
    assert_type: str = ""
    content: str = ""


@dataclass
class ApiDomainChain:
    """API到Domain链路"""
    api: str
    kit: str = ""
    module: str = ""
    subsystem: str = ""
    domain_hex: str = ""
    import_line: int = 0
    test_cases: List[str] = field(default_factory=list)
    assert_locations: List[Dict] = field(default_factory=list)


class ImportParser:
    """import 语句解析器
    
    支持三种 import 语法：
    1. named import: import { X, Y } from '@kit.Module' 或 '@ohos.module'
    2. default import: import name from '@ohos.module'
    3. legacy import: import * as name from '@ohos.module' 或 import name from '@ohos.module'
    """
    
    # named import: import { A, B } from 'module'
    NAMED_PATTERN = re.compile(
        r'import\s+\{\s*([^}]+)\s*\}\s+from\s+[\'"]([^\'"]+)[\'"]'
    )
    
    # default import: import Name from 'module'
    DEFAULT_PATTERN = re.compile(
        r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
    )
    
    # legacy import: import * as Name from 'module'
    LEGACY_PATTERN = re.compile(
        r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
    )
    
    # namespace import: import '@kit.Module'
    NAMESPACE_PATTERN = re.compile(
        r'import\s+[\'"]([^\'"]+)[\'"]'
    )
    
    # @kit 语法匹配
    KIT_PATTERN = re.compile(r'@kit\.(\w+)')
    
    # @ohos 语法匹配
    OHOS_PATTERN = re.compile(r'@ohos\.([\w.]+)')
    
    @classmethod
    def parse_line(cls, line: str, line_number: int = 0) -> Optional[ImportInfo]:
        """解析单行 import 语句
        
        Args:
            line: 源码行
            line_number: 行号
            
        Returns:
            ImportInfo 或 None
        """
        line = line.strip()
        
        # 跳过注释
        if line.startswith('//') or line.startswith('/*'):
            return None
        
        # 尝试匹配各种 import 模式
        # 1. named import: import { X, Y } from 'module'
        match = cls.NAMED_PATTERN.search(line)
        if match:
            names_str, module_path = match.groups()
            names = [n.strip() for n in names_str.split(',')]
            import_type = cls._get_import_type(module_path)
            return ImportInfo(
                raw_statement=line,
                module_path=module_path,
                import_type=import_type,
                imported_names=names,
                line_number=line_number
            )
        
        # 2. legacy import: import * as Name from 'module'
        match = cls.LEGACY_PATTERN.search(line)
        if match:
            name, module_path = match.groups()
            import_type = cls._get_import_type(module_path)
            return ImportInfo(
                raw_statement=line,
                module_path=module_path,
                import_type=import_type,
                imported_names=[f'*:{name}'],
                line_number=line_number
            )
        
        # 3. default import: import Name from 'module'
        match = cls.DEFAULT_PATTERN.search(line)
        if match:
            name, module_path = match.groups()
            import_type = cls._get_import_type(module_path)
            return ImportInfo(
                raw_statement=line,
                module_path=module_path,
                import_type=import_type,
                imported_names=[name],
                line_number=line_number
            )
        
        # 4. namespace import: import 'module'
        match = cls.NAMESPACE_PATTERN.search(line)
        if match:
            module_path = match.group(1)
            import_type = cls._get_import_type(module_path)
            return ImportInfo(
                raw_statement=line,
                module_path=module_path,
                import_type=import_type,
                imported_names=[],
                line_number=line_number
            )
        
        return None
    
    @classmethod
    def _get_import_type(cls, module_path: str) -> str:
        """获取 import 类型
        
        Args:
            module_path: 模块路径
            
        Returns:
            'kit' | 'ohos' | 'other'
        """
        if cls.KIT_PATTERN.search(module_path):
            return 'kit'
        elif cls.OHOS_PATTERN.search(module_path):
            return 'ohos'
        return 'other'
    
    @classmethod
    def extract_kit_module(cls, module_path: str) -> Tuple[Optional[str], Optional[str]]:
        """从模块路径提取 kit 和 module
        
        Args:
            module_path: 模块路径（如 '@kit.ArkUI' 或 '@ohos.hilog'）
            
        Returns:
            (kit, module) 元组
        """
        # @kit.X 语法
        kit_match = cls.KIT_PATTERN.search(module_path)
        if kit_match:
            kit = kit_match.group(1)
            return kit, None
        
        # @ohos.Y 语法
        ohos_match = cls.OHOS_PATTERN.search(module_path)
        if ohos_match:
            module = ohos_match.group(1)
            return None, module
        
        return None, None


class HypiumTestParser:
    """Hypium 测试框架解析器
    
    解析 it() 测试用例块和断言语句
    """
    
    # it() 函数匹配模式
    IT_PATTERN = re.compile(
        r'it\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*([^,]+)\s*,'
    )
    
    # describe() 块匹配
    DESCRIBE_PATTERN = re.compile(
        r'describe\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,'
    )
    
    # 断言匹配模式
    ASSERT_PATTERNS = [
        # expect().assertFail()
        re.compile(r'expect\s*\(\s*\)\s*\.\s*assertFail\s*\(\s*\)'),
        # expect(x).assertEqual(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertEqual\s*\([^)]*\)'),
        # expect(x).assertTrue()
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertTrue\s*\(\s*\)'),
        # expect(x).assertFalse()
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertFalse\s*\(\s*\)'),
        # expect(x).assertNull()
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertNull\s*\(\s*\)'),
        # expect(x).assertNotNull()
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertNotNull\s*\(\s*\)'),
        # expect(x).assertUndefined()
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertUndefined\s*\(\s*\)'),
        # expect(x).assertClose(y, z)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertClose\s*\([^)]*\)'),
        # expect(x).assertContain(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertContain\s*\([^)]*\)'),
        # expect(x).assertLarger(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertLarger\s*\([^)]*\)'),
        # expect(x).assertLess(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertLess\s*\([^)]*\)'),
        # expect(x).assertLargerOrEqual(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertLargerOrEqual\s*\([^)]*\)'),
        # expect(x).assertLessOrEqual(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertLessOrEqual\s*\([^)]*\)'),
        # expect(x).assertInstanceOf(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*assertInstanceOf\s*\([^)]*\)'),
        # expect(x).not().assertEqual(y)
        re.compile(r'expect\s*\([^)]*\)\s*\.\s*not\s*\(\s*\)\s*\.\s*assertEqual\s*\([^)]*\)'),
    ]
    
    # 失败断言模式（特别关注）
    FAIL_ASSERT_PATTERN = re.compile(r'expect\s*\(\s*\)\s*\.\s*assertFail\s*\(\s*\)')
    
    @classmethod
    def parse_file(cls, content: str) -> Tuple[List[TestCaseInfo], List[AssertLocation]]:
        """解析文件内容，提取测试用例和断言
        
        Args:
            content: 文件内容
            
        Returns:
            (测试用例列表, 断言位置列表)
        """
        lines = content.split('\n')
        test_cases = []
        assert_locations = []
        
        # 查找所有 it() 块
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 匹配 it() 开始
            match = cls.IT_PATTERN.search(line)
            if match:
                test_name = match.group(1)
                test_type = match.group(2).strip()
                
                # 查找 it() 块的结束（通过括号匹配）
                start_line = i + 1
                end_line = cls._find_block_end(lines, i)
                
                # 提取块内的断言
                block_content = '\n'.join(lines[i:end_line])
                block_asserts = cls._find_asserts_in_block(lines, i, end_line)
                
                test_cases.append(TestCaseInfo(
                    name=test_name,
                    start_line=start_line,
                    end_line=end_line,
                    description=f"Test type: {test_type}",
                    test_type=test_type
                ))
                
                assert_locations.extend(block_asserts)
                i = end_line
            else:
                i += 1
        
        return test_cases, assert_locations
    
    @classmethod
    def _find_block_end(cls, lines: List[str], start_idx: int) -> int:
        """查找代码块结束位置
        
        通过括号匹配确定 it() 回调函数的结束位置
        
        Args:
            lines: 所有行
            start_idx: it() 开始的行索引
            
        Returns:
            结束行号（1-indexed）
        """
        brace_count = 0
        paren_count = 0
        found_start = False
        
        for i in range(start_idx, len(lines)):
            line = lines[i]
            
            # 计算括号
            for char in line:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == '{':
                    brace_count += 1
                    found_start = True
                elif char == '}':
                    brace_count -= 1
            
            # 当括号都闭合时，找到结束
            if found_start and brace_count == 0 and paren_count <= 0:
                return i + 1
        
        return len(lines)
    
    @classmethod
    def _find_asserts_in_block(cls, lines: List[str], start_idx: int, end_idx: int) -> List[AssertLocation]:
        """在代码块内查找断言
        
        Args:
            lines: 所有行
            start_idx: 开始行索引
            end_idx: 结束行索引
            
        Returns:
            断言位置列表
        """
        asserts = []
        
        for i in range(start_idx, end_idx):
            line = lines[i]
            
            for pattern in cls.ASSERT_PATTERNS:
                for match in pattern.finditer(line):
                    # 确定断言类型
                    assert_type = cls._get_assert_type(match.group())
                    
                    asserts.append(AssertLocation(
                        line_number=i + 1,
                        column=match.start(),
                        assert_type=assert_type,
                        content=match.group().strip()
                    ))
                    break  # 每行只取第一个匹配
        
        return asserts
    
    @classmethod
    def _get_assert_type(cls, assert_str: str) -> str:
        """获取断言类型
        
        Args:
            assert_str: 断言字符串
            
        Returns:
            断言类型名称
        """
        if 'assertFail' in assert_str:
            return 'assertFail'
        elif 'assertEqual' in assert_str:
            return 'assertEqual'
        elif 'assertTrue' in assert_str:
            return 'assertTrue'
        elif 'assertFalse' in assert_str:
            return 'assertFalse'
        elif 'assertNull' in assert_str:
            return 'assertNull'
        elif 'assertNotNull' in assert_str:
            return 'assertNotNull'
        elif 'assertUndefined' in assert_str:
            return 'assertUndefined'
        elif 'assertClose' in assert_str:
            return 'assertClose'
        elif 'assertContain' in assert_str:
            return 'assertContain'
        elif 'assertLargerOrEqual' in assert_str:
            return 'assertLargerOrEqual'
        elif 'assertLessOrEqual' in assert_str:
            return 'assertLessOrEqual'
        elif 'assertLarger' in assert_str:
            return 'assertLarger'
        elif 'assertLess' in assert_str:
            return 'assertLess'
        elif 'assertInstanceOf' in assert_str:
            return 'assertInstanceOf'
        return 'unknown'


class DatabaseManager:
    """数据库管理器
    
    管理 kit_module 和 module_domain 表的查询
    """
    
    def __init__(self, db_path: str = None):
        """初始化数据库管理器
        
        Args:
            db_path: 数据库路径，默认使用脚本同级的相对路径
        """
        if db_path is None:
            db_path = DB_PATH
        self.db_path = os.path.abspath(db_path)
        self.conn = None
        
    def connect(self):
        """连接数据库"""
        if not os.path.exists(self.db_path):
            print(f"警告: 数据库文件不存在: {self.db_path}")
            return False
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return True
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def ensure_tables(self):
        """确保必要的表存在
        
        如果 kit_module 和 module_domain 表不存在，则创建
        """
        if not self.conn:
            return False
        
        cursor = self.conn.cursor()
        
        # 检查表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='kit_module'
        """)
        if not cursor.fetchone():
            # 创建 kit_module 表
            cursor.execute("""
                CREATE TABLE kit_module (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kit TEXT NOT NULL,
                    module TEXT NOT NULL,
                    subsystem TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(kit, module)
                )
            """)
            print("已创建 kit_module 表")
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='module_domain'
        """)
        if not cursor.fetchone():
            # 创建 module_domain 表
            cursor.execute("""
                CREATE TABLE module_domain (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module TEXT NOT NULL,
                    subsystem TEXT,
                    domain_hex TEXT,
                    owner TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(module)
                )
            """)
            print("已创建 module_domain 表")
        
        self.conn.commit()
        return True
    
    def query_by_kit(self, kit: str) -> Optional[Dict]:
        """通过 kit 查询信息
        
        Args:
            kit: kit 名称（如 'ArkUI'）
            
        Returns:
            查询结果字典
        """
        if not self.conn:
            return None
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT kit_name, module_name, subsystem_cn
            FROM kit_module
            WHERE kit_name = ?
            LIMIT 1
        """, (kit,))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def query_by_module(self, module: str) -> Optional[Dict]:
        """通过 module 查询信息
        
        Args:
            module: module 名称（如 'hilog'）
            
        Returns:
            查询结果字典
        """
        if not self.conn:
            return None
        
        cursor = self.conn.cursor()
        
        # 先查 kit_module 表
        cursor.execute("""
            SELECT kit_name, module_name, subsystem_cn
            FROM kit_module
            WHERE module_name = ?
            LIMIT 1
        """, (module,))
        
        row = cursor.fetchone()
        if row:
            result = dict(row)
            cursor.execute("""
                SELECT domain_hex, short_hex, tag_example
                FROM module_domain
                WHERE module_name = ?
                LIMIT 1
            """, (module,))
            domain_row = cursor.fetchone()
            if domain_row:
                result['domain_hex'] = domain_row['domain_hex']
                result['short_hex'] = domain_row['short_hex']
                result['tag'] = domain_row['tag_example']
            return result
        
        # 查 module_domain 表
        cursor.execute("""
            SELECT module_name, subsystem_cn, domain_hex, short_hex, tag_example
            FROM module_domain
            WHERE module_name = ?
            LIMIT 1
        """, (module,))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        
        return None
    
    def query_by_subsystem_mapping(self, directory: str) -> Optional[str]:
        """通过目录名查询子系统
        
        Args:
            directory: 目录名
            
        Returns:
            子系统名称
        """
        if not self.conn:
            return None
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT subsystem 
            FROM subsystem_mapping 
            WHERE directory = ?
            LIMIT 1
        """, (directory,))
        
        row = cursor.fetchone()
        if row:
            return row['subsystem']
        return None


class SourceAnalyzer:
    """源码分析器
    
    整合 import 解析、测试用例解析和数据库查询
    """
    
    def __init__(self, db_path: str = None):
        """初始化分析器
        
        Args:
            db_path: 数据库路径
        """
        self.db = DatabaseManager(db_path)
        self.db.connect()
        self.db.ensure_tables()
    
    def analyze_file(self, file_path: str) -> Dict:
        """分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            分析结果字典
        """
        result = {
            'file': file_path,
            'imports': [],
            'test_cases': [],
            'api_chains': [],
            'error': None
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result['error'] = str(e)
            return result
        
        lines = content.split('\n')
        
        # 1. 解析 import 语句
        imports = []
        for i, line in enumerate(lines, 1):
            import_info = ImportParser.parse_line(line, i)
            if import_info and import_info.import_type in ('kit', 'ohos'):
                imports.append(import_info)
        
        # 2. 解析测试用例和断言
        test_cases, assert_locations = HypiumTestParser.parse_file(content)
        
        # 3. 构建 API 到 Domain 链路
        api_chains = []
        for imp in imports:
            chain = self._build_api_chain(imp, test_cases, assert_locations, file_path)
            api_chains.append(chain)
        
        result['imports'] = [asdict(imp) for imp in imports]
        result['test_cases'] = [asdict(tc) for tc in test_cases]
        result['api_chains'] = api_chains
        
        return result
    
    def _build_api_chain(self, import_info: ImportInfo, 
                         test_cases: List[TestCaseInfo],
                         assert_locations: List[AssertLocation],
                         file_path: str) -> Dict:
        """构建 API 到 Domain 的链路
        
        Args:
            import_info: import 信息
            test_cases: 测试用例列表
            assert_locations: 断言位置列表
            file_path: 文件路径
            
        Returns:
            API 链路字典
        """
        kit, module = ImportParser.extract_kit_module(import_info.module_path)
        
        # 构建 API 名称
        if import_info.imported_names:
            api = import_info.imported_names[0]
            if api.startswith('*:'):
                api = api[2:]  # 去掉 *: 前缀
        else:
            api = module or kit or import_info.module_path
        
        # 委托 map_domain 做确定性映射（固化常量 + 校正字段名）
        # 不再直接查 db，杜绝 kit/module/subsystem 字段名脱节 bug
        domain_info = None
        if module and map_sut:
            sut = map_sut('@ohos.' + module)
            if sut.get('status') == 'mapped':
                domain_info = sut
        if kit and not domain_info and expand_kit:
            exp = expand_kit(kit)
            if exp.get('status') == 'expanded':
                for m in exp.get('mappings', []):
                    if m.get('status') == 'mapped':
                        domain_info = m
                        break

        # 构建链路
        chain = {
            'api': api,
            'kit': kit or '',
            'module': module or (domain_info.get('module', '').replace('@ohos.', '') if domain_info else ''),
            'subsystem': domain_info.get('subsystem', '') if domain_info else '',
            'subsystem_en': domain_info.get('subsystem_en', '') if domain_info else '',
            'domain_hex': domain_info.get('domain', '') if domain_info else '',
            'tag': domain_info.get('tag', '') if domain_info else '',
            'filter_regex': domain_info.get('filter_regex', '') if domain_info else '',
            'mapped': bool(domain_info),
            'import_file': os.path.basename(file_path),
            'import_line': import_info.line_number,
            'test_cases': [tc.name for tc in test_cases],
            'assert_locations': [
                {
                    'file': os.path.basename(file_path),
                    'line': loc.line_number,
                    'type': loc.assert_type,
                    'content': loc.content[:50] + '...' if len(loc.content) > 50 else loc.content
                }
                for loc in assert_locations
            ]
        }
        
        return chain
    
    def analyze_directory(self, dir_path: str, recursive: bool = True) -> List[Dict]:
        """分析目录下的所有 .ets 文件
        
        Args:
            dir_path: 目录路径
            recursive: 是否递归子目录
            
        Returns:
            分析结果列表
        """
        results = []
        dir_path = Path(dir_path)
        
        if recursive:
            pattern = '**/*.ets'
        else:
            pattern = '*.ets'
        
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                result = self.analyze_file(str(file_path))
                results.append(result)
        
        return results
    
    def close(self):
        """关闭分析器"""
        self.db.close()


def format_output(results: List[Dict], format_type: str = 'json') -> str:
    """格式化输出结果
    
    Args:
        results: 分析结果列表
        format_type: 格式类型 ('json' | 'summary')
        
    Returns:
        格式化后的字符串
    """
    if format_type == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    elif format_type == 'summary':
        lines = []
        lines.append("=" * 60)
        lines.append("源码分析摘要")
        lines.append("=" * 60)
        
        for result in results:
            lines.append(f"\n文件: {result.get('file', 'unknown')}")
            
            if result.get('error'):
                lines.append(f"  错误: {result['error']}")
                continue
            
            lines.append(f"  Import 数量: {len(result.get('imports', []))}")
            lines.append(f"  测试用例数: {len(result.get('test_cases', []))}")
            
            # API 链路
            for chain in result.get('api_chains', []):
                lines.append(f"\n  API: {chain['api']}")
                if chain.get('kit'):
                    lines.append(f"    Kit: {chain['kit']}")
                if chain.get('module'):
                    lines.append(f"    Module: {chain['module']}")
                if chain.get('subsystem'):
                    lines.append(f"    Subsystem: {chain['subsystem']}")
                if chain.get('domain_hex'):
                    lines.append(f"    Domain: {chain['domain_hex']}")
                lines.append(f"    Import: {chain['import_file']}:{chain['import_line']}")
                
                if chain.get('assert_locations'):
                    lines.append(f"    断言数: {len(chain['assert_locations'])}")
                    for loc in chain['assert_locations'][:3]:  # 只显示前3个
                        lines.append(f"      - {loc['file']}:{loc['line']} [{loc['type']}]")
                    if len(chain['assert_locations']) > 3:
                        lines.append(f"      ... 还有 {len(chain['assert_locations']) - 3} 个断言")
        
        return '\n'.join(lines)
    
    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='源码解析脚本 - 提取API到Domain链路',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单个文件
  python3 analyze_source.py test.ets
  
  # 分析目录（递归）
  python3 analyze_source.py ./tests
  
  # 输出摘要格式
  python3 analyze_source.py test.ets --format summary
  
  # 指定数据库路径
  python3 analyze_source.py test.ets --db /path/to/xts_rules.db
        """
    )
    
    parser.add_argument('path', help='要分析的文件或目录路径')
    parser.add_argument('--format', '-f', choices=['json', 'summary'], 
                       default='json', help='输出格式 (默认: json)')
    parser.add_argument('--db', help='数据库路径')
    parser.add_argument('--no-recursive', action='store_true', 
                       help='不递归子目录')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = SourceAnalyzer(args.db)
    
    try:
        path = Path(args.path)
        
        if path.is_file():
            # 分析单个文件
            result = analyzer.analyze_file(str(path))
            results = [result]
        elif path.is_dir():
            # 分析目录
            results = analyzer.analyze_directory(
                str(path), 
                recursive=not args.no_recursive
            )
        else:
            print(f"错误: 路径不存在: {path}")
            sys.exit(1)
        
        # 输出结果
        output = format_output(results, args.format)
        print(output)
        
    finally:
        analyzer.close()


if __name__ == '__main__':
    main()