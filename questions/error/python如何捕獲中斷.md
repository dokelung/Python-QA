# python 如何捕獲中斷

## 問題

我目前有一個爬蟲, 爬取的東西目測要好些天才能完

所以我設計成了能夠自動續爬的形式, 不過我選擇想再進一步

記錄每次開始和結束的時間

但是不知道怎樣在 `<ctrl-C>` 這種鍵盤終端的時候去寫下程序退出的時間

望指點指點, 感覺是要捕獲異常..

問題出自 [segmentfault](https://segmentfault.com/q/1010000006102391/a-1020000006102562), by [Rancho](https://segmentfault.com/u/rancho)

## 回答

catch `KeyboardInterrupt`

```python
import time
import datetime

print('stime:', datetime.datetime.now())
try:
    while True:
        time.sleep(1)
        print('go')
except KeyboardInterrupt:
    print('etime:', datetime.datetime.now())
```

測試:

```
stime: 2016-07-28 01:54:21.647561
go
go
go
<Ctrl+c>
etime: 2016-07-28 01:54:25.010312
```
