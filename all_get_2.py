# -*- coding: utf-8 -*-
# 该代码文件作用：爬取某具体视频的评论内容
import requests
import json
import pandas as pd
import sys
import time
import random
import re
from datetime import datetime
import math
import paddlehub as hub
from selenium.webdriver.common.by import By



def view_bar(num, total):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    bar = '\r[%s%s]%d%%,%d' % ("=" * rate_num, "" * (100 - rate_num), rate_num, num)
    sys.stdout.write(bar)
    sys.stdout.flush()


def random_sleep(mu, sigma):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
        time.sleep(secs)


# 时间戳转时间
def timeStamp(timeNum):
    timestamp = float(timeNum / 1000)
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# GMT格式转换时间
def gmt_trans(dd):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    time1 = datetime.strptime(dd, GMT_FORMAT)
    return time1

#新浪微博mid和url的互算
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

def url_to_mid(url):
    '''
    >>> url_to_mid('z0JH2lOMb')
    3501756485200075L
    >>> url_to_mid('z0Ijpwgk7')
    3501703397689247L
    >>> url_to_mid('z0IgABdSn')
    3501701648871479L
    >>> url_to_mid('z08AUBmUe')
    3500330408906190L
    >>> url_to_mid('z06qL6b28')
    3500247231472384L
    >>> url_to_mid('yCtxn8IXR')
    3491700092079471L
    >>> url_to_mid('yAt1n2xRa')
    3486913690606804L
    '''
    url = str(url)[::-1]
    size = len(url) // 4 if len(url) % 4 == 0 else len(url) // 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))

# B站bv号转av号
def bv2av(bv_url):
    bv_num = re.findall(r'.+BV(.+)?from.+', bv_url)
    BV = ''.join(bv_num)
    # 密码表0-57
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    pows = [6, 2, 4, 8, 5, 9, 3, 7, 1, 0]
    bv_sum = 0
    for i in range(0, min(10, len(BV))):  # 添加了对BV长度的检查
        for j in range(0, 58):
            if table[j] == BV[i]:
                # print(pows[k])
                res = j * math.pow(58, pows[i])
                bv_sum += int(res)
            else:
                continue
    bv_sum -= 100618342136696320
    temp = 177451812
    av = bv_sum ^ temp
    return av



class GetWeiboInfo:
    def __init__(self, publisher1,location1,fan_number1, transmit_count1, comment_count1, like_count1,
                 text2, weibo_tag, id1, sim1, url):
        self.data = []
        self.publisher = publisher1
        self.transmit_count = transmit_count1
        self.comment_count = comment_count1
        self.like_count = like_count1
        self.text = text2
        self.fan_number=fan_number1
        self.loc = location1
        self.wtag = weibo_tag
        self.id = id1
        self.sim = sim1
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36',
            'Cookie': 'SINAGLOBAL=2091729837087.3728.1661664246202; UOR=,,login.sina.com.cn; XSRF-TOKEN=9cy-hdaSldlPBhk8N9dPNo4v; SSOLoginState=1662793242; _s_tentry=weibo.com; Apache=9202328576743.148.1662793253762; ULV=1662793253807:10:5:2:9202328576743.148.1662793253762:1662278254307; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Lr7ToH0NN_3s3_hzAsuhz5JpX5KMhUgL.FoMfSoBX1K-pe0n2dJLoIEyuIg_ai--NiKnRi-zpi--fiKnpiKLWi--Xi-i2iKLhi--Xi-zRiKLW; ALF=1694415715; SCF=Amps_M75cltwDa7Bm_lemms_kl0xDiagRUKtvtZqGgW6WNxeESW5ES1ufOTvUm3f2LzojE5PPF1njc3WePGDlZc.; SUB=_2A25OGfezDeRhGeFL7VYV-SvNyDSIHXVtb257rDV8PUNbmtAKLRjFkW9NfcyWNj9SBew44xJfg6w0UX1HmqagYrAy; WBPSESS=5g_hz7cPq45HfXaHdb9Wl6SPRm-0FeswQvjkL6s4XgmDmjLb1CMnMJdsrhYvUOFL1XBz0L2zT3_MI2GMesFODxW8Z4CQwVBBllKHPf-VdLRtXhN44idYX_e61yXbyzyJsuwANVj2Yv70bVG8GS9tCA==',
            'Connection' : 'close'
        }

    def second_comment(self, temp, w2, root_id,follow_count1):
        if temp == 0:
            sub_comment = requests.get(
                f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={root_id}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={w2}&count=20',
                headers=self.headers)
        else:
            sub_comment = requests.get(
                f'https://weibo.com/ajax/statuses/buildComments?flow={temp}&is_reload=1&id={root_id}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={w2}&count=20',
                headers=self.headers)
        sub_comments = json.loads(sub_comment.text)
        sub_num = len(sub_comments['data'])
        for k in range(0, sub_num):
            tag = 1
            user_name = sub_comments['data'][k]['user']['screen_name']
            comment = sub_comments['data'][k]['text_raw']
            post_time = sub_comments['data'][k]['created_at']
            c_post_time = gmt_trans(post_time)
            like_count = sub_comments['data'][k]['like_counts']
            try:
                loc2 = sub_comments['data'][k]['user']['location']
                loc2 = loc2.split(" ")[0]
                #print(loc2)
            except IndexError:
                loc2=None

            self.data.append(
                [self.publisher,self.loc,self.fan_number, self.transmit_count, self.comment_count,  self.like_count,
                self.text, self.wtag,follow_count1,user_name,loc2,comment, c_post_time, like_count, self.sim, tag, self.url])
        sub_max_id = sub_comments['max_id']
        return sub_max_id
    
    def first_comment(self, w1):
        comment = requests.get(
            f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={self.id}&is_show_bulletin=2&is_mix=0&max_id={w1}&count=20',
            headers=self.headers)
        comment.encoding = 'utf-8-sig'
        # try:
        comments = json.loads(comment.text)
        # 一级评论个数
        num = len(comments['data'])
        if num != 0:
            for i in range(0, num):
                tag = 0
                user_name = comments['data'][i]['user']['screen_name']
                comment = comments['data'][i]['text_raw']
                post_time = comments['data'][i]['created_at']
                c_post_time = gmt_trans(post_time)
                like_count = comments['data'][i]['like_counts']
                follow_count=comments['data'][i]['user']['followers_count']
                try:
                    loc2=comments['data'][i]['user']['location']
                    loc2 = loc2.split(" ")[0]
                    #print(loc2)
                except IndexError:
                    loc2 = None

                self.data.append(
                    [self.publisher,self.loc,self.fan_number,self.transmit_count, self.comment_count,  self.like_count,
                    self.text, self.wtag, follow_count, user_name,loc2,comment, c_post_time, like_count, self.sim, tag, self.url])
                root_comment_id = comments['data'][i]['id']
                # 二级评论个数
                sub_num_real = comments['data'][i]['total_number']
                if sub_num_real:
                    sub_max_id = 0
                    temp = sub_max_id
                    w2 = 1
                    while w2 != 0:
                        if temp == 0:
                            w2 = GetWeiboInfo.second_comment(self, temp, sub_max_id, root_comment_id,follow_count)
                            temp += 1
                        else:
                            sub_max_id = w2
                            w2 = GetWeiboInfo.second_comment(self, temp, sub_max_id, root_comment_id,follow_count)
                else:
                    continue
            max_id = comments['max_id']
            if max_id == 0:
                max_id = 1
            return max_id
        else:
            max_id = 1
            return max_id


    def get_data(self):
        return self.data
    
    
    def weibo_craw(self):
        w = 0
        while w != 1:
            time.sleep(3)
            w = GetWeiboInfo.first_comment(self, w)
        print('爬虫完成')



lda_news = hub.Module(name="lda_news")


def weibo(url1, num1, key, driver):
    data = []  # 初始化一个空列表来存储数据
    if num1 != 2:
        try:
            driver.get(url1)
            driver.implicitly_wait(10)  # 10秒内找到元素就开始执行

            # 发布者       
            publisher = driver.find_element(By.XPATH, "//div[@class='woo-box-flex woo-box-alignCenter head_nick_1yix2']").text
            print(publisher)
            # 博客转发数量
            transmit = driver.find_element(By.XPATH,"//span[@class='toolbar_num_JXZul']").text
            res1 = re.findall(r'\d', transmit)
            transmit_count = ''.join(res1)
            if transmit_count == '':
                transmit_count = 0

            # 博客评论数
            comment = driver.find_element(By.XPATH,
                                          "//div[@class='woo-box-flex woo-box-alignCenter woo-box-justifyCenter toolbar_wrap_np6Ug toolbar_cur_JoD5A']/span[@class='toolbar_num_JXZul']").text
            res2 = re.findall(r'\d', comment)
            comment_count = ''.join(res2)
            if comment_count == '':
                comment_count = 0

            # 博客点赞数量
            like = driver.find_element(By.XPATH,
                                       "//span[@class='woo-like-count']").text
            res3 = re.findall(r'\d', like)
            like_count = ''.join(res3)
            if like_count == '':
                like_count = 0

            # text
            text2 = driver.find_element(By.XPATH, "//div[@class='detail_wbtext_4CRf9']").text
            t = re.findall('[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]',
                           text2)
            t = ''.join(t)

            # tag
            weibo_tag = []
            tags = driver.find_elements(By.XPATH, "//div[@class='detail_wbtext_4CRf9']/a")
            for tag in tags:
                weibo_tag.append(tag.text)
            weibo_tag = ''.join(weibo_tag)

            #帖子账号粉丝数
            fans = driver.find_element(By.XPATH, "//a[@class='ALink_none_1w6rm PopCard_alink_LHzuI PopCard_pointer_2u0ZP']").text # ------ 代查看-----
            text1 = ''.join(fans)
            if '万' in text1:
                num = re.findall(r'(.+?)万', text1)
                data1 = ''.join(num)
                if '.' in data1:
                    number = float(data1) * 10000
                else:
                    data1 = re.findall(r'\d+', text1)
                    data1 = ''.join(data1)
                    number = float(data1) * 10000
                fan_number = int(number)
            else:
                data = re.findall(r'\d+', text1)
                data1 = ''.join(data)
                if data1:  # 检查data1是否为空
                    fan_number = int(float(data1))
                else:
                    fan_number = 0  # 如果data1为空，设置fan_number为0或其他默认值

            #发布者ip地址
            try:
                location = driver.find_element(By.XPATH, "//div[@class='head-info_ip_3ywCW']").text
                loc = location.split(" ")[1]
                print(loc)
            except IndexError:
                loc=None

            if comment_count != 0:

                #计算主题相似度
                lda_sim = lda_news.cal_query_doc_similarity(query=key, document=t)
                print("主题相似度为：", lda_sim)

                video_id = driver.find_element(By.XPATH, "//a[@class='head-info_time_6sFQg']").get_attribute('href').split('/')[4]
                video_id = url_to_mid(video_id)
                getinfo = GetWeiboInfo(publisher,loc,fan_number, transmit_count, comment_count, like_count,
                                         t, weibo_tag, video_id,lda_sim, url1)
                getinfo.weibo_craw()
                data.extend(getinfo.get_data())  # 将数据添加到列表中

        except (Exception, BaseException) as e:
            print(e)
            num1 += 1
            data.extend(weibo(url1, num1, key, driver))  # 收集递归调用的数据
    else:
        return []

    return data  # 返回收集到的数据


def remove_duplicates(input_csv, output_csv):
    # 读取CSV文件
    df = pd.read_csv(input_csv)

    # 去除重复的行
    df = df.drop_duplicates()

    # 将结果保存到新的CSV文件中
    df.to_csv(output_csv, index=False)


def cleandata(data):
    print('---------------------------------------------------------------')
    print("根据主题相似度过滤信息开始")
    
    # 将空值替换为0
    data = data.fillna(0)
    
    sim = data['主题相似度']
    if len(sim) > 0:  # 检查sim序列是否为空
        Max = float(max(sim))
        Min = float(min(sim))

        for i in range(0, len(sim)):
            m = (float(sim[i]) - Min) / (Max - Min)
            if m <= 0.1:
                data = data.drop(i, axis=0)
    
    # 删除完全相同的行
    data = data.drop_duplicates()

    print("信息过滤完成")
    return data  # 返回清理后的数据



# remove_duplicates('2023台风tweets_by_region.csv','2023台风tweets_by_region.csv')
