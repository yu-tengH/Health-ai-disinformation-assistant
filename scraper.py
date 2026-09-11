"""
從台灣事實查核中心，抓取健康相關的查核報告，
整理成跟 fact_check_cases/ 一樣的格式。
"""

import requests    # 發送HTTP請求，去索要網頁內容回來
from bs4 import BeautifulSoup
import os


# classification欄位目前抓到的是英文代碼，將其轉換回中文對應的文字，方便後續使用
CLASSIFICATION_MAP = {
    "incorrect": "錯誤",
    "partially-incorrect": "部分錯誤",
    "insufficient-evidence": "證據不足",
    "correct": "正確",
    "clarification": "事實釐清",
}


LIST_URL = "https://tfc-taiwan.org.tw/fact-check-reports-all/"  # 事實查核中心的健康查核列表頁面
Headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
KEYWORDS = ["健康", "疫苗", "食物", "食品", "藥", "醫", "營養", "瘦身", "保健", "減重", "疾病", "醫療", "中醫", "西醫", "醫院", "診所", "醫師", "藥物", "保健食品"]  
# 篩選健康相關的關鍵字
# headers 裡的 User-Agent 是為了讓網站以為你是一般瀏覽器，而不是程式自動抓取，避免被擋掉


# 找出列表頁裡所有查核報告的網址，並回傳一個清單
def get_report_links(list_url):
    response = requests.get(list_url, headers=Headers) # 真正發送請求，把列表頁的網頁內容下載回來，存進response這個變數。
    soup = BeautifulSoup(response.text, "html.parser")# 下載的內容用BeautifulSoup解析HTML，方便後續抓取特定元素，"html.parser"是告訴BeautifulSoup「請用HTML的規則去理解這份文字」

    reports = []
    # 改成裝字典的清單，而不是單純的網址字串清單，為了幫網址分類如生活、政治、醫療
    # 一份清單裡的每個元素，如果只能裝「一個值」，就沒辦法同時記錄「這篇文章的網址」跟「這篇文章的分類」兩件事。
    for li_tag in soup.find_all("li", class_="kb-query-item"): # 幫我找出所有符合條件的標籤，找出所有<li>標籤
        classes = li_tag.get("class", [])

    # li_tag是BeautifulSoup抓到的一個HTML標籤，而HTML標籤在BeautifulSoup裡，運作起來很像一個字典—
    # 每個標籤的屬性（例如class、href、id這些），可以想成是這個標籤的「key」，屬性的值就是對應的「value」。
    # li_tag.get("class", []) = 去讀取這個標籤的class屬性，如果它有這個屬性，回傳裡面的值；如果沒有這個屬性（有些標籤可能沒設定class），就回傳我指定的預設值，這裡預設值是空清單[]」。
    # 給預設值[]？ 這是一種防呆機制——如果你直接用li_tag["class"]去強制取值，遇到剛好沒有class屬性的標籤，程式會直接報錯中斷。
        report_type = None
        for c in classes:
            if c.startswith("fact-check-report-type-"):
                report_type = c.replace("fact-check-report-type-", "")

        a_tag = li_tag.find("a", href=True)
        if a_tag:
            reports.append({
                "url": a_tag["href"],
                "type": report_type,
            })

    return reports

# 解析單篇查核報告的文章或標題內容，回傳一個字典
def parse_report(url):
    response = requests.get(url, headers=Headers)
    soup = BeautifulSoup(response.text, "html.parser")  # soup.title直接抓到頁面的<title>標籤

    full_title = soup.title.string
    title = full_title.split(" - ")[0].strip() #字串依照「空格-空格」這個分隔符切開，變成一份清單（例如["內容農場...", "台灣事實查核中心"]），[0]取第一個元素，也就是真正的標題

    article_tag = soup.find("article")
    classes = article_tag.get("class", [])

    classification = None
    report_type = None
    for c in classes:
        if c.startswith("fact-check-report-classification-"):
            classification = c.replace("fact-check-report-classification-", "")
        if c.startswith("fact-check-report-type-"):
            report_type = c.replace("fact-check-report-type-", "")

    first_h2 = soup.find("h2")  # 找頁面上第一個<h2>標籤，標題用h2，內容用p標籤，h3是小標題
    content_container = first_h2.find_parent("div", class_="kt-inside-inner-col") 
    # find_parent是「從這個標籤往上找，符合條件的父層容器」
    # 這裡的邏輯是：先找到第一個<h2>，再往上找<div class="kt-inside-inner-col">，這個<div>就是包住所有內文段落的容器

    paragraphs = []
    for tag in content_container.find_all(["p", "h2", "h3"]):
        text = tag.get_text(strip=True) # get_text()，把一個標籤裡面所有的文字內容取出來
        if text:
            paragraphs.append(text) # if text:：防呆，過濾掉抓出來是空字串的標籤（有些<p>可能是空的，只是排版用）

    content = "\n".join(paragraphs) #「拿一份清單，把裡面每個字串元素("a", "bca")接在一起，變成一個大字串，元素跟元素之間，用前面指定的符號填補」。

    return {
        "url": url,
        "title": title,
        "classification": classification,
        "type": report_type,
        "content": content,
    }
    
    
# 儲存爬蟲檔案
def save_report(report, output_dir="scraped_cases"):
    os.makedirs(output_dir, exist_ok=True) # exist_ok=True代表「如果這個資料夾已經存在，不要報錯，直接沿用」

    slug = report["url"].rstrip("/").split("/")[-1]
    filename = f"tfc_{slug}.txt"
    path = os.path.join(output_dir, filename)
    # eport["url"].rstrip("/").split("/")[-1]:這裡從網址裡取出唯一的識別名稱。
    # .rstrip("/")先把網址最尾巴的斜線去掉（避免切割時多一個空字串），.split("/")把網址依照斜線切開變成一份清單
    # ，[-1]取最後一個元素——這是Python的方便寫法，負數索引代表「從尾巴數過來」，-1就是最後一個。
    # 例如網址是.../fact-check-reports/top-10-poisonous-insects-taiwan/，
    # 處理完會得到top-10-poisonous-insects-taiwan

    classification_zh = CLASSIFICATION_MAP.get(report["classification"], report["classification"])

    file_content = f"""案例編號：tfc_{slug}
謠言原文：{report['title']}
查核結果：{classification_zh}
查核理由：{report['content']}
來源：台灣事實查核中心
主題標籤：{report['type']}
        """
        # 謠言原文：{report['title']}不能縮排，不然會多出空格，影響後續向量化的結果

    with open(path, "w", encoding="utf-8") as f:    # "w"（write，寫入模式）
        f.write(file_content)

    return path




def main():
    reports = get_report_links(LIST_URL)
    print(f"抓到 {len(reports)} 篇報告")

    for r in reports:
        detail = parse_report(r["url"])
        saved_path = save_report(detail)
        print(f"已存檔：{saved_path}")


        
if __name__ == "__main__":
    main()