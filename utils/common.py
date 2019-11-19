#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "JentZhang"
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import datetime
from hashlib import sha1
import calendar
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os


# from config import EMAIL_USER, EMAIL_PWD, EMAIL_HOST
# from utils.config import EMAIL_USER, EMAIL_PWD, EMAIL_HOST

class ReturnValue(object):
    """
    返回结果集
    """

    def __init__(self, error=False, message='', code=1, data=None):
        """
        初始化参数
        :param has_error: 是否出错，默认值为否
        :param message: 返回信息，默认为空
        :param return_code: 返回代码，默认1，代表信息请求成功
        :param return_obj: 返回的对象
        """
        self.error = error
        self.message = message
        self.code = code
        self.data = data

    def dict(self):
        return {"error": self.error, "message": self.message, "code": self.code,
                "data": self.data}

    def __str__(self):
        dict_str = {"error": self.error, "message": self.message, "code": self.code,
                    "data": self.data}
        return str(dict_str)


class ValidateCode(object):
    """
    验证码相关
    """

    def getCode(self, length):
        """
        生成随机验证码
        :param length:验证码的长度
        :return:
        """
        res = ''
        for i in range(length):
            x = random.randint(1, 9)
            if x % 3:
                res += str(random.randint(2, 9))
            else:
                res += chr(random.randint(97, 122))
        return res

    def getNumCode(self, length):
        """
        生成数字随机验证码
        :param length:验证码的长度
        :return:
        """
        res = ''
        for i in range(length):
            res += str(random.randint(1, 9))
        return res

    def rndColor(self):
        """
        随机颜色1
        :return:
        """
        # return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
        return (random.randint(210, 255), random.randint(210, 255), random.randint(210, 255))

    def rndColor2(self):
        """
        随机颜色2
        :return:
        """
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def getCodeImage(self, code):
        # 验证码长度
        length = len(code)
        # 图片的宽和高
        width, height = 60 * length, 60
        # 新建图片
        image = Image.new('RGB', (width, height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype("arial.ttf", 48)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self.rndColor())
        # 输出文字
        for t in range(length):
            draw.text((60 * t + 10, 6), code[t], font=font, fill=self.rndColor2())
        # 模糊:
        image = image.filter(ImageFilter.BLUR)
        # with open("pic.png", "wb") as f:
        #     image.save(f, format="png")
        return image


class Common(object):
    """
    常用方法类
    """

    @classmethod
    def sha1_encryption(cls, msg):
        """
        sha1加密
        :param msg:加密前的字符串
        :return:
        """
        s1 = sha1()
        s1.update(msg.encode())
        return s1.hexdigest()

    @classmethod
    def get_current_month_start_and_end(cls, date):
        """
        年份 date(2017-09-08格式)
        :param date:
        :return:本月第一天日期和本月最后一天日期
        """
        if str(date).count('-') != 2:
            raise ValueError('- is error')
        year, month = str(date).split('-')[0], str(date).split('-')[1]
        end = calendar.monthrange(int(year), int(month))[1]
        start_date = '%s-%s-01' % (year, month)
        end_date = '%s-%s-%s' % (year, month, end)
        return start_date, end_date

    @classmethod
    def get_current_date(cls):
        """
        获取当前日期（2019-07-01）
        :return:
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def get_filePath_fileName_fileExt(cls, file_url):
        """
        获取文件路径， 文件名， 后缀名
       :param file_url:
       :return:
        """
        filepath, tmpfilename = os.path.split(file_url)
        shotname, extension = os.path.splitext(tmpfilename)

        return filepath, shotname, extension

    @classmethod
    def get_num_code(cls, length):
        """
        生成数字随机验证码
        :param length:验证码的长度
        :return:
        """
        res = ''
        for i in range(length):
            res += str(random.randint(1, 9))
        return res


class SendEmail(object):
    """
    邮件发送类
    """

    def __init__(self):
        """
        构造函数：初始化基本信息
        :param host:邮件服务器地址
        :param user:邮件用户名
        :param passwd:邮件登录口令
        """
        from utils.config import EMAIL_USER, EMAIL_PWD, EMAIL_HOST
        self.user = EMAIL_USER
        self.passwd = EMAIL_PWD
        self.host = EMAIL_HOST

        server = smtplib.SMTP_SSL(host=self.host)
        server.connect(self.host, 465)
        server.login(self.user, self.passwd)
        self.server = server

    def sendTxtMail(self, to_list, sub, content, is_html=False):
        """
        发送文件或html邮件
        :param to_list:
        :param sub:
        :param content:
        :param subtype:
        :return:
        """
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def sendAttachMail(self, to_list, sub, content, attach_path=[], is_html=False):
        """
        发送带附件的文件或html邮件
        :param to_list:收件人列表
        :param sub:主题
        :param content:邮件内容
        :param attach_path:附件路径列表
        :param is_html:是否是html格式
        :return:
        """
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"

        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        # 邮件正文内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        # 构造附件
        if len(attach_path) > 0:
            for path in attach_path:
                with open(r'' + path, 'rb') as f:
                    attach = MIMEText(f.read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    # 根据路径获取文件名称
                    filepath, shotname, extension = Common().get_filePath_fileName_fileExt(r'' + path)
                    attach["Content-Disposition"] = 'attachment;filename="{0}"'.format(
                        shotname + extension)
                    msg.attach(attach)

        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def sendImageMail(self, to_list, sub, content, pic_path, is_html=False):
        """
        发送到图片附件的邮件
        :param to_list:
        :param sub:
        :param content:
        :param is_html:
        :return:
        """
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        if is_html:
            subtype = "html"
        else:
            subtype = "plain"

        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ";".join(to_list)
        # 邮件正文内容
        msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))

        # 构造附件
        if len(pic_path) > 0:
            for path in pic_path:
                with open(r'' + path, 'rb') as f:
                    image = MIMEImage(f.read())
                    # 根据路径获取文件名称
                    filepath, shotname, extension = Common().get_filePath_fileName_fileExt(r'' + path)
                    image.add_header('Content-Disposition',
                                     'attachment;filename="{0}"'.format(shotname + extension))
                    msg.attach(image)

        try:
            self.server.sendmail(self.user, to_list, msg.as_string())
            return True
        except Exception as e:
            print(str(e))
            return False

    def __del__(self):
        """
        析构函数：释放资源
        :return:
        """
        # self.server.quit()
        self.server.close()


if __name__ == "__main__":
    # Vcode = ValidateCode()
    # code = Vcode.getCode(4)
    # print(Vcode.getNumCode(5))
    # print(code)
    # # Vcode.getCodeImage(code).show()
    # com = Common()
    # print(com.get_current_month_start_and_end('2019-11-10'))

    mailto_list = ['1002723914@qq.com']
    mail = SendEmail()

    if mail.sendTxtMail(mailto_list, "你好zt", "<p>hello world！</p><br><br><h1>HelloWorld</h1>", is_html=True):
        print("发送成功")
    else:
        print("发送失败")
