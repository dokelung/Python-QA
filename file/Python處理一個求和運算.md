# Python 處理一個求和運算

我現在有個 txt 文件如下：

```
1 167 334555717
2 19 334555718
2 167 334555718
3 167 334555720
4 172 334555721
5 21 334555723
5 147 334555723
5 50 334555723 
```

* 第一列是序號
* 第二列是字數
* 第三列是ID。

相同 ID 的序號是相同的。

然後現在我需要用 python 進行下述處理：

就是將相同 id 的字數相加得到一個總和 `sum`，然後對 `sum` 進行如下的公式計算：

```
result=字數1/sum log(字數1/sum)+字數2/ sum log(字數2/sum)+...... 
```

按這個文件舉例來說，就是比如

334555718 的這個 id 的 result 計算如下：

```
sum=19+167 
result=19/sum log(19/sum)+ 167/sum log(167/sum) 
```

33455723 的這個 id 的 result 就是:

```
sum=21+147+50 
result=21/sum log(21/sum)+147/sum log(147/sum)+50/sum*log (50/sum)
```

然後依次輸出每個 id 的序號, id號 跟 result。

我的代碼如下：

```python
import math
f = open("F:\\net.txt")         
lines = f.readlines()
    
rev_id=[]
    
for line in lines:
    num = line.split()[0]
    zishu = line.split()[2]
    revid = line.split()[3]
    sum = zishu
    if revid in rev_id:
    	 sum += zishu
    	 result += zishu/sum*(math.log(zishu/sum))
    rev_id.append(revid)
```

我的 result 的結果肯定不對，因為 `sum` 的值不是固定的全部總和...請問該怎麼做。

## 問題

問題出自 [segmentfault](https://segmentfault.com/q/1010000005089896/a-1020000005093803), by [starryer](https://segmentfault.com/u/starryer)

## 回答

這邊是Python3的代碼，給你參考:

```python
import math
    
dic = {}
    
# read file
with open('net.txt' , 'r') as reader:
    for line in reader:
        idx, num, revid = line.strip().split()
        lst = dic.setdefault(revid, [])
        lst.append(int(num))
    
results = {}
    
# calculate results
for revid, lst in dic.items():
    s = sum(lst)
    result = sum([num/s * math.log(num/s) for num in lst])
    results.update({revid:result})
    
# output
for revid, result in results.items():
    print(revid, result)
```

### 說明與建議

Python 讀取檔案的確是使用 `open` function，但是開啟了的檔案，必須記得關閉以免發生問題，像你給出的代碼中，文件被你 `open` 了卻沒有 `close`，這是一種較不安全的寫法，應當緊記: 有 `open` 就有 `close`，他們是成對的。 為了避免忘記關閉文件的可能，使用 `with` 述句是個理想的辦法。
