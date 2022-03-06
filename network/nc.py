import sys
import socket
import getopt
import threading
import subprocess


listen = False
command = False
uplad = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print("nc\n")
    print("Usage: nc.py -t target_host -p port\n")
    print("-l --listen                  - listen on [host]:[port] for incoming connections\n")
    print("-e --execyte=file_to_run     - execute the hive file upon receiving a connection\n")
    print("-c --command                 - initialaze a command shell")
    print("-u --upload=destination      - upon receiving connection upload a file and write to [destination]\n\n")
    print("Examples:\n")
    print("nc.py -t 192.168.0.1 -p 5555 -l -c\n")
    print("nc.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe\n")
    print("nc.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./nc.py -t 192.168.0.1 -p 135")
    sys.exit(0)


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data     = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break
            
            print(response,)

            buffer = input("")
            buffer+= "\n"

            client.send(buffer)

    except:
        print("[*] Exception! Exiting.")
        client.close()



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        print("\n")
        usage()


    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--cammanda"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"


    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()



main()


    








    

