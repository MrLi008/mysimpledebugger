# coding: utf-8
'''
Created from 2016-07-18 15:47:53

@author: MrLi
@note: 
@function: 输入: snap, 创建一个进程快照
输入: restore, 进程恢复到快照状态
'''

# snapshot.py 

from pydbg import *
from pydbg.defines import *
import threading
import time
import sys 

class snapshotter(object):
    def __init__(self, exe_path):
        
        self.exe_path = exe_path
        self.pid = None
        self.dbg = None
        self.running = True
        
        # Start the debugger thread, and loop until it sets the PID
        # of our target process
        pydbg_thread = threading.Thread(target=self.start_debugger)
        pydbg_thread.setDaemon(0)
        pydbg_thread.start()
        
        while self.pid == None:
            time.sleep(1)
        # We now have a PID and the target is running;
        # Let's get a second thread running to do the snapshots
        monitor_thread = threading.Thread(target=self.monitor_debugger)
        monitor_thread.setDaemon(0)
        monitor_thread.start()
        
    def monitor_debugger(self):
        
        while self.running == True:
            
            input = raw_input("Enter: 'snap','restore', or 'quit")
            input = input.lower().strip()
            
            if input == 'quit':
                print '[*] Exiting the snapshotter.'
                self.running = False
                self.dbg.terminate_process()
                
            elif input == 'snap':
                print '[*] Suspending all threads.'
                self.dbg.suspend_all_threads()
                
                print '[*] Obtaining snapshot.'
                self.dbg.process_snapshot()
                
#                 print '[*] self.dbg,resume_all_threads()'
#                 self.dbg.resume_all_threads()    
                
            elif input == 'restore':
#                 print '[*] Suspengding all threads'
#                 self.dbg.suspend_all_threads()
#                 
#                 print '[*] Restoring snapshot'
#                 self.dbg.process_snapshot()      
                
                print '[*] Resuming operation.'
                self.dbg.resume_all_threads()
            
    def start_debugger(self):
        
        self.dbg = pydbg()
        
        pid = self.dbg.load(self.exe_path)
        self.pid = self.dbg.pid 
        self.dbg.run()
exe_path = 'C:\\WINDOWS\\System32\\calc.exe'
snapshotter(exe_path)
                
        
        
        
        
        
        
        
        
        
        
        