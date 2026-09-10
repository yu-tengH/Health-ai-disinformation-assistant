"""
把 fact_check_cases 資料夾裡的案例文字檔，
轉成向量後存進 Chroma 向量資料庫。
"""
import os # 這個可以看資料夾中有哪些資料，跟作業系統互動
import chromadb # 這個可以用來建立向量資料庫
from sentence_transformers import SentenceTransformer # 這個可以把文字轉成向量

CASE_DIR = "fact_check_cases" # 假資訊案例資料夾
DB_DIR = "chromadb" # 向量資料庫存放的資料夾
COLLECTION_NAME = "health_misinfo_cases" 
# 向量資料庫中 collection 的名稱，collection 可以想成一個chromadb資料庫裡的一個子倉庫，可以分不同種類
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
# 要用來把文字轉成向量的模型名稱，這是Hugging Face上一個公開的模型，支援多國語言（包含中文），等一下執行時程式會自動去下載這個模型回來用

def main():
    print("載入嵌入模型（第一次執行會下載，請稍候）...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("嵌入模型載入完成。")
    
    # 讀取案例檔.txt
    case_files = []
    for f in os.listdir(CASE_DIR):
        if f.endswith(".txt"):
            case_files.append(f)
    case_files.sort() # 排序，按檔名字母順序
    # 確認案例檔是否存在
    if not case_files:
        print(f"在{CASE_DIR}找不到任何 .txt 案例檔，請確認資料夾位置正確。")
        return # 如果沒有案例檔就結束程式，避免繼續跑向量化
    
    documents = [] # 用來存放案例文字
    ids = [] # 用來存放案例檔名，作為向量資料庫的 id，例如 "case_001.txt"
    for filename in case_files:
        path = os.path.join(CASE_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append(content)
            ids.append(filename.replace(".txt", "")) # 去掉 .txt，存成 id，例如case_001.txt變成case_001
    # open(路徑, "r", ...)：Python內建的開檔函式，"r" 代表 read（讀取模式）
    # encoding="utf-8"：這行很重要，不能省略。因為你的案例檔案裡有中文，如果沒指定編碼，某些系統預設編碼可能不是UTF-8，讀中文檔案時會出現亂碼或報錯
    # with ... as f:：這是Python的**「安全開檔」寫法**，好處是：不管後面程式執行順不順利，這個區塊結束後，檔案會自動關閉，你不用自己手動記得寫f.close()。這是業界標準寫法，以後開檔幾乎都會看到這個with語法
    
    
    print(f"共讀到 {len(documents)} 則案例，開始轉成向量...")
    embeddings = model.encode(documents).tolist()
    # 回傳的原始格式是Numpy的陣列（array）格式，不是Python原生的清單（list）格式。
    # 因為等一下Chroma資料庫要求資料要是Python原生的list格式才能吃，所以用.tolist()把它轉換一下型別
    
    # Numpy array 專門設計給數值運算用的，裡面所有元素型別必須一致（例如全部都是浮點數
    # 尤其深度學習裡動輒要處理幾百萬、幾千萬個數字的矩陣運算，如果用list做，會慢到不能忍受，這就是為什麼PyTorch、TensorFlow底層邏輯、還有你之前用的numpy，都是圍繞著這種「陣列」概念設計的
    # sentence-transformers這個套件的作者，在設計.encode()這個方法時，自己決定內部用numpy處理、並且預設回傳numpy array
    # Python list（清單）：通用容器，什麼型別都能裝。靈活但運算效率較差，因為Python要一個一個檢查每個元素的型別再處理
    
    
    print("建立 / 連接 Chroma 資料庫...")
    client = chromadb.PersistentClient(path=DB_DIR)
    # 建立一個跟Chroma資料庫溝通的「客戶端」物件。
    # Persistent（持久性）的意思是，資料庫的內容會真正存在硬碟上（存在DB_DIR，也就是chroma_db這個資料夾）
    # 不是只存在記憶體裡、程式關掉就消失
    
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    # 這是一個防呆機制
    # 如果已經跑將一次，資料庫裡已經有同名的 collection，所以第二次跑的話會先刪掉原先的，避免重複建立
    # 但是若是第一次跑，資料庫裡沒有同名 collection，刪除時就會報錯，所以用 try/except 包起來，若報錯就 pass 掉
    
    
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
    )
    # 正式建立一個新的collection（分類櫃），名字就是我們最上面定義的常數
    # 把資料寫進去。這裡用了「關鍵字參數」的寫法（documents=、embeddings=、ids=），明確指出每份資料該對應到哪個欄位：
    # documents =documents：存原始文字（案例的完整內容）
    # embeddings=embeddings：存對應的向量（剛剛算出來的那批數字）
    # ids=ids：每筆資料的唯一識別碼（case01、case02...）
    
    print(f"完成！已將 {len(documents)} 則案例存進 {DB_DIR}/ 資料庫。")
    print(f"Collection 名稱：{COLLECTION_NAME}")
    
if __name__ == "__main__":
    main()
# 好處是：
# 假設你之後想在另一支程式裡import build_vector_db、只借用它裡面定義好的東西（例如那些常數），
# 但不想要它自動整包重新跑一次向量化流程（因為那樣會很慢，而且可能會重複覆寫你的資料庫），
# 這時候這個判斷式就能保護你——匯入這份檔案本身，不會自動觸發main()執行。
# 只有你真正在終端機打指令執行這份檔案時，main()才會被呼叫。
    
# 如果你在終端機直接打 "python build_vector_db.py" 執行這份檔案，Python會自動把這份檔案的 __name__ 設成字串 "__main__"
# 但如果未來你寫了另一支程式，裡面用 import build_vector_db 去引用這份檔案裡的東西（例如之後你可能想在別的程式裡重複使用這裡定義的某個函式），這時候__name__的值就不會是"__main__"，而是這支檔案的檔名