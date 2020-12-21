# V2Ray

科学上网，从娃娃抓起！

#打赏我 https://www.paypal.com/paypalme/uaa2020

BTC: 3FZxUtcR22xjJGwxp4G8jV9QjZJ2qHxKWL
BTC-Bitcoin单笔充币大于0.00005BTC-Bitcoin才可以到账

ETH： 0xfde5b338c528e07996495f997fb74c87123c0737

LTC 地址: 3CBbSryJyVJhDTWtdMmPgjyTSTb6Jd8j1s

USDT-Omni USDT 充币地址:

3Dgv41cSDGqTdw4kZExRHepunjbBsF5FK3

USDT-TRC20 USDT充币地址:

TMkRymhb8PzpEFjWVzYyNiwwoGpStcUstr

USDT-ERC20 USDT充币地址:

0xfde5b338c528e07996495f997fb74c87123c0737

## :carousel_horse: Intro

- 运行`V2Ray.exe` 即可启动**v2ray**获取订阅连接。
- **运行脚本**||**开箱即用**
- [使用说明](https://github.com/QIN2DIM/V2RayCloudSpider/blob/master/V2Ray云彩姬使用说明.md)

## :eagle: Quick Start

- 下载方案1【Windows用户 and 网速困难户】(推荐；约17MB)：[下载安装向导](https://t.qinse.top/subscribe/installer.zip)	

- 下载方案2【Python用户推荐】：Clone项目，项目源代码都在**V2RaycSpider[驱动号]**的文件夹中

  ![Snipaste_2020-10-22_13-53-00](https://i.loli.net/2020/10/22/s9vC6RI7FtVJahe.png)


## :video_game: Advanced Gameplay

> 该脚本未在macOS测试运行，可能存在非常多的bug，欢迎感兴趣的小伙伴来跑一下程序- -

- `/V2RaySpider0925`中存放该项目通用版本的源代码

- 运行`main.py`启动程序

- 安装依赖`当前目录：/V2RaycSpider0925`

  ```
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

- 修改配置` config.py`

### :balance_scale: Configure project parameters

- 请在此正确填写你的服务器信息，并将整个项目文件`V2RaycSpider0925`上传至linux服务器的`/qinse`文件夹

- 服务器首次运行请确保已安装`redis`并正确配置（开放）访问权限，且安装项目Python第三方库

- 运行`./funcBase/deploy_engine.py`则可部署脚本。

- **一定确保宁的环境部署在非大陆VPS上否则大概率翻车**

  ```powershell
  # 预览运行效果;如下为默认路径
  python3 /qinse/V2RaycSpider0925/funcBase/deploy_engine.py
  ```
  
  ```python
  # 部署
  nohup python3 /qinse/V2RaycSpider0925/funcBase/deploy_engine.py &
  ```
  
  ```python
  # /V2RaycSpider0925/config.py
  # SYS_PATH = f'/qinse/V2RaycSpider{verNum}'
  
  # ---------------------------------------
  # Cloud server configuration(SSH)
  # ---------------------------------------
  ECS_HOSTNAME: str = 'your ip'
  ECS_PORT: int = 29710
  ECS_USERNAME: str = ''
  ECS_PASSWORD: str = ''
      
  # ---------------------------------------
  # Redis server configuration(SSH)
  # ---------------------------------------
  
  REDIS_HOST: str = 'your ip'
  REDIS_PORT: int = 6379
  REDIS_PASSWORD: str = ''
  ```

- **设置驱动执行权限**

  给`chromedriver`设置可执行权限，如果用`Finalshell`l或`Xshell`的同学，直接右键目标文件即可设置文件权限；项目预装的驱动是最新版本的[2020.10]所以`Linux`中要下载`v85.0.4183.102`或更新版本的Chrome

  ```python
  CHROMEDRIVER_PATH = os.path.dirname(__file__) + '/MiddleKey/chromedriver'
  ```

- 安装`gcc`

  ```
  yum install gcc-c++
  ```

- `Linux`**安装Chrome**

  - 指定yum源

  ```powershell
  wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
  ```

  - 安装

  ```powershell
  curl https://intoli.com/install-google-chrome.sh | bash
  ```

  - 安装后执行

  ```powershell
  google-chrome-stable --no-sandbox --headless --disable-gpu --screenshot https://www.baidu.com/
  ```

- [安装](https://shimo.im/docs/5bqnroJYDbU4rGqy/)`redis`

### :zap:Other

- 快速获取

  - 使用requests的get请求，分别访问以下链接，使用text抽取订阅链接

    ```python
    # Python3.8
    # quick——get Subscribe API
    import requests
    
    subs_target = 'https://t.qinse.top/subscribe/{}.txt'
    
    subs_ssr = requests.get(subs_target.format('ssr')).text
    subs_trojan = requests.get(subs_target.format('trojan')).text
    subs_v2ray = requests.get(subs_target.format('v2ray')).text
    
    print("subs_ssr: {}\nsubs_: {}\nsubs_v2ray: {}\n".format(subs_ssr,subs_trojan,subs_v2ray))
    
    ```

    ![image-20201020112752998](https://i.loli.net/2020/10/20/XaJc4qA1ehPUM5V.png)

##  :grey_question:Q&A

- **防火墙警告**

  - 首次运行可能会弹出提示

    ![3](https://i.loli.net/2020/10/06/MhwiZfOz3VdDPU5.png)

    ![3](https://i.loli.net/2020/10/06/gmLksO3HCtyWu9r.png)

## :world_map: TODO

- [x] 支持Trojan-go、Trojan-gfw机场的采集
- [ ] 融合网络代理核心，形成自洽的科学上网模块
- [x] 合并订阅链接消息队列，PC端可查看目前在库最多25条Subscribe订阅链接，并择一获取
  - [x] 合并队列
  - [x] 查看链接
  - [x] 择一获取
- [ ] 逐渐停用easyGUI前端模块，兼容跨平台访问(手机，电脑，嵌入式系统)
