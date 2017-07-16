# -*- coding: utf-8 -*-

from config import whois_info_list, ipaddress_info_list, csv_file
from utils import link_to_lxmlsoup, csv_to_list, print_counter, dict_to_csv, print_progress
import time
import sys

def whois_parser(soup, result_dict):
    try:
        raw_text = soup.find(id='registryData').get_text()
        list_text = raw_text.split("\n")
    except:
        try:
            raw_text = soup.find(id='registrarData').get_text()
            list_text = raw_text.split("\n")
        except:
            list_text = []

    for info in whois_info_list:
        try:
            item = [x for x in list_text if info+":" in x][0].split(': ')
            item = item[1]
        except:
            item = ''
        try:
            result_dict.setdefault(str(info),[]).append(item.encode(encoding='UTF-8'))
        except:
            print item
            raise ValueError('Encoding Error for whois_parser - item')
    return result_dict

def ipaddress_parser(soup, result_dict):
    try:
        info_list = soup.find_all('th')[:4]
        info_list = [x.get_text().replace(':','') for x in info_list]
        item_list = soup.find_all('td')[:4]
        item_list = [x.get_text() for x in item_list]
    except:
        item_list = ['']*4
        info_list = ipaddress_info_list
    for key, values in zip(info_list, item_list):
        try:
            result_dict.setdefault(str(key),[]).append(values.encode(encoding='UTF-8'))
        except:
            print values
            raise ValueError('Encoding Error for ipaddress_parser - item')
    return result_dict

def main():
    raw_list = csv_to_list(csv_file)
    total_len = len(raw_list)
    counter = 0
    result_dict = dict()
    print "Commencing Web Scraping..."
    start_time = time.time()
    for raw_link in raw_list:
        try:
            raw_link = raw_link[0]
            whois_link = "http://www.whois.com/whois/" + raw_link
            ipaddress_link = "http://"+raw_link+".ipaddress.com/"
            whois_soup = link_to_lxmlsoup(whois_link)
            ipaddress_soup = link_to_lxmlsoup(ipaddress_link)
            result_dict.setdefault('Raw Link',[]).append(str(raw_link))
            result_dict = whois_parser(whois_soup, result_dict)
            result_dict = ipaddress_parser(ipaddress_soup, result_dict)
            counter, total_len = print_counter(counter, total_len)
            if counter % 400 == 0:
                print "Commencing 30 Second Sleep after 400 iterations"
                time.sleep(30)
            time_elapsed = time.time() - start_time
            print_progress(time_elapsed, counter, total_len)
        except:
            dict_to_csv(result_dict, 'output.csv')
            print "Unexpected Error", sys.exc_info()[0]
            raise
    dict_to_csv(result_dict, 'output.csv')


if __name__ == '__main__':
    main()
