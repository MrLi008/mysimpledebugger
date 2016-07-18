# coding: utf-8
'''
Created from 2016-07-18 08:28:45

@author: MrLi
@note: 处理buffer_overflow.py中的溢出
'''


from pydbg import *
from pydbg.defines import *

# Utility libraries included with pydbg
import utils

# This is our access violation handler
def check_accessv(dbg):
    
    # We skip first-change Exception
    if dbg.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED 
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print crash_bin.crash_synopsis()
    dbg.terminate_process()
    
    return DBG_EXCEPTION_NOT_HANDLED

pid = raw_input('PID: ')
dbg = pydbg()
dbg.attach(int(pid))

dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, check_accessv)

dbg.run()