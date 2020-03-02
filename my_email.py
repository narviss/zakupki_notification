import requests, json

def sendEsputnik(to, html, subject):
    user = 'admin@r2000.site';
    password = 'R5Qskq4Qdy';
    send_email_url = 'https://esputnik.com/api/v1/message/email';
    fromEmail = 'ООО ФКГ Развитие 2000 <admin@r2000.site>'

    json_value = {
        'from': fromEmail,
        'subject': subject,
        'htmlText': html,
        'emails': (to,)
    }

    headers = {'Content-type': 'application/json',
           'Accept': 'application/json'}
    r = requests.post(send_email_url, data=json.dumps(json_value), headers=headers, auth=(user, password), verify=False)
    print(r.text)