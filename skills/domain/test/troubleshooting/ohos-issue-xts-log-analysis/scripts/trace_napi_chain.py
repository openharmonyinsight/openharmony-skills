#!/usr/bin/env python3
"""
trace_napi_chain.py - NAPI接口完整追溯工具

设计原则：
1. 从测试文件提取 .so 引用
2. 查找封装层配置（oh-package.json5）
3. 扫描 C++ 实现文件提取底层接口
4. 查询数据库获取 subsystem 和 kit
5. 推断 domain 并生成证据链

用法：
    python3 trace_napi_chain.py <测试文件路径> --xts-root <XTS根路径>
    python3 trace_napi_chain.py AVTransCoderNdk.test.ets --xts-root /path/to/xts
"""

import os
import re
import sys
import json
import sqlite3
import argparse
from typing import List, Dict, Optional

class NapiChainTracer:
    def __init__(self, test_file: str, xts_root: str = None, db_path: str = None):
        self.test_file = os.path.abspath(test_file)
        self.xts_root = xts_root or self._default_xts_root()
        self.db_path = db_path or self._default_db_path()
        
    def _default_xts_root(self) -> str:
        """默认 XTS 根路径"""
        home = os.path.expanduser("~")
        return os.path.join(home, "master", "test", "xts", "acts")
    
    def _default_db_path(self) -> str:
        """默认数据库路径"""
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(here, "..", "data", "xts_rules.db"))
        
    def trace(self) -> Dict:
        """主追溯流程"""
        # Step 1: 提取 .so 引用
        so_refs = self._extract_so_references()
        if not so_refs:
            return {
                'status': 'skip',
                'reason': '未发现 .so 引用（非NAPI接口测试）',
                'test_file': self.test_file,
                'so_references': [],
                'sdk_interfaces': [],
                'evidence_chain': None
            }
        
        # Step 2: 查找封装层配置
        wrapper_info = self._find_wrapper_layer(so_refs)
        
        # Step 3: 扫描 C++ 实现
        cpp_impl = self._scan_cpp_impl()
        sdk_interfaces = self._extract_sdk_interfaces(cpp_impl) if cpp_impl else []
        
        # Step 4: 查询数据库
        api_info = self._query_api_info(sdk_interfaces)
        
        # Step 5: 推断 domain
        domain_info = self._infer_domain(api_info)
        
        # Step 6: 生成证据链
        evidence_chain = self._build_evidence_chain(
            so_refs, wrapper_info, cpp_impl, sdk_interfaces, api_info, domain_info
        )
        
        return {
            'status': 'ok',
            'test_file': self.test_file,
            'so_references': so_refs,
            'wrapper_layer': wrapper_info,
            'cpp_impl': cpp_impl,
            'sdk_interfaces': sdk_interfaces,
            'api_info': api_info,
            'domain_filter': domain_info,
            'evidence_chain': evidence_chain
        }
    
    def _extract_so_references(self) -> List[str]:
        """从测试文件提取 .so 引用"""
        imports = []
        
        if not os.path.exists(self.test_file):
            return imports
        
        with open(self.test_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 匹配 import xxx from 'libxxx.so' 或 "libxxx.so"
                match = re.search(r"import\s+\w+\s+from\s+['\"](lib\w+\.so)['\"]", line)
                if match:
                    so_name = match.group(1)
                    imports.append(so_name)
        
        return list(set(imports))  # 去重
    
    def _find_wrapper_layer(self, so_refs: List[str]) -> Dict:
        """查找封装层配置"""
        wrapper_info = {}
        
        for so_ref in so_refs:
            # 提取 so 名称的核心部分（去掉 lib 和 .so）
            so_core = so_ref.replace('lib', '').replace('.so', '')
            
            # 从测试文件路径推断 XTS 工程根目录
            test_dir = os.path.dirname(self.test_file)
            project_root = test_dir
            while project_root and project_root != self.xts_root:
                parent = os.path.dirname(project_root)
                if parent == project_root:
                    break
                project_root = parent
            
            # 搜索 oh-package.json5
            oh_pkg_path = self._search_oh_package(so_core, project_root)
            
            if oh_pkg_path and os.path.exists(oh_pkg_path):
                oh_pkg = self._parse_oh_package(oh_pkg_path)
                wrapper_info[so_ref] = {
                    'oh_package_path': oh_pkg_path,
                    'oh_package_content': oh_pkg,
                    'status': 'found'
                }
            else:
                wrapper_info[so_ref] = {
                    'oh_package_path': None,
                    'status': 'not_found',
                    'note': '未找到对应的 oh-package.json5'
                }
        
        return wrapper_info
    
    def _search_oh_package(self, so_core: str, search_root: str) -> Optional[str]:
        """搜索 oh-package.json5 文件（优先搜索测试文件同目录下的 cpp/types）"""
        if not search_root or not os.path.exists(search_root):
            return None
        
        # 优先级1: 测试文件同目录下的 cpp/types/
        test_dir = os.path.dirname(self.test_file)
        project_root = test_dir
        
        # 向上查找项目根目录（包含 entry 的目录）
        while project_root and 'entry' not in os.path.basename(project_root):
            parent = os.path.dirname(project_root)
            if parent == project_root or parent == search_root:
                break
            project_root = parent
        
        # 检查 cpp/types/ 目录
        cpp_types_dir = os.path.join(project_root, 'src', 'main', 'cpp', 'types')
        if os.path.exists(cpp_types_dir):
            for root, dirs, files in os.walk(cpp_types_dir):
                if 'oh-package.json5' in files:
                    file_path = os.path.join(root, 'oh-package.json5')
                    return file_path
        
        # 优先级2: 向上两级目录的 cpp/types/
        for i in range(3):
            search_dir = test_dir
            for _ in range(i):
                search_dir = os.path.dirname(search_dir)
            
            cpp_types_dir = os.path.join(search_dir, 'cpp', 'types')
            if os.path.exists(cpp_types_dir):
                for root, dirs, files in os.walk(cpp_types_dir):
                    if 'oh-package.json5' in files:
                        file_path = os.path.join(root, 'oh-package.json5')
                        return file_path
        
        # 优先级3: 全局搜索（受限）
        for root, dirs, files in os.walk(search_root):
            # 限制深度
            depth = root.count(os.sep) - search_root.count(os.sep)
            if depth > 15:
                del dirs[:]
                continue
            
            # 只搜索 cpp/types/ 路径
            if 'cpp' in root and 'types' in root and 'oh-package.json5' in files:
                file_path = os.path.join(root, 'oh-package.json5')
                # 检查文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if '.so' in content:
                            return file_path
                except Exception:
                    pass
        
        return None
    
    def _parse_oh_package(self, file_path: str) -> Dict:
        """解析 oh-package.json5"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 去除注释
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                content = re.sub(r'//.*', '', content)
                # 去除尾部逗号
                content = re.sub(r',\s*}', '}', content)
                content = re.sub(r',\s*]', ']', content)
                return json.loads(content)
        except Exception:
            return {}
    
    def _scan_cpp_impl(self) -> Optional[str]:
        """扫描 C++ 实现文件"""
        test_dir = os.path.dirname(self.test_file)
        
        # 查找 entry 根目录
        entry_root = test_dir
        while entry_root and entry_root != self.xts_root:
            if 'entry' in os.path.basename(entry_root):
                break
            entry_root = os.path.dirname(entry_root)
        
        # C++ 目录
        cpp_dir = os.path.join(entry_root, 'src', 'main', 'cpp')
        
        if not os.path.exists(cpp_dir):
            return None
        
        # 提取测试类名
        test_basename = os.path.basename(self.test_file)
        test_class = test_basename.replace('.test.ets', '').replace('.test.ts', '')
        
        # 可能的 C++ 文件名（多种大小写组合）
        cpp_names = [
            f"{test_class}Test.cpp",
            f"{test_class}.cpp",
            test_class.replace('Ndk', '') + "Test.cpp",
        ]
        
        # 精确匹配
        for cpp_name in cpp_names:
            cpp_file = os.path.join(cpp_dir, cpp_name)
            if os.path.exists(cpp_file):
                return cpp_file
        
        # 模糊匹配（优先匹配测试类名）
        test_class_lower = test_class.lower()
        best_match = None
        best_score = 0
        
        for file in os.listdir(cpp_dir):
            if file.endswith('.cpp'):
                file_lower = file.lower()
                # 计算匹配分数
                score = 0
                if test_class_lower in file_lower:
                    score = 100
                elif test_class_lower.replace('ndk', '') in file_lower:
                    score = 80
                elif 'test' in file_lower:
                    score = 50
                
                if score > best_score:
                    best_score = score
                    best_match = os.path.join(cpp_dir, file)
        
        return best_match
    
    def _extract_sdk_interfaces(self, cpp_file: str) -> List[str]:
        """从 C++ 文件提取 SDK 接口"""
        interfaces = []
        
        if not cpp_file or not os.path.exists(cpp_file):
            return interfaces
        
        with open(cpp_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # 匹配 OH_XXX_ 接口调用（多种模式）
            patterns = [
                r'OH_[A-Z][a-zA-Z0-9_]+\s*\(',           # OH_AVTranscoder_Prepare(
                r'OH_[A-Z][a-zA-Z0-9_]+\s*=',             # OH_AVTranscoder_Create =
                r'OH_[A-Z][a-zA-Z0-9_]+\s*\)',            # OH_XXX_YYY)
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # 提取接口名
                    interface_name = re.match(r'OH_[A-Z][a-zA-Z0-9_]+', match)
                    if interface_name:
                        interfaces.append(interface_name.group(0))
        
        return list(set(interfaces))  # 去重
    
    def _query_api_info(self, sdk_interfaces: List[str]) -> List[Dict]:
        """查询数据库获取接口信息"""
        api_info = []
        
        if not sdk_interfaces:
            return api_info
        
        if not os.path.exists(self.db_path):
            return api_info
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for interface in sdk_interfaces:
            # 推断 SDK 头文件名
            sdk_header = self._infer_sdk_header(interface)
            
            if not sdk_header:
                continue
            
            # 查询 api_path_mapping 表
            cursor.execute('''
                SELECT api_path, subsystem_cn, kit_cn, kit_en, sdk_type
                FROM api_path_mapping
                WHERE module_name = ? OR api_path LIKE ?
                LIMIT 1
            ''', (sdk_header, f'%{sdk_header}'))
            
            row = cursor.fetchone()
            if row:
                api_info.append({
                    'interface': interface,
                    'sdk_header': sdk_header,
                    'api_path': row[0],
                    'subsystem_cn': row[1],
                    'kit_cn': row[2],
                    'kit_en': row[3],
                    'sdk_type': row[4]
                })
        
        conn.close()
        return api_info
    
    def _infer_sdk_header(self, interface: str) -> str:
        """推断 SDK 头文件名
        
        规则：
        - OH_AVTranscoder_Create → avtranscoder.h
        - OH_AVPlayer_Play → avplayer.h
        - OH_Camera_Open → camera.h
        """
        # 提取核心模块名（去掉 OH_ 前缀）
        parts = interface.replace('OH_', '').split('_')
        
        # 映射表
        module_map = {
            'AVTranscoder': 'avtranscoder.h',
            'AVTranscoderConfig': 'avtranscoder.h',
            'AVPlayer': 'avplayer.h',
            'AVRecorder': 'avrecorder.h',
            'Camera': 'camera.h',
            'Image': 'image.h',
            'NativeWindow': 'native_window.h',
            'NativeBuffer': 'native_buffer.h',
            'NativePixelMap': 'native_pixelmap.h',
            'HiAppEvent': 'hiappevent.h',
            'HiLog': 'hilog.h',
            'Napi': 'native_api.h',
        }
        
        # 查找匹配的模块
        for part in parts:
            if part in module_map:
                return module_map[part]
        
        # 默认：使用第一部分的小写形式
        if parts:
            return f'{parts[0].lower()}.h'
        
        return None
    
    def _infer_domain(self, api_info: List[Dict]) -> Dict:
        """推断 domain"""
        if not api_info:
            return {
                'status': 'unmapped',
                'reason': '未找到接口信息',
                'subsystem': None,
                'domain_prefix': None,
                'filter_regex': None
            }
        
        # 查询 subsystem_domain_inference 表（如果存在）
        subsystem = api_info[0]['subsystem_cn']
        
        # 尝试查询数据库
        domain_info = self._query_domain_inference(subsystem)
        
        if domain_info:
            return domain_info
        
        # 使用内置映射表（兜底）
        subsystem_domain_map = {
            '多媒体': {'domain_prefix': '0xD002B', 'filter_regex': 'C002B[0-9a-fA-F]/'},
            'OS媒体软件': {'domain_prefix': '0xD002B', 'filter_regex': 'C002B[0-9a-fA-F]/'},
            'ArkUI开发框架': {'domain_prefix': '0xD0039', 'filter_regex': 'C0039[0-9a-fA-F]/'},
            '元能力': {'domain_prefix': '0xD0013', 'filter_regex': 'C0013[0-9a-fA-F]/'},
            'DFX': {'domain_prefix': '0xD002D', 'filter_regex': 'C002D[0-9a-fA-F]/'},
            '公共基础类库': {'domain_prefix': '0xD003F', 'filter_regex': 'C003F[0-9a-fA-F]/'},
            '图形图像': {'domain_prefix': '0xD0014', 'filter_regex': 'C0014[0-9a-fA-F]/'},
        }
        
        domain_info = subsystem_domain_map.get(subsystem)
        
        if domain_info:
            return {
                'status': 'inferred',
                'subsystem': subsystem,
                'domain_prefix': domain_info['domain_prefix'],
                'filter_regex': domain_info['filter_regex'],
                'confidence': 'high',
                'source': 'builtin_mapping'
            }
        
        return {
            'status': 'unmapped',
            'reason': f'子系统 {subsystem} 的 domain 暂无映射',
            'subsystem': subsystem,
            'domain_prefix': None,
            'filter_regex': None
        }
    
    def _query_domain_inference(self, subsystem: str) -> Optional[Dict]:
        """查询 subsystem_domain_inference 表"""
        if not os.path.exists(self.db_path):
            return None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subsystem_domain_inference'")
            if not cursor.fetchone():
                conn.close()
                return None
            
            # 查询
            cursor.execute('''
                SELECT domain_prefix, filter_regex, confidence, note
                FROM subsystem_domain_inference
                WHERE subsystem_cn = ?
            ''', (subsystem,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'status': 'inferred',
                    'subsystem': subsystem,
                    'domain_prefix': row[0],
                    'filter_regex': row[1],
                    'confidence': row[2],
                    'source': 'database'
                }
        except Exception:
            pass
        
        return None
    
    def _build_evidence_chain(self, so_refs, wrapper_info, cpp_impl, sdk_interfaces, api_info, domain_info) -> str:
        """生成证据链文本"""
        chain = []
        
        test_basename = os.path.basename(self.test_file)
        chain.append(f"失败用例源码({test_basename})")
        
        if so_refs:
            chain.append(f"    │ import xxx from '{so_refs[0]}'")
            chain.append("    │ ⚠️ Step 1: 识别 .so 引用 → 启动 NAPI 追溯")
        chain.append("    ▼")
        
        chain.append("┌─────────────────────────────────────────────┐")
        chain.append("│ Step 2: 检查封装层配置                       │")
        
        if so_refs and wrapper_info.get(so_refs[0], {}).get('status') == 'found':
            oh_pkg_path = wrapper_info[so_refs[0]].get('oh_package_path', '')
            chain.append(f"│ oh-package.json5: {os.path.basename(oh_pkg_path) if oh_pkg_path else 'N/A'}")
            chain.append("│ 状态: 已找到                                 │")
        else:
            chain.append("│ oh-package.json5 未找到                      │")
            chain.append("│ → 跳过此步骤，直接扫描 C++ 实现              │")
        chain.append("└─────────────────────────────────────────────┘")
        chain.append("    ▼")
        
        chain.append("┌─────────────────────────────────────────────┐")
        chain.append("│ Step 3: 扫描 C++ 实现                        │")
        if cpp_impl:
            chain.append(f"│ 文件: {os.path.basename(cpp_impl)}")
            if sdk_interfaces:
                chain.append(f"│ 底层接口数: {len(sdk_interfaces)}")
                for interface in sdk_interfaces[:5]:  # 显示前5个
                    chain.append(f"│ → {interface}")
                if len(sdk_interfaces) > 5:
                    chain.append(f"│ ... 还有 {len(sdk_interfaces) - 5} 个接口")
            else:
                chain.append("│ 未提取到 SDK 接口")
        else:
            chain.append("│ C++ 文件未找到                               │")
        chain.append("└─────────────────────────────────────────────┘")
        chain.append("    ▼")
        
        chain.append("┌─────────────────────────────────────────────┐")
        chain.append("│ Step 4: 查询 SDK 接口                        │")
        if api_info:
            info = api_info[0]
            chain.append(f"│ 接口: {info['interface']}")
            chain.append(f"│ subsystem: {info['subsystem_cn']}")
            chain.append(f"│ kit: {info['kit_cn']} / {info['kit_en']}")
        else:
            chain.append("│ 未找到接口信息                               │")
        chain.append("└─────────────────────────────────────────────┘")
        chain.append("    ▼")
        
        chain.append("┌─────────────────────────────────────────────┐")
        chain.append("│ Step 5: 推断 domain                          │")
        if domain_info.get('domain_prefix'):
            chain.append(f"│ subsystem: {domain_info['subsystem']}")
            chain.append(f"│ domain_prefix: {domain_info['domain_prefix']}xx")
            chain.append(f"│ filter_regex: {domain_info['filter_regex']}")
            chain.append(f"│ confidence: {domain_info.get('confidence', 'unknown')}")
        else:
            chain.append("│ domain 推断失败                               │")
        chain.append("└─────────────────────────────────────────────┘")
        chain.append("    ▼")
        
        chain.append("精准日志过滤 → 行[起始行号]-[结束行号]")
        chain.append("    ▼")
        chain.append("问题定界")
        
        return '\n'.join(chain)

def main():
    parser = argparse.ArgumentParser(description='NAPI接口追溯工具')
    parser.add_argument('test_file', help='测试文件路径')
    parser.add_argument('--xts-root', help='XTS工程根路径')
    parser.add_argument('--db', help='数据库路径')
    parser.add_argument('--format', choices=['json', 'text', 'chain'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.test_file):
        print(f"错误：测试文件不存在: {args.test_file}")
        sys.exit(1)
    
    tracer = NapiChainTracer(args.test_file, args.xts_root, args.db)
    result = tracer.trace()
    
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.format == 'chain':
        print(result['evidence_chain'])
    else:
        print(f"测试文件: {result['test_file']}")
        print(f"状态: {result['status']}")
        if result['so_references']:
            print(f"\nSO引用: {result['so_references']}")
        if result['sdk_interfaces']:
            print(f"\n底层接口数: {len(result['sdk_interfaces'])}")
            for interface in result['sdk_interfaces'][:10]:
                print(f"  - {interface}")
        if result['api_info']:
            info = result['api_info'][0]
            print(f"\n子系统: {info['subsystem_cn']}")
            print(f"Kit: {info['kit_cn']} / {info['kit_en']}")
        if result['domain_filter'].get('filter_regex'):
            print(f"\nDomain推断: {result['domain_filter']['domain_prefix']}xx")
            print(f"过滤正则: {result['domain_filter']['filter_regex']}")

if __name__ == '__main__':
    main()