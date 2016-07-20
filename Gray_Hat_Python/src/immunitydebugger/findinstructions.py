# coding: utf-8
'''
Created from 2016-07-20 13:45:03

@author: MrLi
@note: 
1, 转化搜索代码
2, 找到整个程序空间中, 包含这个指令的地址
3, 找到地址所属的页
4, 确认页是可执行的
5, 打印该页
'''

# findinstructions.py 
from immlib import *
# from idlelib import *

def main(args):
    imm = Debugger()
    search_code = ''.join(args)
    search_bytes = imm.Assemble( search_code)
    search_results = imm.Search( search_bytes)
    
    for hit in search_results:
        
        # Retrieve the memory page where this hit exists 
        # and makes sure it's executable
        code_page = imm.getMemoryPagebyAddress( hit)
        access = code_page.getAccess( human = True)
        if 'execute' in access.lower():
            imm.log( '[*] Found: %s(0x%08x)' %(search_code, hit),address = hit)
            
    return '[*] Finished searching for instructions, check the log window.'