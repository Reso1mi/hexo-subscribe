## hexo邮件订阅插件
一直想给自己博客添加一个订阅的功能，所以用py3自己随便写了一个，一边学一边写的，代码比较糟糕，大佬轻喷，web框架采用的`flask`，orm框架采用的`peewee`，数据库使用的`sqlite3`，利用GitHub的webhook做同步推送
### 使用前提
1. 有一个能跑py3的云服务器
2. hexo博客文件的`_posts`文件夹是一个git仓库，并且同步到了github（我为了同步文章将其同步上去了）
3. 使用了[hexo-abbrlink](https://github.com/rozbo/hexo-abbrlink)插件生成永久文章url

> 第三点我主要针对自己的博客进行开发的，可以根据自己的情况进行调整，修改`get_url(md_name)`方法就行了

### 使用

#### WebHook配置
首先配置好博客文件仓库的的hook，填写好对应的回调地址，设置好密钥。
![](https://i.loli.net/2021/07/18/HFRlqGQuUABzhfp.png)

#### 订阅配置
先安装好依赖：`pip install -r requirements.txt`，然后`cp config-example.py config.py`，修改对应的配置项
```python
class Config:
    # Flask端口
    server_port = 9993
    # web路径上下文
    server_context = '/sbe'
    # sqlite的db文件地址
    db = 'C:/PycharmSpace/hexo-subscribe/address.db'
    # 博客主域名
    domain = 'https://imlgw.top/'
    # 发邮件的账户
    account = 'xxxxx@xx.com'
    # 邮件授权码
    password = '****************'
    # smtp服务器地址
    smtp_server = 'smtp.qq.com'
    # smtp服务器端口
    smtp_port = 587
    # 邮件更新的subject
    upd_subject = '🎉您订阅的Tadow小站又更新啦~'
    # 邮件订阅通知的subject
    sub_subject = '🎉感谢订阅Tadow~'
    # git远程仓库文件raw的api
    raw_api = 'https://cdn.jsdelivr.net/gh/username/repo/'
    # git远程仓库compare分支的api
    diff_api = 'https://api.github.com/repos/username/repo/compare/'
    # hook的签名密钥
    key = '*************'
```
然后直接直接运行`subscribe.py`脚本就ok了。当博客更新后只要向GitHub推送一下就会触发钩子向订阅者发送邮件，实现订阅的效果。
### 效果

订阅页面

![](https://i.loli.net/2021/07/18/N21hTfVlt5Kncyi.png)

博客更新通知邮件

![](https://i.loli.net/2021/07/18/VUPCpDEZxJoWScL.png)

> 页面部分大家可以自行修改