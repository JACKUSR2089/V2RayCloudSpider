try:
    import json
    import os
    import csv
    import base64
    import random
    import time
    import schedule

    from PIL import Image
    import requests
    from requests.exceptions import *
    from bs4 import BeautifulSoup
    from datetime import datetime
    from string import printable
    from selenium import webdriver
    from selenium.webdriver import ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.common.exceptions import *
    from config import CHROMEDRIVER_PATH
except ModuleNotFoundError:
    pass


# ------------------------------------
# v4.3.X版本配件
# ------------------------------------

# 滑动验证模组
class SliderMechanism(object):

    def __init__(self, driver):
        self.api = driver
        self.wait = WebDriverWait(self.api, 5)

    @staticmethod
    def save_base64img(data_str, save_name):
        """
        将 base64 数据转化为图片保存到指定位置
        :param data_str: base64 数据，不包含类型
        :param save_name: 保存的全路径
        """
        img_data = base64.b64decode(data_str)
        file = open(save_name, 'wb')
        file.write(img_data)
        file.close()

    @staticmethod
    def get_base64_by_canvas(driver, class_name, contain_type):
        """
        将 canvas 标签内容转换为 base64 数据
        :param class_name: canvas 标签的类名
        :param contain_type: 返回的数据是否包含类型
        :param driver: 返回的数据是否包含类型
        :return: base64 数据
        """
        # 防止图片未加载完就下载一张空图
        bg_img = ''
        while len(bg_img) < 5000:
            getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
            bg_img = driver.execute_script(getImgJS)

            time.sleep(0.5)
        # print(bg_img)
        if contain_type:
            return bg_img
        else:
            return bg_img[bg_img.find(',') + 1:]

    def save_full_bg(self, driver, full_bg_path="fbg.png",
                     full_bg_class='geetest_canvas_fullbg geetest_fade geetest_absolute'):
        """
        保存完整的的背景图
        :param driver: webdriver 对象
        :param full_bg_path: 保存路径
        :param full_bg_class: 完整背景图的 class 属性
        :return: 保存路径
        """
        bg_img_data = self.get_base64_by_canvas(driver, full_bg_class, False)
        self.save_base64img(bg_img_data, full_bg_path)
        return full_bg_path

    def save_bg(self, driver, bg_path="bg.png",
                bg_class='geetest_canvas_bg geetest_absolute'):
        """
        保存包含缺口的背景图
        :param driver: webdriver 对象
        :param bg_path: 保存路径
        :param bg_class: 背景图的 class 属性
        :return: 保存路径
        """
        bg_img_data = self.get_base64_by_canvas(driver, bg_class, False)
        self.save_base64img(bg_img_data, bg_path)
        return bg_path

    @staticmethod
    def is_pixel_equal(img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img2: 图片1
        :param img1: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_offset(self, full_bg_path, bg_path, offset=60):
        """
        获取缺口偏移量
        :param full_bg_path: 不带缺口图片路径
        :param bg_path: 带缺口图片路径
        :param offset: 偏移量， 默认 35
        :return:
        """
        full_bg = Image.open(full_bg_path)
        bg = Image.open(bg_path)
        for i in range(offset, full_bg.size[0]):
            for j in range(full_bg.size[1]):
                if not self.is_pixel_equal(full_bg, bg, i, j):
                    offset = i
                    return offset
        return offset

    @staticmethod
    def get_track(distance):
        """
        根据偏移量获取拟人的移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        track = []
        current = 0
        mid = distance * 3 / 4
        t = 0.1
        v = 0
        while current < distance:
            if current < mid:
                a = random.randint(2, 3)
            else:
                a = -random.randint(7, 8)
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    @staticmethod
    def get_slider(driver, slider_class='geetest_slider_button'):
        """
        获取滑块
        :param driver:
        :param slider_class: 滑块的 class 属性
        :return: 滑块对象
        """
        while True:
            try:
                slider = driver.find_element_by_class_name(slider_class)
                break
            except:
                time.sleep(0.5)
        return slider

    def drag_the_ball(self, driver, track):
        """
        根据运动轨迹拖拽
        :param driver: webdriver 对象
        :param track: 运动轨迹
        """
        slider = self.get_slider(driver)
        ActionChains(driver).click_and_hold(slider).perform()
        while track:
            x = random.choice(track)
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
            track.remove(x)
        time.sleep(0.1)
        # 模拟人往回滑动
        imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
        # 放开圆球
        ActionChains(driver).pause(random.randint(6, 14) / 10).release(slider).perform()

    def is_try_again(self):
        """[summary]

        判断是否能够点击重试
        """
        button_text = self.api.find_element_by_class_name('geetest_radar_tip_content')
        text = button_text.text
        if text == '尝试过多' or text == '网络不给力' or text == '请点击重试':
            button = self.api.find_element_by_class_name('geetest_reset_tip_content')
            button.click()

    def is_success(self):
        """[summary]

        判断是否成功
        """
        button_text2 = self.api.find_element_by_class_name('geetest_success_radar_tip_content')
        text2 = button_text2.text
        if text2 == '验证成功':
            # print(text2)
            return True
        return False

    def verity_mechanism(self):

        # 唤醒极验
        try:
            activate_button = self.api.find_element_by_class_name('geetest_radar_tip')
            activate_button.click()
            time.sleep(1)
        except:
            pass

        try:
            # 加载 Geetest 验证码
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice')))
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
        except Exception as e:
            # print(e)
            pass

        while True:

            # get full image
            full_bg_path = self.save_full_bg(self.api)

            # get defective image
            bg_path = self.save_bg(self.api)

            # 移动距离
            distance = self.get_offset(full_bg_path, bg_path, offset=24)

            # 获取移动轨迹
            track = self.get_track(distance)

            # 滑动圆球至缺口处
            self.drag_the_ball(self.api, track)

            try:
                time.sleep(1.5)
                if self.is_success():
                    break
                try:
                    self.is_try_again()
                except:
                    pass
            except Exception as e:
                pass
        return True


# 反爬虫组件
def anti_slider(api):
    """
    :api: 传入driver驱动
    """
    # 加载 Geetest 验证码 滑动验证
    try:
        sm = SliderMechanism(api)
        sm.verity_mechanism()
        return True
    except Exception as e:
        # print(e)
        return False


# 文本修饰器
def magic_msg(text: str, text_color, show_style='default', bk_color='default'):
    """
    修饰打印信息
    设置颜色开始 ：\033[显示方式;前景色;背景色m
    https://www.cnblogs.com/easypython/p/9084426.html
    :param text: 要装饰的文本
    :param show_style: 设置显示方式，使用系统默认
    :param text_color: 颜色模式，前景色，可选参数 见 set_text_color()
    :param bk_color:
    :return:字符串
    """

    def set_show_style():
        """
        设置显示方式
        0                    终端默认设置
        1                    高亮显示
        22　　　　　　　　　　　非高亮显示
        4                    使用下划线
        24　　　　　　　　　　　去下划线
        5                    闪烁
        25　　　　　　　　　　　去闪烁
        7                    反白显示
        27　　　　　　　　　　　非反显
        8                    不可见
        28　　　　　　　　　　　可见
        :return:
        """
        if show_style == 'default':
            return '1'
        else:
            return '1'

    def set_text_color():
        """
        设置字体颜色,也叫前景色
        前景色         背景色              颜色
        ---------------------------------------
        30                40              黑色
        31                41              红色
        32                42              绿色
        33                43              黃色
        34                44              蓝色
        35                45              洋红
        36                46              青色
        37                47              白色
        :return:
        """
        if text_color == 'bk' or text_color == 'black':
            return '30'
        elif text_color == 'r' or text_color == 'red':
            return '31'
        elif text_color == 'g' or text_color == 'green':
            return '32'
        elif text_color == 'y' or text_color == 'yellow':
            return '33'
        elif text_color == 'bl' or text_color == 'blue':
            return '34'
        elif text_color == 'm' or text_color == 'magenta':
            return '35'
        elif text_color == 'c' or text_color == 'cyan ':
            return '36'
        elif text_color == 'w' or text_color == 'white':
            return '37'
        else:
            # 输入有误时默认返回红色
            return '31'

    def set_background_color():
        """
        设置背景色
        :return:
        """
        if bk_color == 'default':
            return '1'
        else:
            return '1'

    # The foreground
    #     设置颜色开始 ：\033[显示方式;前景色;背景色m
    setup_msg = '\033[{};{};{}m'.format(set_show_style(), set_text_color(), set_background_color())
    release_msg = '\033[0m'

    master_msg = setup_msg + text + release_msg

    return master_msg


# 获取FAKE USERAGENT
def get_header(deployment=False) -> str:
    if deployment:
        from fake_useragent import UserAgent
        from Panel.master_panel import PrepareENV
        # fixme: v4.2.1error
        try:
            PrepareENV.init_fake_user_agent()
            return UserAgent().random
        except Exception as e:
            print(e)
            return get_header()
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

        return headers['User-Agent']


def get_proxy(deployment=False) -> str or bool:
    proxy_pool_interface = 'http://127.0.0.1:5555/random'
    if deployment:
        try:
            return 'http://{}'.format(requests.get(proxy_pool_interface).text.strip())
        except RequestException:
            return False


# ------------------------------------
# v4.3.X版本弃用
# ------------------------------------

# 获取STAFF机场关键信息：可用时长、可用流量
def get_STAFF_info(api):
    """

    :param api: chrome driver broswer
    :return:
    """
    time.sleep(3)
    try:
        card_body = api.find_elements_by_xpath("//div[@class='card-body']")

        # 会员时长
        available_time = card_body[0].text

        # 可用流量
        available_flow = card_body[1].text

        print(available_time, available_flow)
        return available_time, available_flow

    except NoSuchElementException:
        return '找不到元素,或本机场未基于STAFF开发前端'


# 注册
def sign_up_STAFF(api, user, psw, timeout: float):
    # 等待加载
    WebDriverWait(api, timeout) \
        .until(EC.presence_of_element_located((By.ID, 'name'))) \
        .send_keys(user)

    # 输入昵称
    api.find_element_by_id('email').send_keys(user)

    # 输入密码
    api.find_element_by_id('passwd').send_keys(psw)

    # 确认密码
    api.find_element_by_id('repasswd').send_keys(psw)

    # 点击【注册】按钮
    api.find_element_by_id('register-confirm').click()
    time.sleep(1)


# 断言审计规则
def TOS_STAFF(api, timeout: float):
    try:
        WebDriverWait(api, timeout) \
            .until(EC.presence_of_element_located((
            By.XPATH, "//button[@class='swal2-confirm swal2-styled']"
        ))).click()
    except NoSuchElementException:
        pass
