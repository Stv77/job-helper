from selenium import webdriver

destination_extract = r'.\Lib\site-packages\selenium\webdriver\chrome'
options = webdriver.ChromeOptions()
options.add_argument(open("dumping_ground.txt", "r").read())
driver = webdriver.Chrome(executable_path=destination_extract+ r"\chromedriver.exe", chrome_options=options)