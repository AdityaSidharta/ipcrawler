import csv
import urllib
import pandas as pd
from bs4 import BeautifulSoup
from retrying import retry
import sys
import json

def is_io_error(exception):
    return isinstance(exception, IOError)

@retry(retry_on_exception=is_io_error, stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def link_to_lxmlsoup(link):
    try:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html, 'lxml')
        return soup
    except IOError:
        print "IOError detected. Attempting Reconnection. Program will be terminated after 10 Unsuccesful Connection"
    except:
        print "Unexpected Error", sys.exc_info()[0]
        raise

def soup_to_txt(soup, txt_output):
    text_file = open(txt_output, "w")
    text_file.write(soup.prettify(encoding='utf-8'))
    text_file.close()


def csv_to_df(csv_file):
    df = pd.read_csv(csv_file, header=False, index_col=False)
    return df


def csv_to_list(csv_file):
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        list_output = list(reader)
    return list_output

def print_counter(counter, total_len):
    counter = counter+1
    print 'Progress: '+str(counter)+' out of '+ str(total_len)
    return counter, total_len

def dict_to_json(dict_file, output):
    with open(output, 'w') as fp:
        json.dump(dict_file, fp)

def dict_to_csv(dict_file, output):
    result_df = pd.DataFrame.from_dict(dict_file)
    result_df.to_csv(output)

def calc_eta(time_elapsed, counter, total_len):
    return time_elapsed / counter * (total_len - counter)

def handle_seconds(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "%dh %dm %ds" %(h, m, s)
    elif m > 0:
        return "%dm %ds" %(m , s)
    else:
        return "%ds" % s

def print_progress(time_elapsed, counter, total_len):
    eta = handle_seconds(calc_eta(time_elapsed, counter, total_len))
    cur = handle_seconds(time_elapsed)
    print "--- %s elapsed, ETA: %s ---" % (cur, eta)

