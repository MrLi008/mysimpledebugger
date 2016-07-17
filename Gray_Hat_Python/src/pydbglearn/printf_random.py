# coding: utf-8
'''
Created from 2016-07-17 10:20:26

@author: MrLi
@note: 实现一个自定义的回调函数, 
读取printf函数用到的counter变量, 并替换值, 再打印出来
'''

from pydbg import *
from pydbg.defines import *
from ctypes import *
import struct 
import random

# kernel32 = windll.kernel32


# This is our user defined callback function
def printf_randomizer(dbg):
    
    # Read in the value of the counter at ESP + 0x8 as a DWORD
    parameter_addr = dbg.context.Esp + 0x8
    counter = dbg.read_process_memory(parameter_addr, 4)
#     print 'kernel32.getlasterror(): ', kernel32.GetLastError()
    
    # When we user read_process_memory, it returns a packed binary
    # string. We must first unpack it before we can use it further.
    print 'old tuple', struct.unpack('L', counter),
    counter = struct.unpack('L', counter)[0]
    print 'old Counter: %d' % int(counter)

    # Generate a random number and pack it into binary format
    # so that it is written correctly back into the process
    random_counter = random.randint(1,50)
    print 'new Counter: %d' % int(random_counter)
    random_counter = struct.pack('L', random_counter)[0]
    
    

    # Now swap in our random number and resume the process
    dbg.write_process_memory(parameter_addr, random_counter)
#     print 'kernel32.getlasterror(): ', kernel32.GetLastError()
    
    return DBG_CONTINUE

# Instantiate the pydbg class
dbg = pydbg()
# Now enter the PID of the printf_loop.py process
pid = raw_input('Enter the PID of the process to attach: ')
print 'attach: ', dbg.attach(int(pid))

# Set the breakpoint with the printf_randomizer function
# defined as a callback
printf_address = dbg.func_resolve('msvcrt', 'printf')

print 'bp set', dbg.bp_set(printf_address, description='printf_address', handler=printf_randomizer)

# Resume the process
dbg.run()


    


