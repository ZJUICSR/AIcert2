#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import argparse
import threading
from aicert.utils.threads import IOtool
from web import run


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help='ip')
    parser.add_argument('--port', type=int, default='12345', help='port')
    parser.add_argument('--debug', type=bool, default=False, help='debugifopen')
    return parser.parse_args()


def main():
    # init threading
    t = threading.Thread(target=IOtool.check_sub_task_threading)
    t.setDaemon(True)
    t.start()
    # run web
    args = get_args()
    run(args)


if __name__ == '__main__':
    main()