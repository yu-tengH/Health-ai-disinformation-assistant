"""
把 thesis_qa_dataset.jsonl (instruction/input/output 格式)
轉成 mlx-lm LoRA 訓練要求的格式 (messages 對話格式)，
並自動切成 train.jsonl / valid.jsonl，存到 data/ 資料夾裡。

使用方式：
    python convert_dataset.py

前提：thesis_qa_dataset.jsonl 要跟這支程式放在同一個資料夾。
"""

import json
import random

# ---- 可調整的參數 ----
SOURCE_FILE = "thesis_qa_dataset.jsonl"
OUTPUT_DIR = "data"
VALID_RATIO = 0.2   # 20% 資料拿去當驗證集，其餘當訓練集
SEED = 42             # 固定亂數種子，確保每次切分結果一樣，方便重現

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 讀取原始資料
    records = []
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    print(f"讀到 {len(records)} 筆原始資料")

    # 轉換格式：instruction/input/output -> messages (user/assistant)
    converted = []
    for r in records:
        question = r["instruction"]
        if r.get("input"):  # 如果有 input，接在 instruction 後面一起當作使用者提問
            question = f"{question}\n\n{r['input']}"
        converted.append({
            "messages": [
                {"role": "user", "content": question},
                {"role": "assistant", "content": r["output"]},
            ]
        })

    # 洗牌後切分 train / valid
    random.seed(SEED)
    random.shuffle(converted)

    valid_count = max(1, int(len(converted) * VALID_RATIO))
    valid_set = converted[:valid_count]
    train_set = converted[valid_count:]

    # 寫出檔案
    def write_jsonl(path, data):
        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    write_jsonl(os.path.join(OUTPUT_DIR, "train.jsonl"), train_set)
    write_jsonl(os.path.join(OUTPUT_DIR, "valid.jsonl"), valid_set)

    print(f"訓練集：{len(train_set)} 筆 -> {OUTPUT_DIR}/train.jsonl")
    print(f"驗證集：{len(valid_set)} 筆 -> {OUTPUT_DIR}/valid.jsonl")
    print("轉換完成！")

if __name__ == "__main__":
    main()
