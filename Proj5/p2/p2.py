import paramiko
import pathlib
import os
import sys

host = "89.107.170.108"
port = 22
username = "admin"
password = "ptc686grt09"
command = "show version all"


print("opening file 'Checkpoint.txt'")
fe = open("Checkpoint.txt", "r")
Lines = fe.readlines()
for line in Lines:    
  ip=line.split()[0]
  id=line.split()[1]
  host = ip
  print("\n---------")
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(host, port, username, password)

  stdin, stdout, stderr = ssh.exec_command(command)
  lines = stdout.readlines()
  print("idefix id is "+id)
  for l in lines:
    print(l.strip())
fe.close()    



