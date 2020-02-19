import ftp, os, zipfile
from datetime import datetime
name_region = ftp.regions('25')
today = datetime.today()
FTP = ftp.connect()

list_notifications = ftp.cwd(FTP, '/fcs_regions/' + name_region + '/notifications/currMonth/')
files_zip = ftp.download(FTP, list_notifications, today.strftime("%Y%m%d")+'\d\d_\d\d\d\.xml')

for file_zip in files_zip:
    print(file_zip)
    z = zipfile.ZipFile(file_zip['path'], 'r')
    for xml in z.namelist():
        if(xml[-3:] != 'xml'): continue
        print(xml)