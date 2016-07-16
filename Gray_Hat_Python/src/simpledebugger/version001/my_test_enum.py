# coding: utf-8
'''
Created from 2016-07-16 10:10:50

@author: MrLi
@note: 测试function[enumerate_threads]
'''

import my_debugger
debugger = my_debugger.debugger()
pid = raw_input('Enter the PID of the process to attach to: ')
debugger.attach(int(pid))

list = debugger.enumerate_thread()
# For each thread in the list we want to 
# grab the value of each registers

for thread_id in list:
    thread_context = debugger.get_thread_context(thread_id)
    # Now let's output the contents of the registers
    print '[*] Dumping registers for thread id: ', thread_id
    print '[*] EIP 0x%08x' % thread_context.Eip
    print '[*] end dumping'
    
debugger.detach()