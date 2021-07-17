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
    # hook的签名
    key = '*************'
