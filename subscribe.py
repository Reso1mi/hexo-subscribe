import json
from smtplib import SMTPRecipientsRefused
from flask import Flask, request, render_template
from jinja2 import Environment, FileSystemLoader

import config
from mail import send_mail
from models import Addr
import requests
import frontmatter
import string
from pypinyin import lazy_pinyin
from zhon.hanzi import punctuation
import os

app = Flask(__name__)
# 项目根路径
context = config.SERVER_CONFIG['context']

punctuation += string.punctuation


class Blog:
    def __init__(self, dicts):
        self.__dict__ = dicts

    def __str__(self):
        return self.__dict__.__str__()


@app.route(context + '/hook', methods=['POST'])
def hook():
    payload = json.loads(request.get_data())
    before = payload['before']
    after = payload['after']
    blogs = get_diff(config.SERVER_CONFIG['github_compare_api'], before, after)

    path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template('mail.html')
    content = template.render(blogs=blogs)
    # send_mail(emails, config.CLIENT_CONFIG['upd_subject'], content, 'html')


@app.route(context + '/subscribe', methods=['POST'])
def save_adds():
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


def get_diff(api, before, after):
    adds = api + before + '...' + after
    resp = requests.get(adds).json()
    print(resp)
    files = resp.get('files')
    print(files)
    blogs = [Blog(file) for file in files]
    # 获取日期
    for blog in blogs:
        blog.date = get_date(blog.filename)
        blog.url = config.CLIENT_CONFIG['domain'] + blog.date + '/' + '-'.join(
            lazy_pinyin(''.join(c for c in blog.filename.replace(' ', '').lower().split('.')[0] if
                                c not in punctuation)))
    return blogs


def get_date(md_name):
    file_raw = requests.get(config.SERVER_CONFIG['github_raw_api'] + md_name).text
    md = frontmatter.loads(file_raw)
    return md.metadata['date']


if __name__ == '__main__':
    Addr.create(ip="127.0.0.1", email="print@qq.com", name="lgw")
    users = Addr.select()
    emails = [user.email for user in users]
    # app.run(port=config.SERVER_CONFIG['port'])