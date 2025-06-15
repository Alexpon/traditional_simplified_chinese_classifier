import os
import requests
import shutil
import zipfile
from typing import Set, Tuple

class TCSCBuilder:
    UNI_URL = 'https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip'
    UNI_LOCAL = os.path.join('raw_data', 'Unihan.zip')
    OPENCC_DICT_URL = 'https://github.com/BYVoid/OpenCC/archive/refs/heads/master.zip'
    OPENCC_DICT_LOCAL = os.path.join('raw_data', 'opencc_master.zip')
    OPENCC_DICT_TARGET = os.path.join('raw_data', 'OpenCC', 'data', 'dictionary')

    def __init__(self):
        pass

    def download_unihan(self):
        os.makedirs('raw_data', exist_ok=True)
        print('Downloading Unihan.zip...')
        r = requests.get(self.UNI_URL, stream=True)
        with open(self.UNI_LOCAL, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print('Unihan.zip updated.')

    def download_opencc_dict(self):
        print('Downloading OpenCC dictionary...')
        r = requests.get(self.OPENCC_DICT_URL, stream=True)
        with open(self.OPENCC_DICT_LOCAL, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        with zipfile.ZipFile(self.OPENCC_DICT_LOCAL) as z:
            dict_prefix = 'OpenCC-master/data/dictionary/'
            for member in z.namelist():
                if member.startswith(dict_prefix) and member.endswith('.txt'):
                    rel_path = member[len(dict_prefix):]
                    target_path = os.path.join(self.OPENCC_DICT_TARGET, rel_path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with z.open(member) as src, open(target_path, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
        print('OpenCC dictionary updated.')
        os.remove(self.OPENCC_DICT_LOCAL)

    def load_unihan_variants(self, unihan_zip: str) -> Tuple[Set[str], Set[str]]:
        simp = set()
        trad = set()
        with zipfile.ZipFile(unihan_zip) as z:
            with z.open('Unihan_Variants.txt') as f:
                for line in f:
                    line = line.decode('utf-8')
                    if line.startswith('#') or not line.strip():
                        continue
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

    def load_opencc_diff(self, opencc_dir: str) -> Tuple[Set[str], Set[str]]:
        simp = set()
        trad = set()
        for filename, is_ts in [("TSCharacters.txt", True), ("STCharacters.txt", False)]:
            path = os.path.join(opencc_dir, filename)
            with open(path, encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
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

    def load_set(self, filename) -> Set[str]:
        s = set()
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    ch = line.strip()
                    if ch:
                        s.add(ch)
        return s

    def build_sets(self) -> Tuple[Set[str], Set[str], Set[str]]:
        map_dir = 'map'
        only_simp_path = os.path.join(map_dir, 'only_simp.txt')
        only_trad_path = os.path.join(map_dir, 'only_trad.txt')
        both_path = os.path.join(map_dir, 'both.txt')
        if all(os.path.exists(p) for p in [only_simp_path, only_trad_path, both_path]):
            only_simp = self.load_set(only_simp_path)
            only_trad = self.load_set(only_trad_path)
            both = self.load_set(both_path)
            return only_simp, only_trad, both
        simp1, trad1 = self.load_unihan_variants(self.UNI_LOCAL)
        simp2, trad2 = self.load_opencc_diff(self.OPENCC_DICT_TARGET)
        only_simp = (simp1 | simp2) - (trad1 | trad2)
        only_trad = (trad1 | trad2) - (simp1 | simp2)
        both = (simp1 | simp2) & (trad1 | trad2)
        return only_simp, only_trad, both

    def save_set(self, filename, s):
        with open(filename, 'w', encoding='utf-8') as f:
            for ch in sorted(s):
                f.write(f'{ch}\n')

    def update_and_save(self):
        self.download_unihan()
        self.download_opencc_dict()
        print('All resources updated.')
        only_simp, only_trad, both = self.build_sets()
        self.save_set(os.path.join('map', 'only_simp.txt'), only_simp)
        self.save_set(os.path.join('map', 'only_trad.txt'), only_trad)
        self.save_set(os.path.join('map', 'both.txt'), both)
        print('Diff files saved: map/only_simp.txt, map/only_trad.txt, map/both.txt')

if __name__ == '__main__':
    tcsc = TCSCBuilder()
    tcsc.update_and_save()
