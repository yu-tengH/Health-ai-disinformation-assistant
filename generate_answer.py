"""
把 RAG 檢索到的案例，跟使用者問題組合成提示詞，
送進 LoRA 微調過的模型，生成最終回答。
"""
# streamlit run app.py --server.fileWatcherType none


import chromadb
from sentence_transformers import SentenceTransformer
from mlx_lm import load, generate

from retrieve import search

# load：負責載入模型（包含你的LoRA adapter）的函式
# generate：負責根據提示詞生成文字的函式
# from retrieve import search: 從retrieve.py這個檔案裡，把search這個函式借過來用」。

DB_DIR = "chromadb"
COLLECTION_NAME = "health_misinfo_cases"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 2

LLM_MODEL = "mlx-community/gemma-2-2b-it-4bit"
ADAPTER_PATH = "adapters_iter20"

# 有些常數（DB_DIR、COLLECTION_NAME這些）跟retrieve.py裡定義的一模一樣，等於同樣的東西寫了兩次。
# 這確實不是最理想的做法——比較講究的專案會把這些共用常數抽出來，放進一個獨立的config.py檔案，兩支程式都從那裡匯入，避免重複維護。


GENERAL_QUESTION_KEYWORDS = ["理論", "原理", "什麼是", "差別", "區別", "定義", "為什麼", "有沒有幫助", "有沒有用", "有助於", "有效嗎"]


def build_prompt(query, search_results):
    is_general = any(keyword in query for keyword in GENERAL_QUESTION_KEYWORDS)

    if is_general:
        prompt = f"""你是一個健康資訊識讀助理，具備計畫行為理論與AI生成健康假訊息研究的專業知識。

使用者問題：{query}

請直接根據你所學的知識回答這個問題，用你自己的分析講清楚，不要說「根據XX查證」，因為這是一個概念性問題，不是在分析特定案例："""
        return prompt

    documents = search_results["documents"][0]
    context = "\n\n".join(documents)

    prompt = f"""你是一個健康資訊識讀助理，請根據以下查核案例，分析使用者的問題。

參考案例：
{context}

使用者問題：{query}

請根據上述案例的查核邏輯，分析這個問題，並說明理由："""

    return prompt
    


# 載入所有工具
def main():
    print("載入嵌入模型...")
    embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME) # 載入嵌入模型，將問題轉換為向量

    print("連接向量資料庫...")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME) # 連接資料庫，跟retrieve.py一樣的邏輯

    print("載入 LoRA 微調模型...")
    llm_model, tokenizer = load(LLM_MODEL, adapter_path=ADAPTER_PATH) # 告訴它要載入哪個基礎模型
    
    print("\n輸入問題，我會結合真實案例來分析（輸入 exit 離開）")
    
    while True:
        query = input("\n> ")
        if query.strip().lower() == "exit":
            break
        
        if not query.strip():
            print("請輸入問題")
            continue
        search_results = search(query, embed_model, collection)

        prompt = build_prompt(query, search_results)

        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,   # 告訴它「請在最後補上『輪到模型講話了』的提示符號」
            tokenize=False,         # 回傳的是還沒斷詞的純文字
        )
        # 把我們組合好的提示詞，包成模型期待的「訊息」格式——一個字典，標明這是user（使用者）說的話，內容就是我們準備好的完整提示詞
        # 不然我們直接問，沒有照格式會跑不出來
        # tokenizer.apply_chat_template 這是Hugging Face生態系通用的方法，tokenizer知道這個模型的官方對話格式長什麼樣，呼叫這個方法會自動幫你套上正確的特殊符號跟排版

        response = generate(
            llm_model,
            tokenizer,
            prompt=formatted_prompt,
            max_tokens=500,
        )
           # 這是生成回答的核心

        print("\n=== 回答 ===")
        print(response)


if __name__ == "__main__":
    main()