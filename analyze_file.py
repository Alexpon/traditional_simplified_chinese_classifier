import json
import os
from classify_st import tag_text, load_punctuation
from tcsc_builder import TCSCBuilder

# 設定要分析的 JSON 檔案路徑
filename = 'your-file.json'
JSON_PATH = os.path.join('source_data', filename)

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

    total_counts = {'T': 0, 'S': 0, 'B': 0, 'P': 0}
    #from ipdb import set_trace
    #set_trace()  # 用於除錯，查看 items 結構
    simplified_word = dict()
    for item in items:
        text = item[0]['model_output']
        tagged = tag_text(text, only_simp, only_trad, punctuation)
        for charactor, tag in tagged:
            if tag in total_counts:
                if tag=='S':
                    #print(f"{charactor} in {text}")
                    simplified_word[charactor] = simplified_word.get(charactor, 0) + 1
                total_counts[tag] += 1

    print(f"統計結果：T={total_counts['T']}, S={total_counts['S']}, B={total_counts['B']}, P={total_counts['P']}")
    for char, count in sorted(simplified_word.items(), key=lambda x: x[1], reverse=True):
        print(f"{char}: {count}")