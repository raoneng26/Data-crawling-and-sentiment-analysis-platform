import streamlit as st
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker
import streamlit_echarts
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from streamlit.components.v1 import html
import main
import 画图
import numpy as np



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


# uploaded_file = st.file_uploader("Upload your data here")
# if uploaded_file is not None:
#     st.success('upload success!')
#     main.emotion_analysis(uploaded_file.name)
# else:
#     st.error('upload failed!')
# side_bar = st.sidebar.radio(
#     '数据情感分析结果：',
#     ['群体情绪排行榜', '群体情绪中国地图', '集群密度排行', '点赞评论转发占比图', '群体情绪趋势图']
# )

def analysis(side_bar,uploaded_file):
    
    st.session_state.average_score= 画图.calculate_score_and_average(uploaded_file)
    

    if side_bar == '群体情绪排行榜':
        title_P, emotion_P, url_P, title_N, emotion_N, url_N = 画图.read_data(uploaded_file)
        title_P, emotion_P, url_P = title_P[-10:], emotion_P[-10:], url_P[-10:]  # 只选择前10个正面情绪
        title_N, emotion_N, url_N = title_N[:10], emotion_N[:10], url_N[:10]  # 只选择前10个负面情绪
        st.session_state.title_N=title_N
        st.session_state.title_P=title_P
        st.session_state.name=None

        if st.session_state.p2=="正面":
           
            option = {
                'grid': {'top': 10, 'left': 300, 'right': 10, 'bottom': 50},
                'tooltip': {'trigger': 'axis', 'confine': 'true'},
                'yAxis': {'triggerEvent': 'true', 'data': title_P},
                'xAxis': {},
                'series': [{
                    'name': '群体正向情绪',
                    'type': 'bar',
                    'data': [{'value' : i, "url" : url} for i, url in zip(list(emotion_P), url_P)],
                    'itemStyle': {'normal': {'label': {'show': 'true', 'position': 'right', 'textStyle': {'color': 'black'}}}}
                }]
            }

            events1 = {
                "click": "function(params) { window.open(params.data.url, '_blank'); console.log(params.name); return params.name }",
                "dblclick":"function(params) { return [params.type, params.name, params.value] }"
            }

            value1 = st_echarts(options=option, height='450px', width='650px', events=events1)
            
            if value1:
                st.session_state.name=value1

        if st.session_state.p2=="负面":
            option = {'grid': {'top': 48, 'left': 300, 'right': 15, 'bottom': 50},
                      'tooltip': {'trigger': 'axis', 'confine': 'true'},
                      'yAxis': {'triggerEvent': 'true', 'data': title_N, 'inverse': 'true'},
                      'xAxis': {'inverse': 'true'},
                      'series': [{'name': '群体负向情绪', 'type': 'bar', 
                                  'data': [{'value' : i, "url" : url} for i, url in zip(list(emotion_N), url_N)],
                                'itemStyle': {'normal':{'label': {'show': 'true','position': 'right','textStyle': {'color': 'black'}}}}
                }]
            }
            events2 = {
                "click": "function(params) { window.open(params.data.url, '_blank'); console.log(params.name); return params.name }",
                "dblclick":"function(params) { return [params.type, params.name, params.value] }"
            }

            value2=st_echarts(options=option, height='450px', width='650px',events=events2)
            if value2:
                st.session_state.name=value2


    if side_bar == '群体情绪世界地图':
        dic = 画图.emotion_map(uploaded_file, st.session_state.average_score)
        dic1 = normalize_location_names(dic)

        c = Map(init_opts=opts.InitOpts(bg_color='#DCDCDC'))
        c.add('群体情绪地图', [list(z) for z in zip(dic.keys(), dic.values())], maptype="world")
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        c.set_global_opts(title_opts=opts.TitleOpts(title='World'),
                        visualmap_opts=opts.VisualMapOpts(max_=1, min_=-1,
                                                            range_color=['#B40404', '#FFFFFF',
                                                                        '#31B404']))
        text = c.render_embed()
        html(text, height=500, width=800)


    if side_bar == '群体情绪中国地图':
        dic = 画图.emotion_map(uploaded_file, st.session_state.average_score)
        dic1 = normalize_location_names(dic)

        c = Map(init_opts=opts.InitOpts(bg_color='#DCDCDC'))
        c.add('群体情绪地图', [list(z) for z in zip(dic1.keys(), dic1.values())], maptype="china")
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        c.set_global_opts(title_opts=opts.TitleOpts(title='中国'),
                        visualmap_opts=opts.VisualMapOpts(max_=1, min_=-1,
                                                            range_color=['#B40404', '#FFFFFF',
                                                                        '#31B404']))
        text = c.render_embed()
        # html(text, height=600, width=640)
        html(text, height=500, width=800)


    if side_bar=="群体情绪强度饼图":
        dic = 画图.emotion_map(uploaded_file, st.session_state.average_score)
        dic1 = normalize_location_names(dic)


        dic1_non_zero = {}
        for k, v in dic1.items():
            if v != 0:
                dic1_non_zero[k] = v
        dic1_positive = {}
        dic1_negative = {}
        for k, v in dic1_non_zero.items():
            if v >= 0:
                dic1_positive[k] = v
            else:
                dic1_negative[k] = v
        if st.session_state.p=="正面":
            options_p = {
                "title": {"text": "各地区正面情绪强度饼图", "subtext": "未显示情绪值为零的地区", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left",},
                "series": [
                    {
                        "name": "地区",
                        "type": "pie",
                        "radius": "50%",
                        "data": [{"value": v, "name": k} for k, v in dic1_positive.items()],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }            
            st_echarts(
                    options=options_p, height="600px",)
        if st.session_state.p=="负面":
            options_n = {
                "title": {"text": "各地区负面情绪强度饼图", "subtext": "未显示情绪值为零的地区", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left",},
                "series": [
                    {
                        "name": "地区",
                        "type": "pie",
                        "radius": "50%",
                        "data": [{"value": v, "name": k} for k, v in dic1_negative.items()],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }
            st_echarts(
                    options=options_n, height="600px",)


    if side_bar == '集群密度排行':
        title_D, density = 画图.cluster_density(uploaded_file.name)
        c1, c2 = st.columns([1, 0.3])
        with c1:
            st.write('集群密度排行榜')
        with c2:
            st.empty()
        option = {'grid': {'top': 48, 'left': 300, 'right': 10, 'bottom': 50},
                  'tooltip': {'trigger': 'axis', 'confine': 'true'},
                  'yAxis': {'triggerEvent': 'true', 'data': title_D,
                            'axisLabel': {'show': 'true'}},
                  'xAxis': {},
                  'series': [{'name': '集群密度', 'type': 'bar', 'data': density,
                              'itemStyle': {'normal': {'label': {'show': 'true', 'position': 'right',
                                                                 'textStyle': {'color': 'black'}}}}}]}

        st_echarts(options=option, height='700px', width='700px')
        with st.expander('展开显示全部标题'):
            ld = len(title_D)
            for i in range(0, ld):
                st.write(str(i) + ': ' + title_D[ld - i - 1])
                

    if side_bar == '点赞评论转发占比图':
        p_p, p_n = 画图.emotion_pie(uploaded_file.name,st.session_state.average_score)
        b1, b2, b3 = st.columns([1, 0.3, 0.3])
        with b1:
            st.empty()
        with b2:
            pp = st.button('正面')
        with b3:
            pn = st.button('负面')
        if pp:
            option1 = {'title': {'text': '正面情绪点赞评论转发占比图', 'x': 'center'},
                       'tooltip': {'trigger': 'item', 'formatter': "{a} <br/>{b} : {c} ({d}%)"},
                       'legend': {'orient': 'vertical', 'left': 'left', 'data': ['评论', '转发', '点赞']},
                       'series': [{'name': '访问来源', 'type': 'pie', 'radius': '55%',
                                   'label': {'show': 'true', 'formatter': '{b} : {c} ({d}%)'},
                                   'labelLine': {'show': 'true'},
                                   'data': [{'value': int(p_p["评论"]), 'name': '评论'},
                                            {'value': int(p_p["转发"]), 'name': '转发'},
                                            {'value': int(p_p["点赞"]), 'name': '点赞'}]}]}
            st_echarts(options=option1, height='500px')
        if pn:
            option2 = {'title': {'text': '负面情绪点赞评论转发占比图', 'x': 'center'},
                       'tooltip': {'trigger': 'item', 'formatter': "{a} <br/>{b} : {c} ({d}%)"},
                       'legend': {'orient': 'vertical', 'left': 'left', 'data': ['评论', '转发', '点赞']},
                       'series': [{'name': '访问来源', 'type': 'pie', 'radius': '55%',
                                   'label': {'show': 'true', 'formatter': '{b} : {c} ({d}%)'},
                                   'labelLine': {'show': 'true'},
                                   'data': [{'value': int(p_n["评论"]), 'name': '评论'},
                                            {'value': int(p_n["转发"]), 'name': '转发'},
                                            {'value': int(p_n["点赞"]), 'name': '点赞'}]}]}
            st_echarts(options=option2, height='500px')


    if side_bar == '群体情绪趋势图':
        dp, dz, dn = 画图.emotion_tendency(uploaded_file,st.session_state.average_score)
        if st.session_state.post_url is None:
            st.session_state.post_url = {k: "#" for k in dp.keys()}
        option = {
            'title': {'text': '群体情绪趋势图'},
            'legend': {'data': ['正面', '中性', '负面']},
            'xAxis': {'type': 'category', 'data': [list(z) for z in zip(dp.keys())], 'axisLabel': {'interval': 0}},
            'yAxis': {'type': 'value'},
            'tooltip': {               
                'show': 'true',
                'trigger': 'axis',
                'formatter': '''<div><img src='https://i.imgur.com/ocrN2uf.jpg' style='width: 180px; height: 150px;'/> 
                <br/> <span style='color: #57caf4;'>●</span> 正面: <span style='color: #333; font-weight: bold;'>  {c0}
                </span><br/><span style='color: #76c900;'>●</span> 中性: <span style='color: #333; font-weight: bold;'>  {c1}
                </span><br/><span style='color: #f1c40f;'>●</span> 负面: <span style='color: #333; font-weight: bold;'>  {c2}</span></div>'''
            },
            'dataZoom': {
                'type': 'slider', 
                'xAxisIndex': [0], 
                'show': 'true', 
                'height': 20, 
                'bottom': 0,
                'zoomLock': 'true', 
                'minValueSpan': 0, 
                'maxValueSpan': 7, 
                'realtime': 'true',
                'showDetail': 'false', 
                'filterMode': 'empty'
            },
            # 指定图标的类型
            'series': [
                {'name': '正面', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dp.values()), st.session_state.post_url.values())]
                },
                {'name': '中性', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dz.values()), st.session_state.post_url.values())]
                },
                {'name': '负面', 
                "type": "line", 
                "itemStyle": {
                    "normal": {
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": "{c}"
                        }
                    }
                },
                "data": [{'value' : i, "url" : url} for i, url in zip(list(dn.values()), st.session_state.post_url.values())]
                }
            ]
        }

        events = {
            "click": """function(params) { window.open(params.data.url, '_blank'); }"""
        }

        st.session_state.data = st_echarts(options=option, height='500px', width='1050px', events=events)


    if side_bar == '单视频情绪极性':
            emotion_list = []
            with open(uploaded_file,  'r') as f:  ##更改点
                for line in f.readlines():
                    line = line.strip('\n')
                    emotion_list.append(line)
            print(emotion_list)
            emotion_key = ['生气', '反感', '害怕', '高兴', '悲伤', '惊讶']  # mosei
            emotion_colors = ['#FF7F7F', '#7FFF7F', '#7F7FFF', '#FFFF7F', '#7FFFFF', '#FF7FFF']  # 为每种情绪设置一种颜色
            emotion_data = [{'value': emotion_list[i], 'itemStyle': {'color': emotion_colors[i]}} for i in range(len(emotion_list))]
            # 显示视频情绪极性
            max_emotion = emotion_key[np.argmax(emotion_list)]
            negative = ['生气', '反感', '害怕', '悲伤']
            positive = ['高兴', '惊讶']
            if max_emotion in positive:
                st.success('该视频情绪是积极的')  ##显示语言
            if max_emotion in negative:
                st.error('该视频情绪是消极的')  # 显示语言
            option = {
                'grid': {'top': 10, 'left': 50, 'right': 50, 'bottom': 50},
                'tooltip': {'trigger': 'axis', 'confine': 'true'},
                'yAxis': {'triggerEvent': 'true', 'data': emotion_key},
                'xAxis': {},
                'series': [{
                    'name': 'emotion',
                    'type': 'bar',
                    'data': emotion_data,
                    'itemStyle': {
                        'normal': {
                            'label': {
                                'show': 'true',
                                'position': 'right',
                                'textStyle': {'color': 'black'}
                            }
                        }
                    }
                }]
            }

            st_echarts(options=option, height='400px', width='300px')
    
    
    if side_bar == '单视频模态细粒度':
        data = pd.read_csv(uploaded_file,encoding='utf-8', sep=';') 
        option = {  # 提示框，鼠标悬浮交互时的信息提示
            # 'title': {'text': ' 单模态分析结果'},
            'tooltip': {'show': 'true',  # 是否显示
                        'trigger': 'axis',  # 触发类型，默认数据触发，见下图，可选为：'item' | 'axis'
                        'axisPointer': {
                            'type': 'shadow'
                        }
                        },
            'legend': {},
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': 'true'
            },
            'xAxis': {
                'type': 'value'
            },
            'yAxis': {
                'type': 'category',
                'data': [' 文本（负相关）', '视频', '音频']
            },
            'series': [
                {
                    'name': '生气',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['angry'][i]) for i in range(3)]
                },
                {
                    'name': '反感',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['disgusted'][i]) for i in range(3)]
                },
                {
                    'name': '害怕',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['fear'][i]) for i in range(3)]
                },
                {
                    'name': '高兴',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['happy'][i]) for i in range(3)]
                },
                {
                    'name': '悲伤',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['sad'][i]) for i in range(3)]
                },
                {
                    'name': '惊讶',
                    'type': 'bar',
                    'stack': 'total',
                    'label': {
                        'show': 'true'
                    },
                    'emphasis': {
                        'focus': 'series'
                    },
                    'data': [float(data['surprise'][i]) for i in range(3)]
                }

            ]
        }
        st_echarts(options=option, height='400px')
   