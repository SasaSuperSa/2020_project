# -*- coding: utf-8 -*-
# 导入库的作用

# 绘制柱形图
import matplotlib.pyplot as plt
# 规范网页内容用的
from lxml import etree
# 用于延迟
import time
# 模拟浏览器发送网络请求
import requests

# 模拟浏览器发送的请求 不让服务器发现我们是爬虫
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '\
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

# ---------------------函数------------------------------------------------

# 处理获取到的数据-6℃～5℃，提取出-6 和 5 -6℃～3℃ 分割成一个列表 [-6,3]
def solveData(tdData):
    # 将tdData通过'～'分割成两个数据，并提取第二个数据
    highData = tdData.split('～')[1]
    # 去除℃
    highData = highData.replace('℃', '')
    # 将数据变成整数类型
    highData = int(highData)
    # 把数据存进resultHighValue列表
    resultHighValue.append(highData)

    # 将tdData通过'～'分割成两个数据，并提取第一个数据
    lowData = tdData.split('～')[0]
    # 去除℃
    lowData = lowData.replace('℃', '')
    # 将数据变成整数类型
    lowData = int(lowData)
    # 把数据存进resultLowValue列表
    resultLowValue.append(lowData)

# 用于展示图中显示正数的函数
def autolabel1(rects):
    for rect in rects:
        # 定义长度
        width = rect.get_width()
        # 定义高度
        heigth = rect.get_y() + 0.25
        plt.text(width, heigth, width)

# 用于展示图中显示负数的函数
def autolabel2(rects):
    for rect in rects:
        # 定义长度
        width = rect.get_width()
        width = width-1

        # 定义高度
        heigth = rect.get_y() + 0.25

        plt.text(width, heigth, width)

# 用于展示图的函数
def solvePng(resultKey,resultLowValue,resultHighValue):
    #  展示图显示中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 绘制柱形图
    bart1 = plt.barh(range(len(resultHighValue)), resultHighValue, tick_label=resultKey)
    autolabel1(bart1)
    bart2 = plt.barh(range(len(resultLowValue)), resultLowValue, tick_label=resultKey)
    autolabel2(bart2)

    # 展示图x轴标题
    plt.xlabel('温度')
    # 展示图y轴标题
    plt.ylabel('地区')

    # 展示图标题
    plt.title('辽宁今天天气')
    # 展示图保存的文件名
    plt.savefig('辽宁天气.png')

# ---------------------------------------------------------------

# --------------------------数据---------------------------------

# 地区字典 网址所需要用到的参数
areas = {
    'AnShan':'鞍山',
    'baita':'白塔',
    'BeiPiao':'北票',
    'BeiZhen':'北镇',
    'BenXi':'本溪',
    'BenXiXian':'本溪县',
    'ChangHai':'长海',
    'ChangTu':'昌图',
    'ChaoYang':'朝阳',
    'dadong':'大东',
    'DaLian':'大连',
    'DanDong':'丹东',
    'dashiqiao':'大石桥',
    'DaWa':'大洼',
    'DengTa':'灯塔',
    'Diaobingshan':'调兵山',
    'Donggang':'东港',
    'dongzhou':'东洲',
}


# 结果的纵坐标值
resultKey = []
# 结果的高温度列表
resultHighValue = []
# 结果的低温度列表
resultLowValue = []

# -----------------------------------------------------------


# ----------------------主程序-----------------------------
print('------------开始爬取-----------------------')

# 循环地区列表
for area in areas:
    print('爬取'+areas[area]+'温度')

    # 模拟浏览器发送请求
    html = requests.get('https://qq.ip138.com/weather/liaoning/'+area+'.htm', headers=headers)
    # 能够显示中文编码 默认很多网页编码是gbk
    html.encoding = 'utf-8'

    # 将爬取到的网页数据 转换为一个etree对象
    htmlText = etree.HTML(html.text)
    # 找出tr数据中所有包括td标签的数据，获取第一个的文本数据
    tdData = htmlText.xpath('//table//tr//td[2]/text()')[0]
    print(tdData)

    # 传入solveData用于处理数据
    solveData(tdData)
    # 将该地区的名字保存进resultKey列表
    resultKey.append(areas[area])

    time.sleep(1)
print('------------结束爬取-----------------------')

print('------------正在出图-----------------------')
# solvePng处理获取到的数据 绘制图片
solvePng(resultKey,resultLowValue,resultHighValue)
print('-----出图完毕，名字为辽宁天气.png----------')