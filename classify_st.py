import sys
from typing import Set, Tuple, List
from tcsc_builder import TCSCBuilder

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

if __name__ == '__main__':
    tcsc = TCSCBuilder()
    #tcsc.update_and_save()
    only_simp, only_trad, _ = tcsc.build_sets()
    text = input('輸入要判斷的文字：')
    for ch, tag in tag_text(text, only_simp, only_trad):
        print(f'{ch}\t{tag}')
        
    print('統計結果：')
    count_t = sum(1 for _, tag in tag_text(text, only_simp, only_trad) if tag == 'T')
    count_s = sum(1 for _, tag in tag_text(text, only_simp, only_trad) if tag == 'S')
    count_b = sum(1 for _, tag in tag_text(text, only_simp, only_trad) if tag == 'B')
    print(f'總計：T={count_t}, S={count_s}, B={count_b}')