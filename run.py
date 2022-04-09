import argparse
import csv
import os
import random
import sys
from argparse import ArgumentParser, Namespace
from time import sleep
from tkinter import E
import trace
import traceback
from typing import Dict, List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

USED_LIST = './used.csv'
UNUSED_LIST = './unused.csv'

class MusicForm():
    DEFAULT_INPUT = {
        'song': '',
        'artist': '',
        'target': '',
        'message': '',
        'comment': '',
        'name': ''
    }
    def __init__(self, driver: WebDriver, refresh_url: str):
        self.url = refresh_url
        self.__driver = driver
        self.__driver.implicitly_wait(3)
        self.refresh_element()
        self.reset_field()

    def refresh_element(self):
        self.__driver.get(self.url)
        self.__form = self.__driver.find_element(By.CLASS_NAME, 'fields')
        self._song_field = self.__form.find_element(By.NAME, 'F20')
        self._artist_field = self.__form.find_element(By.NAME, 'F3')
        self._target_field = self.__form.find_element(By.NAME, 'F9')
        self._message_field = self.__form.find_element(By.NAME, 'F1')
        self._comment_field = self.__form.find_element(By.NAME, 'F2')
        self._name_field = self.__form.find_element(By.NAME, 'F4')
        self._submit_button = self.__form.find_element(By.ID, 'btnSubmit')

    def reset_field(self):
        self.song = ''
        self.artist = ''
        self.target = ''
        self.message = ''
        self.comment = ''
        self.name = '匿名'

    def set_song(self, name: str):
        self.song = name
        return self

    def set_artist(self, name: str):
        self.artist = name
        return self

    def set_target(self, name: str):
        self.target = name
        return self

    def set_message(self, msg: str):
        self.message = msg
        return self

    def set_comment(self, comment: str):
        self.comment = comment
        return self

    def set_name(self, name:str = '匿名'):
        self.name = name
        return self

    def submit_form(self, reset: bool = False):
        if self.song == '' and self.artist == '':
            print('Required field not set: song and artist', file=sys.stderr)
            return
        self._song_field.clear()
        self._artist_field.clear()
        self._target_field.clear()
        self._message_field.clear()
        self._comment_field.clear()
        self._name_field.clear()

        self._song_field.send_keys(self.song)
        self._artist_field.send_keys(self.artist)
        self._target_field.send_keys(self.target)
        self._message_field.send_keys(self.message)
        self._comment_field.send_keys(self.comment)
        self._name_field.send_keys(self.name)

        self._submit_button.click()
        if reset:
            self.reset_field()
        self.refresh_element()

class MusicInfoList():
    def __init__(self, unused_path: str, used_path: str) -> None:
        self.unused_path, self.used_path = unused_path, used_path
        self.fieldnames, self.unused = MusicInfoList.read_csv(unused_path)
        _, self.used = MusicInfoList.read_csv(used_path)

    def read_csv(path: str) -> Tuple[List[str], List[Dict]]:
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

    def wrtie_csv(path: str, fieldnames: List[str] , data: List[Dict]) -> None:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def get_one(self, index:int = 0) -> Dict:
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
            music_num = len(self.unused)
            index_list = random.sample(range(music_num), num)
            for index in index_list:
                selected.append(self.get_one(index))
        self.save()
        return selected
    
    def save(self) -> None:
        MusicInfoList.wrtie_csv(self.unused_path, self.fieldnames, self.unused)
        MusicInfoList.wrtie_csv(self.used_path, self.fieldnames, self.used)

def parse_args(args: List[str]) -> argparse.Namespace:
    parser = ArgumentParser(description='Auto submit forms')
    parser.add_argument('-n', '--num', action='store', type=int, default=0, dest='num', help='Sets total submits')
    parser.add_argument('-t', '--interval', action='store', type=float, default=0, dest='interval', help='Sets the wait interval(in seconds) between every submit.')
    parser.add_argument('-p', '--pause', action='store_true', default=False, dest='pause', help='Pauses the program after all submitions complete.')
    parser.add_argument('-r', '--random', action='store_true', default=False, dest='random', help='Randomly selects music from list.')

    if len(args) == 0:
        parser.print_usage()
        exit(0)
    return parser.parse_args(args)

if __name__ == '__main__':
    config = parse_args(sys.argv[1:])

    music_list = MusicInfoList(UNUSED_LIST, USED_LIST)

    if config.random:
        selected_list = music_list.random_get(config.num)
    else:
        selected_list = list(music_list.get_one(0) for i in range(config.num))
        music_list.save()

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    form = MusicForm(driver, 'http://jsform2.com/web/formview/61357bc475a03c55d035e26e')
    try:
        for music_info in selected_list:
            # MUSIC, ARTIST, LINK, MESSAGE, no NAME & TARGET
            form.set_song(music_info['MUSIC']).set_artist(music_info['ARTIST']).\
                set_message(music_info['MESSAGE']).set_comment(music_info['LINK'])
            form.submit_form()
            if config.interval > 0:
                sleep(config.interval)

        if config.pause:
            input('Task finished, press ENTER to continue..')
    except Exception as e:
        traceback.print_exc(e)
    finally:
        driver.quit()
