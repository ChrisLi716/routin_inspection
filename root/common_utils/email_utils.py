import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from root.common_utils.settings_util import SettingsUtil
from email.mime.multipart import MIMEMultipart
import traceback
import os

from root.common_utils.log_util import Logger


class EmailUtils(object):
    logger = Logger.get_instance()
    __settings = SettingsUtil.get_instance()

    @staticmethod
    def build_content(sender, receiver, cc, subject, body):
        # 设置邮件正文，这里是支持HTML的
        # 设置正文为符合邮件格式的HTML内容
        m = MIMEText(_text=body, _subtype='html', _charset='utf-8')
        # 设置邮件标题
        m['subject'] = subject
        # 设置发送人
        m['from'] = sender
        # 设置接收人
        m['to'] = receiver
        m['cc'] = cc

        return m

    @staticmethod
    def build_attach_file(text_content, sender, receiver, cc, subject, files_tuple):
        m = MIMEMultipart()
        m.attach(text_content)
        EmailUtils.logger.info("files_tuple:" + str(files_tuple))
        for file in files_tuple:
            file_name = os.path.basename(file)
            EmailUtils.logger.info("build_attach_file:filename " + file)
            file_apart = MIMEApplication(open(file, "rb").read())
            file_apart.add_header('Content-Disposition', 'attachment', filename=file_name)
            m.attach(file_apart)

        m['Subject'] = subject
        m['from'] = sender
        m['to'] = receiver
        m['cc'] = cc

        return m

    @staticmethod
    def test_attach_email():
        file = 'demo1.txt'
        file_apart = MIMEApplication(open("D:/code/python-project/demo/tmp/demo1.txt", 'rb').read())
        file_apart.add_header('Content-Disposition', 'attachment', filename=file)

        content = "<h1>You've already sent eamil successfully!</h1>" \
                  "<p>Chris</p>"
        text_apart = MIMEText(content)

        m = MIMEMultipart()
        m.attach(text_apart)
        m.attach(file_apart)
        m['subject'] = 'title'
        m['from'] = 'lilunlogic@163.com'
        m['to'] = '872343840@qq.com'

        return m

    @classmethod
    def sent_email(cls, receiver, cc, subject, body, file_tuple):
        # 设置发件服务器地址
        host = cls.__settings.email_host
        # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
        non_ssl_port = cls.__settings.email_non_ssl_port
        # ssl_port = cls.__settings.email_ssl_port

        # 设置发件邮箱，一定要自己注册的邮箱
        sender = cls.__settings.email_sender
        # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
        pwd = cls.__settings.email_pwd

        m = EmailUtils.build_content(sender, receiver, cc, subject, body)
        m = EmailUtils.build_attach_file(m, sender, receiver, cc, subject, file_tuple)
        # m = test_attach_email()
        try:
            s = smtplib.SMTP(host, non_ssl_port)
            # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
            # s = smtplib.SMTP_SSL(host, ssl_port)
            # 登陆邮箱
            s.login(sender, pwd)
            s.sendmail(sender, receiver, m.as_string())
            # 发送邮件！
            print('Done. sent email success')
            s.quit()
        except smtplib.SMTPException:
            print('Error. sent email fail', traceback.print_exc())


if __name__ == '__main__':

    # 设置邮件接收人，可以是QQ邮箱
    receiver = 'chris.li@allsale.site'

    subject = "send email with attachments"
    body = "<h1>You've already sent eamil successfully!</h1>" \
           "<p>Chris</p>"

    full_file_name = []
    dir_path = os.getcwd() + os.sep + "tmp"
    for file in os.listdir(dir_path):
        full_file_name.append(os.path.join(dir_path, file))

    EmailUtils.sent_email(receiver, subject, body, tuple(full_file_name))
