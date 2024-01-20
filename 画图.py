import csv
import streamlit as st
import numpy as np
import pandas as pd
import re
from snownlp import SnowNLP
import datetime
import io

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


def calculate_score(text):
    text = ''.join(text.split())
    s = SnowNLP(text)
    score = s.sentiments
    # score = score * 2 - 1 
    return score

def calculate_score_and_average(file):
    file.seek(0)
    if 'xlsx' in file.name:
        data = pd.read_excel(io.BytesIO(file.read()))
    else:
        data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
    
    # 计算情绪得分的平均值
    total_score = 0
    text_list = data['评论内容'].tolist()
    for text in text_list:
        score = calculate_score(text)
        total_score += score
    average_score = total_score / len(text_list)
    return average_score


# def emotion_map(file_name,average_score):
#     path=get_middle_part(file_name)
#     if 'xlsx' in file_name:
#         data = pd.read_excel(path+"/"+file_name)
#     else:
#         data = pd.read_csv(path+"/"+file_name, encoding='utf-8', sep=';')
#     # print(path+"/"+file_name)

#     sim = data['IP属地']

#     for i in range(0, len(sim)):
#         if sim[i] == np.nan:
#             # 删除整行数据
#             data = data.drop(i, axis=0)  # 注意：drop() 方法不改变原有的 df 数据！

#     # location_p = data['发布者地理位置'].values
#     location_p = data['IP属地'].values
#     # location_c = data['一级地理位置'].values
#     location_c = data['评论属地'].values

#     for i in range(0, len(location_p)):
#         if isinstance(location_p[i], str) is not True:
#             location_p[i]=" "  # 跳过这个值
#         # print(location_p[i])
#         # print(type(location_p[i]))
#         if location_p[i] == np.nan:
#             continue

#         if 'IP' in location_p[i]:
#             location_p[i] = re.findall(r'IP属地：(\S+)', location_p[i])
#             location_p[i] = ''.join(location_p[i])
#         else:
#             location_p[i] = location_p[i][0:2]
#         if len(location_c[i]) >= 4:
#             location_c[i] = location_c[i][0:2]
#         else:
#             location_c[i] = location_c[i]
#     data.loc[len(data)] = data.columns
#     data1 = data.drop_duplicates(subset=['文本'], keep='last', inplace=False)
#     comment = data['评论内容']
#     tag = data['标记']
#     m = 0
#     len0 = 0
#     add_p = 0
#     add_c = 0
#     ave_sp = 0
#     loc_p = data1['IP属地'][0:len(data1) - 1].values
#     d = {}
#     for loc in loc_p:
#         d[loc] = 0
#     for j in range(0, len(comment)):
#         comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
#         s = SnowNLP(comment[j])
#         score = s.sentiments
#         if st.session_state.style=="标准情绪值":
#             score = (score)*2-1.5
#         if st.session_state.style=="相对情绪值":
#             score = (score-average_score)
#         if tag[j] == 0:  # 一级评论
#             #print(j,data1.index[m])
#             if j <= data1.index[m]:
#                 add_p += score
#                 len0 += 1
#             else:
#                 ave_sp = add_p / len0
#                 if d[loc_p[m]] != 0:
#                     ave_sp = (ave_sp + d[loc_p[m]]) / 2
#                     d[loc_p[m]] = ave_sp
#                 else:
#                     d[loc_p[m]] = ave_sp
#                 add_p = 0
#                 len0 = 1
#                 add_p += score
#                 m += 1
#         elif tag[j] == '标记':
#             ave_sp = add_p / len0
#             if d[loc_p[m]] != 0:
#                 ave_sp = (ave_sp + d[loc_p[m]]) / 2
#                 d[loc_p[m]] = ave_sp
#             else:
#                 d[loc_p[m]] = ave_sp

#     len1 = 0  # 计算二级评论个数
#     loc = ''
#     for j in range(0, len(comment)):
#         comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
#         s = SnowNLP(comment[j])
#         score = s.sentiments
#         if st.session_state.style=="标准情绪值":
#             score = (score)*2-1.5
#         if st.session_state.style=="相对情绪值":
#             score = (score-average_score)
#         if tag[j] == 0:
#             loc = location_c[j]
#             if location_c[j] not in loc_p:
#                 d.update({location_c[j]: 0})
#         elif tag[j] == 1:
#             add_c += score
#             len1 += 1
#             if tag[j + 1] != 1:
#                 if d[loc] != 0:
#                     ave_sp = (ave_sp + d[loc]) / 2
#                     d[loc] = ave_sp
#                 else:
#                     d[loc] = ave_sp
#                 len1 = 0
#                 add_c = 0

#     with open(path + '/map_result.txt', 'w', encoding='utf-8') as f:
#         for loc, score in d.items():
#             f.write(f'"{loc}": {score},\n')

#     return d


def emotion_map(file,average_score):
    file.seek(0)
    if 'xlsx' in file.name:
        data = pd.read_excel(io.BytesIO(file.read()))
    else:
        data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')

    sim = data['IP属地']

    for i in range(0, len(sim)):
        if sim[i] == np.nan:
            # 删除整行数据
            data = data.drop(i, axis=0)  # 注意：drop() 方法不改变原有的 df 数据！

    # location_p = data['发布者地理位置'].values
    location_p = data['IP属地'].values
    # location_c = data['一级地理位置'].values
    location_c = data['评论属地'].values

    for i in range(0, len(location_p)):
        if isinstance(location_p[i], str) is not True:
            location_p[i]=" "  # 跳过这个值
        # print(location_p[i])
        # print(type(location_p[i]))
        if location_p[i] == np.nan:
            continue

        if 'IP' in location_p[i]:
            location_p[i] = re.findall(r'IP属地：(\S+)', location_p[i])
            location_p[i] = ''.join(location_p[i])
        else:
            location_p[i] = location_p[i][0:2]
        if len(location_c[i]) >= 4:
            location_c[i] = location_c[i][0:2]
        else:
            location_c[i] = location_c[i]
    data.loc[len(data)] = data.columns
    data1 = data.drop_duplicates(subset=['文本'], keep='last', inplace=False)
    comment = data['评论内容']
    tag = data['标记']
    m = 0
    len0 = 0
    add_p = 0
    add_c = 0
    ave_sp = 0
    loc_p = data1['IP属地'][0:len(data1) - 1].values
    d = {}
    for loc in loc_p:
        d[loc] = 0
    for j in range(0, len(comment)):
        comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
        s = SnowNLP(comment[j])
        score = s.sentiments
        if st.session_state.style=="标准情绪值":
            score = (score)*2-1.5
        if st.session_state.style=="相对情绪值":
            score = (score-average_score)
        if tag[j] == 0:  # 一级评论
            #print(j,data1.index[m])
            if j <= data1.index[m]:
                add_p += score
                len0 += 1
            else:
                ave_sp = add_p / len0
                if d[loc_p[m]] != 0:
                    ave_sp = (ave_sp + d[loc_p[m]]) / 2
                    d[loc_p[m]] = ave_sp
                else:
                    d[loc_p[m]] = ave_sp
                add_p = 0
                len0 = 1
                add_p += score
                m += 1
        elif tag[j] == '标记':
            ave_sp = add_p / len0
            if d[loc_p[m]] != 0:
                ave_sp = (ave_sp + d[loc_p[m]]) / 2
                d[loc_p[m]] = ave_sp
            else:
                d[loc_p[m]] = ave_sp

    len1 = 0  # 计算二级评论个数
    loc = ''
    for j in range(0, len(comment)):
        comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
        s = SnowNLP(comment[j])
        score = s.sentiments
        if st.session_state.style=="标准情绪值":
            score = (score)*2-1.5
        if st.session_state.style=="相对情绪值":
            score = (score-average_score)
        if tag[j] == 0:
            loc = location_c[j]
            if location_c[j] not in loc_p:
                d.update({location_c[j]: 0})
        elif tag[j] == 1:
            add_c += score
            len1 += 1
            if tag[j + 1] != 1:
                if d[loc] != 0:
                    ave_sp = (ave_sp + d[loc]) / 2
                    d[loc] = ave_sp
                else:
                    d[loc] = ave_sp
                len1 = 0
                add_c = 0

    return d


def read_data(file):
    file.seek(0)  # Move the pointer back to the beginning of the file
    if 'xlsx' in file.name:
        data = pd.read_excel(io.BytesIO(file.read()))
    else:
        data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
    data.drop_duplicates(subset=['文本'], keep='last', inplace=True)
    title_p, emotion_p, url_p, title_n, emotion_n, url_n = [], [], [], [], [], []
    for index, row in data.iterrows():
        text = ''.join(row['文本'].split())
        s = SnowNLP(text)
        score = s.sentiments

        if st.session_state.style == "标准情绪值":
            score = score * 2 - 1.5
        if score >= 0:
            title_p.append(row['文本'])
            emotion_p.append(score)
            url_p.append(row['url'])
        else:
            title_n.append(row['文本'])
            emotion_n.append(score)
            url_n.append(row['url'])

    # 创建一个DataFrame来存储标题、情绪值和URL
    data_p = pd.DataFrame({
        'title': title_p,
        'emotion': emotion_p,
        'url': url_p
    })

    data_n = pd.DataFrame({
        'title': title_n,
        'emotion': emotion_n,
        'url': url_n
    })

    # 按照情绪值对DataFrame进行排序
    data_p = data_p.sort_values(by='emotion')
    data_n = data_n.sort_values(by='emotion')

    # 更新标题、情绪值和URL
    title_p = data_p['title'].tolist()
    emotion_p = data_p['emotion'].tolist()
    url_p = data_p['url'].tolist()
    title_n = data_n['title'].tolist()
    emotion_n = data_n['emotion'].tolist()
    url_n = data_n['url'].tolist()

    return title_p, emotion_p, url_p, title_n, emotion_n, url_n






def cluster_density(file_name):
    path=get_middle_part(file_name)
    data = pd.read_csv(path+'/宏观集群密度.csv', encoding='utf-8', sep=';')
    df = data.sort_values(by="集群密度", ascending=True)
    den = df['集群密度'].values
    title = df['文本'].values
    title_d = []
    density = []
    for i in range(0, len(title)):
        title_d.append(title[i])
        density.append(den[i])
        title_d[i] = title_d[i].replace('\n', '')
    return title_d, density


def change_date(times):
    time2 = []
    for time1 in times:
        time1 = str(time1)[:10]
        time2.append(time1)
    return time2


def emotion_tendency(file,average_score):
    file.seek(0)
    if 'xlsx' in file.name:
        data = pd.read_excel(io.BytesIO(file.read()))
    else:
        data = pd.read_csv(io.BytesIO(file.read()), encoding='utf-8', sep=';')
    data['评论时间'] = change_date(data['评论时间'].values)
    df = data.sort_values(by="评论时间", ascending=True)
    times1 = df['评论时间'].values
    comment = data['评论内容'].values
    d_p = {}
    d_z = {}
    d_n = {}
    vb = 0.1
    times = []
    for time1 in times1:
        # time1 = str(time1)[:10]
        times.append(time1)
        d_p[time1] = 0
        d_z[time1] = 0
        d_n[time1] = 0
    for j in range(0, len(comment)):
        comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
        s = SnowNLP(comment[j])
        score = s.sentiments
        if st.session_state.style=="标准情绪值":
            score = (score)*2-1.5
        if st.session_state.style=="相对情绪值":
            score = (score-average_score)
        if score > vb:
            d_p[times[j]] += 1
        elif vb > score > -vb:
            d_z[times[j]] += 1
        else:
            d_n[times[j]] += 1
            

    return d_p, d_z, d_n


def emotion_pie(file_name,average_score):
    if 'xlsx' in file_name:
        data = pd.read_excel(file_name)
    else:
        data = pd.read_csv(file_name, encoding='utf-8', sep=';')
    com_num = data['评论数'].values
    tran_num = data['转发数'].values
    like_num = data['点赞数'].values
    clike_num = data['评论点赞数'].values
    comment = data['评论内容'].values
    data1 = data.drop_duplicates(subset=['文本'], keep='last', inplace=False)
    title = data1['文本'].values
    p_p = {}
    p_p['评论'] = 0
    p_p['转发'] = 0
    p_p['点赞'] = 0
    p_n = {}
    p_n['评论'] = 0
    p_n['转发'] = 0
    p_n['点赞'] = 0
    for i in range(0, len(title)):
        title[i] = ''.join(title[i].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
        s = SnowNLP(title[i])
        score = s.sentiments
        if st.session_state.style=="标准情绪值":
            score = (score)*2-1.5
        if st.session_state.style=="相对情绪值":
            score = (score-average_score)
        if score > 0:
            p_p['评论'] += com_num[data1.index[i]]
            p_p['转发'] += tran_num[data1.index[i]]
            p_p['点赞'] += like_num[data1.index[i]]
        else:
            p_n['评论'] += com_num[data1.index[i]]
            p_n['转发'] += tran_num[data1.index[i]]
            p_n['点赞'] += like_num[data1.index[i]]
    for j in range(0, len(comment)):
        comment[j] = ''.join(comment[j].split())  # 去除待情绪分析语料中的空格，防止情绪分析失败
        s = SnowNLP(comment[j])
        score = s.sentiments
        if st.session_state.style=="标准情绪值":
            score = (score)*2-1.5
        if st.session_state.style=="相对情绪值":
            score = (score-average_score)
        if score > 0:
            p_p['评论'] += clike_num[j]
        else:
            p_n['点赞'] += clike_num[j]

    return p_p, p_n


def save_emotion(file_name):

    # 计算情绪得分
    def calculate_score(text):
        text = ''.join(text.split())
        s = SnowNLP(text)
        score = s.sentiments
        return score

    if 'xlsx' in file_name:
        data = pd.read_excel(file_name)
    else:
        data = pd.read_csv(file_name, encoding='utf-8', sep=';')
    
    # 计算情绪平均值
    scores = [calculate_score(text) for text in data['评论内容'].tolist()]
    average_score = sum(scores) / len(scores)


    data['情绪得分'] = data['评论内容'].apply(lambda x: calculate_score(x)*2-1)
    # 计算情绪得分与平均值的差值
    data['相对情绪得分'] = data['评论内容'].apply(lambda x: calculate_score(x) - average_score)
    
    # 保存新的csv文件
    new_file_name = file_name.split('.')[0] + '情绪值.csv'
    data.to_csv(new_file_name, index=False, sep=';')


def process_file(file_name):
    # 使用分号作为分隔符来读取CSV文件
    df = pd.read_csv(file_name, sep=';')

    # 数据预处理

    if '情绪得分' in df.columns: # 检查“情绪得分”字段的类型，并将其数值放大100倍
        if df['情绪得分'].dtype == 'float64' or df['情绪得分'].dtype == 'int64':
            df['情绪得分'] = df['情绪得分'] * 100 -50
        elif df['情绪得分'].dtype == 'object':
            df['情绪得分'] = df['情绪得分'].str.replace(',', '.').astype(float) * 100 -50

    if '相对情绪得分' in df.columns: # 检查“相对情绪得分”字段的类型，并将其数值放大100倍
        if df['相对情绪得分'].dtype == 'float64' or df['相对情绪得分'].dtype == 'int64':
            df['相对情绪得分'] = df['相对情绪得分'] * 100
        elif df['相对情绪得分'].dtype == 'object':
            df['相对情绪得分'] = df['相对情绪得分'].str.replace(',', '.').astype(float) * 100 
    
    new_file_name = file_name.split('.')[0] + '_可用于数据分析.csv'

    # 将处理后的数据写入新的CSV文件
    df.to_csv(new_file_name)


if __name__ == '__main__':
    # filename = input('请输入待处理的文件：')
    filename = "D:\电磁辐射网络舆情分析系统\code\微博疫情后的经济数据\clean-微博疫情后的经济数据.csv"
    new_file_name = filename.split('.')[0] + '情绪值.csv'
    save_emotion(filename)
    process_file(new_file_name)
    process_file(new_file_name)
