import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.mlab as mlab
from matplotlib.font_manager import FontProperties
import pymssql
import pandas as pd
import requests
import math

from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]

#连接数据库
def conn(ip_string,name_string,password_string,databasename_string):
    connect=pymssql.connect(ip_string,name_string,password_string,databasename_string)
    return connect

#连接数据库，输入sql语句
def input_sql(ip_string, name_string, password_string, databasename_string, sql):
    connect = conn(ip_string, name_string, password_string, databasename_string)
    cursor = connect.cursor();
    sql = sql
    cursor.execute(sql)
    des = cursor.description
    row = cursor.fetchall()
    title_list = [item[0] for item in des]
    title = tuple(title_list)
    row.insert(0, title)
    cursor.close()
    connect.close()
    return row

#画柱状-折线图
def bar_line_graph(bar_data, line_data, xaxis, bar_name, line_name,width,lenth,lablesize,xfontsize,y1fontsize,y2fontsize):
    a = bar_data  # 做柱状图的数据
    b = line_data  # 做折线图的数据
    l = [i for i in range(len(xaxis))]

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    fmt = '%.2f%%'
    yticks = mtick.FormatStrFormatter(fmt)  # 设置百分比形式的坐标轴
    lx = xaxis

    fig = plt.figure(figsize=(lenth, width))
    rect = fig.patch
    rect.set_facecolor('#ffffff')

    ax1 = fig.add_subplot(111,fc='#ffffff')
    plt.bar(l, a, alpha=0.3, color='blue', label=bar_name)
    ax1.legend(loc=2)
    ax1.set_ylim([math.floor(min(a)-100), math.ceil(max(a)+100)])  # 设置y轴取值范围
    ax1.set_ylabel(bar_name);
    for j,a in zip(l, a):  # 柱子上的数字显示
        plt.text(j, a, '%.2f' % a, ha='center', va='top', fontsize=10)
    plt.legend(prop={'family': 'SimHei', 'size': lablesize}, loc="upper left")

    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(l, b, 'or-', label=line_name);
    ax2.yaxis.set_major_formatter(yticks)
    # for i, (_x, _y) in enumerate(zip(l, b)): #b改成a 显示bar上的数值
    #     plt.text(_x, _y, b[i], color='black', fontsize=10, )  # 将数值显示在图形上
    ax2.legend(loc=1)
    ax2.set_ylim([math.floor(min(b)-10), math.ceil(max(b)+10)])  # 设置y轴取值范围
    ax2.set_ylabel(line_name);
    plt.legend(prop={'family': 'SimHei', 'size': lablesize}, loc="upper right")  # 设置中文

    plt.xticks(l, lx)

    ax1.tick_params(axis='x',labelsize=xfontsize)
    ax1.tick_params(axis='y', labelsize=y1fontsize)
    ax2.tick_params(axis='y', labelsize=y2fontsize)

    return plt

def pie_chart(title,name,value, lenth,width):
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.figure(figsize=(lenth, width))  # 将画布设定为正方形，则绘制的饼图是正圆
    label= name
    explode = [0.01for x in range(len(value))]  # 设定各项距离圆心n个半径
    values=value
    #plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')  # 绘制饼图
    plt.title(title)  # 绘制标题

    return plt

def line_line_chart(xaxis,y1axis,y2axis,y1lable,y2lable,xlable,ylable,lenth,width):
    plt.rcParams['font.family'] = 'SimHei'
    fig=plt.figure(figsize=(lenth, width))  # 将画布设定为正方形，则绘制的饼图是正圆
    rect = fig.patch
    rect.set_facecolor('#ffffff')
    x = xaxis
    y1 = y1axis
    y2 = y2axis
    y3 = y1.copy()
    y3.extend(y2)
    plt.plot(x, y1, 'p-', color='r', label=y1lable)
    plt.plot(x, y2, '*-', color='b', label=y2lable)
    plt.ylim(math.floor(min(y3)), math.ceil(max(y3)))
    plt.legend(loc="best")
    plt.xlabel(xlable)  # 横坐标名字
    plt.ylabel(ylable)  # 纵坐标名字
    return plt

def Ability_chart(Abilitykind,Abilitydata,title,lenth,width):
    fig = plt.figure(figsize=(lenth, width))
    labels = np.array(Abilitykind)
    # 数据个数
    dataLenth = len(labels)
    # 数据
    data = np.array(Abilitydata)
    angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    labels = np.concatenate((labels, [labels[0]]))
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, data, 'ro-', linewidth=2)
    ax.set_thetagrids(angles * 180 / np.pi, labels,fontproperties="SimHei")
    ax.set_title(title, va='bottom', fontproperties="SimHei")
    ax.fill(angles, data, alpha=0.25)
    ax.grid(True)
    return plt

def double_ability_graph(Abilitykind,Abilitydata1,Abilitydata2,title,label1,label2,lenth,width):
    fig = plt.figure(figsize=(lenth, width))
    # 用于正常显示中文
    plt.rcParams['font.sans-serif'] = 'SimHei'
    # 用于正常显示符号
    plt.rcParams['axes.unicode_minus'] = False
    # 使用ggplot的绘图风格，这个类似于美化了，可以通过plt.style.available查看可选值，你会发现其它的风格真的丑。。。
    plt.style.use('ggplot')
    # 构造数据
    values = Abilitydata1
    feature = Abilitykind
    # 设置每个数据点的显示位置，在雷达图上用角度表示
    angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False)
    # 拼接数据首尾，使图形中线条封闭
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    feature = np.concatenate((feature, [feature[0]]))
    # 绘图
    fig = plt.figure()
    # 设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'o-', linewidth=2)
    # 填充颜色
    ax.fill(angles, values, alpha=0.25)
    # 设置图标上的角度划分刻度，为每个数据点处添加标签
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    values_2 = Abilitydata2
    values_2 = np.concatenate([values_2, [values_2[0]]])
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2, label=label1)
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, values_2, 'o-', linewidth=2, label=label2)
    ax.fill(angles, values_2, alpha=0.25)
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    y1 = Abilitydata1.copy()
    y2 = Abilitydata2.copy()
    y3 = y1.copy()
    y3.extend(y2)
    ax.set_ylim(math.floor(min(y3)), math.ceil(max(y3)))
    plt.title(title)
    plt.legend(loc='best')
    ax.grid(True)
    return plt

def non_axix_bar_graph(x,y,xlabel,lenth,width):
    X=x
    Y=y
    fig, ax = plt.subplots(figsize=(lenth, width))
    plt.bar(X, Y, 0.4, color="green")
    plt.xlabel(xlabel)
    #plt.title("bar chart")
    frame = plt.gca()
    # y 轴不可见
    frame.axes.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return plt

