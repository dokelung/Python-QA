# csv 模塊生成 CSV 文件問題(0字頭數字缺失與漢字亂碼)

## 問題

python CSV模塊寫入CSV文件時，0開頭的數字會丟失

```python
# _*_ coding:utf-8 _*_ 
#win7+python2.7.x 
import csv
csvfile = file( 'csvtest.csv' , 'wb' )
writer = csv.writer(csvfile)
writer.writerow([ 'id' , 'url' , 'keywords' ])
data = [
  ( '0011' , 'http://www.59store.com/' , '59store.com' ),
  ( '0022' , 'http://59data.top/' , '59data.top' ),
  ( '0033' , 'http://my.space.zmx/' , '漢子亂碼？' )
]
writer.writerows(data)
csvfile.close()
```

寫入CSV時會丟失0字頭，漢字亂碼

![img](https://segmentfault.com/img/bVwHjb)

問題出自 [segmentfault](https://segmentfault.com/q/1010000005370629/a-1020000005436450), by [messiah163](https://segmentfault.com/u/messiah163)

## 回答

我測試的結果:

```
id,url,keywords
0011,http://www.59store.com/,59store.com
0022,http://59data.top/,59data.top
0033,http://my.space.zmx/,汉子乱码？
```

看起來純文字 file 沒有什麼問題，猜測可能是你**用來開啟 csv 文件的試算表軟體**造成的．(mac 的 `Numbers` 和 `OpenOffice Calc` 都有這個現象)

比如說，id 欄位的型態如果設為數字，則前面不必要的 0 可能會自動被忽略． 像這一點可以試試看改成純文字型態再開啟．

P.S. `Excel` 的部分可以見 玉河CC 大的說明．

要更精準更細節地處理 xlsx 文件，可以用 [XlsxWriter][1]，他能夠控制資料的型態(data type)，甚至樣式(format)．

  [1]: http://xlsxwriter.readthedocs.io/index.html
