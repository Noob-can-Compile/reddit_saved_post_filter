import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os.path


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
class Reddit:
    def __init__(self, username, password):
        self.username  = username
        self.password = password
        self.bot = webdriver.Firefox()
    def login(self):
        bot = self.bot
        bot.get('https://reddit.com/login')
        time.sleep(5)
        username = bot.find_element_by_id('loginUsername')
        password = bot.find_element_by_id('loginPassword')
        username.clear()
        password.clear()
        username.send_keys(self.username)
        password.send_keys(self.password)
        signin = bot.find_element_by_class_name('AnimatedForm__submitButton')
        signin.send_keys(Keys.RETURN)
        time.sleep(5)
        bot.get('https://www.reddit.com/user/"your-username"/saved/')
        self.get_saved_post()

    def get_saved_post(self, is_nsfw_allowed=False):
        saved_links_query = "div.saved.link"
        if not is_nsfw_allowed:
            saved_links_query += ":not(.over18)"
        saved_links_query += " a.title"
        saved_links = self.bot.find_elements_by_css_selector(saved_links_query)
        #print("Total post found: " + count(saved_links))
        posts = []
        for link in saved_links:
            print("---")
            title = link.get_attribute("innerText")
            print("Title: " + title)
            desc = link.get_attribute("href")
            print("Link:  " + desc)
            posts.append([title, desc])
        output = csv.writer(open("test.csv", "w", newline=''))
        output.writerows(posts)
        print(output)

        
ed = Reddit('your-username', 'your-password')
ed.login()               
    



