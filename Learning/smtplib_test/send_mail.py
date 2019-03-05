# _*_ coding: utf-8 _*_

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart

HOST = 'smtp.163.com'
PORT = '25'  # 端口

FROM = 'xxx@163.com'
password = 'xxx'
TO = 'xxx@163.com;xxx@qq.com'
# TO = 'qiwenlong@jd.com'

def message_plain_html(TYPE, CONTENT, SUBJECT, FROM, TO):
    message = MIMEText(CONTENT, TYPE, 'utf-8')
    message['Subject'] = Header(SUBJECT, 'utf-8')
    message['From'] = FROM
    message['To'] = TO

    return message


def addfile(src):
    with open(src, 'rb') as fp:
        att = MIMEText(fp.read(), TYPE, 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; filename="%s"' %src

    return att


def message_file(TYPE, CONTENT, SUBJECT, FROM, TO, file_list):
    message = MIMEMultipart()  # 创建一个带附件的实例
    # 邮件正文内容
    message.attach(MIMEText(CONTENT, 'plain', 'utf-8'))
    # 构造附件
    for file in file_list:
        att = addfile(file)
        message.attach(att)
    message['Subject'] = Header(SUBJECT, 'utf-8')
    message['From'] = FROM
    message['To'] = TO

    return message


def addimg(src, imgid):
    with open(src, 'rb') as fp:
        msgImage = MIMEImage(fp.read())
    msgImage.add_header('Conten-ID', imgid)

    return msgImage


def message_image(TYPE, CONTENT, SUBJECT, FROM, TO):
    message = MIMEMultipart('related')  # 创建MIMEMultipart对象，采用related定义内嵌资源的邮件体
    message.attach(MIMEText(CONTENT, 'html', 'utf-8'))
    message.attach(addimg('1.jpg', 'image1'))

    message['Subject'] = Header(SUBJECT, 'utf-8')
    message['From'] = FROM
    message['To'] = TO

    return message


SUBJECT = '自动化测试报告'
# plain测试邮件
# TYPE = 'plain'
# CONTENT = '这是一个测试邮件!'
# message = message_plain_html(TYPE, CONTENT, SUBJECT, FROM, TO)


# html测试邮件
# TYPE = 'html'
# CONTENT = '''
# <p>Python 邮件发送测试...</p>
# <p><a href="http://www.runoob.com">这是一个链接</a></p>
# '''
# message = message_plain_html(TYPE, CONTENT, SUBJECT, FROM, TO)


# 附件测试邮件
# TYPE = 'base64'
# CONTENT = '这是一个测试邮件!'
# file_list = ['test.txt', 'test.xlsx']
# message = message_file(TYPE, CONTENT, SUBJECT, FROM, TO, file_list)


# HTML文本中添加图片测试邮件
TYPE = 'image'
CONTENT = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
message = message_image(TYPE, CONTENT, SUBJECT, FROM, TO)


smtp_obj = smtplib.SMTP()
smtp_obj.connect(HOST, PORT)
result = smtp_obj.login(FROM, password)
print('登陆结果: ', result)
smtp_obj.sendmail(from_addr=FROM, to_addrs=TO.split(';'), msg=str(message))
print("邮件发送成功...")

# try:
#    smtp_obj = smtplib.SMTP()
#    smtp_obj.connect(HOST, PORT)
#    result = smtp_obj.login(FROM, password)
#    print('登陆结果: ', result)
#    smtp_obj.sendmail(from_addr=FROM, to_addrs=TO.split(';'), msg=str(message))
#    print("邮件发送成功...")
# except smtplib.SMTPException:
#     print("Error: 无法发送邮件...")
