import ftp, os, zipfile, re, requests, json, my_email, datetime
from xml.etree import ElementTree as ET
from datetime import datetime
name_region = ftp.regions('25')
today = datetime.today()
today = datetime.strptime('2020-02-26', '%Y-%m-%d')
print(today)
FTP = ftp.connect()

url_mail = 'http://pm_zakupki.ru/scripts/mail.php'
list_notifications = ftp.cwd(FTP, '/fcs_regions/' + name_region + '/notifications/prevMonth/')
#list_notifications = ftp.cwd(FTP, '/fcs_regions/' + name_region + '/notifications/currMonth/')
files_zip = ftp.download(FTP, list_notifications, today.strftime("%Y%m%d")+'\d\d_\d\d\d\.xml')

'''
	    $rowp = array(
	    	'name_obj' => 'lol утепленное для осужденных женского пола тип А:;:Полупальто утепленное для осужденных женского пола тип А',
		    'Ktru' => '',
		    'okpd' => '14.12.30.112:;:14.12.30.112',
		    'znvlp' => '',
		    'formdrug' => '',
		    'dozdrug' => '',
		    'PlacingwayName' => 'Электронный аукцион',
		    'objectname' => 'полупальто',
		    'preimuschestva_ogranich' => 'Преимущества',
		    'nacrezim' => '',
		    'date_position' => '2020-02-26'
	    );
'''

def getTextXml(nodelist):
    print(nodelist)
    print(nodelist[0].childNodes)
    return " ".join(t.nodeValue for t in nodelist[0].childNodes if t.nodeType == t.TEXT_NODE)

def isDefinedXmlNode(var, emptystr = ''):
    if(var != None and var.text != None):
        return var.text
    else:
        return emptystr

'''
for server in doc.findall('server'):
    host = server.find('./host').text
    print host
    for channel in server.findall('channel'):
        name = channel.find('name').text
        print name
'''

for file_zip in files_zip:
    print(file_zip)
    z = zipfile.ZipFile(file_zip['path'], 'r')
    for xml_name in z.namelist():
        if(xml_name[-3:] != 'xml'): continue
        try:
            data = {}
            xmlstring = z.read(xml_name)
            xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring.decode('utf-8'))
            xml_tree = ET.fromstring(xmlstring)
            data['nacrezim'] = ''
            for nacrezim in xml_tree.findall('*//requirement/content'):
                data['nacrezim'] += nacrezim.text
            data['preimuschestva_ogranich'] = ''
            for preim in xml_tree.findall('*//preferense/name'):
                data['preimuschestva_ogranich'] += preim.text
            data['Ktru'] = []
            data['name_obj'] = []
            data['okpd'] = []
            for ktru in xml_tree.findall('*//KTRU'):
                data['Ktru'].append(ktru.find('code').text)
                data['okpd'].append(ktru.find('code').text[:12])
                data['name_obj'].append(ktru.find('name').text)
            for okpd in xml_tree.findall('*//OKPD2'):
                data['okpd'].append(okpd.find('code').text)
                data['name_obj'].append(okpd.find('name').text)
            data['Ktru'] = ':;:'.join(data['Ktru'])
            data['name_obj'] = ':;:'.join(data['name_obj'])
            data['okpd'] = ':;:'.join(data['okpd'])
            data['PlacingwayName'] = isDefinedXmlNode(xml_tree.find('*//placingWay/name'))
            data['objectname'] = isDefinedXmlNode(xml_tree.find('*//purchaseObjectInfo'))
            data['inn'] = xml_tree.find('*//INN').text
            data['date_position'] = isDefinedXmlNode(xml_tree.find('*//directDate'))
            data['org_name'] = xml_tree.find('*//fullName').text
            data['contactEMail'] = xml_tree.find('*//contactEMail').text
            data['contactPerson'] = xml_tree.find('*//contactPerson/lastName').text + ' ' + xml_tree.find('*//contactPerson/firstName').text + ' ' + xml_tree.find('*//contactPerson/middleName').text
            data['purchaseNumber'] = xml_tree.find('*//purchaseNumber').text
            data['auth'] = 'Support2000'
            r = requests.post(url_mail, data=data)
            if(r.text == 'false'):
                print("false s")
            else:
                placeDate = datetime.strptime(data['date_position'][:19], '%Y-%m-%dT%H:%M:%S')
                subject = 'В Вашем извещении № ' + data['purchaseNumber'] + ' размещенном ' + placeDate.strftime('%d.%m.%Y %H:%M') + ' найдены нарушения 44-ФЗ'
                email = data['contactEMail']
                email = 'ivad1004@gmail.com'
                my_email.sendEsputnik(email, r.text, subject)
                #with open('test.html', 'w+') as f:
                #    f.write(r.text)
                print("send "+data['contactEMail']+' '+data['purchaseNumber'])
                #print(data['nacrezim'] + data['preimuschestva_ogranich'])
                #exit(0)
        except Exception as E:
            print(E)
        #data['preimuschestva_ogranich'] = getTextXml(xml_tree.getElementsByTagName('name'))
        #print(data)
