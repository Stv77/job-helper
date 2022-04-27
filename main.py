from errno import ENOENT
from hashlib import new
from msilib.schema import Error
import re
import time
import nltk
from nltk.corpus import stopwords
import requests
import wget
import zipfile
import os
import requests
from requests_html import HTMLSession
from webdriver import driver
from webdriver import destination_extract
import asyncio
from selenium.common.exceptions import NoSuchElementException

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

#checking the existence of webdriver & download nltk stopwrods 1st time
if(os.path.isfile('webdriverInstalled.txt')):
    print("Webdriver has been installed!")
else:
    extract_webdriver(destination_extract)
    nltk.download("stopwords")

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


#Checking the existence of lists
if(os.path.isfile('list_of_links.txt')):
    print("The lists are ready!")
else:
    get_links(driver=driver)

with open('list_of_links.txt','r') as l:
    links = l.readlines()
with open('yours.txt', 'r') as p:
    private = p.readlines()

async def main(num):
    for x in range(num):
        driver.maximize_window()
        driver.get(links[x])
        time.sleep(3)

        await asyncio.sleep(0.5)
        get_company_name()
        get_job_position()
        get_requirements()
        await asyncio.sleep(0.5)

        list_of_requirements = get_requirements().split(".")
        dump_txt(requirement_lists=list_of_requirements)
        apply()
        time.sleep(600)
        # remove_txt()

def get_requirements():
    temp_c = ""
    requirements = driver.find_elements_by_css_selector("ul > li")
    for y in requirements:
        temp_c+=y.text.lower()
    return temp_c

def login():
    masuk = driver.find_element_by_css_selector("a.sx2jih0.sx2jihf.uf80sq3")
    masuk.click()
    time.sleep(3)
    user = driver.find_element_by_id("login_id")
    user.click()
    user.send_keys(private[0])
    pwd = driver.find_element_by_id('password')
    pwd.click()
    pwd.send_keys(private[1])
    try:
        log = driver.find_element_by_css_selector("button.btn.btn-primary")
        log.click()
    except NoSuchElementException:
        print("Little error")
        

def get_job_position():
    position = driver.find_element_by_css_selector('h1.sx2jih0._18qlyvc0').text
    return position

def get_company_name():
    the_company_name = driver.find_element_by_xpath('//*[@id="contentContainer"]/div/div[1]/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/span').text
    return the_company_name

def apply():
    apply = driver.find_element_by_css_selector("div.sx2jih0.zcydq8fu > a")
    apply.click()

    write = driver.find_element_by_css_selector("textarea.form-control")
    write.click()

def dump_txt(requirement_lists):
    if(os.path.isfile('details.txt')):
        rewrite = open("details.txt", "w")
        rewrite.write('%s ' % get_company_name())
        rewrite.write(': %s' % get_job_position())
        for x in range(len(requirement_lists)):
            if x == 0:
                rewrite.write('\n\t%s\n' % requirement_lists[x])
            elif x > 0:
                rewrite.write('\t%s\n' % requirement_lists[x])
    else:
        with open("details.txt", "w") as rewrite:
            rewrite.write('%s ' % get_company_name())
            rewrite.write(': %s' % get_job_position)
            for x in range(len(requirement_lists)):
                if x == 0:
                    rewrite.write('\n\t%s\n' % requirement_lists[x])
                elif x > 0:
                    rewrite.write('\t%s\n' % requirement_lists[x])

def remove_txt():
    clear = open("details.txt", "r+")
    clear.truncate()

def call_use_links():
    driver.maximize_window()
    driver.get(links[0])
    login()
    loop = asyncio.get_event_loop()
    task = [loop.create_task(main(len(links)))]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()
    driver.quit()

call_use_links()