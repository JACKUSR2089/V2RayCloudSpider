from Panel.master_panel import *

"""欢迎使用V2Ray云彩姬"""
if __name__ == '__main__':
    V2Rayc = V2RaycSpider_Master_Panel()
    try:
        V2Rayc.home_menu()
    except Exception as e:
        V2Rayc.debug(e)
    finally:
        V2Rayc.kill()
