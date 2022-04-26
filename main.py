from errno import ENOENT
from hashlib import new
from msilib.schema import Error
import re
import time
import nltk
from nltk.corpus import stopwords
from selenium import webdriver
import requests
import wget
import zipfile
import os
import requests
from requests_html import HTMLSession


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

#checking the existence of webdriver & download nltk stopwrods 1st time
if(os.path.isfile('webdriverInstalled.txt')):
    print("Webdriver has been installed!")
else:
    extract_webdriver(destination_extract)
    nltk.download("stopwords")

#driver
options = webdriver.ChromeOptions()
options.add_argument(open("dumping_ground.txt", "r").read())
driver = webdriver.Chrome(executable_path=destination_extract+ r"\chromedriver.exe", chrome_options=options)

def link(url):
    session = HTMLSession()
    response = session.get(url)

    links_html = response.html.absolute_links
    storing = """"""
    for x in links_html:
        storing+=x+"\n"
    new_links = re.compile("https://www.jobstreet.co.id/id/job/\w.+")
    return new_links.findall(storing)

def get_links(driver):
    #Open the page to get the biggest page number
    main_link = 'https://www.jobstreet.co.id/id/job-search/staff-notaris-jobs/'
    driver.maximize_window()
    driver.get(main_link)

    container_num = []

    #Get the biggest page number
    num_pag = driver.find_elements_by_css_selector('select.sx2jih0.sx2jih1 > option')
    for num_pags in num_pag:
        container_num.append(num_pags.text)

    biggest_num = container_num[-1]

    final_lists = []
    #Pagination
    for x in range(int(biggest_num)):
        #First page: get the link
        if x == 0:
            copy_list = link(url=main_link).copy()
            for x in copy_list:
                final_lists.append(x)
        #The rest: reload and get the link
        elif x >= 1:
            new_link = main_link +str(x+1)+'/'
            driver.get(new_link)
            time.sleep(3)
            copy_list = link(url=new_link).copy()
            for x in copy_list:
                final_lists.append(x)

    # Store the links in txt file
    if len(final_lists) == 0:
        pass
    elif len(final_lists) > 0:
        with open('list_of_links.txt','w') as l:
            for items in final_lists:
                l.write('%s\n' % items)
    driver.quit()

get_links(driver=driver)