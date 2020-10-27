# coding=UTF-8
class InterviewPanel(object):

    @staticmethod
    def HomePanel():
        """

        :return:
        """
        import easygui
        easygui.fileopenbox('打开配置文件csv')


class InterviewDocker(object):
    account_sid = {
        # SMTP邮箱
        'username': '',
        # SMTP验证码
        'sid': '',
    }

    def __init__(self,
                 # SMTP账号信息，填写范式如上
                 account_sid: dict,
                 # 你的公司名/组织名，部门名，职位，姓名
                 org='《海大校友》杂志社',
                 dep='技术部',
                 position='部长',
                 I_am='张亦先',
                 # 通知【通过面试】或【被录用的】面试者下一步工作的截止时间，既该参数不会在向【被淘汰的】面试者发送的邮件中启用
                 ddl: str = '10月10日（周六）晚18:00',
                 # 公司/组织 XX数据库名称简写，用于向【被淘汰的】面试者发送的邮件正文编写,以及smtp邮箱设置
                 zone='「海南大学」人才库',
                 # 官方邮箱
                 official_mailbox='xyh.hainanu@qq.com',
                 # 公司/组织 网站域名
                 website_domain='yao.qinse.top',
                 # 加群分享链接,此项不可为空!
                 official_group_link='',
                 # 落款
                 SIGN='海大校友办公室｜Alkaid 团队',
                 # 邮件主题
                 header='《海大校友》杂志社面试通知',
                 **kwargs):
        self.err = kwargs.get('err')
        # -----------------------------------------
        # 邮件内容设置
        # -----------------------------------------
        # 你的公司名/组织名，部门名，职位，姓名 以及 正文称呼
        self.org, self.dep, self.position, self.I_am = org, dep, position, I_am
        self.I_AM = self.org + self.dep + self.position + self.I_am

        # 邮件大标题 |《海大校友》杂志社 面试通知
        self.TITLE = self.org + '面试通知'

        # 通知【通过面试】或【被录用的】面试者下一步工作的截止时间，既该参数不会在向【被淘汰的】面试者发送的邮件中启用
        self.ddl = ddl

        # 公司/组织 XX数据库名称简写，用于向【被淘汰的】面试者发送的邮件正文编写,以及smtp邮箱设置
        self.zone = zone

        # 官方邮箱,
        self.official_mailbox: str = official_mailbox

        # 公司/组织 网站域名
        self.website_domain = website_domain

        # 加群分享链接
        self.official_group_link: str = official_group_link

        # 落款
        self.SIGN = SIGN

        # -----------------------------------------
        # 邮件发送设置
        # -----------------------------------------

        # 邮件主题
        self.header = header

        # SMTP SETTING
        self.account_sid = {
            f'{self.zone}': {
                'username': account_sid['username'],
                'sid': account_sid['sid'],
            },
        }

    def send_email(self, text_body: str, to_=None):
        """

        :param text_body: -> str文本
        :param to_: -> 接收者
        :return:
        """
        from smtplib import SMTP_SSL
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.header import Header
        from smtplib import SMTPDataError

        if isinstance(to_, str):
            to_ = [to_, ]
        #####################################################
        sender_name = self.account_sid[f'{self.zone}']['username']
        sender_sid = self.account_sid[f'{self.zone}']['sid']
        # 连接服务器
        server = SMTP_SSL(host='smtp.qq.com')
        qq_email = 'smtp.qq.com'
        port = 465
        #####################################################
        # 邮件的正文内容

        mail_content = "{}".format(text_body)
        # 构建多媒体实例
        msg = MIMEMultipart()
        msg['Subject'] = Header(self.header)
        msg['From'] = sender_name
        msg.attach(MIMEText(mail_content, 'html', 'utf-8'))
        #####################################################
        errorList = []  # 发送失败的object
        try:
            # 链接服务器
            server.connect(host=qq_email, port=port)
            # 登陆服务器
            server.login(user=sender_name, password=sender_sid)
            for receiver in to_:
                try:
                    # 发送邮件:success
                    server.sendmail(sender_name, receiver, msg.as_string())
                    print('>>> success to {}'.format(receiver))
                except SMTPDataError:
                    # 发送邮件:retry
                    errorList.append(receiver)
                    # server.sendmail(sender_name, sender_name, msg.as_string())  # 备用信道
                    print('error list append: {}'.format(receiver))
                    continue
            while errorList.__len__() > 0:
                to_ = errorList.pop()
                try:
                    server.sendmail(sender_name, to_, msg.as_string())
                except SMTPDataError:
                    print('panic object !!!  {}'.format(to_))
        finally:
            server.quit()

    def text_temple(self, to_name: str, temple: str, ):
        """

        :param to_name:
        :param temple: success,loser,winner
        :return:
        """

        # 称呼
        TO_TAG = f'{to_name}同学，您好！',

        # 致谢
        TO_END_1 = '收到请回复，谢谢，幸苦了！',
        TO_END_2 = '再次感谢您的信任与参与。',

        # 正文模版1:录用
        BODY_SUCCESS = [
            TO_TAG,
            f'我是{self.I_AM}。很高兴通知您，您已通过{self.dep}的综合能力测试，我们对您的整体表现非常满意。',
            f'现通知您于{self.ddl}前加入{self.dep}工作群，后续通知将于群内发布，期待您的到来。',
            TO_END_1
        ]
        # 正文模版2:淘汰
        BODY_LOSER = [
            TO_TAG,
            f'感谢您关注{self.org}校园招新，我们已经收到您提交的考核项目。',
            f'很遗憾，结合您的技能熟练度、项目经历等进行综合评估，您与{self.dep}目前的需求仍有差距。',
            f'您在考核过程中的应试态度给我们留下了深刻印象，我们会将您的信息保留在{self.zone}中，以便未来有合适的机会再与您联系。',
            TO_END_2,
        ]

        # 正文模版3:通过X轮面试
        BODY_WINNER = [
            TO_TAG,
            f'我是{self.I_AM}。很高兴通知您，您已通过{self.dep}的首轮面试，我们对您的整体表现非常满意。',
            f'现通知您于{self.ddl}前加入{self.dep}终轮考核群，相关挑战将于群内发布，期待您的到来。',
            TO_END_1
        ]

        # v2rayc spider
        BODY_V2RAYC = [
            TO_TAG,
            self.err,
            TO_END_1
        ]

        # 模版返回
        if temple == 'v2rayc_spider':
            top_img = 'https://images.pexels.com/photos/3876430/pexels-photo-3876430.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260'
            return self.__txt2html__(top_img, BODY_V2RAYC, temple)

        if temple == 'success':
            top_img = 'https://images.pexels.com/photos/3876430/pexels-photo-3876430.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260'
            return self.__txt2html__(top_img, BODY_SUCCESS, temple)
        elif temple == 'loser':
            top_img = 'https://images.pexels.com/photos/3651615/pexels-photo-3651615.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
            return self.__txt2html__(top_img, BODY_LOSER, temple)
        elif temple == 'winner':
            top_img = 'https://images.pexels.com/photos/3747154/pexels-photo-3747154.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'
            return self.__txt2html__(top_img, BODY_WINNER, temple)
        else:
            return None

    def __txt2html__(self, img_link, body, temple):
        """

        :param img_link:
        :param body:
        :return:
        """

        def generate_imgAtlas():
            tag = '<img class="gnd-corner-image gnd-corner-image-center gnd-corner-image-top" style="border: 0; display: block; height: auto; width: 100%; max-width: 900px;" src="{}" width="600" border="0px">'
            return tag.format(img_link)

        def generate_text_title():
            tag = '<h1 style="margin-top: 0; margin-bottom: 0; font-style: normal; font-weight: normal; color: #b59859; font-size: 26px; line-height: 34px; font-family: source sans pro,apple sd gothic neo,pt sans,trebuchet ms,sans-serif; text-align: left;"><span class="font-source-sans-pro"><strong><span style="color: #262626;">{}</span></strong></span></h1> '
            return tag.format(self.TITLE)

        def generate_text_body():
            tag = '<p style="margin-top: 20px; margin-bottom: 0; font-family: roboto,tahoma,sans-serif;"><span class="font-roboto"><span style="color: #1b4665;">{}</span></span></p>'
            docker = []
            for text in body:
                if isinstance(text, tuple):
                    docker.append(tag.format(text[0]))
                    continue
                docker.append(tag.format(text))
            return ''.join(docker)

        def generate_text_sign():
            tag = '<p style="margin-top: 20px; margin-bottom: 0; font-family: roboto,tahoma,sans-serif;"><span class="font-roboto"><br><span style="color: #1b4665;">{}</span></span></p>'
            return tag.format(self.SIGN)

        def generate_contact_details():
            if temple == 'success' or temple == 'winner':
                href = self.official_group_link
            else:
                href = self.website_domain

            tag = f"""<span class="font-roboto" style="font-size: 12px; color: #808080;">访问网站：<a href="{href}"
                            rel="noopener" target="_blank">{self.website_domain}</a>
                            <br>联系我们：<a href="mailto:{self.official_mailbox}?to=qinse.top%40foxmail.com&amp;biz_type=&amp;
                            crm_mtn_tracelog_template=2001649455&amp;crm_mtn_tracelog_task_id=e47d2ad7-c107-4106-b332-4ed631556abe&amp;
                            crm_mtn_tracelog_from_sys=service_wolf-web&amp;crm_mtn_tracelog_log_id=23765736451&amp;
                            from=teambition%40service.alibaba.com" rel="noopener" target="_blank">{self.official_mailbox}</a></span></p> 
                           """
            return tag

        HTML_TEXT_BODY = f"""
                    <div id="contentDiv" onmouseover="getTop().stopPropagation(event);" onclick="getTop().preSwapLink(event, 'html', 'ZC2813-K3KnnHZmbHcpPiJ90Yb0fa9');" style="position:relative;font-size:14px;height:auto;padding:15px 15px 10px 15px;z-index:1;zoom:1;line-height:1.7;" class="body">    <div id="qm_con_body"><div id="mailContentContainer" class="qmbox qm_con_body_content qqmail_webmail_only" style="">
    
    
                  <p>&nbsp;</p> 
    
                  <table class="wrapper" style="border-collapse: collapse; table-layout: fixed; min-width: 320px; width: 100%; background-color: #f0eee7;" cellspacing="0" cellpadding="0"> 
                   <tbody> 
                    <tr> 
                     <td> 
                      <div> 
                       <div class="preheader" style=" margin: 0 auto; max-width: 560px; min-width: 280px;  "> 
                        <div style="border-collapse: collapse; display: table; width: 100%;">
    
                         <div class="snippet" style=" display: table-cell; float: left; font-size: 12px; line-height: 19px; max-width: 280px; min-width: 140px;  padding: 10px 0 5px 0; color: #b3b3b3; font-family: PT Sans,Trebuchet MS,sans-serif; ">
                          &nbsp;
                         </div> 
    
                         <div class="webversion" style=" display: table-cell; float: left; font-size: 12px; line-height: 19px; max-width: 280px; min-width: 139px;  padding: 10px 0 5px 0; text-align: right; color: #b3b3b3; font-family: PT Sans,Trebuchet MS,sans-serif; ">
                          &nbsp;
                         </div> 
    
                        </div> 
                       </div> 
                      </div> 
                      <div> 
                       <div class="layout one-col fixed-width stack" style=" margin: 0 auto; max-width: 600px; min-width: 320px;  overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; "> 
                        <div class="layout__inner" style="border-collapse: collapse; display: table; width: 100%; background-color: #ffffff;">
    
                         <div class="column" style="text-align: left; color: #61606c; font-size: 16px; line-height: 24px; font-family: PT Serif,Georgia,serif;"> 
                          <div style="font-size: 12px; font-style: normal; font-weight: normal; line-height: 19px;" align="center">
                           {generate_imgAtlas()}
                          </div> 
                          <div style="margin-left: 20px; margin-right: 20px; margin-top: 20px;"> 
                           <div style="mso-line-height-rule: exactly; line-height: 20px; font-size: 1px;">
                            &nbsp;
                           </div> 
                          </div> 
                          <div style="margin-left: 20px; margin-right: 20px;"> 
                           <div style="mso-line-height-rule: exactly; mso-text-raise: 11px; vertical-align: middle; padding: 30px;"> 
                            {generate_text_title()} 
                            <p style="margin-top: 20px; margin-bottom: 0;">&nbsp;</p> 
                            {generate_text_body()}
                            <p style="margin-top: 20px; margin-bottom: 0; font-family: roboto,tahoma,sans-serif;">&nbsp;</p> 
                            {generate_text_sign()}
                           </div> 
                          </div> 
                         </div> 
                        </div> 
                       </div> 
                      </div> 
                      <div> 
                       <div class="layout one-col fixed-width stack" style=" margin: 0 auto; max-width: 600px; min-width: 320px;  overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; "> 
                        <div class="layout__inner" style="border-collapse: collapse; display: table; width: 100%; background-color: #ffffff;"> 
                         <div class="column" style="text-align: left; color: #61606c; font-size: 16px; line-height: 24px; font-family: PT Serif,Georgia,serif;"> 
                          <div style="margin-left: 20px; margin-right: 20px;"> 
                           <div style="mso-line-height-rule: exactly; mso-text-raise: 11px; vertical-align: middle; padding: 30px;"> 
                            <p style="margin-top: 20px; margin-bottom: 0; font-family: roboto,tahoma,sans-serif;">
                            {generate_contact_details()}
                            </div> 
                          </div> 
                         </div> 
                        </div> 
                       </div> 
                       <div style="mso-line-height-rule: exactly; line-height: 30px; font-size: 30px;">
                        &nbsp;
                       </div> 
                      </div> </td> 
                    </tr> 
                   </tbody> 
                  </table>
                </div>"""

        return HTML_TEXT_BODY

    def do_senderEne(self, name_list: dict, func: str):
        """

        :param name_list:
        :param func: loser、winner、success
        :return:
        """
        for info in name_list.items():
            self.send_email(
                text_body=self.text_temple(to_name=info[0], temple=func),
                to_=info[-1]
            )


err_warning = ''


def prepare(err: str, func_name: str):
    """仅用于报错填充"""
    global err_warning
    from datetime import datetime
    now_ = str(datetime.now()).split('.')[0]
    err_warning = f'>>> {now_}||{func_name}||{err}'


def run():
    """群发"""
    beta_smtp = {
        # SMTP邮箱
        'username': 'xyh.hainanu@qq.com',
        # SMTP验证码
        'sid': 'jppbcewcqrdgicec',
    }

    nameList = {
        'GGboy': 'qinse.top@foxmail.com'
    }

    ivd = InterviewDocker(beta_smtp, err=err_warning)

    # v2rayc spider
    ivd.do_senderEne(nameList, func='v2rayc_spider')

    # 面试失败的邮件
    # ivd.do_senderEne(nameList, func='loser', )

    # 面试成功的邮件(X轮)
    # ivd.do_senderEne(nameList, func='winner')

    # 面试录用的邮件
    # ivd.do_senderEne(nameList, func='success')


if __name__ == '__main__':
    run()
