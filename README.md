ZABBIX可以实现短信、邮件、微信等各种报警，这三种基本大家都很熟悉， 现在基于微信写py，之前写了个无图的，感觉微信色彩不丰富，再加个有图的，说可以实现微信报警，苍老师的话牢记心头：Life is short,you need python!

[TOC]
### 1 微信配置（与无图版一样）
微信公众号官网：https://qy.weixin.qq.com/
我们主要获取四个参数：部门id，应用ID和CorpID和CorpSecret
#### 1.1 注册安装
注册微信企业号，安装手机微信略过
##### 1.1.1 部门设置
在通信录管理里面设置部门，如下图，我们这里设置的运维部，这个部门id要记住，在ZABBIX里面要配置这个名称，然后把你需要发送告警的人员添加到这个部门里面
##### 1.1.2 应用设置
点击左侧“应用中心”，新建消息型应用，应用名称为“服务器报警”，“应用可见范围”，添加刚刚新建的子部门（运维部），点击“服务器报警”，记录应用ID
##### 1.1.3 权限管理
点击左侧“设置”，权限管理，新建普通管理组，名称填写“服务器报警组”。点击修改“通讯录权限”，勾选管理，点击修改“应用权限”，勾选刚刚创建的“服务器报警”，点击刚刚创建的“服务器报警组”，记录左侧的CorpID与CorpSecret
### 2 程序配置
代码托管到github：https://github.com/bluetom520/zabbix-weixin-picture
下载
```
git clone https://github.com/bluetom520/zabbix-weixin-picture.git
```
安装requests
```
pip install requests/requests-2.12.4-py2.py3-none-any.whl
```
安装selenium
```
tar zxvf selenium-3.0.2.tar.gz
cd selenium-3.0.2
python setup.py install
```
安装phantomjs
```
rpm -Uvh freetype-2.4.11-12.el7.x86_64.rpm
rpm -Uvh  fontconfig-2.10.95-10.el7.x86_64.rpm
tar -jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2
mv phantomjs-2.1.1-linux-x86_64 /usr/local/phantomjs-2.1.1
```
程序部署
```
cp zabbix-weixin-picture/* /usr/lib/zabbix/alertscripts/
cd /usr/lib/zabbix/alertscripts/
chown -R zabbix:zabbix pic
chown -R zabbix:zabbix weixin.py
chmod o+x weixin.py
chown -R zabbix:zabbix config.ini
chmod o+w config.ini
```
修改config.ini，把上节获得的三个参数填入，web 设置为zabbix服务器主页，是点击报警信息后跳转的页面，设置的监控数据的最新出图。
```
[wei]
corpid = wx3317042c8bcf7551
corpsecret = m0VqePgfDsTbVoFlGSx5-JOCbE5p43rf5G-GC2CqN4Wq2Ce0OJQkgo0JnXMqKypv
agentid = 2
toparty =
web = http://192.168.1.199/zabbix/
```
### 3 ZABBIX配置
#### 3.1 报警媒介类型
到管理-》报警媒介类型配置我们的微信
![](leanote://file/getImage?fileId=587386aa4f1ffe4e59000001)
#### 3.2 配置用户
到管理-》用户-》报警媒介-》添加，注意填写收件人为我们之前设置的运维部id 2
![](leanote://file/getImage?fileId=587386cf4f1ffe4e59000002)
#### 3.3 动作设置
到配置-》动作-》创建动作（触发器）
 - 动作
![](leanote://file/getImage?fileId=587089ffd31d9c3103000006)
 - 条件
![](leanote://file/getImage?fileId=58708a1dd31d9c3103000007)
 - 操作
![](leanote://file/getImage?fileId=587386fb4f1ffe4e59000003)

### 4 效果展现
故障图
![](leanote://file/getImage?fileId=5874b25d2eb3ec5799000005)
恢复图
![](leanote://file/getImage?fileId=5874b2292eb3ec5799000004)

### 5 docker环境修改
参照无图版



