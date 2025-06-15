import sys
from typing import Set, Tuple, List
from tcsc_builder import TCSCBuilder

# 新增：讀取標點符號清單
import os

def load_punctuation(path: str) -> Set[str]:
    with open(path, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def tag_text(text: str,
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

if __name__ == '__main__':
    tcsc = TCSCBuilder()
    #tcsc.update_and_save()
    only_simp, only_trad, _ = tcsc.build_sets()
    # 新增：載入標點符號清單
    punct_path = os.path.join(os.path.dirname(__file__), 'map', 'punctuation.txt')
    punctuation = load_punctuation(punct_path)
    text = input('輸入要判斷的文字：')
    tagged = tag_text(text, only_simp, only_trad, punctuation)
    for ch, tag in tagged:
        print(f'{ch}\t{tag}')
    
    print('統計結果：')
    count_t = sum(1 for _, tag in tagged if tag == 'T')
    count_s = sum(1 for _, tag in tagged if tag == 'S')
    count_b = sum(1 for _, tag in tagged if tag == 'B')
    count_p = sum(1 for _, tag in tagged if tag == 'P')
    print(f'總計：T={count_t}, S={count_s}, B={count_b}, P={count_p}')