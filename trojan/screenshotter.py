import win32gui
import win32ui
import win32con
import win32api

# obtém um handle para a janela de todos os monitores em pixels
hdesktop = win32gui.GetDesktopWindow()

# determina o tamanho de todos os m0onitores em pixels
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# cria um contexto de dispositivo
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# cria um contexto de dispositivo em memoria
mem_dc = img_dc.CreateCompatibleDC()

# cria um objeto bitmap
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copia a tecla para o nosso contexto de dispositivo em memoria
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# salva o bitmap em um arquivo
screenshot.saveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

# remove nossos objetos
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
