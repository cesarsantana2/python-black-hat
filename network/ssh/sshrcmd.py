import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/justin/.ssh/know_hosts')
    client.set_missing_host_policy(paramiko.AutoAddPolicy())