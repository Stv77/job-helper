from errno import ENOENT
from msilib.schema import Error
import nltk
#nltk.download("stopwords") -> run once
from nltk.corpus import stopwords
import selenium
import requests
import wget
import zipfile
import os

id_stopwords = stopwords.words('indonesian')
en_stopwords = stopwords.words('english')

def extract_webdriver(extract_location):
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url,'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_location) # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)
    with open('webdriverInstalled.txt', 'w') as w:
        w.write('The webdriver has been installed.')


destination_extract = r'.\Lib\site-packages\selenium\webdriver\chrome'

#checking the existence of webdriver
if(os.path.isfile('webdriverInstalled.txt')):
    print("Webdriver has been installed!")
else:
    extract_webdriver(destination_extract)