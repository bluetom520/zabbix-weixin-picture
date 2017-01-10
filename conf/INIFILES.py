#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TT'
import sys,os,time
import ConfigParser


class Config:
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result

    def set(self, field, key, value):
        try:
            self.cf.set(field, key, value)
            self.cf.write(open(self.path,'w'))
        except:
            return False
        return True


def read_config(config_file_path, field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result


def write_config(config_file_path, field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except:
        sys.exit(1)
    return True

if __name__ == "__main__":
    config_file_path = 'config.ini'
    print read_config(config_file_path, 'baseconf', "host")

    write_config(config_file_path, 'baseconf', "host", '192.168.0.101')

    print read_config(config_file_path, 'baseconf', "host")