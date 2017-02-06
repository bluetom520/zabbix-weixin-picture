#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'bluetom'

from lxml import etree
xml_file = etree.parse('problem.xml')
root_node = xml_file.getroot()
a = root_node.find(u"告警等级").text
print a

root2 = etree.fromstring(open('problem.xml').read())
print root2.xpath(u"告警等级")[0].text
print root2.xpath(u"监控项目")[0].text
print root2.xpath(u"告警等级")[0].text