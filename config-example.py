DATABASE_CONFIG = {
    # 数据库host
    'host': '',
    # 数据库表名
    'dbname': 'subscribe',
    'user': '',
    'passwd': '',
    'port': 3306
}

CLIENT_CONFIG = {
    'domain': 'https://imlgw.top/',
    # hexo的_posts路径（git）
    'git_post_dir': 'E:/MyBlog/blog/source/_posts',
    # 邮箱账号
    'account': '*********',
    # 邮箱授权码（不是密码）
    'password': '*********',
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 587,
    # 邮箱消息类型
    'msg_type': 'html',
    # 博客更新邮件的subject
    'upd_subject': '🎉您订阅的Tadow小站又更新啦~',
    # 博客订阅邮件的subject
    'sub_subject': '🎉感谢订阅Tadow~'
}

SERVER_CONFIG = {
    # 服务端端口
    'port': 9993,
    # 服务端context
    'context': '/sbe'
}