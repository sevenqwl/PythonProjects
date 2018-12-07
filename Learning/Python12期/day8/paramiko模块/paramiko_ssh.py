#!_*_ coding:utf-8 _*_

import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='106.14.118.100', port=22, username='root', password='SeVeN&%^94756756')
stdin, stdout, stderr = ssh.exec_command(sys.argv[1])
result = stdout.read().decode()
print(sys.argv[1])
print(result)
ssh.close()