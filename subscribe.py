import hashlib
import hmac
import json
from datetime import datetime
from smtplib import SMTPRecipientsRefused
from flask import Flask, request, render_template
from jinja2 import Environment, FileSystemLoader

from config import Config
from mail import send_mail
import requests
import frontmatter
import os
from urllib.parse import urlparse

from models import Addr

app = Flask(__name__)
# 项目根路径
context = Config.server_context


# todo: 日志

class Blog:
    def __init__(self, dicts):
        self.__dict__ = dicts

    def __str__(self):
        return self.__dict__.__str__()


@app.route(context + '/hook', methods=['POST'])
def hook():
    # if not verify_signature(request.data):
    #     return 'authentication failed'
    payload = json.loads(request.data)
    before = payload['before']
    after = payload['after']
    blogs = get_diff(Config.diff_api, before, after)
    path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template('mail.html')
    content = template.render(blogs=blogs)
    emails = [address.email for address in Addr.select()]
    # send_mail("privateli@qq.com", Config.upd_subject, content, 'html')
    send_mail(emails, Config.upd_subject, content, 'html')
    return 'success'


# 验证hook签名（https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks）
def verify_signature(payload):
    h = hmac.new(key=Config.key.encode('UTF-8'), msg=payload, digestmod=hashlib.sha256)
    signature = 'sha256=' + h.hexdigest()
    return hmac.compare_digest(signature, request.headers['X-Hub-Signature-256'])


@app.route(context + '/subscribe', methods=['POST'])
def save_adds():
    ip = request.remote_addr
    email = request.form['email']
    name = request.form['name']
    if email == "" or name == "":
        return render_template('./subscribe.html', status=2, msg="请输入正确的邮箱和用户名！")
    # print(email, name)
    if Addr.select().where(Addr.email == email).count() == 0:
        order = Addr.select().count()
        content = render_template('./success.html', name=name, order=order + 1)
        try:
            send_mail([email], Config.sub_subject, content, 'html')
        except SMTPRecipientsRefused:
            return render_template('./subscribe.html', status=2, msg="请输入正确的邮箱！！！")
        # 验证邮箱合法后再插入数据库
        Addr.create(ip=ip, email=email, name=name)
        return render_template('./subscribe.html', status=1)
    else:
        return render_template('./subscribe.html', status=2, msg="该邮箱已经订阅过了喔~")


@app.route(context + '/')
def index():
    return render_template('./subscribe.html')


def get_diff(api, before, after):
    adds = api + before + '...' + after
    resp = requests.get(adds).json()
    blogs = [Blog(file) for file in resp.get('files')]
    # 调整属性值返回给前端
    for blog in blogs:
        blog.url, patch = get_url_patch(blog.raw_url)
        blog.filename = blog.filename[:-3]
        blog.patch = patch
    return blogs


def get_url_patch(gh_raw_url):
    res = urlparse(gh_raw_url)
    raw_url = Config().raw_api + res.path.replace('/raw', '')
    print(raw_url)
    file_raw = requests.get(raw_url).text
    # print(file_raw)
    md = frontmatter.loads(file_raw)
    # 规格化一下：2021/7/1 -> 2021/07/01
    date = datetime.strptime(md.metadata['date'], '%Y/%m/%d')
    sdate = datetime.strftime(date, '%Y/%m/%d')
    abbrlink = md.metadata['abbrlink']
    # print(md.content)
    return Config.domain + sdate + '/' + abbrlink, md.content[:100]


if __name__ == '__main__':
    # 建表
    Addr.create_table()
    app.run(port=Config.server_port)
