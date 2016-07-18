# coding: utf-8
'''
Created from 2016-07-17 16:27:48

@author: MrLi
@note: 
测试struct的pack和unpack
'''


import struct

val = 1
val2 = struct.pack('L', val)[0]
print val2
val3 = struct.unpack('L', )[0]
print val3