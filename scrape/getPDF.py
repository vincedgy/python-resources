""" 
getPDF.py : scrape all PDF listed as href anchors in on target page (The Whitepaper at AWS in this case)
version : 0.1b
author : Vincent DAGOURY

Fonction : 
Create a sub directory odf
Show downloading progress file by file
Can be interrupted by user

TODO : 
Add argument and logging

"""
import ntpath
import os
import re
import sys
import urllib2
from HTMLParser import HTMLParser
from colorama import Fore
from tqdm import tqdm

# Generals
URL = 'http://aws.amazon.com/whitepapers'
BASEDIR = os.path.normpath(os.path.join(os.getcwd(), './pdf'))

request_headers = {
"Accept-Language": "en-US,en;q=0.5",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Referer": "http://aws.amazon.com",
"Connection": "keep-alive" 
}

# This class will parse the HTML file from URL, containing all PDF href anchors
class MyHTMLParser(HTMLParser):
    """ xxx """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
            for name, value in attrs:
               # If href is defined, print it.
                if name == "href" and re.search('.pdf', value):
                    self.data.append('http:' + value)

# -1- Get page content
print 'Hello !'
try:
    print Fore.RESET + '_ Retriving all AWS Whitepapers PDF from ' + URL
    #Response = urllib2.urlopen(URL, timeout=5)
    Parser = MyHTMLParser()
    Request = urllib2.Request(url=URL, headers=request_headers)
    Parser.feed(urllib2.urlopen(Request).read())
    PdfFiles = Parser.data
except urllib2.HTTPError as error:
    print Fore.RED + 'Error occured during retrieval of main page ' + URL + ' :', error, Fore.RESET 
    sys.exit(1)
# -2- Walk thru the list and get each file
if len(PdfFiles):
    # build pdf directory in current dir if needed
    if not os.path.exists(BASEDIR):
        print Fore.RESET + '_ Make dir ' + BASEDIR
        os.mkdir(BASEDIR)
    # Download and show progress of downloading
    print Fore.RESET + '_ Start downloading ' + str(len(PdfFiles)) + ' PDF file(s) in the directory ' + BASEDIR
    for i in tqdm(range(len(PdfFiles)), total=len(PdfFiles), unit='files'):
        try:
            Request = urllib2.Request(url=urllib2.quote(PdfFiles[i], safe='/:'), headers=request_headers)
            Response = urllib2.urlopen(Request)
            File = open(os.path.normpath(os.path.join(BASEDIR, ntpath.basename(PdfFiles[i]))), mode='w')
            File.write(Response.read())
            #File.flush()
            File.close()
        except urllib2.HTTPError as error:
            print Fore.RED + 'An error occured during downloading of ' + PdfFiles[i], error.reason, Fore.RESET
        except KeyboardInterrupt:
            print Fore.BLUE + '\nDownloading interrupted by user, the last file ' 
            print '/!\\ Last file ' + ntpath.basename(PdfFiles[i]) + ' can be corrupted !' + Fore.RESET 
            break
    print Fore.RESET + '_ Done. Please check out content of ' + os.path.normpath(os.path.join(os.getcwd(), BASEDIR))
# The end
sys.exit(0)

# #!/bin/bash
# wget -O w1.txt http://aws.amazon.com/whitepapers/ && \
# for i in `awk -F'"' '$0=$2' w1.txt | grep pdf | grep -v http`; 
# do 
#     wget http:$i
# done
