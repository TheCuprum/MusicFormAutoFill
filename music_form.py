import time
import sys

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from form_resource import NameProvider

class MusicForm():
    DEFAULT_INPUT = {
        'song': '',
        'artist': '',
        'target': '',
        'message': '',
        'comment': '',
        'name': ''
    }
    __NAME_PROVIDER  = NameProvider()

    def __init__(self, driver: WebDriver, refresh_url: str):
        self.url = refresh_url
        self.name_gen = MusicForm.__NAME_PROVIDER.random_select_name(3)
        self.__driver = driver
        self.__driver.implicitly_wait(3)
        self.refresh_element()
        self.reset_field()

    def refresh_element(self):
        self.__driver.get(self.url)
        self.__form = self.__driver.find_element(By.CLASS_NAME, 'fields')
        self._song_field = self.__form.find_element(By.NAME, 'F1')
        self._artist_field = self.__form.find_element(By.NAME, 'F2')
        self._target_field = self.__form.find_element(By.NAME, 'F3')
        self._message_field = self.__form.find_element(By.NAME, 'F4')
        self._comment_field = self.__form.find_element(By.NAME, 'F5')
        self._name_field = self.__form.find_element(By.NAME, 'F6')
        self._submit_button = self.__driver.find_element(By.ID, 'btnSubmit')

    def reset_field(self):
        self.song = ''
        self.artist = ''
        self.target = ''
        self.message = ''
        self.comment = ''
        self.name = next(self.name_gen)

    def set_song(self, name: str) -> 'MusicForm':
        self.song = name
        return self

    def set_artist(self, name: str) -> 'MusicForm':
        self.artist = name
        return self

    def set_target(self, name: str) -> 'MusicForm':
        self.target = name
        return self

    def set_message(self, msg: str) -> 'MusicForm':
        self.message = msg
        return self

    def set_comment(self, comment: str) -> 'MusicForm':
        self.comment = comment
        return self

    def set_name(self, name:str = None) -> 'MusicForm':
        self.name = next(self.name_gen) if name is None else name
        return self

    def set_name_gen(self, count: int = 3) -> 'MusicForm':
        self.name_gen = count if count > 0 else 0
        return self

    def submit_form(self, reset: bool = False, delay: int = 0):
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

        if delay > 0:
            time.sleep(delay)

        self._submit_button.click()
        if reset:
            self.reset_field()
        else:
            self.refresh_element()