import time
import random
import os
from multiprocessing import Process
import multiprocessing
import string
import socket
import paramiko
import base64
import configparser
import glob
from io import StringIO


conffile = 'config.conf'
config = configparser.ConfigParser()
config.read(conffile)

try:
    f = open(conffile)
    f.close()
except FileNotFoundError:
    print('Config file does not exist.')

sshkey = config.get('KEY', 'key_filename')
sshuser = config.get('KEY', 'username')
jobit = config.get('STORAGEARRAYS', 'arrays').split()
tgtsrv = config.get('TRANS', 'host')
tgtport = int(config.get('TRANS', 'port'))

def datasender(message):
    host = tgtsrv
    port = tgtport

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.connect((host, port))
    mySocket.sendall(message.encode())



#data to telegraf
def datapusher(purkki):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(purkki, username=sshuser, key_filename=sshkey)
        stdin, stdout, stderr = client.exec_command('statvlun -hostsum -csvtable -nohdtot -d 20')

        for line in stdout:

                if not line:
                        #time.sleep(10)
                        print("perse" + purkki)
                else:
                        message = locationlabel(purkki) + line.rstrip()
                        datasender(message)
                        #print(purkki)
                        time.sleep(.001)
        client.close()

        
#test workker
def workkeri(workker):
    while True:
        satunnaisuus = random.randint(1, 5)
        print("workker-name" , workker, "os-pid ", os.getpid(), proc)
        time.sleep(satunnaisuus)


if __name__ == '__main__':

    procs = []
    #jobit = ["stor1", "stor2", "stor3", "stor4", "stor5"]
    for jobi in jobit:
        luku = jobi
        workker = jobi
        proc = Process(target=workkeri, args=(workker,))
        procs.append(proc)
        proc.start()

    while True:

        time.sleep(5)
        print(procs)

        for duuni in  range(len(procs)):
            print(duuni)

            if procs[duuni].is_alive() is True:
                print(duuni, "Elossa", procs[duuni].is_alive())

            if procs[duuni].is_alive() is not True:
                print("Ei elossa", procs[duuni].is_alive())
                time.sleep(1)
                print("Start new workker")
                workker = jobi
                procs.remove(procs[duuni])
                proc = Process(target=workkeri, args=(workker,))
                procs.append(proc)
                proc.start()

        time.sleep(1)
