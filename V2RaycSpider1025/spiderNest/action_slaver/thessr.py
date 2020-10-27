import sys

sys.path.append('/qinse/V2RaycSpider0925')
from spiderNest.action_base import *


class Action_TheSSR(BaseAction):
    def __init__(self, silence=True, anti=True, email='@qq.com', life_cycle=1):
        super(Action_TheSSR, self).__init__(silence, anti, email, life_cycle)

        self.register_url = 'https://thessr.site/auth/register'

    def sign_up(self, api):
        WebDriverWait(api, 15) \
            .until(EC.presence_of_element_located((By.ID, 'name'))) \
            .send_keys(self.username)
        api.find_element_by_id('email').send_keys(self.username)
        api.find_element_by_id('passwd').send_keys(self.password)
        api.find_element_by_id('repasswd').send_keys(self.password)
        api.find_element_by_id('register-confirm').click()

        time.sleep(1)
        api.find_element_by_xpath("//button[contains(@class,'confirm')]").click()

    def run(self):
        api = self.set_spiderOption()
        api.get(self.register_url)

        try:
            self.sign_up(api)

            self.wait(api, 30, "//div[@class='card-body']")

            # get v2ray link
            self.load_any_subscribe(
                api,
                "//div[@class='buttons']//a[contains(@class,'v2ray')]",
                'data-clipboard-text',
                'v2ray'
            )

            # get ssr link
            self.load_any_subscribe(
                api,
                "//div[@class='buttons']//div//a[contains(@class,'copy')]",
                'data-clipboard-text',
                'ssr'
            )

        except Exception as e:
            print(e)
        finally:
            api.quit()


if __name__ == '__main__':
    coroutine_local_test(Action_TheSSR)
