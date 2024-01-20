import streamlit as st
import os, sys
import time
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from time import sleep


@st.cache_data
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
opts = FirefoxOptions()
#-----------------------------------------------云部署必须开启无头模式---------------------------------------------
opts.add_argument("--headless")    
driver = webdriver.Firefox(options=opts)

# # driver.get('http://example.com')
# # st.write(driver.page_source)
weibo_url = 'https://s.weibo.com/'
driver.get(weibo_url)
time.sleep(3)

class CookieLogin:
    def __init__(self,f_path):
        """
        对象初始化
        :param url: 首页地址
        :param f_path: Cookies文件保存路径
        """
        # self.url = url
        self.f_path = f_path
        # self.browser = self.start_browser(executable_path)

    def save_cookies(self, data, encoding="utf-8"):
        """
        Cookies保存方法
        :param data: 所保存数据
        :param encoding: 文件编码,默认utf-8
        """
        with open(self.f_path, "w", encoding=encoding) as f_w:
            json.dump(data, f_w)
        print("save done!")

    def load_cookies(self, encoding="utf-8"):
        """
        Cookies读取方法
        :param encoding: 文件编码,默认utf-8
        """
        if os.path.isfile(self.f_path):
            with open(self.f_path, "r", encoding=encoding) as f_r:
                user_cookies = json.load(f_r)
            return user_cookies


driver.delete_all_cookies()
# 持久化登录，之后登录就不需要上面的扫二维码
login = CookieLogin("cookie.json")
cookies = login.load_cookies()
try:
    for cookie in cookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        print(cookie_dict)
        driver.add_cookie(cookie_dict)
except Exception as e:
    print(e)

sleep(3)

driver.refresh()

# 现在您可以使用 driver 访问已登录的微博页面
driver.get("https://weibo.com")


st.session_state.keyword="日本排放核污水"
date="2023-09-01-0:2023-09-20-23"
data = []
for i in range(1, 50):
    try:
        w_url = f"https://s.weibo.com/weibo?q={st.session_state.keyword}&timescope=custom:{date}&Refer=g&sudaref=s.weibo.com&page={i}"
        driver.get(w_url)
        driver.implicitly_wait(10)
        blogs = driver.find_elements(By.XPATH, "//div[@class='main-full']//div[@class='card-wrap']")
        if blogs:
            for blog in blogs:
                publish_time = blog.find_element(By.CSS_SELECTOR, "div.from> a:nth-child(1)").text
                print(publish_time)
                up_name = blog.find_element(By.CSS_SELECTOR, ".name").text
                print(up_name)
                try:
                    blog_url = blog.find_element(By.CSS_SELECTOR, "div.from> a:nth-child(1)").get_attribute('href')
                except:
                    blog_url = 'NULL'
                print(blog_url)
                data.append({"发布者": up_name, "发布时间": publish_time, "博客url链接": blog_url})
        else:
            st.warning('爬取失败')
    except:
        st.warning('一共爬取了'+str(i-1)+'页,'+'页数' + str(i) + '不存在')
        break
driver.close()

df = pd.DataFrame(data)
st.session_state.orifile=df
csv_data = df.to_csv(index=False, sep=';').encode('utf-8')
st.download_button(label="下载链接文件", data=csv_data, file_name='微博' + st.session_state.keyword + 'url.csv', mime='text/csv')
st.write(df)
st.session_state.geturl=True