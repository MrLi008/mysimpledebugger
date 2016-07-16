# coding: utf-8
'''
Created from 2016-07-16 11:06:15

@author: MrLi
@note: 测试function[func_resolve, bp_set_soft]
'''

import my_debugger
debugger = my_debugger.debugger()
pid = raw_input('Enter the PID of the process to attach to: ')
debugger.attach(int(pid))

printf_address = debugger.func_resolve('msvcrt', 'printf')
print '[*] Address of printf: 0x%08x' % printf_address
debugger.bp_set_software(printf_address)

strcpy_address = debugger.func_resolve('msvcrt', 'strcpy')
print '[*] Address of strcpy: 0x%08x' % strcpy_address
debugger.bp_set_hardware(strcpy_address, 1, my_debugger.HW_EXECUTE)

strlen_address = debugger.func_resolve('msvcrt', 'strlen')
print '[*] Address of strlen: 0x%08x' % strlen_address
debugger.bp_set_memory(strlen_address, 10)

debugger.run()
