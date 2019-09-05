import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os.path
import re



headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
class Reddit:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        self.posts = []
        self.last_post_id = -1
        self.is_nsfw_allowed = False
        self.has_saved_posts = True
        self.is_last_post_reached = False
    
    def run(self):
        self.login()
        self.fetch_saved_posts()
        self.write_csv()

    def allow_nsfw(self):
        self.is_nsfw_allowed = True

    def login(self):
        bot = self.bot
        print('Logging into reddit..')
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
        print('Login successful.')
        time.sleep(5)
    
    def set_last_post_id(self, post_id):
        self.last_post_id = post_id

    def fetch_saved_posts(self):
        print('Loading saved post page..')
        self.bot.get('https://www.reddit.com/user/"Your-Username"/saved/')
        self.has_saved_posts = True

        print('Capturing saved posts..')
        while self.has_saved_posts and not self.is_last_post_reached:
            self.get_posts()
            self.goto_next_page()
            time.sleep(5)
        
        print('Capturing complete.')
        self.bot.quit()

    def get_posts(self):
        print('Processing post info..')
        post_list = self.bot.find_elements_by_css_selector("[data-type=link]")
        
        for post in post_list:
            is_post_nsfw = post.get_attribute("data-nsfw") == "true"
            link = post.find_element_by_css_selector("[data-event-action=title]")
            title = link.get_attribute("innerText")
            desc = link.get_attribute("href")
            post_id = post.get_attribute("data-fullname")

            if self.last_post_id == post_id:
                self.is_last_post_reached = True
                break

            if not self.is_nsfw_allowed and is_post_nsfw:
                continue            

            self.posts.append([title, desc, post_id])
    
    def goto_next_page(self):
        #TODO: Update next button selector check
        next_btn = self.bot.find_element_by_css_selector(".next-button a")
        
        if next_btn and not self.is_last_post_reached:
            print('Loading next page..')
            self.has_saved_posts = True
            next_btn.click()
            time.sleep(5)
        else:
            self.has_saved_posts = False
            return

    def write_csv(self):
        #TODO: instead of overwriting allo user to select mode - write new file or append to existing
        print('Writing data to CSV..')
        output = csv.writer(open("test.csv", "w", newline=''))
        output.writerows(self.posts)
        print('Data successfully written.')

        
ed = Reddit("Your-Username", "Your-password")
ed.run()               
    

