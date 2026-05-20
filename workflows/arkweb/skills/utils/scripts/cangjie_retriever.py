#!/usr/bin/env python3
"""
仓颉编程语言混合检索器：
- 结合向量检索（语义）和 BM25 检索（关键词）
- 从本地持久化的数据库中加载索引
- 提供统一的检索接口和 LLM 格式化输出
"""
import json
import os
import pickle
from typing import List, Dict

import jieba

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from dotenv import load_dotenv

# 确保读取 scripts 目录下的 .env 文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

# 定义停用词表（中英文）
STOP_WORDS = {
    'how', 'to', 'the', 'a', 'an', 'in', 'on', 'of', 'for', 'is', 'are',
    'what', 'use', 'using', 'with', 'from', 'by', 'at', 'this', 'that',
    'and', 'or', 'but', 'if', 'when', 'where', 'why', 'can', 'will',
    'do', 'does', 'did', 'have', 'has', 'had', 'be', 'been', 'being',
    '如何', '怎么', '什么', '的', '了', '是', '在', '使用', '用', '与',
    '和', '或', '但', '如果', '当', '哪里', '为什么', '能', '会',
    '做', '有', '被', '正在', '这', '那', '这个', '那个', '一个'
}

# 路径映射：将 RAG_Lite 中的源文件路径映射到本地 hm-docs 目录
# 返回的路径用于显示，相对于 scripts 目录
PATH_MAPPING: Dict[str, str] = {
    "zh-cn/application-dev/": "hm-docs/ui-dev/",
    "docs/dev-guide/": "hm-docs/syntax/source_zh_cn/",
    "docs/tools/": "hm-docs/tools/source_zh_cn/",
    "std/doc/": "hm-docs/stdlib/std/",
    "doc/": "hm-docs/stdx/libs_stdx/",
    "tools/doc/": "hm-docs/tools/source_zh_cn/",
}


def map_source_file_to_local(source_file: str) -> str:
    """
    将 RAG_Lite 中的源文件路径映射到本地 hm-docs 目录
    返回格式化的路径，作为显示用（相对于 scripts 目录）

    Args:
        source_file: RAG_Lite 中的原始路径，如 "zh-cn/application-dev/arkui-cj/xxx.md"

    Returns:
        本地路径（相对于 scripts 目录），如 "hm-docs/ui-dev/arkui-cj/xxx.md"
    """
    for prefix, local_prefix in PATH_MAPPING.items():
        if source_file.startswith(prefix):
            mapped = source_file.replace(prefix, local_prefix)
            return mapped
    # 没有匹配的映射，返回原始路径
    return source_file


def chinese_tokenizer(text: str) -> List[str]:
    """
    中文分词函数（搜索引擎模式）+ 停用词过滤。
    注意：必须与 Database-Builder.py 中的分词逻辑保持一致！

    过滤规则：
    1. 过滤停用词（中英文）
    2. 过滤纯标点符号
    3. 过滤长度为1的非中文字符
    """
    tokens = jieba.cut_for_search(text)
    filtered_tokens = []

    for token in tokens:
        token_stripped = token.strip()

        # 跳过空字符串
        if not token_stripped:
            continue

        # 转为小写进行停用词检查
        token_lower = token_stripped.lower()

        # 跳过停用词
        if token_lower in STOP_WORDS:
            continue

        # 跳过纯标点符号
        if token_stripped.isspace() or all(not c.isalnum() for c in token_stripped):
            continue

        # 跳过长度为1的非中文字符（保留中文单字）
        if len(token_stripped) == 1 and not ('\u4e00' <= token_stripped <= '\u9fff'):
            continue

        # 统一转为小写，确保大小写不敏感匹配
        filtered_tokens.append(token_lower)

    return filtered_tokens


class CustomEnsembleRetriever:
    """自定义混合检索器，替代 EnsembleRetriever"""

    def __init__(self, retrievers: List, weights: List[float]):
        self.retrievers = retrievers
        self.weights = weights

    def invoke(self, query: str) -> List[Document]:
        """执行混合检索"""
        all_docs = []

        # 从每个检索器获取结果
        for i, retriever in enumerate(self.retrievers):
            try:
                if hasattr(retriever, 'invoke'):
                    docs = retriever.invoke(query)
                elif hasattr(retriever, 'get_relevant_documents'):
                    docs = retriever.get_relevant_documents(query)
                elif hasattr(retriever, 'similarity_search'):
                    docs = retriever.similarity_search(query)
                else:
                    continue

                # 给每个文档添加权重分数
                weight = self.weights[i]
                for j, doc in enumerate(docs):
                    # 简单的分数计算：权重 * (1 / (排名 + 1))
                    score = weight * (1.0 / (j + 1))
                    doc.metadata['_score'] = score
                    all_docs.append(doc)
            except Exception as e:
                print(f"检索器 {i} 出错: {e}")
                continue

        # 按分数排序
        all_docs.sort(key=lambda x: x.metadata.get('_score', 0), reverse=True)
        return all_docs


class CangjieRetriever:
    """仓颉编程语言知识检索器"""

    def __init__(
        self,
        chroma_db_dir: str = "./chroma_db",
        bm25_docs_path: str = "./chroma_db/bm25_documents.pkl",
        collection_name: str = "cangjie_rag_db",
        embedding_model: str = "Qwen/Qwen3-Embedding-8B",
        api_key: str = None,
        base_url: str = None
    ):
        """
        初始化混合检索器

        Args:
            chroma_db_dir: Chroma 向量库目录
            bm25_docs_path: BM25 文档数据文件路径
            collection_name: Chroma 集合名称
            embedding_model: 嵌入模型名称
            api_key: SiliconFlow API Key
            base_url: API 基础URL
        """
        self.chroma_db_dir = chroma_db_dir
        self.bm25_docs_path = bm25_docs_path

        # 检查必要文件是否存在
        if not os.path.exists(chroma_db_dir):
            raise FileNotFoundError(f"向量库目录不存在: {chroma_db_dir}")

        if not os.path.exists(bm25_docs_path):
            raise FileNotFoundError(
                f"BM25 文档数据不存在: {bm25_docs_path}\n"
                f"请先运行 python Database-Builder.py 构建索引"
            )

        # 配置 API Key 和其他参数（从环境变量读取）
        self.vector_enabled = True
        if api_key is None:
            api_key = os.environ.get("SILICONFLOW_API_KEY", "").strip()
        if not api_key or api_key == "YOUR_API_KEY":
            self.vector_enabled = False
            print("[WARNING] 未检测到有效 API Key，将以纯 BM25 关键词模式启动检索器")
        if base_url is None:
            base_url = os.environ.get("SILICONFLOW_API_BASE_URL", "https://api.siliconflow.cn/v1")
        if embedding_model == "Qwen/Qwen3-Embedding-8B":
            embedding_model = os.environ.get("SILICONFLOW_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-8B")

        # 1) 加载 Chroma 向量库 (仅在启用向量时加载)
        if self.vector_enabled:
            print("[LOADING] 正在加载向量库...")
            embeddings = OpenAIEmbeddings(
                model=embedding_model,
                api_key=api_key,
                base_url=base_url
            )

            self.chroma = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=chroma_db_dir
            )
            print("[OK] 向量库加载完成")
        else:
            self.chroma = None

        # 2) 加载 BM25 检索器 (始终加载)
        print("[LOADING] 正在构建 BM25 索引...")
        with open(bm25_docs_path, "rb") as f:
            bm25_documents = pickle.load(f)

        self.bm25_retriever = BM25Retriever.from_documents(
            bm25_documents,
            preprocess_func=chinese_tokenizer
        )
        self.bm25_retriever.k = 6  # BM25 返回候选数量
        print("[OK] BM25 索引构建完成")

        # 3) 组装混合检索器（根据是否启用向量动态配置）
        if self.vector_enabled:
            self.ensemble_retriever = CustomEnsembleRetriever(
                retrievers=[self.chroma.as_retriever(search_kwargs={"k": 6}), self.bm25_retriever],
                weights=[0.4, 0.6]  # 混合权重（向量检索占比40%，BM25 占比60%）
            )
        else:
            self.ensemble_retriever = CustomEnsembleRetriever(
                retrievers=[self.bm25_retriever],
                weights=[1.0]
            )
        print("[OK] 混合检索器初始化完成")

    def query(self, user_input: str, top_k: int = 8) -> List[Document]:
        """
        执行混合检索

        Args:
            user_input: 用户问题
            top_k: 返回的文档数量

        Returns:
            检索到的文档列表
        """
        try:
            # 使用混合检索器获取结果
            results = self.ensemble_retriever.invoke(user_input)

            # 改进的去重和过滤逻辑
            seen_knowledge_points = set()
            unique_results = []

            for doc in results:
                knowledge_point = doc.metadata.get("knowledge_point", "")

                # 跳过空的或重复的知识点
                if not knowledge_point or knowledge_point in seen_knowledge_points:
                    continue

                # 改进的相关性过滤逻辑
                query_keywords = user_input.lower().split()
                knowledge_lower = knowledge_point.lower()

                # 检查关键词匹配
                has_keyword_match = any(keyword in knowledge_lower for keyword in query_keywords if len(keyword) > 1)

                # 分数分析
                score = doc.metadata.get('_score', 0)

                # 高质量结果：前3名的结果
                is_high_quality = score >= 0.15

                # 中等质量结果：但必须有关键词匹配
                is_medium_quality = score >= 0.05 and has_keyword_match

                if is_high_quality or is_medium_quality:
                    seen_knowledge_points.add(knowledge_point)
                    unique_results.append(doc)

                    if len(unique_results) >= top_k:
                        break

            return unique_results

        except Exception as e:
            print(f"[ERROR] 检索过程出错: {e}")
            return []

    def format_for_llm(self, docs: List[Document]) -> str:
        """
        将检索结果格式化为适合 LLM 阅读的 Prompt

        Args:
            docs: 检索到的文档列表

        Returns:
            格式化后的 Prompt 字符串
        """
        if not docs:
            return "未找到相关知识点。"

        formatted_parts = []

        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            knowledge_point = metadata.get("knowledge_point", "未知知识点")

            # 获取文件路径（现在应该是 source_file）
            source_file = metadata.get("source_file", "")
            category = metadata.get("category", "")

            # 映射到本地路径
            local_path = map_source_file_to_local(source_file) if source_file else ""

            # 解析 rag_content_json
            rag_content_json = metadata.get("rag_content_json", "{}")
            try:
                rag_content = json.loads(rag_content_json)
                concept = rag_content.get("concept", "").strip()
                code_example = rag_content.get("code_example", "").strip()
            except (json.JSONDecodeError, AttributeError):
                concept = "概念信息解析失败"
                code_example = ""

            # 构建单个片段
            part = f"=== 参考片段 {i} ===\n"
            part += f"[知识点]: {knowledge_point}\n"

            # 添加来源信息（如果存在）
            if source_file:
                part += f"[来源文件]: {source_file}\n"
            if local_path:
                part += f"[本地路径]: {local_path}\n"
            if category:
                part += f"[分类]: {category}\n"

            part += f"[概念]: {concept}\n"

            if code_example:
                # 修复编码问题：将乱码替换为正确的符号
                code_example = code_example.replace("-\u003e", "=>").replace("\\u003e", "=>")
                part += f"[代码示例]:\n{code_example}\n"
            else:
                part += "[代码示例]: 无\n"

            formatted_parts.append(part)

        return "\n".join(formatted_parts)

    def search_and_format(self, user_input: str, top_k: int = 3) -> str:
        """
        一键检索并格式化（便捷方法）

        Args:
            user_input: 用户问题
            top_k: 返回的文档数量

        Returns:
            格式化后的 Prompt 字符串
        """
        docs = self.query(user_input, top_k)
        return self.format_for_llm(docs)


if __name__ == "__main__":
    # 自测代码
    print("[INIT] 初始化仓颉检索器...")

    try:
        retriever = CangjieRetriever()

        # 测试问题（中英文对比）
        test_questions = [
            "如何创建线程",
            "how to create thread",
            "IncompatiblePackageException 异常怎么处理",
            "how to handle IncompatiblePackageException",
            "仓颉包兼容性检查规则",
            "cangjie package compatibility check rules"
        ]

        for question in test_questions:
            print(f"\n" + "="*60)
            print(f"[SEARCH] 测试问题: {question}")
            print("="*60)

            # 执行检索
            docs = retriever.query(question, top_k=6)
            print(f"[STATS] 检索到 {len(docs)} 个相关文档")

            # 格式化输出
            formatted_result = retriever.format_for_llm(docs)
            print(f"\n[RESULT] 格式化结果:\n{formatted_result}")

    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        print("请确保已运行 python Database-Builder.py 构建索引")
