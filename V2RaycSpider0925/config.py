import os
import sys

# ---------------------------------------------------
# 云彩姬版本号,版本号必须与工程版本(文件名)号一致
# ---------------------------------------------------
verNum = '0925'
# ---------------------------------------------------
# PC(链接获取)进程锁死的冷却时间
# 进程锁死时长(min)，建议type：float∈(0,1]
# ---------------------------------------------------
BAND_BATCH = 0.25

"""********************************* Action set/PATH->Service ********************"""

# Chromedriver 路径,咱不支持MAC环境的云服务器
# Linux Google Chrome v85.0.4183.102
if 'win' in sys.platform:
    CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver.exe'
elif 'linux' in sys.platform:
    CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver'

# CHROMEDRIVER_PATH_for_LINUX = os.path.dirname(__file__) + '/MiddleKey/chromedriver'
# CHROMEDRIVER_PATH_for_WIN32 = os.path.dirname(__file__) + '/MiddleKey/chromedriver.exe'

# Function Base临时环境变量, format 中填写版本号
SYS_PATH = '/qinse/V2RaycSpider{}'.format(verNum)

# LOG_CSV文件路径
SERVER_LOG_PATH = os.path.dirname(__file__) + '/dataBase/log_information.csv'

# ROOT DATABASE
ROOT_DATABASE = os.path.join(os.path.dirname(__file__), 'dataBase')

# ---------------------------------------------------
# Cloud server configuration(SSH)
# ---------------------------------------------------
ECS_HOSTNAME: str = '104.224.177.249'
ECS_PORT: int = 29710
ECS_USERNAME: str = 'root'
ECS_PASSWORD: str = 'KYU77wh7vpRK'

# 文件路径:查询可用订阅连接
AviLINK_FILE_PATH = '/qinse/V2RaycSpider{}/funcBase/func_avi_num.py'.format(verNum)
# 文件路径:ssr链接抓取接口
SSR_ENE_FILE_PATH = '/qinse/V2RaycSpider{}/funcBase/get_ssr_link.py'.format(verNum)
# 文件路径:v2ray链接抓取接口
V2RAY_ENE_FILE_PATH = '/qinse/V2RaycSpider{}/funcBase/get_v2ray_link.py'.format(verNum)

# Nginx映射路径
NGINX_RES_PATH = '/usr/share/nginx/html'
NGINX_SSR_PATH = os.path.join(NGINX_RES_PATH, 'ssr.txt')
NGINX_V2RAY_PATH = os.path.join(NGINX_RES_PATH, 'v2ray.txt')

"""********************************* Action set/PATH->Local ********************************"""
# TODO: 当前版本不提供安装导航，不支持diy安装目录，若想更改缓存路径，请改动源代码
# 工程目录
ROOT_PROJECT_PATH = os.path.dirname(__file__)
# 软件本地根目录
SYS_LOCAL_fPATH = os.path.join(ROOT_PROJECT_PATH, 'dataBase')
# 访问记录(系统核心文件，请勿删改)
SYS_LOCAL_vPATH = SYS_LOCAL_fPATH + '/log_VMess.txt'
SYS_AIRPORT_INFO_PATH = SYS_LOCAL_fPATH + '/log_information.csv'
# 采集模式，若服务器设置有误 则本机启动
START_MODE = 'local' if ECS_HOSTNAME == '' else 'cloud'

"""********************************* The core set ********************************"""

# 我就是云彩姬!
TITLE = f'V2Ray云彩姬_v{verNum}_{START_MODE}'
