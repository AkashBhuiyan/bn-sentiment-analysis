from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from shutil import which
from parsel import Selector
import csv

url = "https://www.facebook.com/login.php"
prothomAloPage = "https://www.facebook.com/DailyProthomAlo"

bbcBanglaPost1 = 'https://www.facebook.com/BBCBengaliService/posts/4281495428555996'
filename = 'comments'
chrome_path = which("chromedriver")


class FacebookLogin():
    def __init__(self, email, password, browser='Chrome'):
        self.email = email
        self.password = password
        if browser == 'Chrome':
            self.driver = webdriver.Chrome(
                executable_path=chrome_path)
        self.driver.get(url)
        time.sleep(1)

    def login(self):
        email_element = self.driver.find_element_by_id('email')
        email_element.send_keys(self.email)

        password_element = self.driver.find_element_by_id('pass')
        password_element.send_keys(self.password)

        login_button = self.driver.find_element_by_id('loginbutton')
        login_button.click()

        time.sleep(3)

    def post(self, url, filename):
        self.driver.get(url)
        input("Please press enter key!")
        time.sleep(2)
        # sel = Selector(text=self.driver.page_source)
        while True:
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div [@role = 'main']/div[4]/div[1]//span[contains(text(),'View more comments')]"))).click()
                time.sleep(5)
                continue
            except:
                break

        # data = self.driver.find_elements_by_xpath(
        #     "//div [@style = 'text-align: start;']")
        data = self.driver.find_elements_by_xpath(
            "//div [@role = 'main']/div[4]/div[1]//div [@style = 'text-align: start;']")

        print(data)
        for text_data in data:
            data_list = text_data.text
            comments = [data_list.strip()]
            with open(f"./comments/{filename}.csv", "a", newline='', encoding='utf-8-sig') as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow(comments)
        # self.driver.find_element_by_xpath("//div [@role = 'main']/div[4]/div[1]//span[contains(text(),'View more comments')]").click()

    def loops(self, filename):
        while True:
            urls = input("Please enter the url")
            if urls == "none":
                break
            else:
                self.post(urls, filename)
            print(
                "\nCompleted scraping the comments for this content, going to next....\n")


if __name__ == '__main__':
    # Enter your login credentials here
    fb_login = FacebookLogin(email='',
                             password='', browser='Chrome')
    fb_login.login()
    # fb_login.post(url=bbcBanglaPost1, filename=filename)
    fb_login.loops(filename)
