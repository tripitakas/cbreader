#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os.path as path
from controller.app import BASE_DIR

XML_DIR = path.join(BASE_DIR, 'data', 'xml')
MULU_DIR = path.join(BASE_DIR, 'data', 'meta', 'mulu')
JUAN_DIR = path.join(BASE_DIR, 'data', 'meta', 'juan')


def get_juan(code):
    """ 根据code获取它属于第几卷。
    :param code code可以是行编码，也可以是页编码。比对时会根据code的长度进行比较，裁剪掉多余的部分
    :param source_type xml表示xml文本，json表示是从xml文件中提取的json信息"""

    def cmp(page_code1, page_code2):
        # 裁剪到长度一致
        length = min(len(page_code1), len(page_code2))
        page_code1 = page_code1[0:length]
        page_code2 = page_code2[0:length]
        # 判断格式以及藏经类型是否一致
        h1 = regex.search(page_code1)
        h2 = regex.search(page_code2)
        if not h1 or not h2 or h1.group(1) != h2.group(1):
            return False
        # 将栏位转换为数字
        tran = dict(a='1', b='2', c='3')
        if h1.group(5):
            page_code1 = h1.group(1) + h1.group(2) + h1.group(3) + h1.group(4) + tran.get(h1.group(6)) + h1.group(7)
        if h2.group(5):
            page_code2 = h2.group(1) + h2.group(2) + h2.group(3) + h2.group(4) + tran.get(h2.group(6)) + h2.group(7)
        # 比较大小
        num1 = int(re.sub('[a-zA-Z_]', '', page_code1))
        num2 = int(re.sub('[a-zA-Z_]', '', page_code2))
        return num1 - num2

    regex = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)(([abc])(\d+))?')
    head = regex.search(code)
    assert head and head.group(0)

    filename = '%sn%s.json' % (head.group(1) + head.group(2), head.group(3))
    json_file = path.join(JUAN_DIR, head.group(1), head.group(1) + head.group(2), filename)
    with open(json_file, 'r') as fp:
        juan_list = json.load(fp)

    for i, juan in enumerate(juan_list):
        next = juan_list[i + 1]
        if cmp(juan['head'], code) <= 0 <= cmp(next['head'], code) and juan['n'] == next['n']:
            return int(juan['n'])
    return False


def get_juan_cnt(code):
    """ 根据code获取该部经的总卷数 """
    regex = re.compile(r'^([A-Z]{1,2})([A-Z]?\d+[A-Za-z]?)')
    head = regex.search(code)
    assert head and head.group(0)

    filename = '%sn%s.json' % (head.group(1) + head.group(2), head.group(3))
    json_file = path.join(JUAN_DIR, head.group(1), head.group(1) + head.group(2), filename)
    with open(json_file, 'r') as fp:
        juan_list = json.load(fp)

    return int(len(juan_list)/2)


if __name__ == '__main__':
    juan = get_juan('T30n1579_p0299a08')
    print(juan)
