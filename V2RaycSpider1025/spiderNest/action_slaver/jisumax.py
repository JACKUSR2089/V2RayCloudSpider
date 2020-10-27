import sys

sys.path.append('/qinse/V2RaycSpider0925')
from threading import Lock
from spiderNest.action_base import *

global_lock = Lock()


class Action_JiSuMax(BaseAction):
    def __init__(self, silence=True, anti=True, email='@qq.com', life_cycle=61):
        super(Action_JiSuMax, self).__init__(silence, anti, email, life_cycle)

        self.register_url = 'https://jisumax.com/#/register?'

    def sign_up(self, api):
        WebDriverWait(api, 15) \
            .until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='邮箱']"))) \
            .send_keys(self.username)
        for i in api.find_elements_by_xpath("//input[@placeholder='密码']"):
            i.send_keys(self.password)
        api.find_element_by_xpath("//i").click()

    def load_any_subscribe(self, api, element_xpath_str: str, href_xpath_str: str, class_: str, retry=0):

        def loop_step():
            time.sleep(1)
            # get trojan link
            for _ in range(5):
                api.find_element_by_xpath(
                    element_xpath_str).click()

                self.wait(api, 10, 'all')

                api.find_element_by_xpath(href_xpath_str).click()
                self.subscribe = pyperclip.paste()

                self.subscribe = self.subscribe if 'http' in self.subscribe else None

                if self.subscribe:
                    try:
                        save_login_info(self.subscribe, class_, self.life_cycle)
                    except RedisError:
                        time.sleep(3)
                        save_login_info(self.subscribe, class_, self.life_cycle)
                    finally:
                        print('trojan:{}'.format(self.subscribe))
                        break
                else:
                    time.sleep(1)
                    continue

        try:
            if retry >= 3:
                return None
            loop_step()
        except NoSuchElementException or pyperclip.PyperclipException:
            retry += 1
            self.load_any_subscribe(api, element_xpath_str, href_xpath_str, class_, retry)

    def run(self):
        api = self.set_spiderOption()
        try:
            api.get(self.register_url)

            self.sign_up(api)

            self.wait(api, 30, "all")

            self.load_any_subscribe(
                api,
                "//a[@class='btn btn-sm btn-primary btn-rounded px-3 mr-1 my-1 ant-dropdown-trigger']",
                "//i[contains(@class,'copy')]",
                'trojan'
            )

        except NoSuchElementException:
            print('jisumax ip is blocked')
        except TimeoutException:
            print('jisumax ip was timed out')

        finally:
            api.quit()

            # if not self.silence:
            #     print(f'username:{self.username}')
            #     print(f'password:{self.password}')
            #     print(f'email:{self.email}')


if __name__ == '__main__':
    coroutine_local_test(Action_JiSuMax)
