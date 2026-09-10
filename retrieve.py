"""
從使用者輸入的問題，去 chromadb 向量資料庫裡
檢索出最相關的事實查核案例。
"""

import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "chromadb"
COLLECTION_NAME = "health_misinfo_cases"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 6 # 回傳幾筆最相似的結果，目前6

def search(query, model, collection):
    query_embedding = model.encode([query]).tolist()
    # 將輸入的文字轉換為向量，以python list格式回傳，方便後續送進向量資料庫做檢索
    results = collection.query(            # 這是Chroma提供的查詢方法，作用是「拿一個向量，去資料庫裡找出最相似的幾筆資料」
        query_embeddings=query_embedding,  # Chroma預期你可能一次查詢多個問題，所以要求傳入的是「一份向量清單」，所以是複數
        n_results=TOP_K
    )
    return results                         # 回傳查詢結果， results 裡面包含最相似的案例id、案例文字、相似度分數等資訊

# query：使用者輸入的問題文字（例如「蘋果山楂茶可信嗎？」）
# model：已經載入好的嵌入模型，因為要把query轉成向量，需要用到它
# collection：已經連接好的資料庫collection，因為要拿轉好的向量去裡面搜尋



# 這邊的query 不用FAISS，用HNSW（Hierarchical Navigable Small World，階層式可導航小世界）





# 載入模型、連接資料庫，是「昂貴」的動作（花時間、花記憶體），如果每次呼叫search()都在函式內部重新做一次，會非常沒效率。
# 正確做法是：在main()裡只載入一次模型、只連接一次資料庫，然後把這兩個「已經準備好的工具」當作參數，傳給search()重複使用。
# 這是寫程式很常見的效能考量習慣。
def main():
    print("載入嵌入模型...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME) #跟上一支腳本一樣，載入嵌入模型。這裡有件事要注意：因為你已經下載過這個模型了（上一支腳本執行時已經下載過），這次執行不會重新下載，它會直接用電腦裡的快取，速度會快很多
    
    print("連接向量資料庫...")
    client = chromadb.PersistentClient(path=DB_DIR)  # 連到chromadb資料夾
    collection = client.get_collection(COLLECTION_NAME)
    # create_collection：如果collection已存在會報錯
    # get_collection：如果collection不存在會報錯
    # 所以這裡用get_collection，假設你已經執行過 build_vector_db.py 建立好資料庫了，這裡就直接連接它
    
    
    print("\n輸入問題來搜尋相關案例（輸入 exit 離開）")
    while True:
        query = input("\n> ")       # 作用是暫停程式、等待使用者在終端機打字輸入，括號裡的字串（這裡是"\n> "）會顯示成提示符號
        if query.strip().lower() == "exit":
            break
        # .strip()：把字串前後多餘的空白去掉
        # .lower()：把字串轉成全小寫
        
        results = search(query, model, collection)
        documents = results["documents"][0]
        distances = results["distances"][0]
        
        # 這裡要解釋一下Chroma回傳結果的資料結構
        # results其實是一個字典（dictionary），裡面有好幾個欄位，其中"documents"欄位裝的是「找到的文件內容」。
        # 但因為Chroma的設計是「可能一次查詢多個問題」，所以results["documents"]本身其實是一層清單包著清單（例如：[[案例A, 案例B]]
        # ，最外層對應「第幾個查詢問題」，我們只查一個問題，所以永遠取第0個，也就是[0]）。
        # 取出來之後，documents就會是一份單純的案例文字清單，例如[案例A的內容, 案例B的內容]
        
        print(f"\n找到 {len(documents)} 則相關案例：")
        for doc, dist in zip(documents, distances):
            print(f"\n--- 相似度距離: {dist:.4f} ---")
            print(doc)
        
if __name__ == "__main__":
    main()