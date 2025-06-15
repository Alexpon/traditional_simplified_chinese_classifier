import json
import os
from classify_st import tag_text, load_punctuation
from tcsc_builder import TCSCBuilder
from opencc import OpenCC

# 設定要分析的 JSON 檔案路徑
filename = 'test.json'  # 可以替換成其他檔案名稱
JSON_PATH = os.path.join('source_data', filename)

def analyze_with_opencc(text, only_trad, punctuation):
    """
    用 opencc 將 text 轉為繁體，逐字比對，計算簡體、繁體、標點數量
    """
    cc = OpenCC('s2t')
    text_trad = cc.convert(text)
    counts = {'T': 0, 'S': 0, 'P': 0}
    for c_ori, c_trad in zip(text, text_trad):
        if c_ori in punctuation:
            counts['P'] += 1
        elif c_ori == c_trad:
            # 若原字與轉換後相同且在 only_trad，視為繁體
            if c_ori in only_trad:
                counts['T'] += 1
            # 其他情況不計
        else:
            # 原字與轉換後不同，視為簡體
            counts['S'] += 1
    return counts

if __name__ == '__main__':
    # 初始化簡繁字集與標點符號
    tcsc = TCSCBuilder()
    only_simp, only_trad, _ = tcsc.build_sets()
    punct_path = os.path.join(os.path.dirname(__file__), 'map', 'punctuation.txt')
    punctuation = load_punctuation(punct_path)

    # 讀取 JSON 檔案
    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)

    # 支援 list 或 dict 結構
    if isinstance(data, dict):
        items = [data]
    else:
        items = data

    mapping_total_counts = {'T': 0, 'S': 0, 'B': 0, 'P': 0}
    opencc_total_counts = {'T': 0, 'S': 0, 'P': 0}
    simplified_word = dict()
    for item in items:
        text = item[0]['model_output']
        tagged = tag_text(text, only_simp, only_trad, punctuation)
        for charactor, tag in tagged:
            if tag in mapping_total_counts:
                if tag=='S':
                    #print(f"{charactor} in {text}")
                    simplified_word[charactor] = simplified_word.get(charactor, 0) + 1
                mapping_total_counts[tag] += 1

        # 累加 opencc 統計
        opencc_counts = analyze_with_opencc(text, only_trad, punctuation)
        for k in opencc_total_counts:
            opencc_total_counts[k] += opencc_counts[k]

    print(f"[OpenCC] 統計結果：T={opencc_total_counts['T']}, S={opencc_total_counts['S']}, P={opencc_total_counts['P']}")
    print(f"[Mapping] 統計結果：T={mapping_total_counts['T']}, S={mapping_total_counts['S']}, B={mapping_total_counts['B']}, P={mapping_total_counts['P']}")
    for char, count in sorted(simplified_word.items(), key=lambda x: x[1], reverse=True):
        print(f"{char}: {count}")