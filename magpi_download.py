import os
import sys
import argparse
import re
import urllib3
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':

    # base url for magpi magazines
    src = 'https://magpi.raspberrypi.org/issues'

    # parse arguments from user
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--download_directory', help='Directory for magpi files', default=os.getcwd())
    args = parser.parse_args()

    # make sure directory path ends with forward slash
    dst = args.download_directory
    if dst[-1] != '/':
        dst = dst + '/'

    # setup and request initial page
    http = urllib3.PoolManager()
    r = requests.get(src)

    # filter page
    soup = BeautifulSoup(r.content, "html5lib")
    tags = soup('a')

    # cycle thru webpage to find issues
    for hlink in tags:

        # create variable for full url
        issue = hlink.get('href', None)

        # finds '/issues/xx/pdf' in url. these are the download links
        pattern = r'\/issues\/\d+\/pdf'
        matches = re.findall(pattern, issue)

        is_pdf_download_link = len(matches) > 0

        # only follow hlinks with PDF in the url
        if is_pdf_download_link:
            
            # define the url for the issue download page
            issue_link = src + issue[7:]

            r2 = requests.get(issue_link)

            # filter issue download page
            soup2 = BeautifulSoup(r2.content, "html5lib")
            tags2 = soup2('a')

            found_issue_link = False
            for hlink in tags2:
                # create variable for full url
                issue_url = hlink.get('href', None)
                
                # if 'pdf' is in url, then this is the download link 
                if 'pdf' in issue_url:
                    issue_link = issue_url
                    issue_link = 'https://magpi.raspberrypi.org' + issue_link
                    
                    found_issue_link = True

                if found_issue_link:
                    # get issue number
                    issue_match = re.findall(r'\d+', issue)

                    # define issue path at destination
                    issue_path = dst + 'MagPi{}.pdf'.format(issue_match[0])

                    # check if issue already exists in destination folder
                    issue_downloaded = os.path.exists(issue_path)

                    # if issue does not exist then download
                    if not issue_downloaded:
                        print('Downloading to: {}'.format(dst))
                        cmd = 'wget -v --directory-prefix={} -a log.txt {}'.format(dst, issue_link)
                        os.system(cmd)
                    
                    # break
