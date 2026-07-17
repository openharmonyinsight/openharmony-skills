#!/usr/bin/env python3
"""
recommend_template.py - 模板推荐系统

功能：
1. 根据测试文件路径自动识别测试类型
2. 根据API类型推荐对应的报告模板
3. 提供模板路径和参数建议

用法：
    python3 recommend_template.py <测试文件路径>
"""

import os
import re
import json
import argparse
from typing import Dict, List

# 模板映射规则
TEMPLATE_RULES = [
    {
        'name': 'stream_api_error_handling',
        'keywords': ['stream', 'duplex', 'writable', 'readable'],
        'subsystems': ['公共基础类库'],
        'template': 'stream_api_error_handling_template.md',
        'description': 'Stream API错误处理模板',
        'sections': [
            '测试逻辑（Stream API调用）',
            '预期行为（错误码401等）',
            '实际行为（undefined等）',
            '失败原因分析'
        ]
    },
    {
        'name': 'arkui_component',
        'keywords': ['arkui', 'inspector', 'component', 'ui'],
        'subsystems': ['ArkUI'],
        'template': 'arkui_component_template.md',
        'description': 'ArkUI组件测试模板',
        'sections': [
            '组件创建逻辑',
            '属性值验证',
            '组件查找逻辑',
            '渲染结果验证'
        ]
    },
    {
        'name': 'ability_runtime',
        'keywords': ['ability', 'want', 'intent', 'lifecycle'],
        'subsystems': ['元能力'],
        'template': 'ability_runtime_template.md',
        'description': '元能力运行时测试模板',
        'sections': [
            'Ability启动逻辑',
            '生命周期回调验证',
            'Intent传递验证',
            '状态机转换验证'
        ]
    },
    {
        'name': 'file_management',
        'keywords': ['file', 'fs', 'io', 'storage'],
        'subsystems': ['文件管理'],
        'template': 'file_management_template.md',
        'description': '文件管理测试模板',
        'sections': [
            '文件操作逻辑',
            '权限验证',
            '路径处理验证',
            '异常处理验证'
        ]
    },
    {
        'name': 'network',
        'keywords': ['network', 'http', 'socket', 'connection'],
        'subsystems': ['网络管理'],
        'template': 'network_template.md',
        'description': '网络管理测试模板',
        'sections': [
            '网络连接逻辑',
            '请求响应验证',
            '超时处理验证',
            '断线重连验证'
        ]
    }
]

def identify_test_type(file_path: str) -> Dict:
    """识别测试类型"""
    
    # 提取文件名和路径关键词
    file_name = os.path.basename(file_path)
    dir_path = os.path.dirname(file_path).lower()
    
    # 提取关键词
    keywords = []
    
    # 从文件名提取
    parts = re.split(r'[_\-\.]', file_name.lower())
    keywords.extend(parts)
    
    # 从路径提取
    path_parts = dir_path.split('/')
    keywords.extend(path_parts)
    
    return {
        'file_name': file_name,
        'dir_path': dir_path,
        'keywords': list(set(keywords))
    }

def match_template(test_type: Dict, subsystem: str = None) -> List[Dict]:
    """匹配模板"""
    
    matched_templates = []
    keywords = test_type['keywords']
    
    for rule in TEMPLATE_RULES:
        score = 0
        
        # 关键词匹配
        for keyword in keywords:
            for rule_keyword in rule['keywords']:
                if rule_keyword in keyword or keyword in rule_keyword:
                    score += 1
        
        # 子系统匹配
        if subsystem and subsystem in rule['subsystems']:
            score += 3
        
        if score > 0:
            matched_templates.append({
                'name': rule['name'],
                'template': rule['template'],
                'description': rule['description'],
                'sections': rule['sections'],
                'score': score
            })
    
    # 按分数排序
    matched_templates.sort(key=lambda x: x['score'], reverse=True)
    
    return matched_templates

def generate_template_recommendation(
    file_path: str,
    api_info: Dict = None
) -> Dict:
    """生成模板推荐"""
    
    # 识别测试类型
    test_type = identify_test_type(file_path)
    
    # 匹配模板
    subsystem = api_info.get('subsystem') if api_info else None
    matched_templates = match_template(test_type, subsystem)
    
    result = {
        'file': file_path,
        'test_type': test_type,
        'recommended_templates': matched_templates
    }
    
    # 如果有匹配的模板，生成详细建议
    if matched_templates:
        best_template = matched_templates[0]
        result['recommendation'] = {
            'template_name': best_template['template'],
            'template_path': f"modules/L3_Report/templates/{best_template['template']}",
            'description': best_template['description'],
            'sections': best_template['sections'],
            'confidence': '高' if best_template['score'] >= 3 else '中'
        }
    else:
        # 使用默认模板
        result['recommendation'] = {
            'template_name': 'complete_testcase_template.md',
            'template_path': 'modules/L3_Report/templates/complete_testcase_template.md',
            'description': '通用测试用例模板',
            'sections': [
                '基本信息',
                '时间窗提取',
                '源码→领域证据链',
                '关键日志片段',
                '源码定位与分析',
                '问题定界'
            ],
            'confidence': '默认'
        }
    
    return result

def print_recommendation(result: Dict):
    """打印推荐结果"""
    
    print(f"\n{'='*80}")
    print(f"模板推荐结果")
    print(f"{'='*80}\n")
    
    print(f"测试文件: {result['file']}")
    print(f"测试类型关键词: {', '.join(result['test_type']['keywords'][:10])}")
    
    if result.get('recommendation'):
        rec = result['recommendation']
        print(f"\n📋 推荐模板: {rec['template_name']}")
        print(f"   描述: {rec['description']}")
        print(f"   置信度: {rec['confidence']}")
        print(f"   模板路径: {rec['template_path']}")
        
        print(f"\n📝 必填段落:")
        for i, section in enumerate(rec['sections'], 1):
            print(f"   {i}. {section}")
    
    if result.get('recommended_templates'):
        print(f"\n🎯 其他候选模板:")
        for template in result['recommended_templates'][1:4]:
            print(f"   - {template['name']}: {template['description']} (匹配度: {template['score']})")

def main():
    parser = argparse.ArgumentParser(description='模板推荐系统')
    parser.add_argument('file', help='测试文件路径')
    parser.add_argument('--subsystem', help='子系统名称（可选）')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 生成推荐
    api_info = {'subsystem': args.subsystem} if args.subsystem else None
    result = generate_template_recommendation(args.file, api_info)
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_recommendation(result)

if __name__ == '__main__':
    main()