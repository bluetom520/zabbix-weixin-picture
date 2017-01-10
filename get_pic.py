#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'bluetom'

import sys
import time
import datetime
from selenium import webdriver
from conf.INIFILES import read_config
from conf.BLog import Log
import os


def get_item_pic(url, user, passwd, itemid):
    try:
        driver = webdriver.PhantomJS("/usr/local/phantomjs-2.1.1/bin/phantomjs")
        driver.get(url)
        driver.set_window_size(640, 480)
        path = "/usr/lib/zabbix/alertscripts/pic"
        # path = "/tmp/pic"
        if not os.path.exists(path):
            os.makedirs(path)
        driver.find_element_by_id("name").send_keys(user)     #输入用户名
        driver.find_element_by_id("password").send_keys(passwd)     #输入用户名
        driver.find_element_by_id("enter").click()
        item_url = url + "history.php?action=showgraph&fullscreen=1&itemids[]=" + itemid
        driver.get(item_url)
        temp_name = itemid + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        time.sleep(0.5)
        driver.save_screenshot(temp_name)
        driver.close()
        driver.quit()
        return temp_name
        # shutil.move(temp_name, backpath)
        # im = Image.open(temp_name)
        # im = im.crop((0, 0, 640, 480))
        # im.save(temp_name)
    except Exception, e:
        senderr = str(e)
        sendstatus = False

def getpic(item_id):
    try:
        global sendstatus
        global senderr
        start = time.time()
        config_file_path = get_path()
        user = read_config(config_file_path, 'zabbix', "user")
        passwd = read_config(config_file_path, 'zabbix', "passwd")
        url = read_config(config_file_path, 'wei', "web")
        path = get_item_pic(url, user=user, passwd=passwd, itemid=item_id)
        sendstatus = True
    except Exception, e:
        senderr = str(e)
        sendstatus = False
    # logwrite(sendstatus, path)
    return path


def logwrite(sendstatus, content):
    logpath = '/var/log/zabbix/weixin'
    # logpath = "log"
    if not sendstatus:
        content = senderr
    t = datetime.datetime.now()
    daytime = t.strftime('%Y-%m-%d')
    daylogfile = logpath+'/'+str(daytime)+'.log'
    logger = Log(daylogfile, level="info", is_console=False, mbs=5, count=5)
    os.system('chown zabbix.zabbix {0}'.format(daylogfile))
    logger.info(content)


def get_path():
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path = path + '/config.ini'
    return config_path


if __name__ == "__main__":
    print getpic('24099')


