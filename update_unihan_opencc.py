import os
import requests
import zipfile
import shutil
from sets_builder import build_sets
from ipdb import set_trace  

# 下載 Unihan.zip
UNI_URL = 'https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip'
UNI_LOCAL = os.path.join('raw_data', 'Unihan.zip')


def download_unihan():
    os.makedirs('raw_data', exist_ok=True)
    print('Downloading Unihan.zip...')
    r = requests.get(UNI_URL, stream=True)
    with open(UNI_LOCAL, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print('Unihan.zip updated.')

# 下載 OpenCC 字典檔
OPENCC_DICT_URL = 'https://github.com/BYVoid/OpenCC/archive/refs/heads/master.zip'
OPENCC_DICT_LOCAL = os.path.join('raw_data', 'opencc_master.zip')
OPENCC_DICT_TARGET = os.path.join('raw_data', 'OpenCC', 'data', 'dictionary')

def download_opencc_dict():
    print('Downloading OpenCC dictionary...')
    r = requests.get(OPENCC_DICT_URL, stream=True)
    with open(OPENCC_DICT_LOCAL, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    with zipfile.ZipFile(OPENCC_DICT_LOCAL) as z:
        dict_prefix = 'OpenCC-master/data/dictionary/'
        for member in z.namelist():
            if member.startswith(dict_prefix) and member.endswith('.txt'):
                rel_path = member[len(dict_prefix):]
                target_path = os.path.join(OPENCC_DICT_TARGET, rel_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with z.open(member) as src, open(target_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
    print('OpenCC dictionary updated.')
    os.remove(OPENCC_DICT_LOCAL)

if __name__ == '__main__':
    #download_unihan()
    #download_opencc_dict()
    print('All resources updated.')


    only_simp, only_trad, both = build_sets(UNI_LOCAL, OPENCC_DICT_TARGET)
    def save_set(filename, s):
        with open(filename, 'w', encoding='utf-8') as f:
            for ch in sorted(s):
                f.write(f'{ch}\n')
    save_set(os.path.join('map', 'only_simp.txt'), only_simp)
    save_set(os.path.join('map', 'only_trad.txt'), only_trad)
    save_set(os.path.join('map', 'both.txt'), both)
    print('Diff files saved: map/only_simp.txt, map/only_trad.txt, map/both.txt')
