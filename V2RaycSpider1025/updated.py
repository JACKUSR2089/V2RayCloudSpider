# 禁止在本地直接运行该模块!!!!
from MiddleKey.version_IO import InstallGuider

if __name__ == '__main__':
    # Installation guide
    InstallGuider().run()

# pyinstaller -F updated.py
# setup main
# pyinstaller main.py -w -y -n v2ray云彩姬 -i ./images/logo.ico
