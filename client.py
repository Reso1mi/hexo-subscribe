import os
import string
import time
from subprocess import Popen, PIPE
import dateutil.parser
import frontmatter
from pypinyin import lazy_pinyin
import config
from mail import send_mail
from models import Addr
from jinja2 import Environment, FileSystemLoader


class UpdateBlog:
    def __init__(self, name, url):
        self.name = name
        self.url = url


def get_upd(repo_dir):
    # git config --global core.quotepath false
    p = Popen("git diff --name-only HEAD~ HEAD", shell=True, stdout=PIPE, stderr=PIPE, cwd=repo_dir)
    p.wait()
    diff_name = p.stdout
    update_blogs = []
    for article in diff_name:
        # 解码
        article = article.decode("utf-8").strip()
        # 获取时间
        date_time = get_date(repo_dir + '/' + article)
        # 去除空格和后缀.md
        article = article.replace(' ', '').lower().split('.')[0]
        # 拼接文章链接
        url = config.CLIENT_CONFIG['domain'] + date_time + '/' + '-'.join(
            lazy_pinyin(''.join(c for c in article if c not in string.punctuation)))
        update_blogs.append(UpdateBlog(article, url))
    return update_blogs


# frontMatter不能有Tab
def get_date(md_file):
    with open(md_file, 'r', encoding='UTF-8') as f:
        md = frontmatter.load(f)
        dt = os.path.getctime(md_file)
        if 'date' in md.metadata:
            dt = md.metadata['date']
        else:
            return time.strftime('%Y/%m/%d', time.localtime(dt))
        if type(dt) == str:
            # toml 格式下date被识别为字符串
            return dateutil.parser.parse(dt).strftime('%Y/%m/%d')
        else:
            # yaml 格式下date被识别为datetime，直接返回
            return dt.date()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 获取订阅的人
    users = Addr.select()
    emails = [user.email for user in users]
    # print(emails)
    # 获取更新的文章信息
    upd_blogs = get_upd(config.CLIENT_CONFIG['git_post_dir'])
    # 渲染需要发送的html文件
    path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(searchpath=path))
    # print(env)
    template = env.get_template('mail.html')
    content = template.render(blogs=upd_blogs)
    # print(content)
    send_mail(emails, config.CLIENT_CONFIG['upd_subject'], content, 'html')