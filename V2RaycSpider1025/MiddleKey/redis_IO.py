import random
import time
from datetime import datetime

import redis
from config import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, REDIS_DB, REDIS_KEY_NAME_BASE, TIME_ZONE_CN, TIME_ZONE_NY

REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')


class RedisClient_v2(object):
    """redis connection client of v2rayc_spider"""

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, **kwargs):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True, db=db, **kwargs, )
        self.__prepare__()

    def get(self, key_name, retry=0):
        attention_link = self.db.rpop(key_name)
        if attention_link:
            return attention_link
        else:
            if retry >= 3:
                return None
            retry += 1
            self.get(key_name, retry)

    def add(self, key_name, value_of_link_attr, life_cycle=0):
        self.db.lpush(key_name, value_of_link_attr)

    def __prepare__(self, ):
        """初始化环境，当前版本默认弃用，未来将用于分布式锁设计"""

        for x in ['ssr', 'v2ray', 'trojan']:
            if self.db.llen(REDIS_KEY_NAME_BASE.format(x)) == 0:
                self.db.lpush(REDIS_KEY_NAME_BASE.format(x), '')

    def test(self):
        if self.db.ping():
            return 'V2Ray云彩姬'

    def __len__(self, key_name):
        return self.db.llen(name=key_name)

    def kill(self):
        self.db.close()

    def get_driver(self) -> redis.StrictRedis:
        return self.db


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, **kwargs):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True, db=db, **kwargs, )
        self.subscribe = ''

    def add(self, key_name, subscribe, life_cycle: str):
        try:
            self.db.hset(key_name, subscribe, life_cycle)
        finally:
            self.kill()

    def get(self, key_name, ) -> str or bool:
        try:
            while True:
                target_raw: dict = self.db.hgetall(key_name)
                try:
                    self.subscribe, end_life = list(target_raw.items()).pop(0)
                    if self.check_stale(end_life):
                        continue
                    else:
                        return self.subscribe
                except IndexError as e:
                    return None
                finally:
                    self.db.hdel(key_name, self.subscribe)
        finally:
            self.kill()

    def refresh(self, deploy=False):

        def data_cleaning():
            class_list = ['v2ray', 'ssr', 'trojan']
            for class_ in class_list:
                key_name = REDIS_KEY_NAME_BASE.format(class_)
                if self.db.hlen(key_name) != 0:
                    for item, end_life in self.db.hgetall(key_name).items():
                        if self.check_stale(end_life, class_):
                            print(f'del-({class_})--{item}')
                            self.db.hdel(key_name, item)
        if deploy:
            data_cleaning()

    @staticmethod
    def check_stale(item, class_='') -> bool:
        if isinstance(item, str):
            # Expiration time of the subscribe
            check_item = datetime.fromisoformat(item)
            # Shanghai time now
            check_now = datetime.fromisoformat(str(datetime.now(TIME_ZONE_CN)).split('.')[0])
            if check_item >= check_now:
                # survive
                return False
            else:
                # stale
                return True

    def __len__(self, key_name) -> int:
        return self.db.hlen(key_name)

    def kill(self):
        self.db.close()

    def test(self) -> str:
        if self.db.ping():
            return '欢迎使用v2ray云彩姬'

    def get_driver(self) -> redis.StrictRedis:
        return self.db


if __name__ == '__main__':
    print(RedisClient().test())
