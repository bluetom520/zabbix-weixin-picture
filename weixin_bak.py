#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = '懒懒的天空'

import requests
import sys
import json
import time
import Image
from conf.INIFILES import read_config, write_config
from selenium import webdriver
import os
import datetime
from conf.BLog import Log
from get_pic import getpic
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class WeiXin(object):
    def __init__(self, corpid, corpsecret): # 初始化的时候需要获取corpid和corpsecret，需要从管理后台获取
        self.__params = {
            'corpid': corpid,
            'corpsecret': corpsecret
        }

        self.url_get_token = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.url_send = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        self.url_uploadimg = 'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg'
        self.img_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'

        self.__token = self.__get_token()
        self.__token_params = {
            'access_token': self.__token
        }

    def __raise_error(self, res):
        raise Exception('error code: %s,error message: %s' % (res.json()['errcode'], res.json()['errmsg']))
        global senderr
        global sendstatus
        sendstatus = False
        senderr = 'error code: %s,error message: %s' % (res.json()['errcode'], res.json()['errmsg'])

    def __get_token(self):
        # print self.url_get_token
        headers = {'content-type': 'application/json'}
        res = requests.get(self.url_get_token, headers=headers,  params=self.__params)

        try:
            return res.json()['access_token']
        except:
            self.__raise_error(res.content)


    def send_message(self,  agentid, messages, userid='', toparty=''):
        payload = {
            'touser': userid,
            'toparty': toparty,
            'agentid': agentid,
            "msgtype": "news",
            "news": messages
        }
        headers = {'content-type': 'application/json'}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        params = self.__token_params
        res = requests.post(self.url_send, headers=headers, params=params, data=data)
        try:
            return res.json()
        except:
            self.__raise_error(res)

    def get_media_ID(self, path):
        params = self.__token_params
        params['type'] = 'image\r\n'
        data = {'media': open(path, 'rb')}
        r = requests.post(url=self.img_url, params=params, files=data)
        dict = r.json()
        return dict['media_id']

    def get_imaging(self, path):
        params = self.__token_params
        data = {'media': open(path, 'rb')}
        r = requests.post(url=self.url_uploadimg, params=params, files=data)
        dict = r.json()
        return dict['url']


def main(send_to, subject, content, value):
    try:
        global sendstatus
        global senderr
        data = ''
        messages = {}
        body = {}
        config_file_path = get_path()
        CorpID = read_config(config_file_path, 'wei', "CorpID")
        CorpSecret = read_config(config_file_path, 'wei', "CorpSecret")
        agentid = read_config(config_file_path, 'wei', "agentid")
        web = read_config(config_file_path, 'wei', "web")
        content = json.loads(content)
        messages["message_url"] = web
        itemid = content[u'监控ID']
        itemvalue = value
        s = re.match(r'^[0-9\.]+$', itemvalue)
        if s:
            body["url"] = web + "history.php?action=showgraph&itemids[]=" + itemid
        else:
            body["url"] = web + "history.php?action=showvalues&itemids[]=" + itemid
        warn_message = ''
        if content[u'当前状态'] == 'PROBLEM':
            body["title"] = "服务器故障"
            warn_message += subject + '\n'
            warn_message += '详情：\n'
            warn_message += '告警等级：'+ content[u'告警等级'] + '\n'
            warn_message += '告警时间：'+ content[u'告警时间'] + '\n'
            warn_message += '告警地址：'+ content[u'告警地址'] + '\n'
            warn_message += '持续时间：'+ content[u'持续时间'] + '\n'
            warn_message += '监控项目：'+ content[u'监控项目'] + '\n'
            warn_message += content[u'告警主机'] + '故障(' + content[u'事件ID']+ ')'
        else:
            body["title"] = "服务器恢复"
            warn_message += subject + '\n'
            warn_message += '详情：\n'
            warn_message += '告警等级：'+ content[u'告警等级'] + '\n'
            warn_message += '恢复时间：'+ content[u'恢复时间'] + '\n'
            warn_message += '告警地址：'+ content[u'告警地址'] + '\n'
            warn_message += '持续时间：'+ content[u'持续时间'] + '\n'
            warn_message += '监控项目：'+ content[u'监控项目'] + '\n'
            warn_message += content[u'告警主机'] + '恢复(' + content[u'事件ID']+ ')'
        body["title"] = "服务器故障"
        body['description'] = warn_message
        wx = WeiXin(CorpID, CorpSecret)
        pic_path = getpic(itemid,s)
        picurl = wx.get_imaging(pic_path)
        body['picurl'] = picurl
        data = []
        data.append(body)
        messages['articles'] = data
        data = wx.send_message(toparty=send_to, agentid=agentid, messages=messages)
        sendstatus = True
    except Exception, e:
        senderr = str(e)
        sendstatus = False
    logwrite(sendstatus, data)


def get_path():
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path = path + '/config.ini'
    return config_path


def logwrite(sendstatus, content):
    logpath = '/var/log/zabbix/weixin'
    if not sendstatus:
        content = senderr
    t = datetime.datetime.now()
    daytime = t.strftime('%Y-%m-%d')
    daylogfile = logpath+'/'+str(daytime)+'.log'
    logger = Log(daylogfile, level="info", is_console=False, mbs=5, count=5)
    os.system('chown zabbix.zabbix {0}'.format(daylogfile))
    logger.info(content)


def get_item_pic(url, user, passwd, itemid, flag):
    try:
        driver = webdriver.PhantomJS("/usr/local/phantomjs-2.1.1/bin/phantomjs",service_log_path=os.path.devnull)
        # driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs-2.1.1/bin/phantomjs', service_log_path='/var/log/ghostdriver.log', service_args=["--webdriver-loglevel=NONE"])
        driver.get(url)
        driver.set_window_size(640, 480)
        picpath = "/usr/lib/zabbix/alertscripts/pic"
        driver.find_element_by_id("name").send_keys(user)     #输入用户名
        driver.find_element_by_id("password").send_keys(passwd)     #输入用户名
        driver.find_element_by_id("enter").click()
        if flag:
            item_url = url + "history.php?action=showgraph&fullscreen=1&itemids[]=" + itemid
        else:
            item_url = url + "history.php?action=showvalues&fullscreen=1&itemids[]=" + itemid
        driver.get(item_url)
        temp_name = picpath+"/"+itemid + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        time.sleep(0.5)
        driver.save_screenshot(temp_name)
        driver.close()
        driver.quit()
        # shutil.move(temp_name, backpath)
        if flag:
            im = Image.open(temp_name)
            im = im.crop((0, 0, 640, 480))
            im.save(temp_name)
        return temp_name
    except Exception, e:
        global senderr
        senderr = str(e)
        global sendstatus
        sendstatus = False
    logwrite(sendstatus, e)


def getpic(item_id, s):
    try:
        config_file_path = get_path()
        user = read_config(config_file_path, 'zabbix', "user")
        passwd = read_config(config_file_path, 'zabbix', "passwd")
        url = read_config(config_file_path, 'wei', "web")
        ppath = get_item_pic(url, user=user, passwd=passwd, itemid=item_id, flag=s)
        global sendstatus
        sendstatus = True
        return ppath
    except Exception, e:
        global senderr
        senderr = str(e)
        sendstatus = False
    logwrite(sendstatus, e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_to = sys.argv[1]
        subject = sys.argv[2]
        content = sys.argv[3]
        itemvalue = sys.argv[4]
        logwrite(True, content)
        main(send_to, subject, content, itemvalue)


