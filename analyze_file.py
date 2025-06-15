import json
import os
import csv
from classify_st import analyze_with_mapping_table, load_punctuation, analyze_with_opencc
from tcsc_builder import TCSCBuilder

# 設定要分析的 JSON 檔案路徑
def get_json_path(filename):
    return os.path.join('source_data', filename)

def compare_mapping_opencc(items, only_simp, only_trad, punctuation, csv_path='compare_mapping_opencc.csv'):
    """
    比較 mapping 與 opencc 方法辨識簡體字，並將結果存成 csv。
    """
    mapping_total_counts = {'T': 0, 'S': 0, 'B': 0, 'P': 0}
    opencc_total_counts = {'T': 0, 'S': 0, 'P': 0}
    simplified_word = dict()
    csv_rows = []
    for item in items:
        text = item[0]['model_output']
        tagged = analyze_with_mapping_table(text, only_simp, only_trad, punctuation)
        mapping_simp_chars = [c for c, tag in tagged if tag == 'S']
        mapping_simp_count = len(mapping_simp_chars)
        for char, tag in tagged:
            if tag in mapping_total_counts:
                if tag == 'S':
                    simplified_word[char] = simplified_word.get(char, 0) + 1
                mapping_total_counts[tag] += 1

        # opencc 統計與簡體字清單合併
        opencc_counts, opencc_simp_chars = analyze_with_opencc(text, only_trad, punctuation)
        opencc_simp_count = len(opencc_simp_chars)
        for k in opencc_total_counts:
            opencc_total_counts[k] += opencc_counts[k]

        csv_rows.append({
            'model_output': text,
            'mapping_simplified_chars': ''.join(mapping_simp_chars),
            'mapping_simplified_count': mapping_simp_count,
            'opencc_simplified_chars': ''.join(opencc_simp_chars),
            'opencc_simplified_count': opencc_simp_count
        })

    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['model_output', 'mapping_simplified_chars', 'mapping_simplified_count',
                      'opencc_simplified_chars', 'opencc_simplified_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)

    print(f"[OpenCC] 統計結果：T={opencc_total_counts['T']}, S={opencc_total_counts['S']}, P={opencc_total_counts['P']}")
    print(f"[Mapping] 統計結果：T={mapping_total_counts['T']}, S={mapping_total_counts['S']}, B={mapping_total_counts['B']}, P={mapping_total_counts['P']}")
    for char, count in sorted(simplified_word.items(), key=lambda x: x[1], reverse=True):
        print(f"{char}: {count}")
    print(f"比較結果已輸出至 {csv_path}")

def main():
    # 設定要分析的 JSON 檔案名稱
    filename = 'test.json'  # 可根據需求切換
    JSON_PATH = get_json_path(filename)

    # 初始化簡繁字集與標點符號
    tcsc = TCSCBuilder()
    only_simp, only_trad, _ = tcsc.build_sets()
    punct_path = os.path.join(os.path.dirname(__file__), 'map', 'punctuation.txt')
    punctuation = load_punctuation(punct_path)

    # 讀取 JSON 檔案
    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)

    # 支援 list 或 dict 結構
    items = [data] if isinstance(data, dict) else data

    compare_mapping_opencc(items, only_simp, only_trad, punctuation)

if __name__ == '__main__':
    main()