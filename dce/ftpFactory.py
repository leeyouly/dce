#-*- coding: utf-8 -*-  
import ftplib
from ftplib import FTP  
import os
  
def ftpconnect(ftphost,username,password):
 
    ftp=FTP()  
    ftp.set_debuglevel(2) 
    ftp.connect(ftphost,21) 
    ftp.login(username,password) 
    return ftp  
      
# def downloadfile():
#     remotepath = "/home/pub/dog.jpg";  
#     ftp = ftpconnect()  
#     print ftp.getwelcome() 
#     bufsize = 1024 
#     localpath = 'f:\\test\\dog.jpg'  
#     fp = open(localpath,'wb') 
#     ftp.retrbinary('RETR ' + remotepath,fp.write,bufsize) 
#     ftp.set_debuglevel(0) 
#     fp.close()  
#     ftp.quit()
  
def uploadfile(ftphost,username,password,target_path,target_name,localpath):
    #操作返回1成功0失败
  
    ftp = ftpconnect(ftphost,username,password)  
    try:
        ftp.cwd(target_path)
    except ftplib.error_perm:
        try:
            ftp.mkd(target_path)
            ftp.cwd(target_path)
        except ftplib.error_perm:
            ftp.quit()
            print 'U have no authority to make dir'
            return  0
    bufsize = 1024  
    try:
        localpath = localpath+os.path.sep+target_name 
        fp = open(localpath,'rb')  
        ftp.storbinary('STOR '+ target_name ,fp,bufsize) 
        ftp.set_debuglevel(0)  
        fp.close() 
        ftp.quit()  
        return 1
    except:
        return 0
