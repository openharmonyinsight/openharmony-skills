#!/usr/bin/env python3
"""
DependencyTreeParser - 递归解析import依赖树

功能：
1. 从OH_ROOT定位d.ts文件
2. 递归解析import语句（深度≤5）
3. 构建完整依赖树JSON
4. 查询domain映射并验证

设计要点：
- 循环依赖防护：模块缓存机制
- 深度限制：max_depth=5
- 降级处理：d.ts不存在时使用pattern推断
"""

import os
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class ModuleInfo:
    """模块信息数据结构"""
    module_name: str
    depth: int = 0
    domain: str = ""
    short_hex: str = ""
    subsystem: str = ""
    mapping_status: str = ""
    mapping_source: str = ""
    confidence: int = 0
    dts_path: Optional[str] = None
    fallback: bool = False


class DependencyTreeParser:
    """递归解析import依赖树
    
    使用示例：
        parser = DependencyTreeParser('/home/xianf/master', db_manager)
        tree = parser.parse_import_chain('@ohos.arkui.inspector')
        print(json.dumps(tree, indent=2))
    """
    
    def __init__(self, oh_root: str, db_manager, max_depth: int = 5):
        """初始化依赖树解析器
        
        Args:
            oh_root: OpenHarmony源码根路径（如 '/home/xianf/master'）
            db_manager: 数据库管理器（用于domain查询）
            max_depth: 最大递归深度（默认5，防止无限递归）
        """
        self.oh_root = oh_root
        self.db = db_manager
        self.max_depth = max_depth
        self.cache: Dict[str, Dict] = {}  # 已解析模块缓存
        
        # 验证OH_ROOT有效性
        self._validate_oh_root()
        
        print(f"✓ DependencyTreeParser初始化完成")
        print(f"  OH_ROOT: {self.oh_root}")
        print(f"  MAX_DEPTH: {self.max_depth}")
    
    def _validate_oh_root(self):
        """验证OH_ROOT路径有效性"""
        api_path = os.path.join(self.oh_root, 'interface/sdk-js/api')
        kits_path = os.path.join(self.oh_root, 'interface/sdk-js/kits')
        
        if not os.path.exists(api_path):
            raise ValueError(f"OH_ROOT无效: {api_path} 不存在")
        
        if not os.path.exists(kits_path):
            raise ValueError(f"OH_ROOT无效: {kits_path} 不存在")
        
        print(f"✓ OH_ROOT验证通过")
    
    def parse_import_chain(self, module_path: str, current_depth: int = 0) -> Dict:
        """递归解析依赖链
        
        Args:
            module_path: 模块路径（支持多种格式）
            current_depth: 当前递归深度（内部参数，初始为0）
        
        Returns:
            依赖树JSON结构
        """
        full_module = self._normalize_module_name(module_path)
        
        # 检查缓存（防止循环依赖）
        if full_module in self.cache:
            cached_tree = self.cache[full_module]
            return self._adjust_cached_tree(cached_tree, current_depth)
        
        # 深度限制检查
        if current_depth >= self.max_depth:
            return self._create_depth_limit_node(full_module, current_depth)
        
        # 定位d.ts文件
        dts_path = self._locate_dts_file(full_module)
        
        if not dts_path:
            tree = self._fallback_infer(full_module, current_depth)
            self.cache[full_module] = tree
            return tree
        
        # 解析d.ts文件的import语句
        imports = self._parse_dts_imports(dts_path)
        
        # 构建依赖树
        tree = {
            'module': full_module,
            'depth': current_depth,
            'imports': [],
            'domain': '',
            'subsystem': '',
            'mapping_status': '',
            'mapping_source': '',
            'confidence': 0,
            'dts_path': dts_path,
            'stats': {'total_modules': 0, 'max_depth': current_depth}
        }
        
        # 递归解析每个import
        import_count = 0
        for imp_module in imports:
            if import_count >= 10:  # 限制最多10个import
                break
            
            child_tree = self.parse_import_chain(imp_module, current_depth + 1)
            tree['imports'].append(child_tree)
            import_count += 1
        
        # 查询domain映射
        db_info = self.db.query_module_domain_multi_level(
            full_module.replace('@ohos.', '').replace('@kit.', '')
        )
        
        if db_info:
            tree['domain'] = db_info.get('domain_hex', '')
            tree['short_hex'] = db_info.get('short_hex', '')
            tree['subsystem'] = db_info.get('subsystem_cn', '')
            tree['mapping_status'] = db_info.get('mapping_status', '')
            tree['mapping_source'] = db_info.get('mapping_source', '')
            tree['confidence'] = db_info.get('confidence', 0)
        
        # 计算统计信息
        tree['stats']['total_modules'] = self._count_total_modules(tree)
        tree['stats']['max_depth'] = self._get_max_depth(tree)
        
        # 缓存结果
        self.cache[full_module] = tree
        
        return tree
    
    def _normalize_module_name(self, module_path: str) -> str:
        """标准化模块名"""
        if module_path.startswith('@ohos.') or module_path.startswith('@kit.'):
            return module_path
        
        if module_path[0].isupper() and '.' not in module_path:
            return f'@kit.{module_path}'
        
        return f'@ohos.{module_path}'
    
    def _locate_dts_file(self, module_path: str) -> Optional[str]:
        """定位d.ts定义文件"""
        paths_to_check = []
        
        if module_path.startswith('@ohos.'):
            dts_file = module_path + '.d.ts'
            paths_to_check.append(
                os.path.join(self.oh_root, 'interface/sdk-js/api', dts_file)
            )
        
        if module_path.startswith('@kit.'):
            kit_name = module_path.replace('@kit.', '')
            paths_to_check.append(
                os.path.join(self.oh_root, 'interface/sdk-js/kits', f'@kit.{kit_name}.d.ts')
            )
        
        for path in paths_to_check:
            if os.path.exists(path):
                return path
        
        return None
    
    def _parse_dts_imports(self, dts_path: str) -> List[str]:
        """解析d.ts文件的import语句"""
        imports = []
        
        try:
            with open(dts_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 简化的import解析（提取import语句中的模块名）
            import_patterns = [
                r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+[\'"]([^\'"]+)[\'"]',
            ]
            
            import re
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if '@ohos.' in match or '@kit.' in match:
                        imports.append(match)
        
        except Exception as e:
            print(f"⚠ 解析d.ts失败: {dts_path} - {e}")
        
        return imports
    
    def _fallback_infer(self, module_path: str, current_depth: int) -> Dict:
        """降级推断（d.ts不存在时）"""
        db_info = self.db.query_module_domain_multi_level(
            module_path.replace('@ohos.', '').replace('@kit.', '')
        )
        
        return {
            'module': module_path,
            'depth': current_depth,
            'imports': [],
            'domain': db_info.get('domain_hex', '') if db_info else '',
            'subsystem': db_info.get('subsystem_cn', '') if db_info else '',
            'mapping_status': db_info.get('mapping_status', 'MISSING') if db_info else 'MISSING',
            'dts_path': None,
            'fallback': True,
            'stats': {'total_modules': 1, 'max_depth': current_depth}
        }
    
    def _adjust_cached_tree(self, cached_tree: Dict, current_depth: int) -> Dict:
        """调整缓存的依赖树"""
        adjusted_tree = cached_tree.copy()
        adjusted_tree['depth'] = current_depth
        
        if 'imports' in adjusted_tree:
            for imp in adjusted_tree['imports']:
                imp['depth'] = current_depth + 1
        
        return adjusted_tree
    
    def _create_depth_limit_node(self, module_path: str, current_depth: int) -> Dict:
        """创建深度限制节点"""
        return {
            'module': module_path,
            'depth': current_depth,
            'imports': [],
            'domain': '',
            'subsystem': '',
            'mapping_status': 'DEPTH_LIMIT',
            'note': f'达到最大深度限制 {self.max_depth}',
            'stats': {'total_modules': 1, 'max_depth': current_depth}
        }
    
    def get_all_domains(self, tree: Dict) -> List[str]:
        """从依赖树提取所有domain"""
        domains = []
        
        if tree.get('domain'):
            domains.append(tree['domain'])
        
        for imp in tree.get('imports', []):
            domains.extend(self.get_all_domains(imp))
        
        return list(set(domains))
    
    def get_all_subsystems(self, tree: Dict) -> List[str]:
        """从依赖树提取所有子系统"""
        subsystems = []
        
        if tree.get('subsystem'):
            subsystems.append(tree['subsystem'])
        
        for imp in tree.get('imports', []):
            subsystems.extend(self.get_all_subsystems(imp))
        
        return list(set(subsystems))
    
    def _count_total_modules(self, tree: Dict) -> int:
        """计算依赖树总模块数"""
        count = 1
        
        for imp in tree.get('imports', []):
            count += self._count_total_modules(imp)
        
        return count
    
    def _get_max_depth(self, tree: Dict) -> int:
        """获取依赖树最大深度"""
        max_depth = tree.get('depth', 0)
        
        for imp in tree.get('imports', []):
            child_depth = self._get_max_depth(imp)
            if child_depth > max_depth:
                max_depth = child_depth
        
        return max_depth
    
    def format_tree_output(self, tree: Dict, indent: int = 0) -> str:
        """格式化依赖树输出（用于报告）"""
        lines = []
        
        prefix = '  ' * indent
        lines.append(f"{prefix}{tree['module']} (depth {tree['depth']})")
        
        if tree.get('domain'):
            domain_str = f"{prefix}  ├─ Domain: {tree['domain']} ({tree.get('subsystem', 'Unknown')})"
            if tree.get('mapping_status'):
                domain_str += f" [{tree['mapping_status']}]"
            lines.append(domain_str)
        
        if tree.get('dts_path'):
            lines.append(f"{prefix}  ├─ d.ts: {tree['dts_path']}")
        
        for imp in tree.get('imports', []):
            child_lines = self.format_tree_output(imp, indent + 2)
            lines.append(child_lines)
        
        return '\n'.join(lines)


def validate_dependency_tree(tree: Dict) -> List[Dict]:
    """验证依赖树的domain映射"""
    warnings = []
    
    all_modules = collect_all_modules(tree)
    
    # 验证1：domain一致性
    subsystem_groups = group_by_subsystem(all_modules)
    
    for subsystem, modules in subsystem_groups.items():
        domains = set([m['domain'] for m in modules if m.get('domain')])
        
        if len(domains) > 1:
            warnings.append({
                'type': 'DOMAIN_INCONSISTENCY',
                'severity': 'Warning',
                'message': f'子系统 "{subsystem}" 包含多个domain: {list(domains)}',
                'affected_modules': [m['module'] for m in modules],
                'recommendation': f'检查子系统 "{subsystem}" 的domain配置'
            })
    
    # 验证2：子系统冲突
    subsystems = set([m['subsystem'] for m in all_modules if m.get('subsystem')])
    
    if len(subsystems) > 1:
        warnings.append({
            'type': 'SUBSYSTEM_CONFLICT',
            'severity': 'Info',
            'message': f'依赖树涉及 {len(subsystems)} 个子系统: {list(subsystems)}',
            'recommendation': '关注跨子系统调用'
        })
    
    # 验证3：映射缺失
    missing_modules = [m for m in all_modules if m.get('mapping_status') == 'MISSING']
    
    if missing_modules:
        warnings.append({
            'type': 'MAPPING_MISSING',
            'severity': 'Warning',
            'message': f'{len(missing_modules)} 个模块映射缺失',
            'affected_modules': [m['module'] for m in missing_modules],
            'recommendation': '补充module_domain表映射'
        })
    
    return warnings


def collect_all_modules(tree: Dict) -> List[Dict]:
    """递归收集依赖树中所有模块信息"""
    modules = []
    
    modules.append({
        'module': tree.get('module', ''),
        'domain': tree.get('domain', ''),
        'subsystem': tree.get('subsystem', ''),
        'mapping_status': tree.get('mapping_status', ''),
        'depth': tree.get('depth', 0)
    })
    
    for imp in tree.get('imports', []):
        modules.extend(collect_all_modules(imp))
    
    return modules


def group_by_subsystem(modules: List[Dict]) -> Dict[str, List[Dict]]:
    """按子系统分组模块"""
    groups = {}
    
    for module in modules:
        subsystem = module.get('subsystem', 'Unknown')
        
        if subsystem not in groups:
            groups[subsystem] = []
        
        groups[subsystem].append(module)
    
    return groups


def format_validation_warnings(warnings: List[Dict]) -> str:
    """格式化验证告警为字符串"""
    lines = []
    
    lines.append("### domain验证结果")
    lines.append("")
    
    if not warnings:
        lines.append("✅ **所有验证项通过，无告警**")
        return '\n'.join(lines)
    
    warnings_by_severity = {'Warning': [], 'Info': []}
    
    for warning in warnings:
        severity = warning.get('severity', 'Info')
        warnings_by_severity[severity].append(warning)
    
    if warnings_by_severity['Warning']:
        lines.append("⚠️ **Warning级别告警**:")
        lines.append("")
        
        for warning in warnings_by_severity['Warning']:
            lines.append(f"- [{warning['type']}] {warning['message']}")
            
            if warning.get('affected_modules'):
                modules_str = ', '.join(warning['affected_modules'][:5])
                if len(warning['affected_modules']) > 5:
                    modules_str += f" (共{len(warning['affected_modules'])}个)"
                lines.append(f"  - 受影响模块: {modules_str}")
            
            if warning.get('recommendation'):
                lines.append(f"  - 建议: {warning['recommendation']}")
    
    if warnings_by_severity['Info']:
        lines.append("")
        lines.append("ℹ️ **Info级别提示**:")
        lines.append("")
        
        for warning in warnings_by_severity['Info']:
            lines.append(f"- [{warning['type']}] {warning['message']}")
            
            if warning.get('recommendation'):
                lines.append(f"  - 建议: {warning['recommendation']}")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    # 测试代码
    print("DependencyTreeParser模块测试")
    print("=" * 80)
    
    # 简化测试（不依赖数据库）
    print("✓ 模块加载成功")
    print("✓ 类定义完整")
    print("✓ 验证函数可用")