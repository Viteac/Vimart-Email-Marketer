import getpass
import imaplib
import email
from email.header import decode_header
import os
import codecs
from time import sleep

di = {}


def menu():
    print('* Vimart Market Mailer v1.0')
    print('1. Get Mail Addresses from Gmail.\n2. Get Email Addresses from File.\n3. Display Database.\n'
          '4. Load Database.\n5. Save Database to File.\n6. Exit')
    choice = False
    while choice not in ['1', '2', '3', '4', '5', '6']:
        choice = input('\n>>>')
        if choice == '1':
            mai_load()
        elif choice == '2':
            file_load()
        elif choice == '3':
            display_people()
        elif choice == '4':
            load_data()
        elif choice == '5':
            save_json()
        elif choice == '6':
            send_mail()
        elif choice == '7':
            exit()
        else:
            print('Try again. Enter options 1-6.')


def send_mail():
    import smtplib
    import ssl
    import re
    import time

    while True:
        file = input('Enter file name containing text you want to send.\n>>> ')
        o = os.getcwd()
        if os.path.isfile(o + '//' + file) is True:
            break
        print(f' There\'s no a {file} in your directory\n Try again')

    with open(file) as f:
        read = f.read()
    print(read)

    for p_name, mail in people.items():
        email = mail
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = input('Enter your Gmail account')
        password = input('Enter the password')
        receiver_email = email

        message = f"""\
        Subject: {sub}



        {read}"""

        time.sleep(2)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print(f'{read}\n Emails sent')


def load_data():
    global di

    import json
    print('*Load from JSON File*')
    file_name = input('Input file name: ')
    while os.path.isfile(f'{file_name}.json') is not True:
        print(f' File {file_name}.json is not in a Folder. Enter a correct file name.')
        file_name = input('Input file name: ')
    else:
        f = open(f'{file_name}.json', )
        di = json.load(f)
        f.close()

        # return people


def file_load():
    print('load')
    while True:
        file = input('Enter file name containing email addresses.\n>>> ')
        o = os.getcwd()
        if os.path.isfile(o + '//' + file) is True:
            break
        print(f' There\'s no a file named: " {file}" in your directory\n Try again')
    with open(file, 'r')as f:
        read = f.readlines()
    for i in read:
        if i == '\n':
            pass
        else:
            i = i.rstrip('\n')
            f = i.index(':')
            ind = i[0:f]
            ma = i[f+1:]
            di[ind] = ma

            print(f'New Data added to Database:\n{ind} - {ma} ')
            print('*' * 40)
    choice = False
    while choice not in ['1', '2']:
        choice = input('\n1. Upload data from another File.\n2. Menu.\n>>>')
        if choice == '1':
            return file_load()
        elif choice == 2:
            print(menu())
        else:
            print('Try again. Enter options 1-2.')


def mai_load():
    global u, p

    def pssw():

        while True:
            u = input('Enter the email.\n>>>')
            p = input('Enter the password.\n>>>')
            if len(u) > 0 and '@' in u and len(p) > 5:
                #True

                return u, p
            else:
                print('Enter correct Email and Password')

    if u is not None or p is not None:
        while True:
            choice = input(f' Email downloading set for: {u}\nPress "C" to continue or press "N" to change email.').lower()
            if choice in ['n','c']:
                if choice == 'n':
                   u, p = pssw()
                else:
                    break

    if u is None or p is None:
        u, p = pssw()
    while True:
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(u, p)

        except imaplib.IMAP4.error:
            print(' Wrong login or password')
            sleep(3)
            pssw()
        break

    mail.select()

    status, messages = mail.select("INBOX")
    print(messages)

    # number of top emails to fetch
    n = 199

    # total number of emails
    messages = int(messages[0])
    print(messages)

    #for i in messages[0]:
    for i in range(messages, messages-n,-1):
        # fetch the email message by ID
        res, msg = mail.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])

                fro, encoding = decode_header(msg.get("From"))[0]
                if isinstance(fro, bytes):
                    fro = fro.decode(encoding)
                print("From:", fro)
                print("=" * 100)
                if '@' not in fro:
                    continue
                else:
                    if '<' in fro:
                        s = fro.index('<')
                        d = fro.index('>')
                        q = fro[s + 1:d]
                        w = fro[0:s - 1]

                        if q not in di.values():
                            di[w] = q
                    else:
                        b = sum(1 for key in di if key.startswith('Friend'))
                        if fro not in di.values():
                            di[f'Friend{b + 1}'] = fro
                            b += 1
    # close the connection and logout
    mail.close()
    mail.logout()

    return u, p


def save_json():
    print('---------------------')
    print('* Save file to JSON *')
    print('---------------------')
    print('')
    import json

    file_name = input('Input file name: ')
    json = json.dumps(di)
    f = open(file_name + ".json", "w")
    f.write(json)
    f.close()


def display_people():
    # os.system('clear')
    print('* Vimart Database v.1 *')
    if len(di) == 0:
        print('No data to display.')
    else:

        for p_id, value in di.items():
            print('\n Person ID:', p_id)
            print('_' * 60)
            print(p_id, ':', value)
            print('_' * 60)
        menu()


u = None
p = None
while True:

    menu()
