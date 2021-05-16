from smtplib import SMTPRecipientsRefused

from flask import Flask, request, render_template

import config
from mail import send_mail
from models import Addr

app = Flask(__name__)
# 项目根路径
context = config.SERVER_CONFIG['context']


@app.route(context + '/subscribe', methods=['POST'])
def save_addr():
    ip = request.remote_addr
    email = request.form['email']
    name = request.form['name']
    if email == "" or name == "":
        return render_template('/subscribe.html', status=2, msg="请输入正确的邮箱和用户名！")
    # print(email, name)
    if Addr.select().where(Addr.email == email).count() == 0:
        order = Addr.select().count()
        content = render_template('/success.html', name=name, order=order + 1)
        try:
            send_mail([email], config.CLIENT_CONFIG['sub_subject'], content, config.CLIENT_CONFIG['msg_type'])
        except SMTPRecipientsRefused:
            return render_template('/subscribe.html', status=2, msg="请输入正确的邮箱！！！")
        # 验证邮箱合法后再插入数据库
        Addr.create(ip=ip, email=email, name=name)
        return render_template('/subscribe.html', status=1)
    else:
        return render_template('/subscribe.html', status=2, msg="这个邮箱已经订阅过了喔~")


@app.route(context + '/')
def index():
    return render_template('/subscribe.html')


if __name__ == '__main__':
    app.run(port=config.SERVER_CONFIG['port'])
