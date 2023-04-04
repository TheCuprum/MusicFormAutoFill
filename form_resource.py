import csv
import os
import random
from typing import List, Tuple, Dict

USED_LIST = './used.csv'
UNUSED_LIST = './unused.csv'
NAME_DIR = './name'

class NameProvider():
    def __init__(self, name_dir: str = NAME_DIR) -> None:
        self._name_dict = {}
        self.counter = 1
        for subdir in os.listdir(name_dir):
            name, ext = os.path.splitext(subdir)
            if ext == '.txt':
                name_list = NameProvider._read_name_file(os.path.join(NAME_DIR, subdir))
                self._name_dict[name] = name_list

    def _read_name_file(path: str) -> List[str]:
        with open(path, 'r', encoding='utf-8') as name_file:
            name_list = []
            for line in name_file:
                if line != '\n': name_list.append(line.replace('\n', ''))
        return name_list

    def random_select_name(self, count: int):
        while True:
            keys = list(self._name_dict.keys())
            index_1 = random.randrange(len(keys))
            key = keys[index_1]
            index_2 = random.randrange(len(self._name_dict[key]))
            name = self._name_dict[key][index_2]
            for i in range(count):
                yield name

class MusicInfoList():
    def __init__(self, unused_path: str = UNUSED_LIST, used_path: str = USED_LIST) -> None:
        self.unused_path, self.used_path = unused_path, used_path
        self.fieldnames, self.unused = MusicInfoList._read_csv(unused_path)
        _, self.used = MusicInfoList._read_csv(used_path)

    def _read_csv(path: str) -> Tuple[List[str], List[Dict]]:
        info = []
        fieldnames = []
        if not os.path.exists(path):
            open(path, 'w').close()
        else:
            with open(path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                for info_dict in reader:
                    info.append(info_dict)
        return (fieldnames, info)

    def _wrtie_csv(path: str, fieldnames: List[str] , data: List[Dict]) -> None:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def _get_one(self, index:int = 0) -> Dict:
        music_info = self.unused.pop(index)
        self.used.append(music_info)
        return music_info

    def random_get(self, num: int) -> List[Dict]:
        selected = []
        if num >= len(self.unused):
            random.shuffle(self.unused)
            selected = self.unused.copy()
            self.used.extend(self.unused)
            self.unused.clear()
        else:
            for i in range(num):
                music_num = len(self.unused)
                index = random.randrange(music_num)
                selected.append(self._get_one(index))
                music_num -= 1
        self._save()
        return selected
    
    def _save(self) -> None:
        MusicInfoList._wrtie_csv(self.unused_path, self.fieldnames, self.unused)
        MusicInfoList._wrtie_csv(self.used_path, self.fieldnames, self.used)
