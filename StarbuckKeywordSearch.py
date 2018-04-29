#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import * # 导入 Tkinter 库
import ttk
from FileDialog import *
from tkColorChooser import *
from tkMessageBox import *
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt 
import math
import webbrowser
import json
import datetime
import time
    
posi=pd.read_csv("D:\\directory.csv")
lat = np.array(posi["Latitude"][0:25601])   # 获取维度之维度值
lon = np.array(posi["Longitude"][0:25601])   # 获取经度值
storename = np.array(posi['Store Name'][0:25601])
ownertype = np.array(posi['Ownership Type'][0:25601])
streetaddress = np.array(posi['Street Address'][0:25601])
city = np.array(posi['City'][0:25601])
state = np.array(posi['State/Province'][0:25601])
country = np.array(posi['Country'][0:25601])
postcode = np.array(posi['Postcode'][0:25601])
phonenumber = np.array(posi['Phone Number'][0:25601])

info = []
starbucks = []
for i in range(len(lat)):
    infostr = str(storename[i]) + '  ' + str(ownertype[i]) + '  '\
              + str(country[i]) + ' '+ str(state[i]) + ' ' + str(city[i])\
              + ' ' + str(streetaddress[i])+ '  ' + str(phonenumber[i])
              
    info.append(infostr)
    starbuck = []
    starbuck.append(lon[i])
    starbuck.append(lat[i])
    starbuck.append(infostr)
    starbucks.append(starbuck)
#starbucks = zip(lon,lat,info) #中文字符串的转换有问题

def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000 

#统计关键词及个数 并计算相似度  
def MergeKeys(dic1,dic2):  
    #合并关键词 采用三个数组实现  
    arrayKey = []  
    for i in range(len(dic1)):  
        arrayKey.append(dic1[i][0])       #向数组中添加元素  
    for i in range(len(dic2)):         
        if dic2[i][0] in arrayKey:  
            pass  
        else:                             #合并  
            arrayKey.append(dic2[i][0])       
                
    #计算词频 infobox可忽略TF-IDF  
    arrayNum1 = [0]*len(arrayKey)  
    arrayNum2 = [0]*len(arrayKey)  
      
    #赋值arrayNum1  
    for i in range(len(dic1)):       
        key = dic1[i][0]  
        value = dic1[i][1]  
        j = 0  
        while j < len(arrayKey):  
            if key == arrayKey[j]:  
                arrayNum1[j] = value  
                break  
            else:  
                j = j + 1  
  
    #赋值arrayNum2  
    for i in range(len(dic2)):       
        key = dic2[i][0]  
        value = dic2[i][1]  
        j = 0  
        while j < len(arrayKey):  
            if key == arrayKey[j]:  
                arrayNum2[j] = value  
                break  
            else:  
                j = j + 1             
  
    #计算两个向量的点积  
    x = 0  
    i = 0  
    while i < len(arrayKey):  
        x = x + arrayNum1[i] * arrayNum2[i]  
        i = i + 1      
  
    #计算两个向量的模  
    i = 0  
    sq1 = 0  
    while i < len(arrayKey):  
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]   #pow(a,2)  
        i = i + 1       
      
    i = 0  
    sq2 = 0  
    while i < len(arrayKey):  
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]  
        i = i + 1     
      
    result = float(x) / ( math.sqrt(sq1) * math.sqrt(sq2) )  
    return result
                
#快速选取法        
def partition(seq):
    pi, seq = seq[0], seq[1:]                 # 选取并移除主元
    lo = []
    hi = []
    for x in seq:
        if x[0] > pi[0] or (x[0] == pi[0] and x[1] <= pi[1]):
            lo.append(x)
        else:
            hi.append(x)
    return lo, pi, hi


def select(seq, k):    
    lo, pi, hi = partition(seq)
    m = len(lo)
    if m == k: return lo
    if m < k:
        lo.append(pi)
        return lo+select(hi, k-m-1)
    return select(lo, k)   
        
root = Tk()
root.title('hello Tkinter')

root.geometry('600x400') 

#创建列表框
lb = Listbox(root,width = 80,height = 13)
sl = Scrollbar(root)
sl.pack(side = RIGHT,fill = Y)
lb['yscrollcommand'] = sl.set
lb.place(x = 10,y = 45,anchor = NW)
sl['command'] = lb.yview

listLabel = Label(root,text = '查询列表-经纬度显示')
listLabel.place(x = 250,y = 20,anchor = NW)       
lonLabel = Label(root,text = '经度：')
lonLabel.place(x = 30,y = 300,anchor = NW)

lonv = StringVar()
lonEntry = Entry(root,text = '',textvariable = lonv)
lonEntry.place(x = 70,y = 300,anchor = NW)

latLabel = Label(root,text = '纬度：')
latLabel.place(x = 180,y = 300,anchor = NW)

latv = StringVar()
latEntry = Entry(root,text = '',textvariable = latv)
latEntry.place(x = 220,y = 300,anchor = NW)

kLabel = Label(root,text = 'k值：')
kLabel.place(x = 330,y = 300,anchor = NW)
kv = IntVar()
kEntry = Entry(root,text = '',textvariable = kv)
kEntry.place(x = 370,y = 300,anchor = NW)

keyLabel = Label(root,text = '关键词：')
keyLabel.place(x = 30,y = 350,anchor = NW)
keyv = StringVar()
keyEntry = Entry(root,text = '',textvariable = keyv)
keyEntry.place(x = 80,y = 350,anchor = NW)

findButton = Button(root,text = '查询',width = 10,height = 1)
findButton.place(x = 420,y = 330,anchor = NW)

delayLabel = Label(root,text = '查询时延：')
delayLabel.place(x = 170,y = 350,anchor = NW)
dtLabel = Label(root,text = '0.00')
dtLabel.place(x = 230,y = 350,anchor = NW)

def find(event):
    #清空查询结果显示列表
    lb.delete(0,END)
    try:
        curlat = float(latv.get())
        curlon = float(lonv.get())
        curk = int(kv.get())
        keyword = keyv.get()
        
    except:
        print '输入错误！'
        return
    else:
        #查询时延的开始时间
        starttime = time.time()
        
        #创建进度条
        progressTk = Tk()
        pbar = ttk.Progressbar(progressTk,length = 200,maximum = 100)
        pbar.pack()
        #初始化进度条
        pbar.config(value = 0)
        pbar.update()
        
        keytable = {}
        print keyword
        keyword = keyword.encode('utf-8')
        keyword = keyword.split(' ')
        #字典插入与赋值  
        for word in keyword:  
            if word != "" and keytable.has_key(word):      #如果存在次数加1  
                num = keytable[word]  
                keytable[word] = num + 1  
            elif word != "":                            #否则初值为1  
                keytable[word] = 1
        keywordarr = []
        for key in keytable:
            tem = []
            tem.append(key)
            tem.append(keytable[key])
            keywordarr.append(tem)
         
          
        #计算关键词相似度        
        #计算所有店铺与选定位置的距离
        karr = []
        temdict = {}
        infocount = 0
        for item in starbucks:
            table = {} 
            global info
            words = info[infocount].split(' ')  #空格分隔  
            infocount += 1
              
            #字典插入与赋值  
            for word in words:  
                if word!="" and table.has_key(word):      #如果存在次数加1  
                    num = table[word]  
                    table[word] = num + 1  
                elif word!="":                            #否则初值为1  
                    table[word] = 1
            wordarr = []
            for key in table:
                tem = []
                tem.append(key)
                tem.append(table[key])
                wordarr.append(tem)
              
            #计算关键词相似度
            similarity = MergeKeys(keywordarr,wordarr)  
            
            #计算位置距离
            dis = haversine(curlon, curlat, item[0], item[1])
            temdict[(similarity,dis)] = item    
            karr.append((similarity,dis))
            
        #更新进度条值   
        pbar.config(value = 20)
        pbar.update()   
        
        #top-k查询            
        minkvalue = select(karr,curk)
        print minkvalue
        #更新进度条值   
        pbar.config(value = 80)
        pbar.update()
        
         
        #计算查询时延
        endtime = time.time()
        #findtime = (endtime -starttime).total_seconds()
        findtime = endtime - starttime
        dtLabel['text'] = str(findtime)             
                                             
        result =  [temdict[i] for i in minkvalue]
        
        newresult = [[la,lo,info]for la,lo,info in result]
        for item in newresult:
            address = item[2]
            lb.insert(END,'StarbucksLocation:' + address)
             
        #更新进度条值   
        pbar.config(value = 100)
        pbar.update()      
        
        #关闭进度条窗口
        progressTk.destroy()    
         
        
        GEN_HTML = "demo_1.html"  #命名生成的html
            
        #jsonstr = str(newresult)
        
        file = open(r'D:\\pointresult.js','w') #建立json数据文件
        file.write('var points = [')
        ri = 0
        while ri < len(newresult)-1:
            outt = '[' + str(newresult[ri][0]) + ',' + str(newresult[ri][1]) + ',' + "'" + str(newresult[ri][2]) + "']," 
            file.write(outt)
            ri += 1
        outt = '[' + str(newresult[ri][0]) + ',' + str(newresult[ri][1]) + ',' + "'" + str(newresult[ri][2]) + "']" 
        file.write(outt)    
        file.write(']')
        #file.write(jsonstr)
        file.close()

        f = open(GEN_HTML,'w')
        message = """
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<style type="text/css">
		body, html,#allmap {width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}
		#l-map{height:100%;width:78%;float:left;border-right:2px solid #bcbcbc;}
		#r-result{height:100%;width:20%;float:left;}
	</style>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=Q8keInsWZn6NGnUM7GSePidbHXl6cGFx"></script>
	<script type="text/javascript" src="file:///D:/pointresult.js"></script>
	<title>星巴克查询结果显示</title>
</head>
<body> 
	<div id="allmap"></div>
	<script type="text/javascript">
	// 百度地图API功能
	var map = new BMap.Map("allmap");
	var point = new BMap.Point(116.404, 39.915);
	map.centerAndZoom(point, 2);
	map.enableScrollWheelZoom();
	var opts = {
		width : 300,     // 信息窗口宽度
		height:150,     // 信息窗口高度
		title : "STARBUCK" , // 信息窗口标题
		enableMessage:true//设置允许信息窗发送短息
	};
		 
	
	for (var i = 0; i < points.length; i ++) {	       
		var marker = new BMap.Marker(new BMap.Point(points[i][0],points[i][1]));
		map.addOverlay(marker);
		var content = points[i][2];
		addClickHandler(content,marker);
	}
	
	function addClickHandler(content,marker){
		marker.addEventListener("click",function(e){
			openInfo(content,e)}
		);
	}
	
	function openInfo(content,e){
		var p = e.target;
		var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
		var infoWindow = new BMap.InfoWindow(content,opts);  // 创建信息窗口对象 
		map.openInfoWindow(infoWindow,point); //开启信息窗口
	}
        </script>
</body>
</html>"""

        f.write(message)
        f.close() 
        
        # 打开网页     
        webbrowser.open(GEN_HTML,new = 1)
                
findButton.bind('<Button-1>',find)
root.mainloop()    