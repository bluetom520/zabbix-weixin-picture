#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'bluetom'

"""Package for  operations.
"""

import os
if __name__ == '__main__':
    import sys
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, root_path)

import re
import shlex

import subprocess
import sys
import linecache
reload(sys)
sys.setdefaultencoding('utf8')

# 需要修改，配置文件位置
CONFIG_CFG = '/etc/zabbix/zabbix_agentd.conf'

#{{{loadconfig


def loadconfig(cfgfile=None, detail=False):
    """Read config file and parse config item to dict.
    """
    if not cfgfile:
        cfgfile = CONFIG_CFG

    settings = {}
    with open(cfgfile) as f:
        for line_i, line in enumerate(f):
            # line_i[行号]，line[每行内容]

            # 删除空白符(包括'\n', '\r',  '\t',  ' ')
            line = line.strip()

            # 跳过空行和注释('# '开头的)
            if not line or line.startswith('# '):
                continue

            # detect if it's commented
            if line.startswith('#'):
                line = line.strip('#')
                commented = True
                if not detail:
                    continue
            else:
                commented = False

            # 将行以第一个'='分割
            #########################################
            fs = re.split('=', line, 1)
            if len(fs) != 2:
                continue

            item = fs[0].strip()
            value = fs[1].strip()

            if settings.has_key(item):
                if detail:
                    count = settings[item]['count'] + 1
                if not commented:
                    settings[item] = detail and {
                        'file': cfgfile,
                        'line': line_i,
                        'value': value,
                        'commented': commented,
                    } or value
            else:
                count = 1
                settings[item] = detail and {
                    'file': cfgfile,
                    'line': line_i,
                    'value': fs[1].strip(),
                    'commented': commented,
                } or value
            if detail:
                settings[item]['count'] = count

    return settings

#}}}
#{{{cfg_get


def cfg_get(item, detail=False, config=None):
    """Get value of a config item.
    """
    if not config:
        config = loadconfig(detail=detail)
    if config.has_key(item):
        return config[item]
    else:
        return None
#}}}
#{{{cfg_set


def cfg_set(item, value, commented=False, config=None):
    """Set value of a config item.
       如果可以获取到key，则对key后的item进行修改
       如果获取不到key，则直接在配置文件后进行追加一行
    """
    cfgfile = CONFIG_CFG
    v = cfg_get(item, detail=True, config=config)
    # print v

    if v:
        # detect if value change
        if v['commented'] == commented and v['value'] == value:
            return True

        # empty value should be commented
        # 如果有key，但是传的value值为空，会将此行进行注释
        if value == '':
            commented = True

        # replace item in line
        lines = []
        with open(v['file']) as f:
            for line_i, line in enumerate(f):
                if line_i == v['line']:
                    # 对没注释的行进行操作
                    if not v['commented']:
                        # 检测是否需要注释
                        if commented:
                            if v['count'] > 1:
                                # delete this line, just ignore it
                                pass
                            else:
                                # comment this line
                                #########################################
                                # lines.append('#%s=%s\n' % (item, value))
                                lines.append('#%s\n' % (line,))
                        else:
                            #########################################
                            lines.append('%s=%s\n' % (item, value))
                    else:
                        if commented:
                            # do not allow change comment value
                            lines.append(line)
                            pass
                        else:
                            # append a new line after comment line
                            # lines.append(line)
                            #########################################
                            lines.append('%s=%s\n' % (item, value))
                else:
                    lines.append(line)
        with open(v['file'], 'w') as f:
            f.write(''.join(lines))
    else:
        # append to the end of file
        with open(v['file'], 'a') as f:
            f.write('\n%s%s = %s\n' % (commented and '#' or '', item, value))

    return True
#}}}
if __name__ == '__main__':
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # loadconfig()
    # pp.pprint(loadconfig())
    print cfg_get('Hostname')                     #有#号的不显示
    # print cfg_get('Subsystem', detail=True)     #detail显示细节
    # print cfg_set('Subsystem','')               #直接注释
    # print cfg_set('Subsystem', '44444333')       #设置值
    # # print cfg_set('Subsystem', 'sftp\t/usr/libexec/openssh/sftp-server',commented=False)
    # print cfg_get('Subsystem', detail=True)     #detail显示细节

