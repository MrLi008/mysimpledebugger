# coding: utf-8
'''
Created from 2016-07-16 11:04:16

@author: MrLi
@note: the tested function
'''

from ctypes import *
import time

msvcrt= cdll.msvcrt
counter = 0
while 1:
    msvcrt.printf( 'loop itration, %d\t' , counter)
#     str1 = msvcrt.strcpy('a','b')
#     msvcrt.printf(str(str1)+'\n')
#     print 'len', msvcrt.strlen(str(str1))
    time.sleep(1)
    counter += 1
    if counter > 50:
        break
    
msvcrt.printf('end........%d' % counter)    
