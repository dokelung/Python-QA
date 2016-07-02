# Python處理文本信息

## 問題

有一個文本信息如下:

```
42 453926 Stormwriter restored undeleted 61.1.28.140
44 425968 61.1.28.140
42 425967 Mintguy restored undeleted 61.11.252.22
43 419840 61.11.252.22
```

我做的是需要根據第一列的這個序號的數據來找對應的數據，像這種有著相同序號的行，他們對應的第二列的 ID 數據就是對應的，我需要找到這樣一對一對的 ID 數據。就這個例子來說就是 453926 跟 425967 是對應的，輸出:

```
453926 425967
```

而也會有多個相同序號的情況。比如:

```
42 453926 Stormwriter restored undeleted 61.1.28.140
44 425968 61.1.28.140
42 425967 Mintguy restored undeleted 61.11.252.22
43 419840 61.11.252.22
42 419809 TimStarling
```

就是需要記錄多次，而且是跟最後一個相同序號對應，拿這個例子來說，就是記錄第一個 42 跟最後一個 42 的對應 ID，然後同時也要記錄中間那個 42 跟最後一個 42 的 ID，輸出這樣:

```
453926 419809（restored行的ID是453926）
425967 419809（restored行的ID是425967)
```

我開始想的是用字典，但是字典也就只能保留到最後一個相同的序號，怎麼做才能讓中間的相同序號也能輸出對應的呢TUT

我的偽代碼如下:

```python
dict={}
if xxx: #只是一個判斷處理的條件 
    flag_number = line.split()[0]
    id = line.split()[0]
    next()
elif line.split()[0]==flag_number:
    dict[id] = line.split()[1]
```
但是這個代碼只能輸出第一個跟最後一個相同的序號，如何修改才能也讓中間的相同序號跟最後一個序號也輸出出來呢

問題出自 [segmentfault](https://segmentfault.com/q/1010000005621524/a-1020000005622128), by [starryer](https://segmentfault.com/u/starryer)

## 回答

用字典是可以的，首先是收集:

```python
INDEX = 0
ID = 1

dic = {}

with open('data') as reader:
    for line in reader:
        items = line.strip().split()
        ids = dic.setdefault(items[INDEX], [])
        ids.append(items[ID])
```

輸出:

```python
for index, ids in dic.items():
    for sid in ids[0:-1]:
        print sid, ids[-1]
```

或:

```python
# 如果不太懂這段代碼的意思，請參見下面說明，其實我覺得用上面的方法也夠了
for index, ids in dic.items():
    for sid, eid in ((id, ids[-1]) for id in ids[0:-1]):
        print sid, eid
```

稍微講一下這段代碼:

```python
((id, ids[-1]) for id in ids[0:-1])
```

上面這一行是一個 產生器表達式( generator expression, 簡稱 genexp)，他就類似 list comprehension，不過他並不會馬上產生實際的資料和 list，只有等到你去 iterate 或是取值的時候才會依序產生資料項。這代表在資源的利用上，是比較有效率的。

這邊產生的 generator 可以依序產生一個雙元素的 tuple，這兩個元素都是 id，剛好就是一個 id pair(第一個元素是各個非最後一個id，第二個元素是最後一個id。

至於：

```python
for sid, eid in ((id, ids[-1]) for id in ids[0:-1]):
```

就是依次產生 id pair 並且利用 tuple unpacking 平行賦值給 `sid` 和 `eid`，最後輸出。

----------

`data`:

```
42 453926 Stormwriter restored undeleted 61.1.28.140
44 425968 61.1.28.140
42 425967 Mintguy restored undeleted 61.11.252.22
43 419840 61.11.252.22
42 419809 TimStarling
```

結果:

```
453926 419809
425967 419809
```
