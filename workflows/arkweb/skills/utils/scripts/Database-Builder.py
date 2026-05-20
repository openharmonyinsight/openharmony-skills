"""
LangChain 操控 -> Chroma 存储 -> Document (数据) + Embeddings (由 Qwen 生成的向量)。
LangChain 操控 -> BM25Retriever 索引 -> Document (原始文本数据)。
"""
import json
import os
import pickle
from typing import List, Dict, Tuple

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
    # 英文停用词
    'how', 'to', 'the', 'a', 'an', 'in', 'on', 'of', 'for', 'is', 'are',
    'what', 'use', 'using', 'with', 'from', 'by', 'at', 'this', 'that',
    'and', 'or', 'but', 'if', 'when', 'where', 'why', 'can', 'will',
    'do', 'does', 'did', 'have', 'has', 'had', 'be', 'been', 'being',
    # 中文停用词
    '如何', '怎么', '什么', '的', '了', '是', '在', '使用', '用', '与',
    '和', '或', '但', '如果', '当', '哪里', '为什么', '能', '会',
    '做', '有', '被', '正在', '这', '那', '这个', '那个', '一个'
}


def load_kb_json_files(kb_dir: str) -> List[Dict]:
    """读取知识库目录下所有 JSON 文件并合并为一个列表。"""
    if not os.path.isdir(kb_dir):
        raise FileNotFoundError(f"知识库目录不存在: {kb_dir}")

    all_items: List[Dict] = []
    for name in os.listdir(kb_dir):
        if not name.lower().endswith(".json"):
            continue
        file_path = os.path.join(kb_dir, name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "knowledge_base" in data:
                data = data["knowledge_base"]
            if not isinstance(data, list):
                raise ValueError(f"文件格式不正确，期望 JSON 数组: {file_path}")
            all_items.extend(data)
    if not all_items:
        raise ValueError(f"知识库目录为空或没有有效 JSON: {kb_dir}")
    return all_items


def _sanitize_metadata(payload: Dict) -> Dict:
    """过滤掉 Chroma 不支持的复杂类型（仅保留基础类型）。"""
    allowed = (str, int, float, bool, type(None))
    return {k: v for k, v in payload.items() if isinstance(v, allowed)}


def _serialize_for_metadata(item: Dict) -> Dict:
    """
    将复杂字段序列化进 metadata，避免丢失关键信息。
    - rag_content / trigger_keywords 以 JSON 字符串形式保存
    - source_file 也以单独字段保存，便于后续定位文档
    """
    meta = _sanitize_metadata(item.copy())
    if "rag_content" in item:
        meta["rag_content_json"] = json.dumps(item["rag_content"], ensure_ascii=False)
    if "trigger_keywords" in item:
        meta["trigger_keywords_json"] = json.dumps(item["trigger_keywords"], ensure_ascii=False)
    # 确保 source_file 被保留（它应该已经是字符串类型）
    if "source_file" in item and item["source_file"]:
        # source_file 使用正斜杠替换反斜杠，便于跨平台
        meta["source_file"] = item["source_file"].replace("\\", "/")
    return meta


def process_data_for_indexing(json_data: List[Dict]) -> Tuple[List[Document], List[Document]]:
    """
    输入：原始 JSON 列表
    输出：(BM25文档列表, 向量文档列表)
    """
    bm25_docs: List[Document] = []
    vector_docs: List[Document] = []

    for item in json_data:
        # Chroma metadata 只接受基础类型，列表等复杂类型会报错
        # 这里把复杂字段序列化进 metadata，避免 BM25 命中后拿不到完整信息
        meta_payload = _serialize_for_metadata(item)
        keywords_str = " ".join(item.get("trigger_keywords", []))
        bm25_content = f"{item.get('category', '')} {item.get('knowledge_point', '')} {keywords_str}"

        bm25_doc = Document(
            page_content=bm25_content,  # <- 这里就是 BM25 的匹配内容
            metadata=meta_payload
        )
        bm25_docs.append(bm25_doc)

        # chroma的匹配内容：document = concept + code_example
        rag_content = item.get("rag_content", {})
        vector_content = f"{rag_content.get('concept', '')}\n{rag_content.get('code_example', '')}"

        vector_doc = Document(
            page_content=vector_content,# <- 这里就是向量的匹配内容
            metadata=meta_payload
        )
        vector_docs.append(vector_doc)

    return bm25_docs, vector_docs


def chinese_tokenizer(text: str) -> List[str]:
    """
    中文分词函数（搜索引擎模式）+ 停用词过滤。
    注意：必须与 ask_cangjie.py 中的分词逻辑保持一致！

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


# === 重建数据库开关===
REBUILD_VECTOR_DB = False  # 设置为 True 以重新构建数据库
REBUILD_BM25_INDEX = False


def build_indexes(
    kb_dir: str = "./RAG_Lite",
    collection_name: str = "cangjie_rag_db",
    persist_directory: str = "./chroma_db",
    embedding_model: str = "Qwen/Qwen3-Embedding-8B",
    api_key: str | None = None,
    base_url: str | None = None,
    force_rebuild_vector: bool = False,
    force_rebuild_bm25: bool = False
) -> None:
    """从知识库目录构建向量索引与BM25索引。"""
    bm25_cache_path = os.path.join(persist_directory, "bm25_documents.pkl")

    # 从环境变量读取 API 配置
    vector_enabled = True
    if api_key is None:
        api_key = os.environ.get("SILICONFLOW_API_KEY", "").strip()
    if base_url is None:
        base_url = os.environ.get("SILICONFLOW_API_BASE_URL", "https://api.siliconflow.cn/v1")
    if embedding_model == "Qwen/Qwen3-Embedding-8B":
        embedding_model = os.environ.get("SILICONFLOW_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-8B")
    if not api_key or api_key == "YOUR_API_KEY":
        vector_enabled = False
        print("[WARNING] 缺少 API Key，跳过 Chroma 向量库构建，仅构建 BM25 索引")

    # 4) 构建向量库（Chroma）
    # 初始化嵌入模型客户端
    chroma_db_path = os.path.join(persist_directory, "chroma.sqlite3")
    if vector_enabled:
        embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key,
            base_url=base_url
        )
        # 如果向量库已存在，则直接加载，避免每次重建
        if os.path.exists(chroma_db_path) and not force_rebuild_vector:
            Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=persist_directory
            )
            print("[OK] 向量索引已存在，直接加载")
        else:
            # 1) 读取知识库 JSON 数据
            raw_data = load_kb_json_files(kb_dir)
            # 2) 生成 BM25 文档与向量文档
            bm25_documents, vector_documents = process_data_for_indexing(raw_data)

            # 重建时先清空旧集合，避免重复条目
            if os.path.exists(chroma_db_path):
                import shutil
                shutil.rmtree(persist_directory)
                print("已清空旧向量库")

            # 把你的文档向量化并写入本地向量库
            Chroma.from_documents(
                documents=vector_documents,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=persist_directory
            )
            print("向量索引构建完成！")
    # 5) 构建 BM25 索引（关键词检索）
    # 中文检索需要分词，这里显式使用 jieba 解决中文分词问题
    if os.path.exists(bm25_cache_path) and not force_rebuild_bm25:
        with open(bm25_cache_path, "rb") as f:
            bm25_documents = pickle.load(f)
        bm25_retriever = BM25Retriever.from_documents(
            bm25_documents,
            preprocess_func=chinese_tokenizer
        )
        print("[OK] 关键词索引已存在，直接加载")
    else:
        # 若向量库存在但 BM25 缓存不存在，需要读取知识库生成
        raw_data = load_kb_json_files(kb_dir)
        bm25_documents, _ = process_data_for_indexing(raw_data)
        bm25_retriever = BM25Retriever.from_documents(
            bm25_documents,
            preprocess_func=chinese_tokenizer
        )
        os.makedirs(persist_directory, exist_ok=True)
        with open(bm25_cache_path, "wb") as f:
            pickle.dump(bm25_documents, f)
        print("[OK] 关键词索引构建完成并已持久化")

    bm25_retriever.k = 5


if __name__ == "__main__":
    # 使用基于脚本目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_indexes(
        kb_dir=os.path.join(script_dir, "RAG_Lite"),
        persist_directory=os.path.join(script_dir, "chroma_db"),
        force_rebuild_vector=REBUILD_VECTOR_DB,
        force_rebuild_bm25=REBUILD_BM25_INDEX
    )
