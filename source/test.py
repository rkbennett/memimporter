print("[+] Universal DLL Injector by Y")
print("[+] contact : If you know me then give me a shout")
print("[+] usage: ./dll_injector.py <PID> <DLLPATH>")
print("\n")
 
from ctypes import *
import sys,ctypes
 
# Define constants we use
PAGE_RW_PRIV = 0x04
PROCESS_ALL_ACCESS = 0x1F0FFF
VIRTUAL_MEM = 0x3000
 
#CTYPES handler
kernel32 = windll.kernel32
 
def dll_inject(PID,DLL_PATH):
    print("[+] Starting DLL Injector")
    LEN_DLL = len(DLL_PATH)# get the length of the DLL PATH 
    print("\t[+] Getting process handle for PID:%d " % PID )
    hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,PID)
     
    if hProcess == None:
        print("\t[+] Unable to get process handle")
        sys.exit(0)
    print("\t[+] Allocating space for DLL PATH")
    DLL_PATH_ADDR = kernel32.VirtualAllocEx(hProcess, 
                                            0,
                                            LEN_DLL,
                                            VIRTUAL_MEM,
                                            PAGE_RW_PRIV)
    bool_Written = c_int(0)
    print("\t[+] Writing DLL PATH to current process space")
    kernel32.WriteProcessMemory(hProcess,
                                DLL_PATH_ADDR,
                                DLL_PATH,
                                LEN_DLL,
                                byref(bool_Written))
    print("\t[+] Resolving Call Specific functions & libraries")
    kernel32DllHandler_addr = kernel32.GetModuleHandleA("kernel32")
    print("\t\t[+] Resolved kernel32 library at 0x%08x" % kernel32DllHandler_addr)
    LoadLibraryA_func_addr = kernel32.GetProcAddress(kernel32DllHandler_addr,"LoadLibraryA")
    print("\t\t[+] Resolve LoadLibraryA function at 0x%08x" %LoadLibraryA_func_addr)
     
    thread_id = c_ulong(0) # for our thread id
    print("\t[+] Creating Remote Thread to load our DLL")
    if not kernel32.CreateRemoteThread(hProcess,    
                                None,
                                0,
                                LoadLibraryA_func_addr,
                                DLL_PATH_ADDR,
                                0,
                                byref(thread_id)):
        print("Injection Failed, exiting")
        sys.exit(0)
    else:
        print("Remote Thread 0x%08x created, DLL code injected" % thread_id.value)
PID = int(sys.argv[1])
DLL_PATH = str(sys.argv[2])
dll_inject(PID, DLL_PATH)