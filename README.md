# Download MagPi Issues
This script is used to download any MagPi issues found on the main page of [MagPi Magazine](https://magpi.raspberrypi.org/issues). The script will check to see if the magazine issue matches any previously downloaded files by checking the titles in the specified directory. 

## Running 
To run the script use 
```
python3 magpi_download.py -d <specify download directory>
```
Use this script with cronjob to check the site periodically to automatically download new issues as they appear
