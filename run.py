
import time
import argparse
import random
import sys
from argparse import ArgumentParser
import traceback
from typing import List
import requests

from form_resource import NameProvider, MusicInfoList


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = ArgumentParser(description='Auto submit forms')
    parser.add_argument('-n', '--num', action='store', type=int,
                        default=0, dest='num', help='Sets total submits')
    parser.add_argument('-t', '--interval', action='store', type=float, default=3,
                        dest='interval', help='Sets the wait interval(in seconds) between every submit.')
    parser.add_argument('-p', '--pause', action='store_true', default=False,
                        dest='pause', help='Pauses the program after all submitions complete.')
    parser.add_argument('-r', '--random', action='store_true', default=False,
                        dest='random', help='Randomly selects music from list.')

    if len(args) == 0:
        parser.print_usage()
        exit(0)
    return parser.parse_args(args)


if __name__ == '__main__':
    config = parse_args(sys.argv[1:])

    url = "http://yingkebao.top/web/formview/631157e575a03c5b5f4cb078"
    # url = 'http://jsform2.com/web/formview/61357bc475a03c55d035e26e'
    music_list = MusicInfoList()
    name_provider = NameProvider().random_select_name(5)

    if config.random:
        selected_list = music_list.random_get(config.num)
    else:
        selected_list = list(music_list._get_one(0) for _ in range(config.num))
        music_list.save()

    index = 0
    length = len(selected_list)
    while index < length:
        music_info = selected_list[index]
        form_data = {
            'F1': music_info['MUSIC'],
            'F2': music_info['ARTIST'],
            'F3': "",
            'F4': music_info['MESSAGE'],
            'F5': music_info['LINK'] if random.randrange(10) > 0 else '',
            'F6': next(name_provider) if random.randrange(5) > 0 else '匿名',
            'FRMID': "631157e575a03c5b5f4cb078",
            'INITTIME': round(time.time() * 1000),
            'SECKEY': "",
            'TMOUT_number': random.randrange(30, 200)
        }

        # proxies = urllib.request.getproxies()
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            # 'Origin': 'http://yingkebao.top'
        }
        try:
            response = requests.post(
                url,
                headers=headers,
                json=form_data,
                # proxies=proxies
            )
            response.close()

            index += 1
            if config.interval > 0:
                time.sleep((random.random() + 1.0) / 2)

        except Exception as e:
            traceback.print_exc(e)
            input(f'error occured at index={index}:')

        if config.pause:
            input('Task finished, press ENTER to continue..')
