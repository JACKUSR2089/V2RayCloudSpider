import requests
from config import NGINX_SUBSCRIBE_PATH, REDIS_KEY_NAME_BASE


class Defender(object):
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.subscribe = ''

    def run(self) -> bool or str:
        v2ray_link = requests.get(NGINX_SUBSCRIBE_PATH.format(self.task_name)).text
        self.subscribe = v2ray_link if 'http' in v2ray_link else False
        return self.subscribe

    @staticmethod
    def search(redis_driver) -> list:
        target_list = []
        for task_name in ['v2ray', 'ssr', 'trojan']:
            target = list(redis_driver.hgetall(REDIS_KEY_NAME_BASE.format(task_name)).items())
            target_list += [''.center(2, ' ').join([i[-1], '{}'.format(task_name), i[0]]) for i in
                            target]
        return target_list
