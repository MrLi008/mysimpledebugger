# coding: utf-8
'''
Created from 2016-07-16 10:37:11

@author: MrLi
@note: 测试function[get_debug_event]
'''

import my_debugger
debugger = my_debugger.debugger()

pid = raw_input('Enter the PID of the process to attach to: ')
debugger.attach(int(pid))

debugger.run()
debugger.detach()