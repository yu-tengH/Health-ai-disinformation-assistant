"""
驗證爬蟲抓到的案例，檢查完整性、去除重複，
並把驗證通過的新案例，正式併入 fact_check_cases/ 資料夾。
1. 格式完整性檢查：確認每個.txt檔案裡，五個必要欄位（案例編號、謠言原文、查核結果、查核理由、來源）都有內容，沒有缺漏
2. 重複資料檢查：因為爬蟲之後會定期重跑，同一篇報告可能被重複抓到，要用「案例編號」判斷這筆資料是不是已經存在於你的fact_check_cases/或之前爬過的資料裡，避免重複的案例塞進向量資料庫
3. 內容長度合理性檢查：例如「查核理由」欄位如果短到只有幾個字，可能代表parse_report()抓取失敗、只抓到片段，這種異常資料應該被標記出來，不要直接混入正式資料庫
"""

import os
import shutil # shutil是Python內建的模組，專門處理「複製、搬移、刪除檔案」這類檔案操作，比自己手動讀取再寫入更簡潔可靠。

SCRAPED_DIR = "scraped_cases"      # 爬蟲抓到的新資料
EXISTING_DIR = "fact_check_cases"  # 目前正式使用的資料庫來源
REQUIRED_FIELDS = ["案例編號", "謠言原文", "查核結果", "查核理由", "來源"]
MIN_CONTENT_LENGTH = 50            # 查核理由至少要有多少字，太短視為異常

def get_existing_ids(existing_dir):
    ids = set()   # set 裡面的元素不會重複。如果你對一個集合add()一個已經存在的值，集合會自動忽略，不會產生重複項目。

    for filename in os.listdir(existing_dir):
        if not filename.endswith(".txt"):
            continue # 只處理.txt檔案，跳過其他

        path = os.path.join(existing_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        for line in content.split("\n"):
            if line.startswith("案例編號："):
                case_id = line.replace("案例編號：", "").strip() # 把前綴文字拿掉，只留下真正的編號值。strip()是去掉前後空白字元
                ids.add(case_id)
                break

    return ids


def check_completeness(file_content):
    for field in REQUIRED_FIELDS:  #只檢查欄位是否符合 REQUIRED_FIELDS
        if field not in file_content:
            return False, f"缺少欄位：{field}"
    return True, "完整性檢查通過"


def check_content_length(file_content):
    for line in file_content.split("\n"):
        if line.startswith("查核理由："):
            reason = line.replace("查核理由：", "").strip()
            if len(reason) < MIN_CONTENT_LENGTH:
                return False, f"查核理由過短（僅{len(reason)}字）"
            return True, "長度檢查通過"
    return False, "找不到查核理由欄位"


def main():
    existing_ids = get_existing_ids(EXISTING_DIR)
    print(f"目前已有 {len(existing_ids)} 筆案例")

    scraped_files = [f for f in os.listdir(SCRAPED_DIR) if f.endswith(".txt")]
    print(f"待驗證的新檔案：{len(scraped_files)} 筆")

    passed = 0
    rejected = 0

    for filename in scraped_files:
        path = os.path.join(SCRAPED_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        case_id = filename.replace(".txt", "")

        if case_id in existing_ids:
            print(f"[跳過] {filename}：已存在，重複資料")
            rejected += 1
            continue

        ok, msg = check_completeness(content)
        if not ok:
            print(f"[擋下] {filename}：{msg}")
            rejected += 1
            continue

        ok, msg = check_content_length(content)
        if not ok:
            print(f"[擋下] {filename}：{msg}")
            rejected += 1
            continue

        print(f"[通過] {filename}")
        passed += 1

    print(f"\n驗證完成：通過 {passed} 筆，擋下 {rejected} 筆")



if __name__ == "__main__":
    main()