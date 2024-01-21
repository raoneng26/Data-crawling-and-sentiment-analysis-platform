from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from streamlit import runtime
import sys
from streamlit.web import cli as stcli
import random
import time
import base64
import json
import numpy as np
import pandas as pd
import os
import requests
import csv
import re
import all_get_2
import io
from time import sleep
from streamlit.components.v1 import html
from test import analysis
from streamlit_card import card as st_card
from streamlit_elements import elements, mui, html
from streamlit_echarts import st_echarts
from datetime import datetime,timedelta
from docx2pdf import convert
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions


@st.cache_data
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')


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


def initial():
    global keyword
    keyword = None
    global website
    website = None
    global key
    key = None
    global web
    web = None
    global uploaded_file1
    uploaded_file1 = None
    global uploaded_file2
    uploaded_file2 = None


def progress_bar(max_time):
    start_time = time.time()
    progress_placeholder = st.empty()  # 创建一个占位符
    for i in range(1, 101):
        num_progress=i
        progress_placeholder.markdown(f''' 
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Progress_bar</title>
                <link rel="stylesheet" href="progress_bar.css">
            </head>
            <body>
                <div class="container">
                    <section>
                        <article>
                            <!-- <input type="radio" name="switch-color" id="red" checked>
                            <input type="radio" name="switch-color" id="cyan">
                            <input type="radio" name="switch-color" id="lime"> -->
                            <div class="chart">
                                <div class="bar bar-{num_progress} cyan">
                                    <div class="face top">
                                        <div class="growing-bar"><p style="float: right; margin-right:10px"><strong>{num_progress}</strong>%</p></div>
                                    </div>
                                    <div class="face side-0">
                                        <div class="growing-bar"></div>
                                    </div>
                                    <div class="face floor">
                                        <div class="growing-bar"></div>
                                    </div>
                                    <div class="face side-a"></div>
                                    <div class="face side-b"></div>
                                    <div class="face side-1">
                                        <div class="growing-bar"></div>
                                    </div>
                                </div>
                            </div>
                        </article>
                    </section>
                </div> 
            </body>
            </html>''',unsafe_allow_html=True)
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            break
        if i<100:
            sleep_time = random.uniform(0.01, (max_time - elapsed_time) / (100 - i))
            time.sleep(sleep_time)
            progress_placeholder.empty()
    

def get_base64(bin_file): 
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):  # 设置背景图
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/ipg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def upload_file_to_0x0(file_path):
    """上传文件到0x0并返回URL"""
    with open(file_path, 'rb') as f:
        response = requests.post('https://0x0.st', files={'file': f})
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None
    

def normalize_location_names(locations):
    provinces = ['河南', '江苏', '山西', '福建', '四川', '海南', '吉林', '安徽', '浙江', '陕西', '黑龙江', '广东',  '河北', '山东', '辽宁', '云南', '湖北', '江西', '湖南', '甘肃', '贵州','青海','台湾']
    municipalities = ['天津', '重庆', '北京', '上海']
    special_administrative_regions = ['香港', '澳门']
    autonomous_regions = {'新疆': '新疆维吾尔自治区','内蒙古': '内蒙古自治区','西藏': '西藏自治区','宁夏': '宁夏回族自治区','广西': '广西壮族自治区'}
    others = ['其他']
    all_locations = provinces + municipalities + list(autonomous_regions.keys()) + special_administrative_regions + others
    new_locations = {}
    for location in locations.keys():
        if location in all_locations:
            if location in provinces:
                new_locations[location + "省"] = locations[location]
            elif location in municipalities:
                new_locations[location + "市"] = locations[location]
            elif location in special_administrative_regions:
                new_locations[location + "特别行政区"] = locations[location]
            elif location in autonomous_regions:
                new_locations[autonomous_regions[location]] = locations[location]
            else:
                new_locations[location] = locations[location]
    return new_locations


def report_show():
    st.markdown(r'''<style>
                    .box {
                        position: relative;
                    }
                        .box img {
                        width: 300px;
                    }

                    .box .title {
                        position: absolute;
                        left: 15px;
                        bottom: 20px;
                        z-index: 2;
                        width: 260px;
                        color: #fff;
                        font-size: 20px;
                        font-weight: 700;
                    }
                    .box .mask {
                        position: absolute;
                        left: 0;
                        top: 0;

                        opacity: 0;
                        width: 300px;
                        height: 410px;
                        background-image: linear-gradient(
                            transparent,
                            rgba(0,0,0,.6)
                        );
                        transition: all .5s;
                    }
                    .box:hover .mask {
                        opacity: 1;
                    } 
                </style>''',unsafe_allow_html=True)
    reportpath1='report.jpg' # -----------------更改点--------------
    # reporturl=st.session_state.url_pdf
    if "疫情" in st.session_state.file_in.name:
        reporturl=r"https://shimo.im/file/ZzkLMeKnJ7cyPMAQ/"# -----------------更改点--------------
        
    if "日本" in st.session_state.file_in.name:
        reporturl=r"https://shimo.im/file/m8AZMmW044Sx5xkb"
    with open(reportpath1, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
        data = "data:image/png;base64," + encoded.decode("utf-8")
    st.markdown(f'''
    <body>
        <div class="box">
            <a  href={reporturl}>
            <img src={data} alt="">
            <div class="title">分析报告</div>
            <!-- 渐变背景 -->
            <div class="mask"></div>
            </a>
        </div>
    </body>
    </html>''',unsafe_allow_html=True)


def card_show():
    reportpath='report.jpg'
    bgcpath='bgc.jpg'
    with open(reportpath, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
        data = "data:image/png;base64," + encoded.decode("utf-8")
        # st.markdown(r'''<style>
        #         .css-1mb7ed4 {
        #         background-color: rgba(211, 211, 211, 0.1);
        #         }
                
        #         </style>''',unsafe_allow_html=True)
        
    res = st_card(
    title="分析报告",
    text="analysis",
    image=data,
    styles={
        "card": {
            "width": "250px",
            "height": "320px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",    
        },
    },
    url="https://github.com/gamcoh/st-card",
    on_click=lambda: st.write(''))


def get_middle_part(file_name):
    # 去除文件扩展名
    file_name = file_name.split('.')[0]
    # 按照 "-" 分割文件名
    parts = file_name.split('-')
    
    if len(parts) > 1:
        middle_part = parts[1]
    else:
        middle_part = parts[0]
    
    return middle_part


def change_date(times):
    time2 = []
    for time1 in times:
        time1 = str(time1)[:10]
        time2.append(time1)
    return time2


def find_imppost_data(file):
    file.seek(0)
    if 'xlsx' in file.name:
        data = pd.read_excel(io.BytesIO(file.read()))
    else:
        data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
    data['评论时间'] = change_date(data['评论时间'].values)
    df = data.sort_values(by="评论时间", ascending=True)
    df['评论时间'] = pd.to_datetime(df['评论时间'])
    df['日期'] = df['评论时间'].dt.strftime('%Y-%m-%d')
    # print(df['日期'].to_string())
    df_deduplicated = df.drop_duplicates(subset=['发布者', '文本'], keep='first')
    df_sorted = df_deduplicated.sort_values(['日期', '点赞数'], ascending=[True, False])
    posts_dict_poster= pd.Series(df_sorted[[ '发布者']].values.tolist(), index=df_sorted['日期']).to_dict()
    posts_dict = pd.Series(df_sorted[['文本', '发布者']].values.tolist(), index=df_sorted['日期']).to_dict()
    # print('posts_dict',posts_dict)
    # print('posts_dict_poster',posts_dict_poster)
    return(posts_dict,posts_dict_poster)


def match_url(dict_, csv_file):
    csv_file.seek(0)
    if 'xlsx' in csv_file.name:
        url_data = pd.read_excel(io.BytesIO(csv_file.read()))
    else:
        url_data = pd.read_csv(io.BytesIO(csv_file.read()), encoding='utf-8', sep=';')
    result_dict = {}
    # print('dict_',dict_)
    # print("url_data",url_data)
    for date, publisher in dict_.items():
        date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%Y年%m月%d日')
        matched_row = url_data[(url_data['发布时间'].str.startswith(date_str)) & (url_data['发布者'] == publisher[0])]
        if not matched_row.empty:
            result_dict[date] = matched_row['url'].values[0]
        else:
            # 如果当天没有找到匹配的数据，尝试在前几天找
            for i in range(1, 8):  # 尝试在前7天找
                prev_date_str = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=i)).strftime('%Y年%m月%d日')
                matched_row_prev = url_data[(url_data['发布时间'].str.startswith(prev_date_str)) & (url_data['发布者'] == publisher[0])]
                if not matched_row_prev.empty:
                    result_dict[date] = matched_row_prev['url'].values[0]
                    break
            else:
                result_dict[date] = None
    # print(result_dict)
    return result_dict



def add_publish_time(df, cluster):
    # 将cluster的url设为索引，方便后续的匹配操作
    cluster.set_index('博客url链接', inplace=True)
    # 使用map函数，将df中的url映射到cluster中的发布时间
    df['发布时间'] = df['url'].map(cluster['发布时间'])
    # 获取'发布时间'列
    publish_time = df['发布时间']
    # 删除原来的'发布时间'列
    df.drop(labels=['发布时间'], axis=1, inplace=True)
    # 将'发布时间'列插入到第二个位置
    df.insert(1, '发布时间', publish_time)

    return df


# def find_imppost_data(file):
#     file.seek(0)
#     if 'xlsx' in file.name:
#         data = pd.read_excel(io.BytesIO(file.read()))
#     else:
#         data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
#     data['评论时间'] = change_date(data['评论时间'].values)
#     df = data.sort_values(by="评论时间", ascending=True)
#     df['评论时间'] = pd.to_datetime(df['评论时间'])
#     df['日期'] = df['评论时间'].dt.strftime('%Y-%m-%d')
#     df_deduplicated = df.drop_duplicates(subset=['发布者', '文本'], keep='first')
#     df_sorted = df_deduplicated.sort_values(['日期', '点赞数'], ascending=[True, False])
#     posts_dict_poster= pd.Series(df_sorted[['url']].values.tolist(), index=df_sorted['日期']).to_dict()
#     posts_dict = pd.Series(df_sorted[['文本', '发布者', 'url']].values.tolist(), index=df_sorted['日期']).to_dict()
#     return(posts_dict,posts_dict_poster)


# def match_url(dict_, file):
#     file.seek(0)
#     if 'xlsx' in file.name:
#         url_data = pd.read_excel(io.BytesIO(file.read()))
#     else:
#         url_data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
#     result_dict = {}
#     for date, publisher in dict_.items():
#         date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%m月%d日')
#         matched_row = url_data[(url_data['发布时间'].str.startswith(date_str)) & (url_data['发布者'] == publisher[0])]
#         if not matched_row.empty:
#             result_dict[date] = matched_row['博客url链接'].values[0]
#         else:
#             # 如果当天没有找到匹配的数据，尝试在前几天找
#             for i in range(1, 8):  # 尝试在前7天找
#                 prev_date_str = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=i)).strftime('%m月%d日')
#                 matched_row_prev = url_data[(url_data['发布时间'].str.startswith(prev_date_str)) & (url_data['发布者'] == publisher[0])]
#                 if not matched_row_prev.empty:
#                     result_dict[date] = matched_row_prev['博客url链接'].values[0]
#                     break
#             else:
#                 result_dict[date] = None
#     # print(result_dict)
#     return result_dict


def main():
    initial()
    st.session_state.style="标准情绪值"

    st.set_page_config(layout="wide")
    set_background("bgc.jpg")  ##更改点（背景图）
    col,col_title,col=st.columns([1.7,4,1])
    with col_title:      
        st.header("热点事件引发的群体情绪传播效果评估系统")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Start', 'Regional Analysis', 'Time Domain', 'Comparative Ranking'], 
                            iconName=['star', 'language', 'schedule', 'leaderboard'], default_choice=0)

    


    if tabs =='Start': 
        st.session_state.file_in=" "
        st.subheader('爬取链接')

        if  "geturl" not in st.session_state:

            st.session_state.keyword = st.text_input('请输入爬取的关键词:')
            st.session_state.website = st.selectbox(
                '请选择要爬取的网站:',
                (' ','微博', '哔哩哔哩','抖音'))
            
            #爬取微博帖子urlst.session.
            if st.session_state.website == '微博':
                file = '微博' + st.session_state.keyword + '.csv'
                date = st.text_input('请输入起止时间(eg.2023-09-01-0:2023-11-08-23):')
                if date:
                    st.info('请前往微博页面完成登陆')
                    weibo_url = 'https://s.weibo.com/'

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



                    driver.get(weibo_url)
                    # time.sleep(30)

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
                                    up_name = blog.find_element(By.CSS_SELECTOR, ".name").text
                                    try:
                                        blog_url = blog.find_element(By.CSS_SELECTOR, "div.from> a:nth-child(1)").get_attribute('href')
                                    except:
                                        blog_url = 'NULL'
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
        else:
            st.success('数据链接爬取结束')            

            
        st.subheader('爬取数据')
        # key = st.text_input('请输入爬取的关键词:')
        if  "getdata" not in st.session_state:

            file2 = st.file_uploader("请上传爬取的url文件：")
            if file2 is not None:
                st.success('上传成功')
            else:
                st.warning('未上传')
            if file2 is not None:
                cluster = pd.read_csv(file2, encoding='utf-8', sep=';')
                n = 0
                for i in range(0, cluster.shape[1]):
                    sheet = cluster.iloc[:, i].values
                    if re.match(r"(http|https|ftp)://\S+", str(sheet[0])):
                        n = i
                        break
                    else:
                        continue
                sheet = cluster.iloc[:, n].values

                if "keyword" not in st.session_state:
                    st.session_state.keyword = st.text_input('请输入爬取的关键词: ')
                if "website" not in st.session_state:
                    st.session_state.website = st.selectbox(
                        '请选择要爬取的网站: ',
                        (' ','微博', '哔哩哔哩','抖音'))
            

                if st.session_state.website == '微博':
                    if "geturl" not in st.session_state:
                        _ = installff()
                    opts = FirefoxOptions()
                    #-----------------------------------------------云部署必须开启无头模式---------------------------------------------
                    opts.add_argument("--headless")    
                    driver = webdriver.Firefox(options=opts)

                    weibo_url = 'https://s.weibo.com/'
                    driver.get(weibo_url)
                    time.sleep(3)
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
                    data = []  # 初始化一个空列表来存储数据
                    rows = len(sheet)
                    for i in range(0, rows):
                        url = sheet[i]
                        result = all_get_2.weibo(url, 0, st.session_state.keyword, driver)  # 获取数据
                        if result is not None:  # 检查结果是否为None
                            data.extend(result)  # 如果结果不是None，将数据添加到列表中
                        print(data)
                        time.sleep(10)
                        all_get_2.view_bar(i, rows)

                    # 创建一个DataFrame，列名为你指定的列名，数据为你刚刚获取的数据
                    df = pd.DataFrame(data, columns=["发布者","IP属地","帖子账号粉丝数", "转发数", "评论数", "点赞数", "文本", "话题", "一级账号粉丝数","用户名","评论属地", "评论内容", "评论时间", "评论点赞数", "主题相似度" ,"标记", "url"])
                    df = add_publish_time(df, cluster)  # 添加发布时间
                    st.info('根据主题相似度过滤：')
                    clean_data = all_get_2.cleandata(df)  # 清理数据
                    st.info("信息过滤完成")
                    driver.close()
                    csv_clean_data = clean_data.to_csv(index=False, sep=';').encode('utf-8')  # 将清理后的数据转换为CSV格式的数据
                    st.download_button(label="下载数据文件", data=csv_clean_data, file_name="clean-" + '微博' + st.session_state.keyword + '数据.csv', mime='text/csv')  # 提供下载链接
                    st.write(clean_data)  # 在Streamlit应用中显示清理后的数据
                    st.session_state.getdata=True
        else:
            st.success('数据爬取结束')            




    if tabs == 'Regional Analysis':
        
        st.subheader("地域情感分析")
        if  st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        # else:
        col1,col2=st.columns([3,1])
        
        with col1:
            with st.spinner('Wait about 20 seconds'):
                with st.expander("情绪地图",True):
                    if st.session_state.file_in ==" ":
                        unploaded_in = st.empty() 
                        uploaded_file2=unploaded_in.file_uploader("")
                        if uploaded_file2 is not None:
                            waring.empty()
                            st.session_state.file_in=uploaded_file2
                            st.success('upload success!')
                            # if st.session_state.website==" ":
                            st.session_state.website = st.selectbox('请选数据的地区范围:',(' ','国内', '世界'))
                            style=st.empty()
                            col,col_map,col=st.columns([1,8,1])
                            with col_map:
                                if st.session_state.website=="国内":
                                    # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                    analysis('群体情绪中国地图',uploaded_file2)
                                if st.session_state.website=="世界":
                                    # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                    analysis('群体情绪世界地图',uploaded_file2)
                                unploaded_in.empty()
                    else:
                        uploaded_file2=st.session_state.file_in
                        if st.session_state.website==" ":
                            st.session_state.website = st.selectbox('请选数据的地区范围:',(' ','国内', '世界'))
                        style=st.empty()
                        col,col_map,col=st.columns([1,8,1])
                        with col_map:
                            if st.session_state.website=="国内":
                                # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                analysis('群体情绪中国地图',uploaded_file2)
                            if st.session_state.website=="世界":
                                # st.session_state.style=style.selectbox("  ",("标准情绪值","相对情绪值"))
                                analysis('群体情绪世界地图',uploaded_file2)
                if st.session_state.file_in !=" " and st.session_state.website!=" ":
                        with st.expander("各地区情绪占比",True):
                            b1, b2, b3 = st.columns([1, 0.3, 0.2])
                            with b1:
                                st.empty()
                            with b2:
                                st.session_state.p=st.selectbox("",("正面","负面"))
                            col,col_pie,col=st.columns([1,8,1])
                            with col_pie:
                                analysis("群体情绪强度饼图",uploaded_file2)
                

        with col2:
            if st.session_state.file_in !=" " and st.session_state.website!=" ":
                with st.expander('分析报告',True):
                    report_show()


    if tabs == 'Time Domain':
        # st.session_state.data=None
        st.subheader("时序情感分析")
        if st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        # else:
        col1,col2=st.columns([3,1])
        with col1:
            with st.spinner('Wait about 10 seconds'):
                with st.expander("群体情绪趋势",True):
                    if st.session_state.file_in ==" ":
                        unploaded_in = st.empty() 
                        uploaded_file4=unploaded_in.file_uploader(" ")
                        if uploaded_file4 is not None:
                            waring.empty()
                            st.session_state.file_in=uploaded_file4


                            post_all,post_poster=find_imppost_data(uploaded_file4)
                            st.session_state.post_url=match_url(post_poster,uploaded_file4)


                            st.success('upload success!')       
                            analysis('群体情绪趋势图',uploaded_file4)
                            unploaded_in.empty()
                        
                            if st.session_state.data:
                                st.warning(st.session_state.data+" 的代表帖子")
                                st.warning(st.session_state.imppost[st.session_state.data])

                    else:
                        uploaded_file4=st.session_state.file_in
                       
                        post_all,post_poster=find_imppost_data(uploaded_file4)
                        st.session_state.post_url=match_url(post_poster,uploaded_file4)
                        analysis('群体情绪趋势图',uploaded_file4)
                    
                        if st.session_state.data:
                            st.warning(st.session_state.data+" 的代表帖子")
                            st.warning(st.session_state.imppost[st.session_state.data])
                        
                        st.warning('点击查看各日期的代表帖子')
                             
        with col2:
            if st.session_state.file_in !=" ":
                with st.expander('分析报告',True):
                    report_show()
            

    if tabs == 'Comparative Ranking':
        st.session_state.p2="正面"
        video_path=" "
        st.subheader("多维度情感分析")
        if  st.session_state.file_in==" ":
            st.session_state.average_score=None
            waring=st.empty()
            waring=st.warning("请先获取并上传数据")
        col1,col2=st.columns([1,1])

        with col1:
            with st.expander("正负情绪排行榜",True):
                st.session_state.name=None
                st.session_state.p2 = None
                if st.session_state.file_in ==" ":
                    unploaded_in = st.empty() 
                    uploaded_file6=unploaded_in.file_uploader(" ")
                    if uploaded_file6 is not None:
                        st.session_state.file_in=uploaded_file6
                        waring.empty()
                        st.success('upload success!')
                        b1, b2 = st.columns([1, 0.3])
                        with b1:
                            st.empty()
                        with b2:
                            st.session_state.p2=st.selectbox("",("正面","负面"))
                        analysis('群体情绪排行榜',uploaded_file6)
                        unploaded_in.empty()
                else:
                    uploaded_file6=st.session_state.file_in
                    b1, b2 = st.columns([1, 0.3])
                    with b1:
                        st.empty()
                    with b2:
                        st.session_state.p2=st.selectbox("",("正面","负面"))
                    analysis('群体情绪排行榜',uploaded_file6)
            if st.session_state.p2 is not None:
                with st.expander('展开显示全部标题'):
                    if st.session_state.p2=="负面":
                        ln = len(st.session_state.title_N)
                        for j in range(0, ln):
                            st.write(str(j) + ': ' + st.session_state.title_N[j])
                    else:
                        ln = len(st.session_state.title_P)
                        for j in range(0, ln):
                            st.write(str(j) + ': ' + st.session_state.title_P[j])

        with col2:
            # with st.expander("媒介风格分析",True):
            #     if st.session_state.name!=None:
            #         warn=st.empty()
            #         warn.warning(st.session_state.name)
            #         if "的微博视频" in st.session_state.name:
            #             if'卫星观地球'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\1.mp4'    
            #             if'难舍深蓝'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\2.mp4'    
            #             if'经济过热'in st.session_state.name:
            #                 video_path=r'data_weibo\疫情后的经济\video\1.mp4'
            #             if'德国联邦议院'in st.session_state.name:
            #                 video_path=r'data_weibo\疫情后的经济\video\2.mp4'
            #             if'墨染诗婳'in st.session_state.name:
            #                 video_path=r'data_weibo\日本核污水排放\video\9.mp4'    

            #             result_emotion="result.txt"
            #             file_modality="C:/Users/86187/Desktop/新闻策划与效果评估系统/情感传播效果评估子系统/result_modality.csv"
                        
            #         col_video,col_charts=st.columns([1,1])                

            #         if video_path !=" ":
            #             other_video=st.empty()
            #             with col_video:
            #                 file_video=st.empty()
            #                 file_video.video(video_path) # 更改点                                

            #             with col_charts:                           
            #                 base_name = os.path.basename(video_path)
            #                 fn = os.path.splitext(base_name)[0]
            #                 try:
            #                     V2EM_prediction.main_for_st.emotion_analysis(str(fn)) 
            #                     the_chart=st.selectbox('',('情绪极性','各模态细粒度分析'))
            #                     if the_chart=='情绪极性':
            #                         analysis('单视频情绪极性',result_emotion)
            #                     if the_chart=='各模态细粒度分析':
            #                         analysis('单视频模态细粒度',file_modality)
            #                 except:
            #                     warn.error('该视频多模态情感分析失效，尝试上传其他视频（失效原因：视频中未出现人脸或出现多个人脸）')
            #                     file_video.empty()
            #                     uploaded_video = other_video.file_uploader('  ')
            #                     if uploaded_video is not None:
            #                         warn.success('上传成功！')
            #                         other_video.empty()
            #                         fn = uploaded_video.name.split('.')[0]
            #                         mp4_path = f'D:/电磁辐射网络舆情分析系统/code/data_weibo/日本核污水排放/video/{fn}.mp4'
            #                         file_video.video(mp4_path)
            #                         V2EM_prediction.main_for_st.emotion_analysis(str(fn)) 
            #                         the_chart=st.selectbox('',('情绪极性','各模态细粒度分析'))
            #                         if the_chart=='情绪极性':
            #                             analysis('单视频情绪极性',result_emotion)
            #                         if the_chart=='各模态细粒度分析':
            #                             analysis('单视频模态细粒度',file_modality)
          

            if st.session_state.file_in != " ":
                with st.expander('分析报告',True):
                    col,col_rpt,col=st.columns([1,2,1])
                    with col_rpt:
                        report_show()
                
            
    

if __name__ == '__main__':  # 不用命令端输入“streamlit run app.py”而直接运行
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
