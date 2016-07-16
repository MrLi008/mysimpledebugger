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
    msvcrt.printf( 'loop itration, %d' % counter)
    time.sleep(1)
    counter = counter + 1
    if counter > 50:
        break
    
msvcrt.printf('end........')    
