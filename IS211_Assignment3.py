#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment3 - csv and re module.  Tested in Python 2.7"""

import argparse
import urllib2
import csv
import datetime
import operator
import re

def main():
    """This is the main function where the assignment3 will use
    the following url as data.
    http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Please enter url to be parse.')
    args = parser.parse_args()

    if args.url:
        try:
            csv_file = downloadData(args.url)
            processData(csv_file)

        except urllib2.URLError:
            print('The URL entered is invalid.')
    else:
        print('Please enter URL to be parse.')

def downloadData(url):
    """A function to download the contents located at the url and return
		to the caller.
    """
    content = urllib2.urlopen(url)
    return content

def processData(content):
    """A function to determine image requested and browser agent
    used in the url.  After analyzing the csv file, it is determined that 
	the image extension consist of gif, jpeg, jpg, and png.
    """
    csv_file = csv.reader(content)
    dateFormat = '%Y-%m-%d %H:%M:%S'
    hits = 0
    image_hits = 0
    chrome = 0
    firefox = 0
    msie = 0
    safari = 0

    times = {i:0 for i in range(0, 23)}

    for line in csv_file:
        result = {'path':line[0], 'date':line[1], 'browser': line[2],
                  'status': line[3], 'size': line[4]}

        date = datetime.datetime.strptime(result["date"], dateFormat)
        times[date.hour] = times[date.hour] + 1
        hits += 1
        if re.search(r'\.(?:jpg|jpeg|gif|png)$',
            result['path'], re.I | re.M):  #ignore case and multi-line
            image_hits += 1

        if re.search(r'chrome', result['browser'], re.I):  #ignore case
            chrome += 1

        elif re.search(r'safari', result['browser'], re.I) and not re.search(r'chrome\d+', result['browser'], re.I):  #ignore case
            safari += 1

        elif re.search(r'firefox', result['browser'], re.I):  #ignore case
            firefox += 1

        elif re.search(r'msie', result['browser'], re.I):  #ignore case
            msie += 1

    imagerequest = (float(image_hits) / hits) * 100  #calculate image requested to percentage
    notimagerequest = ((hits - float(image_hits)) / hits) * 100  #cal img not requested to percent
    chromehits = (float(chrome) / hits) * 100
    firefoxhits = (float(firefox) / hits) * 100
    msiehits = (float(msie) / hits) * 100
    safarihits = (float(safari) / hits) * 100

    browser = {'Safari': safari, 'Chrome': chrome, 'Firefox': firefox, 'MSIE': msie}
    print(('=') * 60)
    print('IS211 Assignment 3 Output')
    print(('=') * 60)
    print('Image requests accounts for {0:0.1f}% of all requests.'.format(imagerequest))
    print(('=') * 60)
    print('The most popular browser is %s.' %
          (max(browser.iteritems(), key=operator.itemgetter(1))[0]))
    print(('=') * 60)
    print('Not image requests accounts for {0:0.1f}% of all requests.'.format(notimagerequest))
    print(('=') * 60)
    print('The least popular browser is %s.' %
          (min(browser.iteritems(), key=operator.itemgetter(1))[0]))
    print(('=') * 60)
    print('\n')
    print(('=') * 60)
    print('Extra Credit')
    print(('=') * 60)
    print('Hour of the day with hits.  Sorted by highest to lowest')
    sorted_times = sorted(times.items(), key=operator.itemgetter(1))
    sorted_times.reverse()
    for i in sorted_times:
        print('Hour %02d has %s hits.' % (i[0], i[1]))
    print(('=') * 60)
    print('\n')
    print(('=') * 60)
    print('Browser Statistics')
    print(('=') * 60)
    print("Chrome total hits is"), browser['Chrome']
    print('Chrome total hits accounts for {0:0.2f}% of all requests.'.format(chromehits))
    print(('-') * 60)
    print('Firefox total hits is'), browser['Firefox']
    print('Firefox total hits accounts for {0:0.2f}% of all requests.'.format(firefoxhits))
    print(('-') * 60)
    print('MSIE total hits is'), browser['MSIE']
    print('MSIE total hits accounts for {0:0.2f}% of all requests.'.format(msiehits))
    print(('-') * 60)
    print('Safari total hits is'), browser['Safari']
    print('Safari total hits accounts for {0:0.2f}% of all requests.'.format(safarihits))
    print(('=') * 60)

if __name__ == "__main__":
    main()
