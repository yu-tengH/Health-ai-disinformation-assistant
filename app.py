
"""
製作網頁幫助問答
"""
# 執行：streamlit run app.py

import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from mlx_lm import load, generate
import mlx.core as mx

from retrieve import search
from generate_answer import build_prompt  # 重用之前寫好的函式
from concurrent.futures import ThreadPoolExecutor

DB_DIR = "chromadb"
COLLECTION_NAME = "health_misinfo_cases"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 2

LLM_MODEL = "mlx-community/gemma-2-2b-it-4bit"
ADAPTER_PATH = "adapters_iter20"

@st.cache_resource
def get_mlx_executor():
    return ThreadPoolExecutor(max_workers=1)

@st.cache_resource
def load_models():
    print("開始載入嵌入模型...")
    embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("嵌入模型載入完成")

    print("連接向量資料庫...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)
    print("資料庫連接完成")

    print("開始載入 LoRA 模型（這步通常最花時間）...")

    def _load_in_thread():
        return load(LLM_MODEL, adapter_path=ADAPTER_PATH)

    llm_model, tokenizer = get_mlx_executor().submit(_load_in_thread).result()
    print("LoRA 模型載入完成")

    return embed_model, collection, llm_model, tokenizer

def main():
    st.title("健康假訊息識讀助理")  #標題
    st.caption("結合碩士論文研究發現與 RAG 檢索，分析可疑的健康資訊") #次、小型標題

    embed_model, collection, llm_model, tokenizer = load_models() # 有@st.cache_resource保護，就算main()被重跑很多次，這個函式內部真正的載入動作只會發生一次

    query = st.text_input("請輸入想分析的健康資訊：") # 輸入匡

    if query: # 防呆用，只有當使用者真的有輸入內容時，才執行底下的檢索跟生成
        results = search(query, embed_model, collection)
        prompt = build_prompt(query, results)

        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False,
        )

        
        with st.spinner("分析中..."):   # 顯示一個轉圈圈的等待動畫
            def _generate_in_thread():
                return generate(
                    llm_model,
                    tokenizer,
                    prompt=formatted_prompt,
                    max_tokens=500,
                )

            response = get_mlx_executor().submit(_generate_in_thread).result()

        st.subheader("分析結果") # 顯示一個中型標題
        st.write(response) # 把模型生成的回答，顯示在網頁上

if __name__ == "__main__":
    main()