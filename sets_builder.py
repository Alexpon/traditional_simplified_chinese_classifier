import zipfile
import os
from typing import Set, Tuple

def load_unihan_variants(unihan_zip: str) -> Tuple[Set[str], Set[str]]:
    simp = set()
    trad = set()
    with zipfile.ZipFile(unihan_zip) as z:
        with z.open('Unihan_Variants.txt') as f:
            for line in f:
                line = line.decode('utf-8')
                if line.startswith('#') or not line.strip():
                    continue
                # split by both tab and space, then filter out empty strings
                parts = [p for p in line.strip().replace('\t', ' ').split(' ') if p]
                if len(parts) < 3:
                    continue
                code, tag, value = parts[:3]
                if tag == 'kSimplifiedVariant':
                    trad.add(chr(int(code[2:], 16)))
                    for v in value.split(' '):
                        if v.startswith('U+'):
                            simp.add(chr(int(v[2:], 16)))
                elif tag == 'kTraditionalVariant':
                    simp.add(chr(int(code[2:], 16)))
                    for v in value.split(' '):
                        if v.startswith('U+'):
                            trad.add(chr(int(v[2:], 16)))
    return simp, trad

def load_opencc_diff(opencc_dir: str) -> Tuple[Set[str], Set[str]]:
    simp = set()
    trad = set()
    for filename, is_ts in [("TSCharacters.txt", True), ("STCharacters.txt", False)]:
        path = os.path.join(opencc_dir, filename)
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                # split by both tab and space, then filter out empty strings
                parts = [p for p in line.strip().replace('\t', ' ').split(' ') if p]
                if len(parts) < 2:
                    continue
                if is_ts:
                    t, s = parts[:2]
                else:
                    s, t = parts[:2]
                trad.add(t)
                simp.add(s)
    return simp, trad

def build_sets(unihan_zip: str, opencc_dir: str) -> Tuple[Set[str], Set[str], Set[str]]:
    simp1, trad1 = load_unihan_variants(unihan_zip)
    simp2, trad2 = load_opencc_diff(opencc_dir)
    only_simp = (simp1 | simp2) - (trad1 | trad2)
    only_trad = (trad1 | trad2) - (simp1 | simp2)
    both = (simp1 | simp2) & (trad1 | trad2)
    return only_simp, only_trad, both
