#  Python 日期的遞增問題

## 問題

* 初始化開始時間 2016-07-01 
* 設置日期為 31

遞增

```
2016-07-01 
2016-07-02 
... 
2016-07-31
```

除了

```python
count = 0
while (count < 31):
   
   count =count+1
   print '2016-07-',count
```

還有沒其他方式

問題出自 [segmentfault](https://segmentfault.com/q/1010000006007938/a-1020000006008322), by [monkey_cici](https://segmentfault.com/u/monkey_cici)

## 回答

用 [datetime](https://docs.python.org/3.5/library/datetime.html)

datetime 方便又強大, 值得投資一下

```python
from datetime import date, timedelta

def gen_dates(bdate, days):
    day = timedelta(days=1)
    for i in range(days):
        yield bdate + day*i

if __name__ == '__main__':
    bdate = date(2016, 7, 1)
    for d in gen_dates(bdate, 31):
        print(d)
```

**結果**:

```
2016-07-01
2016-07-02
...
2016-07-30
2016-07-31
```

**代碼說明**:

`date(year, month, day)` 可以很輕鬆地製造出日期

`timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)` 可以製造出時間間隔

然後你可以用一般的代數來操作日期計算:

```python
>>> d = date(2016, 7, 1)     # 產生 2016-07-01 這個日期
>>> day = timedelta(days=1)  # 產生 1 天的時間間隔
>>> print(d+day)             # 印出 2016-07-01 + 1 天
2016-07-02
```
