# 操作 csv 文件寫入順序不對

## 問題

我是初學者不太懂

1. 為什麼在終端顯示是正確的順序到了csv 文件中就是另一回事了呢
2. 還有就是csv 文件怎麼可以運行之後繼續填寫而不是清空文件呢？

![img1](https://segmentfault.com/img/bVxKBr)

![img2](https://segmentfault.com/img/bVxKBs)

代碼:

```python
import urllib.request
import re
import bs4 
import csv
from bs4 import BeautifulSoup

url="http://10.104.65.9/home/part/shuiQing.jsp"
data=urllib.request.urlopen(url).read()
data=data.decode('UTF-8')

soup=BeautifulSoup(data,"html.parser")
foundtxt=soup.find_all('td',height='22')

rol=[]
index=0

#with open(r'C:\Users\skyb52\Desktop\12.csv','wb') as csvfile:
with open(r'C:\Users\skyb52\Desktop\12.csv','w',newline='') as csvfile:
   spamwriter = csv.writer(csvfile,dialect='excel')
   for i in foundtxt:
       rol.append(i.string)
       index=index+1
       if index==3:
           spamwriter.writerow({rol[0],rol[1],rol[2]})
           print(rol[0],rol[1],rol[2])
           rol=[]
           index=0
   csvfile.close()  
```

最後添加上內網網站源代碼:

```html
<style type="text/css">
<!--
.style1 {
	font-size:12px;
}
-->
</style>
<body topmargin="0" leftmargin="0">
<table width="244" border="0" cellpadding="0" cellspacing="1" bgcolor="#ffffff" class="style1">
  <tr>
    <td  height="24" align="center" bgcolor="#b8b8b8" width="30%">站名</td>
    <td  align="center" bgcolor="#b8b8b8" width="33%">水位(m)</td>
    <td  align="center" bgcolor="#b8b8b8">流量(m<sup>3</sup>/s)</td>
  </tr>
  
  <tr>
<td height="22" align="center" bgcolor="#eaeaea">小浪底</td>
<td height="22" align="center" bgcolor="#eaeaea">134.63</td>
<td height="22" align="center" bgcolor="#eaeaea">565</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#FFFFFF">花园口</td>
<td height="22" align="center" bgcolor="#FFFFFF">89.05</td>
<td height="22" align="center" bgcolor="#FFFFFF">445</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#eaeaea">夹河滩</td>
<td height="22" align="center" bgcolor="#eaeaea">72.58</td>
<td height="22" align="center" bgcolor="#eaeaea">400</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#FFFFFF">高村</td>
<td height="22" align="center" bgcolor="#FFFFFF">58.98</td>
<td height="22" align="center" bgcolor="#FFFFFF">360</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#eaeaea">孙口</td>
<td height="22" align="center" bgcolor="#eaeaea">44.29</td>
<td height="22" align="center" bgcolor="#eaeaea">358</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#FFFFFF">艾山</td>
<td height="22" align="center" bgcolor="#FFFFFF">36.82</td>
<td height="22" align="center" bgcolor="#FFFFFF">225</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#eaeaea">泺口</td>
<td height="22" align="center" bgcolor="#eaeaea">25.7</td>
<td height="22" align="center" bgcolor="#eaeaea">207</td>
</tr>
<tr>
<td height="22" align="center" bgcolor="#FFFFFF">利津</td>
<td height="22" align="center" bgcolor="#FFFFFF">9.36</td>
<td height="22" align="center" bgcolor="#FFFFFF">76.5</td>
</tr>

  
</table>
</body>
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005621628/a-1020000005624752), by [skyb52](https://segmentfault.com/u/skyb52)

## 回答

你寫到 csv 的代碼:

```python
spamwriter.writerow({rol[0],rol[1],rol[2]})
```

你寫了一個 set 出來，他是無序的，而你 `print` 的時候是有序的:

```python
print(rol[0],rol[1],rol[2])
```

結果自然不同

----------

不清空而是附加新的資料上去的作法，在於使用 `open` 打開文檔時，要使用 `'a'` (append) 模式:

```python
with open(r'C:\Users\skyb52\Desktop\12.csv','w',newline='') as csvfile:
                                            ^^^
                                       寫入模式，會覆蓋掉原本的資料從頭開始寫入
```

改成:

```python
with open(r'C:\Users\skyb52\Desktop\12.csv','a',newline='') as csvfile:
                                            ^^^
                                       附加模式，會從文件最後開始寫入
```
