import sys
from typing import Set, Tuple, List
from tcsc_builder import TCSCBuilder
from opencc import OpenCC

# 新增：讀取標點符號清單
import os

def load_punctuation(path: str) -> Set[str]:
    with open(path, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def analyze_with_mapping_table(text: str,
             only_simp: Set[str],
             only_trad: Set[str],
             punctuation: Set[str]) -> List[Tuple[str, str]]:
    labels = []
    for ch in text:
        if ch.isspace():
            continue  # 自動跳過空格和其他空白字元
        if ch in punctuation:
            labels.append((ch, 'P'))
        elif ch in only_simp:
            labels.append((ch, 'S'))
        elif ch in only_trad:
            labels.append((ch, 'T'))
        else:
            labels.append((ch, 'B'))
    return labels

def analyze_with_opencc(text, only_trad, punctuation):
    """
    用 opencc 將 text 轉為繁體，逐字比對，計算簡體、繁體、標點數量，並回傳簡體字清單
    """
    cc = OpenCC('s2t')
    text_trad = cc.convert(text)
    counts = {'T': 0, 'S': 0, 'P': 0}
    simp_chars = []
    for c_ori, c_trad in zip(text, text_trad):
        if c_ori in punctuation:
            counts['P'] += 1
        elif c_ori == c_trad:
            if c_ori in only_trad:
                counts['T'] += 1
        else:
            counts['S'] += 1
            if c_ori not in punctuation:
                simp_chars.append(c_ori)
    return counts, simp_chars

if __name__ == '__main__':
    tcsc = TCSCBuilder()
    #tcsc.update_and_save()
    only_simp, only_trad, _ = tcsc.build_sets()
    # 新增：載入標點符號清單
    punct_path = os.path.join(os.path.dirname(__file__), 'map', 'punctuation.txt')
    punctuation = load_punctuation(punct_path)
    text = input('輸入要判斷的文字：')
    tagged = analyze_with_mapping_table(text, only_simp, only_trad, punctuation)
    for ch, tag in tagged:
        print(f'{ch}\t{tag}')
    
    print('統計結果：')
    count_t = sum(1 for _, tag in tagged if tag == 'T')
    count_s = sum(1 for _, tag in tagged if tag == 'S')
    count_b = sum(1 for _, tag in tagged if tag == 'B')
    count_p = sum(1 for _, tag in tagged if tag == 'P')
    print(f'總計：T={count_t}, S={count_s}, B={count_b}, P={count_p}')