# coding: utf-8
'''
Created from 2016-07-15 22:51:54

@author: MrLi
@note: 定义要实现的功能
'''
from my_debugger_defines import *
from ctypes import *
kernel32 = windll.kernel32

class debugger(object):
    def __init__(self):
        
        self.h_process = None
        self.pid = None
        self.debugger_active = None #调试器是否活动
        self.h_thread = None
        self.context = None
        self.exception = None
        self.exception_address = None
        
        # breakpoint
        self.breakpoint = {}
        self.first_breakpoint = True
        self.hardware_breakpoint = {}
        
    def load(self, path_to_exe):
        # dwCreation flag determines how to create the Process
        # set creation_flags = CREATE_NEW_CONSOLE if you want 
        # to see the calculator GUI 
        creation_flags = DEBUG_PROCESS
        
        # instantiate the structs 
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the Debugger
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        # We then initialize the cb variavle in the STARTUPINFO struct.
        # which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)
        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print '[*] We have successfully launched the process!'
            print '[*] PID: %d ' % process_information.dwProcessId
            # Obtain a valid handle to the newly created process
            # and store it for future access
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print '[*] Error: 0x%09x.' % kernel32.GetLastError()
            
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process
            
    def attach(self, pid):
        self.h_process = self.open_process(pid)
        # We attempt to attach to the process
        # if this fails we exit the call
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
#             self.run()
        else:
            print '[*] Unable to attach to the process.'
            print 'In attach, Error: ', kernel32.GetLastError()
            
    def run(self):
        # Now we have to poll the debuggee for
        # debugger events
        while self.debugger_active == True:
            self.get_debug_event()
            
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # We are not going build any event handlers
            # just yet. Let's just resume the process for now
#             raw_input('Press key \'Enter\' to continue...')
#             self.debugger_active = False
            
            # Let's obtain the thread and context information
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(debug_event.dwThreadId)
#             print 'event code',debug_event.dwDebugEventCode,\
#                 ', Thread id ', debug_event.dwThreadId
            
            # If the event code is an Exception, we want to 
            # examine it futher
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
                if exception == EXCEPTION_ACCESS_VIOLATION:
                    print 'Accesss violation detected'
                # If a breakpoint is detected, we call an internal 
                # handle
                elif exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                elif exception == EXCEPTION_GUARD_PAGE:
                    print 'Guard Page Access Detected'
                elif exception == EXCEPTION_SINGLE_STEP:
                    print 'single step'
                    self.exception_handler_single_step()
            
            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)
            
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print '[*] Finished debugging. Exiting...'
            return True
        else:
            print 'There was an error: ', kernel32.GetLastError()
            return False
            
            
    
    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)
        if h_thread is not None:
            return h_thread
        else:
            print '[*] Could not obtain a valid thread handle.'
            print 'In open thread Error: ', kernel32.GetLastError()
            return False
        
    def enumerate_thread(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)
        if snapshot is not None:
            # You have to set the size of the struct 
            # or the call will fill
            thread_entry.dwSize = sizeof( thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            print 'In enumerate_thread, Error: ', kernel32.GetLastError()
            return False
        
    def get_thread_context(self, thread_id=None, h_thread=None):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        # Obtain a handle to the thread
        if h_thread is None:
            h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext( h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            print 'In get thread context, Error: ', kernel32.GetLastError()
            return False
    
    # get function's address from dll
    def func_resolve(self, dll, function):
        handle = kernel32.GetModuleHandleA(dll)
        address = kernel32.GetProcAddress(handle, function)
        kernel32.CloseHandle(handle)
        return address
    
    
    # exception handler breakpoint
    def exception_handler_breakpoint(self):
        print '[*] Inside the breakpoint handler'
        print 'Exception Address: 0x%08x' % self.exception_address
        
        # Check if the breakpoint is one that we set
        if not self.breakpoint.has_key(self.exception_address):
            # If it is the first Windows driven breakpoint
            # then let's just continue on
            if self.first_breakpoint == True:
                self.first_breakpoint = False
                print '[*] Hit the first breakpoint'
        else:
            print '[*] Hit user defined the breakpoints we set'
            # this is where we handle the breakpoints we set
            # first output the original_byte back
            self.write_process_memory(self.exception_address,
                                       self.breakpoint[self.exception_address])
             
            # Obtain a fresh context record, reset EIP back to the
            # original_byte and then set the thread's context record
            # with the new EIP value
#             self.context = self.get_thread_context(h_thread=self.h_thread)
            self.context.Eip = self.context.Eip - 1
             
            kernel32.SetThreadContext( self.h_thread, byref(self.context))
            
        return DBG_CONTINUE
    
    def exception_handler_single_step(self):
        # Comment from PyDbg:
        # determine if this single step event occured in reaction a 
        # hardware breakpoint and grab the hit breakpoint 
        # according to the Intel docs, we should be able to check for 
        # the BS flag in Dr6, but it apppears that Windows
        # isn't properly propagating that flag down to us
        if self.context.Dr6 & 0x1 and self.hardware_breakpoint.has_key(0):
            slot = 0
        elif self.contet.Dr6 & 0x2 and self.hardware_breakpoint.has_key(1):
            slot = 1
        elif self.context.Dr6 & 0x4 and self.hardware_breakpoint.has_key(2):
            slot = 2
        elif self.context.Dr6 & 0x8 and self.hardware_breakpoint.has_key(3):
            slot = 3
        else:
            # This isn't an INT1 generated by a hw breakpoint
            continue_status = DBG_EXCEPTION_NOT_HANDLED
        # Now let's remove the the breakpoint from the list
        if self.bp_del_hardware(slot):
            continue_status = DBG_CONTINUE
        print '[*] Hardware breakpoint removed'
        return continue_status
            
    # process memory
    # read process memory
    def read_process_memory(self, address, length):
        data = ''
        read_buf = create_string_buffer(length)
        count = c_ulong(0)
        try:
            if not kernel32.ReadProcessMemory(self.h_process,
                                              address, 
                                              read_buf,
                                              length,
                                              byref(count)):
                print 'In read process memory, Error: ', kernel32.GetLastError()
                return False
            else:
                data = read_buf.raw
                return data
        except Exception, e:
            print 'In read process memory, Exception: ', e
    
    # write process memroy
    def write_process_memory(self, address, data):
        count = c_ulong(0)
        length = len(data)
        c_data = c_char_p(data[count.value:])
        if not kernel32.WriteProcessMemory(self.h_process,
                                           address,
                                           c_data,
                                           length,
                                           byref(count)):
            print 'In write process memory, Error: ', kernel32.GetLastError()
            return False
        else:
            return True
    
    
    # set break point 
    # set software point
    def bp_set_software(self, address):
        if not self.breakpoint.has_key(address):
            try: 
                
                old_protect = c_ulong(0)
                kernel32.VirtualProtectEx(self.h_process,
                                          address, 
                                          1, 
                                          PAGE_EXECUTE_READWRITE, 
                                          byref(old_protect))
                
                print 'virtual protect ex'
                # store the original byte
                original_byte = self.read_process_memory(address, 1)
                
                print 'read process memory,', original_byte
                # write the INT3 opcode
                self.write_process_memory(address, '\xCC')
                
                print 'write process memory'
                
                # register the breakpoint in our internal list
                self.breakpoint[address] = (original_byte)
            except Exception,e:
                    print 'Here, bp set software, Exception: ', e
                    return False
            
        return True
    def bp_set_hardware(self, address, length, condition):
        # Check for a valid length value
        if length not in (1, 2, 4):
            return False
        else:
            length -= 1
        
        # Check for a valid condition
        if condition not in (HW_ACCESS, HW_EXECUTE, HW_WRITE):
            return False
        
        # Check for available slots
        if not self.hardware_breakpoint.has_key(0):
            available = 0
        elif not self.hardware_breakpoint.has_key(1):
            available = 1
        elif not self.hardware_breakpoint.has_key(2):
            available = 2
        elif not self.hardware_breakpoint.has_key(3):
            available = 3
        else:
            return False
        
        # We want to set the debug register in every thread
        for thread_id in self.enumerate_thread():
            context = self.get_thread_context(thread_id=thread_id)
            
            # Enable the appropriate flag in DR7
            # register to set the breakpoint
            context.Dr7 |= 1<<(available*2)
            
            # Save the address of the breakpoint in the 
            # free register that we found
            if available == 0:
                context.Dr0 = address
            elif available == 1:
                context.Dr1 = address
            elif available == 2:
                context.Dr2 = address
            elif available == 3:
                context.Dr3 = address
            
            # set the breakpoint condition
            context.Dr7 |= condition<<((available *4)+16)
            # set the length
            context.Dr7 |= length <<((available * 4)+18)
            
            # set thread context with the break set
            h_thread = self.open_thread(thread_id)
            kernel32.SetThreadContext(h_thread, byref(context))
            
            # update the internal hardware breakpoint array at the used
            # slot index
            self.hardware_breakpoint[available] = (address, length, condition)
        return True
    
    def bp_del_hardware(self, slot):
        # Disable the breakpoint for all active threads
        for thread_id in self.enumerate_thread():
            context = self.get_thread_context(thread_id=thread_id)
            
            # Reset the flags to remove the breakpoint
            context.Dr7 &= ~(1<<(slot*2))
            
            # Zero out the address
            if slot == 0:
                context.Dr0 = 0x00000000
            elif slot == 1:
                context.Dr1 = 0x00000000
            elif slot == 2:
                context.Dr2 = 0x00000000
            elif slot == 3:
                context.Dr3 = 0x00000000
                
            # Remove the condition flag
            context.Dr7 &= ~(3<<((slot*4)+16))
            # Remove the length flag
            context.Dr7 &= ~(3<<((slot*4)+18))
            # Reset the thread's context with the breakpoint removed
            h_thread = self.open_thread(thread_id)
            kernel32.SetThreadContext(h_thread, byref(context))
        # Remove the breakpoint from the internal list
        del self.hardware_breakpoint[slot]
        return True
                             
            
            
            
            
            
            
            
            
            
            
            
            
        