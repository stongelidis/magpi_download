import os
import sys
import urllib3
import requests
from bs4 import BeautifulSoup


def get_directory(issue):
    # sorts issue into directories by issue name

    # example: MagPi83.pdf
    # example: Essentials_AIY_Projects_Voice_v1.pdf
    # example: Projects_Book_v1.pdf

    if issue[:5] == 'MagPi':
        return 'magpi-issues/'
    
    if issue[:8] == 'Projects':
        return 'projects/'

    if issue[:10] == 'Essentials':
        return 'essentials/'

    return 'other/'


if __name__ == '__main__':

    src = 'https://raspberrypi.org/magpi-issues/'

    if len(sys.argv) > 1:
        base = sys.argv[1]

        if base[-1] != '/':
            base = base + '/'

    else:
        base = ''
    
    # setup and request page
    http = urllib3.PoolManager()
    r = requests.get(src)

    # filter page
    soup = BeautifulSoup(r.content, "html5lib")
    tags = soup('a')

    # cycle thru webpage
    for hlink in tags:

        # create variable for full url
        issue = hlink.get('href', None)

        # only follow hlinks with PDF in the url
        if 'pdf' in issue:
            
            # define the url for the issue
            issue_link = src + issue

            # get sub-directory for issue destination
            sub_dir = get_directory(issue)
            dst = base + sub_dir

            # define issue path and replace special characters, if needed
            issue_path = dst + issue
            issue_path = issue_path.replace('%23', '#')
            issue_path = issue_path.replace('%20', ' ')

            # check if issue already exists in destination folder
            issue_downloaded = os.path.exists(issue_path)

            # if issue does not exist then download
            if not issue_downloaded:
                print('Downloading to: {}'.format(dst + issue))
                cmd = 'wget -v --directory-prefix={} -a log.txt {}'.format(dst, issue_link)
                os.system(cmd)
            
            # break
