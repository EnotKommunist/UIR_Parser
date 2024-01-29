from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


url = 'https://www.wildberries.ru/catalog/0/search.aspx?search=iphone%2015'
service = Service(executable_path='D:\\pythonProjects\\UIR_Parser\\chromedriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)


try:
    driver.get(url=url)
    time.sleep(60)
except Exception as ex:
    print(ex)

finally:
    print('хи-хи')
