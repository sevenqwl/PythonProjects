
import paramiko
import os,sys

transport = paramiko.Transport(('106.14.118.100', 22))
transport.connect(username='root', password='SeVeN&%^94756756')

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put('paramiko_ssh.py', '/tmp/paramiko_ssh.py')
sftp.get( '/tmp/paramiko_ssh.py', '123.py')
transport.close()