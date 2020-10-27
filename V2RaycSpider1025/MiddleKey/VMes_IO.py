from spiderNest.preIntro import *
from MiddleKey.redis_IO import RedisClient
from config import SYS_AIRPORT_INFO_PATH, REDIS_KEY_NAME_BASE, NGINX_SUBSCRIBE_PATH
import threading
import sys


def save_login_info(subscribe, class_, life_cycle: str):
    """
    :param life_cycle:
    :param subscribe:
    :param class_:v2ray, ssr, trojan
    """
    # Redis loaded
    # RedisClient().add(key_name=REDIS_KEY_NAME_BASE.format(class_), subscribe=subscribe)
    threading.Thread(target=RedisClient().add, args=(REDIS_KEY_NAME_BASE.format(class_), subscribe, life_cycle)).start()

    # Static data loaded
    with open(SYS_AIRPORT_INFO_PATH, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 入库时间，Vmess,初始化状态:0
        writer.writerow(['{}'.format(life_cycle), '{}'.format(subscribe), class_, '0'])

    # Depolyment mode --> nginx
    if 'linux' in sys.platform:
        try:
            with open(NGINX_SUBSCRIBE_PATH.format(class_), 'w', encoding='utf-8') as f:
                f.write(subscribe)
        except FileNotFoundError as e:
            print(e)


def vmess_IO(class_):
    """
    获取可用订阅链接并刷新存储池
    class_: ssr ; v2ray
    """

    def refresh_log(dataFlow):
        with open(SYS_AIRPORT_INFO_PATH, 'w', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(dataFlow)

    try:
        with open(SYS_AIRPORT_INFO_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            vm_q = [vm for vm in reader]
            new_q = vm_q
            for i, value in enumerate(reversed(vm_q)):
                if value[-1] == '0' and value[-2] == class_:
                    vm = value[1]
                    new_q[-(i + 1)][-1] = '1'
                    break
        refresh_log(new_q)
        return vm
    except UnboundLocalError:
        return '无可用订阅连接'


def avi_num():
    from datetime import datetime, timedelta
    with open(SYS_AIRPORT_INFO_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        vm_list = [i for i in reader]
        # ['2020-08-06 04:27:59', 'link','class_', '1']

        vm_q = [vm for vm in vm_list if vm[-1] == '0']

        tag_items = ''
        for vm in vm_list:
            if vm[-1] == '0':
                bei_ing_time = datetime.fromisoformat(vm[0]) + timedelta(hours=12)
                tag_items += '\n【√可选】【{}】#{}'.format(bei_ing_time, vm[-2])

        return tag_items
