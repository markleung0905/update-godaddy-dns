#!/usr/bin/env python

# Import pif to get your public ip, sys and os.path
import pif, sys, os, os.path

# Partial imports
from godaddypy import Client, Account
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Remember to set your api key and secret
userAccount = Account(api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
userClient = Client(userAccount)
publicIP = pif.get_public_ip('ident.me')

# E.g.: to update your_record.yourdomain.com set domain and record to:
domain = os.getenv('DOMAIN')
names = os.getenv('NAME').split(',')


if os.path.isfile('godaddy_ip.txt'):
    try:
        ip_file = open('godaddy_ip.txt', 'r')
        read_ip = ip_file.read().strip('\n')
        ip_file.close()
    except:
        print("Cannot read IP file")
        sys.exit()
    if read_ip == publicIP:
        print("Read the IP file, no need to change IP")
        sys.exit()


# Try to retrieve the record and update it if necessary 
try:
    for name in names:
        currentIP = userClient.get_records(domain, record_type='A', name=name)
        if (publicIP != currentIP[0]["data"]):
            updateResult = userClient.update_record_ip(publicIP, domain, name, 'A')
            if updateResult is True:
                ip_file = open('godaddy_ip.txt', 'w')
                ip_file.write(publicIP)
                ip_file.close()
                print('Updated DNS record and wrote IP file.')
        else:
            print('Checked the DNS record, no update needed.')
except:
    print(sys.exc_info()[1])
    sys.exit()