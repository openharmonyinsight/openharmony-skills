#!/usr/bin/env python3
"""
batch_generate_graphs.py - 批量生成概念关系图谱
为所有重要概念生成可视化图谱
"""

import os
import sys
from pathlib import Path
from visualize_concept_graph import ConceptGraphVisualizer


def main():
    """批量生成图谱"""
    
    # 重要概念列表
    important_concepts = [
        'lambda', 'generic', 'type-inference', 'class', 'interface', 'struct',
        'function', 'macro', 'parser', 'lexer', 'sema', 'ast', 'chir', 'codegen',
        'type', 'expr', 'decl', 'pattern-match', 'error-handling', 'concurrency',
        'for-loop', 'enum', 'extend', 'overload', 'pointer', 'reference',
        'string', 'array', 'option', 'package', 'modules', 'pipeline',
        'desugaring', 'syntax-sugar', 'inline', 'const', 'var',
        'type-system', 'symbol-table', 'name-resolution', 'reflection'
    ]
    
    # 创建可视化器
    kb_dir = Path(__file__).resolve().parent.parent / 'knowledge-base'
    visualizer = ConceptGraphVisualizer(str(kb_dir))
    
    # 创建输出目录
    graphs_dir = kb_dir / 'graphs'
    graphs_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建输出目录
    graphs_dir = kb_dir / 'graphs'
    graphs_dir.mkdir(exist_ok=True)
    
    print(f"开始批量生成概念关系图谱...")
    print(f"目标概念数量: {len(important_concepts)}\n")
    
    success_count = 0
    failed_concepts = []
    
    for i, concept in enumerate(important_concepts, 1):
        output_file = graphs_dir / f"{concept}-concept-graph.md"
        
        try:
            # 生成图谱
            content = visualizer.generate_concept_graph(concept)
            
            # 检查是否有错误
            if content.startswith('错误:'):
                print(f"[{i}/{len(important_concepts)}] ✗ {concept}: {content}")
                failed_concepts.append(concept)
                continue
            
            # 保存图谱
            visualizer.save_graph(content, str(output_file))
            print(f"[{i}/{len(important_concepts)}] ✓ {concept}")
            success_count += 1
            
        except Exception as e:
            print(f"[{i}/{len(important_concepts)}] ✗ {concept}: {e}")
            failed_concepts.append(concept)
    
    print(f"\n完成！")
    print(f"成功生成: {success_count} 个图谱")
    print(f"失败: {len(failed_concepts)} 个")
    
    if failed_concepts:
        print(f"\n失败的概念: {', '.join(failed_concepts)}")
    
    # 生成所有模块的依赖图谱
    print(f"\n生成模块依赖图谱...")
    
    modules = [
        'sema', 'ast', 'chir', 'codegen', 'parser', 'lexer',
        'modules', 'macro', 'mangle', 'driver', 'frontend'
    ]
    
    module_success = 0
    for module in modules:
        try:
            output_file = graphs_dir / f"{module}-module-deps.md"
            content = visualizer.generate_module_dependency_graph(module)
            
            if not content.startswith('错误:'):
                visualizer.save_graph(content, str(output_file))
                print(f"✓ {module} 模块依赖图谱")
                module_success += 1
            else:
                print(f"✗ {module}: {content}")
        except Exception as e:
            print(f"✗ {module}: {e}")
    
    print(f"\n模块依赖图谱: {module_success}/{len(modules)}")
    print(f"\n所有图谱已保存到: {graphs_dir}")


if __name__ == '__main__':
    main()
