import logging
from decimal import Decimal
import numpy as np
from flask import Flask, request, redirect, render_template, url_for
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.mlab as mlab

import draw

from pylab import mpl
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

month='12'
company='000002'

sql='SELECT Top 5 CONVERT(NVARCHAR, [日期]),[融资余额（亿）],[融券余额（亿）] FROM tb_mdd ORDER BY [日期]'
sql1='''select * from (select Top 5 a.secuabbr,EndDate,year(enddate) nf,month(enddate) yf,convert(char(10),enddate,102)bgq, OperatingReenue/10000.00 yysr,
(select top 1 OperatingReenue/10000.00 from LC_MainDataNew where companycode=b.companycode and enddate=dateadd(yy, -1, b.enddate) and mark in (1,2,6,7,8) order by InfoPublDate desc,CASE Mark
WHEN 1 THEN 1 WHEN 8 THEN 2 WHEN 7 THEN 3 WHEN 6 THEN 4 WHEN  2 THEN 5 END ASC ) yysr1
from xxb_secumain2 a,lc_maindatanew b
where a.companycode=b.companycode
and b.id=(select top 1 id  from lc_maindatanew where companycode=a.companycode  and enddate=b.enddate and mark in (1,2,6,7,8) order by InfoPublDate desc,CASE Mark
WHEN 1 THEN 1 WHEN 8 THEN 2 WHEN 7 THEN 3 WHEN 6 THEN 4 WHEN  2 THEN 5 END ASC)
and month(enddate)='''+'''\''''+month+'''\''''+'''
and secucode='''+'''\''''+company+'''\''''+''' order by enddate  desc) a order by enddate'''

sql2=''

#画图
# 第一张图
img = io.BytesIO()

data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)

a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列
realrate=[]
yysy=[]

for i in range(1, len(data_tuple_list)):
    a_input.append(data_tuple_list[i][2])
    b_input.append(data_tuple_list[i][5])
    c_input.append(data_tuple_list[i][6])

rate=((np.array(b_input)-np.array(c_input))/map(abs,np.array(c_input)))
for i in range(0,len(rate)):
    realrate.append(float(rate[i]))
    yysy.append(float(b_input[i]/10000))
realrate=np.round(realrate,decimals=2)
yysy=np.around(yysy,decimals=2)


a_name = data_tuple_list[0][2]  # 第一列表头
b_name = data_tuple_list[0][5]  # 第二列表头
c_name = data_tuple_list[0][6]  # 第三列表头

data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)
#print(realrate)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()

#第二张图

data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)

a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列

for i in range(1, len(data_tuple_list) - 1):
    a_input.append(data_tuple_list[i][0])
    b_input.append(data_tuple_list[i][1])
    c_input.append(data_tuple_list[i][2])

a_name = data_tuple_list[0][0]  # 第一列表头
b_name = data_tuple_list[0][1]  # 第二列表头
c_name = data_tuple_list[0][2]  # 第三列表头


plt = draw.pie_chart('按产品',a_input,b_input,5.8,4.9)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url2 = base64.b64encode(img.getvalue()).decode()

#第三张图

data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)

a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列

for i in range(1, len(data_tuple_list) - 1):
    a_input.append(data_tuple_list[i][0])
    b_input.append(data_tuple_list[i][1])
    c_input.append(data_tuple_list[i][2])

a_name = data_tuple_list[0][0]  # 第一列表头
b_name = data_tuple_list[0][1]  # 第二列表头
c_name = data_tuple_list[0][2]  # 第三列表头


plt = draw.pie_chart('按地区',a_input,b_input,5.8,4.9)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url3 = base64.b64encode(img.getvalue()).decode()


# 第一张图
img = io.BytesIO()

data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)

a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列
realrate=[]
yysy=[]

for i in range(1, len(data_tuple_list)):
    a_input.append(data_tuple_list[i][2])
    b_input.append(data_tuple_list[i][5])
    c_input.append(data_tuple_list[i][6])

rate=((np.array(b_input)-np.array(c_input))/np.array(c_input)*100)
for i in range(0,len(rate)):
    realrate.append(float(rate[i]))
    yysy.append(float(b_input[i]/10000))
realrate=np.round(realrate,decimals=2)
yysy=np.around(yysy,decimals=2)


a_name = data_tuple_list[0][2]  # 第一列表头
b_name = data_tuple_list[0][5]  # 第二列表头
c_name = data_tuple_list[0][6]  # 第三列表头

plt = draw.bar_line_graph(yysy, realrate, a_input, '营业收入(亿元)', '同比增率(%)', 5, 9, 8, 9, 9, 9)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url4 = base64.b64encode(img.getvalue()).decode()

#第五张图
data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)


a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列

for i in range(1, len(data_tuple_list) - 1):
    a_input.append(data_tuple_list[i][0])
    b_input.append(data_tuple_list[i][1])
    c_input.append(data_tuple_list[i][2])

a_name = data_tuple_list[0][0]  # 第一列表头
b_name = data_tuple_list[0][1]  # 第二列表头
c_name = data_tuple_list[0][2]  # 第三列表头

plt = draw.line_line_chart(a_input,b_input,c_input,b_name,c_name,a_name,'data',10,5)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url5 = base64.b64encode(img.getvalue()).decode()


#第六张图
data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)


a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列

for i in range(1, len(data_tuple_list) - 1):
    a_input.append(data_tuple_list[i][0])
    b_input.append(data_tuple_list[i][1])
    c_input.append(data_tuple_list[i][2])

a_name = data_tuple_list[0][0]  # 第一列表头
b_name = data_tuple_list[0][1]  # 第二列表头
c_name = data_tuple_list[0][2]  # 第三列表头

plt = draw.Ability_chart(a_input,b_input,'Ability graph',5.8,4.9)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url6 = base64.b64encode(img.getvalue()).decode()

#第七张图
data_tuple_list = draw.input_sql('XXXXXXXX', 'XXXXX', 'XXXXXXXX', 'XXXXXX', sql1)


a_input = []  # 存第0列
b_input = []  # 存第1列
c_input = []  # 存第二列

for i in range(1, len(data_tuple_list) - 1):
    a_input.append(data_tuple_list[i][0])
    b_input.append(data_tuple_list[i][1])
    c_input.append(data_tuple_list[i][2])

a_name = data_tuple_list[0][0]  # 第一列表头
b_name = data_tuple_list[0][1]  # 第二列表头
c_name = data_tuple_list[0][2]  # 第三列表头

#print(b_input)
#print(c_input)
c_input=list(map(lambda x:x+14000,c_input))
# print(c_input)

plt = draw.double_ability_graph(a_input, b_input, c_input, 'Double Ability Graph', b_name, c_name, 5.8, 4.9)

plt.savefig(img, format='png',dpi=300)
img.seek(0)
plot_url7 = base64.b64encode(img.getvalue()).decode()

#放入网址
app = Flask(__name__)

@app.route('/')
def build_plot():

    return render_template('testbase.html', plot_url=plot_url, plot_url2=plot_url2, plot_url3=plot_url3, plot_url4=plot_url4, plot_url5=plot_url5, plot_url6=plot_url6,
                           plot_url7=plot_url7)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
