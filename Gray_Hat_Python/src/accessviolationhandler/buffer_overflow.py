# coding: utf-8
'''
Created from 2016-07-18 08:24:36

@author: MrLi
@note: 内存溢出测试
'''

from ctypes import *
msvcrt = cdll.msvcrt

# Give the debugger time to attach, then hit a Button
raw_input('Once the debugger is attached, press any key.')

# Create the 5-byte destination buffer
buffer = c_char_p('AAAAA')

# The overflow string
overflow = 'A'*100

# Run the Overflow
msvcrt.strcpy(buffer, overflow)