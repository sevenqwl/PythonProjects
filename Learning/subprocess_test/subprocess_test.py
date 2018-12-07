#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

import subprocess

cmd = "ping -c 2 10.6.0.29"
for i in range(10):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(p.stdout.read().decode('gbk'))


