## hexo邮件订阅插件
一直想给自己博客添加一个订阅的功能，所以用py3自己随便写了一个，一边学一边写的，代码比较糟糕，大佬轻喷
### 使用前提
1. 有一个能跑py的云服务器
2. hexo博客文件的`_posts`文件夹是一个git仓库（我为了同步文章将这个文件夹设置成立git仓库）
3. hexo博客文章的url链接是由domain+createDate+文件名拼音构成，比如: https://imlgw.top/2020/06/02/gacache-fen-bu-shi-huan-cun/

> 第三点我主要针对自己的博客进行开发的，可以根据自己的设置调整

### 使用
首先安装依赖：`pip install -r requirements.txt`，然后`cp config-example.py config.py`，修改对应的配置，然后执行db.sql初始化数据库
#### Server端
直接运行`python server.py`
#### Client端
文章更新后，在本地的`_posts`文件夹中`commit`，然后执行`client.py`就可以向订阅者发送更新邮件（这里可以通过一些批处理脚本将其合并成一条指令）