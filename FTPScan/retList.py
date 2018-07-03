import ftplib

def returnDefault(ftp):
    try:
        driList = ftp.nlst()
    except :
        driList = []
        print  '[-] could not list directoryu contents '
        print '[-] Skipping to net target'
        return
    retList = []
    for fileName in driList:
        fn = fileName.lower()
        if '.php' or '.html' or '.asp' in fn:
            print '[+] Found default page:' + fileName
            retList.append(fileName)
    return retList

host = '192.168.95.179'
userName = 'guest'
passWord = 'guest'
ftp  = ftplib.FTP(host)
ftp.login(userName,passWord)
returnDefault(ftp)