# Download MagPi Issues
This script is used to download MagPi issues found on the [main page](https://magpi.raspberrypi.org/issues). It will avoid duplications by comparing the issue number on the MagPi homepage with the title of the files already saved in the user specified download directory.

## Running 
To run the script use 
```
python3 magpi_download.py -d <specify download directory>
```
Use this script with cronjob to check the site periodically to automatically download new issues as they appear
