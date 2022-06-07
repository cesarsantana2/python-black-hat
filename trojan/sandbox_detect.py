import ctypes
import random
import time 
import sys


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
keystrokes = 0
mouse_clicks = 0
double_clicks = 0

class LASTINPUTINFO(ctypes.Structure):

    _fields_ = [("cbsize", "ctypes.c_unit", ("dwTime", ctypes.c_ulong))]

def get_last_input():

    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)

    #obtem a ultima entrada registrada
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    #agora determina ha quanto tempo o computador esta executando
    run_time = kernel32.GetTicketCount()

    elapsed = run_time - struct_lastinputinfo.dwTime

    print("[*] It's been %d milliseconds since the last input event." % elapsed)

    return elapsed

# CODIGO DE TESTE. REMOVA O QUE ESTIVER DEPOIS DESTE PARAGRAFO!

while True:
    get_last_input()