import sys
from typing import Set, Tuple, List

def tag_text(text: str,
             only_simp: Set[str],
             only_trad: Set[str]) -> List[Tuple[str, str]]:
    labels = []
    for ch in text:
        if ch in only_simp:
            labels.append((ch, 'S'))
        elif ch in only_trad:
            labels.append((ch, 'T'))
        else:
            labels.append((ch, 'B'))
    return labels

def load_set(filename: str) -> Set[str]:
    with open(filename, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

if __name__ == '__main__':
    only_simp = load_set('map/only_simp.txt')
    only_trad = load_set('map/only_trad.txt')
    text = input('輸入要判斷的文字：')
    for ch, tag in tag_text(text, only_simp, only_trad):
        print(f'{ch}\t{tag}')