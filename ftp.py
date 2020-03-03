import ftplib, re, os

def regions(code):
    region = {
                '01' : 'Adygeja_Resp',
                '04' : 'Altaj_Resp',
                '22' : 'Altajskij_kraj',
                '28' : 'Amurskaja_obl',
                '29' : 'Arkhangelskaja_obl',
                '30' : 'Astrakhanskaja_obl',
                '94' : 'Bajkonur_g',
                '02' : 'Bashkortostan_Resp',
                '31' : 'Belgorodskaja_obl',
                '32' : 'Brjanskaja_obl',
                '03' : 'Burjatija_Resp',
                '20' : 'Chechenskaja_Resp',
                '74' : 'Cheljabinskaja_obl',
                '87' : 'Chukotskij_AO',
                '21' : 'Chuvashskaja_Resp',
                '05' : 'Dagestan_Resp',
                '79' : 'Evrejskaja_Aobl',
                '06' : 'Ingushetija_Resp',
                '38' : 'Irkutskaja_obl',
                '37' : 'Ivanovskaja_obl',
                '89' : 'Jamalo-Neneckij_AO',
                '76' : 'Jaroslavskaja_obl',
                '07' : 'Kabardino-Balkarskaja_Resp',
                '39' : 'Kaliningradskaja_obl',
                '08' : 'Kalmykija_Resp',
                '40' : 'Kaluzhskaja_obl',
                '41' : 'Kamchatskij_kraj',
				'82' : 'Kamchatskij_kraj',
                '09' : 'Karachaevo-Cherkesskaja_Resp',
                '10' : 'Karelija_Resp',
                '42' : 'Kemerovskaja_obl',
                '27' : 'Khabarovskij_kraj',
                '19' : 'Khakasija_Resp',
                '86' : 'Khanty-Mansijskij_AO-Jugra_AO',
                '43' : 'Kirovskaja_obl',
                '11' : 'Komi_Resp',
                '44' : 'Kostromskaja_obl',
                '23' : 'Krasnodarskij_kraj',
                '24' : 'Krasnojarskij_kraj',
                '91' : 'Krim_Resp',
                '45' : 'Kurganskaja_obl',
                '46' : 'Kurskaja_obl',
                '47' : 'Leningradskaja_obl',
                '48' : 'Lipeckaja_obl',
                '49' : 'Magadanskaja_obl',
                '12' : 'Marij_El_Resp',
                '13' : 'Mordovija_Resp',
                '50' : 'Moskovskaja_obl',
                '77' : 'Moskva',
                '51' : 'Murmanskaja_obl',
                '83' : 'Neneckij_AO',
                '52' : 'Nizhegorodskaja_obl',
                '53' : 'Novgorodskaja_obl',
                '54' : 'Novosibirskaja_obl',
                '55' : 'Omskaja_obl',
                '56' : 'Orenburgskaja_obl',
                '57' : 'Orlovskaja_obl',
                '58' : 'Penzenskaja_obl',
                '59' : 'Permskij_kraj',
                '25' : 'Primorskij_kraj',
                '60' : 'Pskovskaja_obl',
                '62' : 'Rjazanskaja_obl',
                '61' : 'Rostovskaja_obl',
                '14' : 'Sakha_Jakutija_Resp',
                '65' : 'Sakhalinskaja_obl',
                '63' : 'Samarskaja_obl',
                '78' : 'Sankt-Peterburg',
                '64' : 'Saratovskaja_obl',
                '92' : 'Sevastopol_g',
                '15' : 'Severnaja_Osetija-Alanija_Resp',
                '67' : 'Smolenskaja_obl',
                '26' : 'Stavropolskij_kraj',
                '66' : 'Sverdlovskaja_obl',
                '68' : 'Tambovskaja_obl',
                '16' : 'Tatarstan_Resp',
                '72' : 'Tjumenskaja_obl',
                '70' : 'Tomskaja_obl',
                '71' : 'Tulskaja_obl',
                '69' : 'Tverskaja_obl',
                '17' : 'Tyva_Resp',
                '18' : 'Udmurtskaja_Resp',
                '73' : 'Uljanovskaja_obl',
                '33' : 'Vladimirskaja_obl',
                '34' : 'Volgogradskaja_obl',
                '35' : 'Vologodskaja_obl',
                '36' : 'Voronezhskaja_obl',
                '75' : 'Zabajkalskij_kraj'
    }
    if(region.get(code[0:2])):
        return region[code[0:2]]
    elif(region.get(code[0:3])):
        return region[code[0:3]]
    else:
        return 0

def connect():
    ftp = ftplib.FTP("ftp.zakupki.gov.ru", "free", "free")
    return ftp

def cwd(ftp, dir):
    ftp.cwd(dir)
    arrfiles = ftp.nlst()
    return arrfiles

def download(ftp, arrFile, pdstr_file):
    tmp = []
    try:
        os.mkdir(os.path.abspath(os.curdir)+'/tmp/')
    except:
        pass
    for file in arrFile:
        if(re.search(pdstr_file,file)):
            if not os.path.isfile(os.path.abspath(os.curdir)+'/tmp/'+file):
                with open(os.path.abspath(os.curdir)+'/tmp/'+file,"wb") as f:
                    ftp.retrbinary("RETR " + file,f.write)
            tmp.append({'name' : file, 'path' : os.path.abspath(os.curdir)+'/tmp/'+file})
    return tmp

