ZABBIX可以实现短信、邮件、微信等各种报警，这三种基本大家都很熟悉， 现在基于微信写py，感觉钉钉的团队是从微信出来的，变量都不改，太懒了，说可以实现微信报警苍老师说过：Life is short,you need python!

[TOC]
### 1 微信配置
微信公众号官网：https://qy.weixin.qq.com/
我们主要获取四个参数：部门id，应用ID和CorpID和CorpSecret
#### 1.1 注册安装
注册微信企业号，安装手机微信略过
##### 1.1.1 部门设置
在通信录管理里面设置部门，如下图，我们这里设置的运维部，这个部门id要记住，在ZABBIX里面要配置这个名称，然后把你需要发送告警的人员添加到这个部门里面
##### 1.1.2 应用设置
点击左侧“应用中心”，新建消息型应用，应用名称为“服务器报警”，“应用可见范围”，添加刚刚新建的子部门（运维部），点击“服务器报警”，记录应用ID
##### 1.1.3 微应用设置
点击左侧“设置”，权限管理，新建普通管理组，名称填写“服务器报警组”。点击修改“通讯录权限”，勾选管理，点击修改“应用权限”，勾选刚刚创建的“服务器报警”，点击刚刚创建的“服务器报警组”，记录左侧的CorpID与CorpSecret
### 2 程序配置
代码托管到github：https://github.com/bluetom520/zabbix-weixin
```
git clone https://github.com/bluetom520/zabbix-weixin.git
pip install requests/requests-2.12.4-py2.py3-none-any.whl
cp dingding/* /usr/lib/zabbix/alertscripts/
chown -R zabbix:zabbix /usr/lib/zabbix/alertscripts/dingding.py
chmod +x   /usr/lib/zabbix/alertscripts/dingding.py
chmod a+w /usr/lib/zabbix/alertscripts/config.ini

```
修改config.ini，把上节获得的三个参数填入，web是点击报警信息后跳转的页面，设置的监控数据的最新出图，但手机浏览器不支持。后面看怎么把图抓下来放到微信报警里面，抓图早已经实现了，看大家有没有兴趣了，有兴趣我加再加：）
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
```
服务器:{HOST.NAME}: {TRIGGER.NAME}已恢复!

{
"告警主机":"{HOST.NAME}",
"告警地址":"{HOST.IP}",
"告警时间":"{EVENT.DATE} {EVENT.TIME}",
"恢复时间":"{EVENT.RECOVERY.DATE} {EVENT.RECOVERY.TIME}",
"告警等级":"{TRIGGER.SEVERITY}",
"告警信息":"{TRIGGER.NAME}",
"监控项目":"{ITEM.NAME}",
"当前状态":"{TRIGGER.STATUS}",
"持续时间":"{EVENT.AGE}",
"事件ID":"{EVENT.ID}",
"监控ID":"{ITEM.ID}",
"监控取值":"{ITEM.LASTVALUE}"
}

服务器:{HOST.NAME}发生: {TRIGGER.NAME}故障!

{
"告警主机":"{HOST.NAME}",
"告警地址":"{HOST.IP}",
"告警时间":"{EVENT.DATE} {EVENT.TIME}",
"告警等级":"{TRIGGER.SEVERITY}",
"告警信息":"{TRIGGER.NAME}",
"监控项目":"{ITEM.NAME}",
"当前状态":"{TRIGGER.STATUS}",
"持续时间":"{EVENT.AGE}",
"事件ID":"{EVENT.ID}",
"监控ID":"{ITEM.ID}",
"监控取值":"{ITEM.LASTVALUE}"
}
```
 - 条件
![](leanote://file/getImage?fileId=58708a1dd31d9c3103000007)
 - 操作
![](leanote://file/getImage?fileId=587386fb4f1ffe4e59000003)

### 4 效果展现
故障图
![](leanote://file/getImage?fileId=587388a24f1ffe4e59000004)
恢复图
![](leanote://file/getImage?fileId=587388ae4f1ffe4e59000005)

### 5 docker环境修改
```
tar zxvf  requests-2.12.4.tar.gz
docker cp requests-2.12.4 zabbix:/usr/local/share/zabbix/alertscripts
docker cp dingding zabbix:/usr/local/share/zabbix/alertscripts
docker exec -it zabbix /bin/bash
cd /usr/local/share/zabbix/alertscripts/requests-2.12.4
python setup.py install
rm -rf requests-2.12.4
cd ..
mv zabbix-weixin/* .
vi config.ini
exit
docker restart zabbix

```
## 具体内容参考：https://note.gitcloud.cc/blog/post/bluetom520/%E9%92%89%E9%92%89%E6%8A%A5%E8%AD%A6%E6%A8%A1%E6%9D%BF

