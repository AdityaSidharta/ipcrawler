import os
from os.path import join

whois_info_list = ['Domain Name', 'Registrar', 'Registrant Name', 'Registrant Email', 'Admin Name', 'Tech Name']
ipaddress_info_list = ['Hostname', 'IP Address', 'Host of this IP', 'Organization']

cwd = os.getcwd()
default_path = join(cwd, 'ipcrawler.csv')

csv_file = os.getenv('CSV_FILE', default_path)
if not os.path.isfile(csv_file):
    raise EnvironmentError('CSV_FILE not found')
