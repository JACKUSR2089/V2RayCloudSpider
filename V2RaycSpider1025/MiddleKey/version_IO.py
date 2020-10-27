# 软件安装引导
import os
import yaml
import easygui
import requests
import shutil
import zipfile
from Panel.master_panel import PrepareENV, INIT_airport_docTree, INIT_process_docTree
from config import version, SYS_LOCAL_fPATH, TITLE, YAML_PROJECT, YAML_PATH
from concurrent.futures import ThreadPoolExecutor

install_title = 'v2ray云彩姬安装向导'


class InstallGuider(object):
    v2raycs_url = 'https://t.qinse.top/subscribe/version_manager.txt'
    v2raycs_name = 'v2ray云彩姬.exe'

    def __init__(self):
        self.open_dir = ''

        self.open_fp = ''

        self.prepare_check()

    @staticmethod
    def prepare_check():
        try:
            requests.get('https://www.baidu.com')
        except requests.exceptions.RequestException:
            easygui.msgbox('网路异常', install_title)
            exit()

    def download(self, ):
        # FILENAME
        res = requests.get(InstallGuider.v2raycs_url)
        res.encoding = res.apparent_encoding
        v2raycs = res.text.strip().split(',')[-1]

        self.open_fp = os.path.join(self.open_dir, v2raycs.split('/')[-1])

        res = requests.get(v2raycs)

        with open(self.open_fp, 'wb') as f:
            f.write(res.content)

    def run(self, use_updated=False):
        try:
            usr_choice = easygui.ynbox('是否执行v2ray云彩姬一键安装脚本？', install_title)
            if usr_choice:
                # 首次安装
                if use_updated is False:
                    INIT_airport_docTree()
                    INIT_process_docTree()
                    for x in range(3):
                        self.open_dir = easygui.diropenbox('请选择安装路径', install_title, default=SYS_LOCAL_fPATH)
                        # 退出-放弃更新
                        if self.open_dir is None:
                            return False
                        # 选择限制
                        if os.listdir(self.open_dir):
                            easygui.msgbox('当前目录下存在其他文件，请选择独立的文件夹！', TITLE)
                        else:
                            # 记录用户选择的下载目录，便于软件更新时的项目文件拉取
                            with open(YAML_PATH, 'w', encoding='utf-8') as f:
                                proj = YAML_PROJECT
                                proj['path'] = self.open_dir
                                yaml.dump(proj, f)
                            break
                    # 给头铁的孩子一点教育
                    else:
                        easygui.msgbox('操作有误，请重试！', TITLE)
                        return False
                # 软件更新
                else:
                    try:
                        VersionControlSystem.kill_main()

                        # fixme:将updated模块移植到系统路径，通过外部操作控制软件更新；
                        # TODO: 将self.open_dir赋值为软件所在路径
                        with open(YAML_PATH, 'r', encoding='utf-8') as f:
                            data = yaml.load(f, Loader=yaml.FullLoader)
                            print(data['path'])
                        # self.open_dir = easygui.diropenbox()
                        self.open_dir = data['path']

                    except Exception as e:
                        print(e)

                # 下载线程
                os.startfile(self.open_dir)
                print(f"install path >> {self.open_dir}")
                with ThreadPoolExecutor(max_workers=1) as t:
                    t.submit(self.download)
                    # t.submit(easygui.msgbox, '正在拉取项目文件，请等待下载', install_title)
                easygui.msgbox('下载完成', install_title)

                # 解压线程
                with ThreadPoolExecutor(max_workers=2) as t:
                    t.submit(UnZipManager, self.open_fp)
                    t.submit(easygui.msgbox, '正在解压核心组件，请等待解压', title=install_title)
                easygui.msgbox('解压完成', install_title)

                # 自启动
                target_file = self.open_fp.replace('.zip', '') + f'_v{VersionControlSystem.get_server_version()[0]}'
                try:
                    os.startfile(os.path.join(
                        target_file,
                        InstallGuider.v2raycs_name))
                except OSError:
                    pass
                finally:
                    for filename in os.listdir(self.open_dir):
                        if '.zip' in filename:
                            try:
                                os.remove(os.path.join(self.open_dir, filename))
                            except OSError:
                                pass
                        elif os.path.basename(target_file).split('_')[-1] != filename.split('_')[-1]:
                            if os.path.basename(target_file).split('_')[0] in filename:
                                try:
                                    shutil.rmtree(os.path.join(self.open_dir, filename))
                                    os.rmdir(os.path.join(self.open_dir, filename))
                                except OSError:
                                    pass

        except Exception as e:
            easygui.exceptionbox(f'{e}')
        # over
        finally:
            easygui.msgbox('感谢使用', install_title)


class UnZipManager(object):
    def __init__(self, target: list or str):
        if isinstance(target, str):
            target = [target, ]

        for i in target:
            if i.endswith('.zip') and os.path.isfile(i):
                self.unzip(i)

    def unzip(self, filename: str):
        try:
            file = zipfile.ZipFile(filename)
            dirname = filename.replace('.zip', '') + f'_v{VersionControlSystem.get_server_version()[0]}'

            # 创建文件夹，并解压
            os.mkdir(dirname)
            file.extractall(dirname)
            file.close()
            # 递归修复编码
            self.rename(dirname)
            return dirname

        except Exception as e:
            print(f'{filename} unzip fail || {e}')

    def rename(self, pwd: str, filename=''):
        """压缩包内部文件有中文名, 解压后出现乱码，进行恢复"""

        path = f'{pwd}/{filename}'
        if os.path.isdir(path):
            for i in os.scandir(path):
                self.rename(path, i.name)
        newname = filename.encode('cp437').decode('gbk')
        os.rename(path, f'{pwd}/{newname}')


# ---------------------------------------
# 环境隔离
# ---------------------------------------
class VersionControlSystem(object):
    vcs_url = 'https://t.qinse.top/subscribe/version_manager.txt'

    @staticmethod
    def get_server_version():
        """
        :return: [version:str, url:str]
        """
        return requests.get(VersionControlSystem.vcs_url).text.split('\n')[-1].split(',')

    def check_different(self):
        server_version, url = self.get_server_version()
        s_top, s_func, s_modify = server_version.split('.')
        l_top, l_func, l_modify = version.split('.')

        if int(s_top) >= int(l_top) and int(s_func) >= int(l_func) and int(s_modify) > int(l_modify):
            print('local version: {}'.format(version))
            print('new version: {}'.format(server_version))
            print('Discover new version!')
            return server_version
        else:
            print('The current version is the latest version!')
            return False

    @staticmethod
    def kill_main(exe_name: str = 'v2ray云彩姬.exe'):
        import psutil
        import signal

        def get_all_pid():
            pid_dict = {}
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                pid_dict[pid] = p.name()
                print(f'pid-{pid},pname-{p.name()}')
            return pid_dict

        def kill(pid):
            try:
                os.kill(pid, signal.SIGABRT)
                print("located pid: {}".format(pid))
            except Exception as e:
                print('NoFoundPID || {}'.format(e))

        dic = get_all_pid()
        for t in dic.keys():
            if dic[t] == exe_name:
                kill(t)

    def run(self, init=False):
        from config import UPDATED_MODEL
        server_version = self.check_different()
        if server_version:
            usr_choice = easygui.ynbox(f'当前版本:{TITLE}\n\n最新版本：v{server_version}\n\n发现新版本软件！是否更新？', install_title)
            if usr_choice:
                os.startfile(UPDATED_MODEL)

            return True
        else:
            if not init:
                easygui.msgbox(f'当前版本:{TITLE}\n\n已是最新版本', install_title)
            return False


if __name__ == '__main__':
    InstallGuider().run()
