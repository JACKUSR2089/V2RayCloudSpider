from spiderNest.action_base import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Action_XjCloud(BaseAction):
    def __init__(self, silence=True, anti=True, email='@qq.com', life_cycle=62):
        super(Action_XjCloud, self).__init__(silence, anti, email, life_cycle)

        self.register_url = 'https://www.xjycloud.xyz/auth/register'

    def sign_up(self, api):
        WebDriverWait(api, 15) \
            .until(EC.presence_of_element_located((By.ID, 'email'))) \
            .send_keys(self.username)
        api.find_element_by_id('passwd').send_keys(self.password)
        api.find_element_by_id('repasswd').send_keys(self.password)
        api.find_element_by_id('reg').click()

    def sign_in(self, api: Chrome):
        for x in range(50):
            try:
                api.find_element_by_id('remember_me')
                api.find_element_by_id('email').send_keys(self.email)
                api.find_element_by_id('passwd').send_keys(self.password)
                api.find_element_by_id('login').click()
                break
            except NoSuchElementException or TimeoutException:
                time.sleep(1)
                continue

    def run(self):
        api = self.set_spiderOption()
        api.get(self.register_url)

        try:
            self.sign_up(api)

            self.sign_in(api)

            self.wait(api, 30, "//h2[contains(@id,'ssr')]")

            # get ssr link
            self.load_any_subscribe(
                api,
                "//button[contains(@class,'ssr')]",
                'data-clipboard-text',
                'ssr'
            )
            print('ssr:{}'.format(self.subscribe))


        except Exception as e:
            print(e)
        finally:
            api.quit()


if __name__ == '__main__':
    coroutine_local_test(Action_XjCloud)
