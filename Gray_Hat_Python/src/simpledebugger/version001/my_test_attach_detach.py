# coding: utf-8
'''
Created from 2016-07-15 23:21:08

@author: MrLi
@note: 测试function[attach, detach]
'''

import my_debugger

debugger = my_debugger.debugger()

pid = raw_input('Enter the PIS of the process to attach to: ')
debugger.attach(int(pid))
debugger.detach()