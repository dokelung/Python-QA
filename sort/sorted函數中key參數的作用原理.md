# sorted 函數中 key 參數的作用原理

## 問題

這是一個字符串排序，排序規則：小寫<大寫<奇數<偶數

```python
s = 'asdf234GDSdsf23'  #排序:小写-大写-奇数-偶数
keyfunc = lambda x: (x.isdigit(), x.isdigit() and int(x) % 2 == 0, x.isupper(), x.islower(), x)
print("".join(sorted(s, key=keyfunc)))
```

這裡 key 接受的函數返回的是一個元組？是如何進行比較的？

問題出自 [segmentfault](https://segmentfault.com/q/1010000005111826/a-1020000005112829), by [肥貓_joe](https://segmentfault.com/u/feimao_joe)

## 回答

讓我們從一個簡單的例子開始:

```python
items = [(1, 2), (2, 1)]
print(sorted(items))
```

結果:

```python
[(1, 2), (2, 1)]
```

`items` 是一個 list of tuple，如果針對 tuple 排序，Python 的 Builtin function `sorted`(或是`sort`) 會從 tuple 的最後一個元素開始進行排序，也就是說一組二元素的 tuple 進行排序可以想像成兩次基本的排序:

原本是:

```python
[(2, 1), (1, 2)]
```

第一次排序以第2個元素為 key，所以排序的結果為:

```python
[(2, 1), (1, 2)]
```

第二次排序以第1個元素為 key，所以排序的結果為:

```python
[(1, 2), (2, 1)] # 最終結果
```

### 結論 1

tuple 的排序由最後的元素往前依次進行排序
也就是說 tuple 的排序權重是由第一個元素開始依次向後遞減

----------

接著我們來觀察一下 Boolean value 的排序:

```python
print(sorted([True, False])
```

結果:

```python
[False, True] # False在前，True在後
```

### 結論 2

Boolean 的排序會將 `False` 排在前，`True`排在後

----------

那我們來看看你給出的例子，我們撰寫一個簡單的 function 來觀察結果:

```python
def show(s):
    for x in s:
        print((x.isdigit(), x.isdigit() and int(x)%2==0, x.isupper(), x.islower(), x))
```

function `show` 會列印出當下的字串 `s` 用來排序時每個字元所產生的 tuple key．

接著我們套用剛剛的結論1，我們先不使用 tuple 來作為 key，反而利用等價的 **由最後一個元素往前依次為 key 排序**，並且逐步觀察 `s` 和 tuple key 的變化:

```python
print('key=x')
s = sorted(s ,key=lambda x: x)
show(s)
    
print('key=islower()')
s = sorted(s ,key=lambda x: x.islower())
show(s)
    
print('key=isupper()')
s = sorted(s ,key=lambda x: x.isupper())
show(s)
    
print('key=isdigit() and int(x)%2==0')
s = sorted(s ,key=lambda x: x.isdigit() and int(x)%2==0)
show(s)
```
    
我們將會發現一如預期地，依照結論(1)，這樣的做法的確等價於一口氣以 tuple 為 key 來排序．
同時觀察，結論(2)，對於 `isdigit()`, `isupper()`, `islower()`等所產生的 Boolean key 來說，排序的結果也如預期．

```python
print('key=isdigit()')
s = sorted(s ,key=lambda x: x.isdigit())
show(s)
```

----------

不過我想這還不是我們最後的結論，因為這是一個碰巧的結果(說碰巧也許太超過了，應該說是不那麼直覺的結果)，讓我們根據 **結論(1)** 對最初的例子進行分析:

```python
sorted(s, key=lambda x: (x.isdigit(), x.isdigit() and int(x) % 2 == 0, x.isupper(), x.islower(), x))
```    

這個排序我們可以翻譯成:

>先對字元x本身做排序，接著是對 字元是否為小寫，字元是否為大寫，字元是否為偶數，字元是否為數字分別作排序．

也可以翻譯成:

> 我們以 字元是否為數字為最高排序權重，接著以字元是否為偶數，字元是否為大寫，字元是否為小寫，字元x本身為權重來做排序．

這似乎與一開始的目標(#排序:小写-大写-奇数-偶数)不同，起碼跟目標沒有直覺上的對應．

建議可以改成:

```python
keyfunc = lambda x: (not x.islower(), not x.isupper(), not(x.isdigit() and int(x)%2==1), x)
print("".join(sorted(s1, key=keyfunc)))
```

這樣就可以解讀為:

> 我們以 字元是否為小寫為最高權重，接著以字元是否為大寫，字元是否為奇數，字元x本身為權重來做排序

有趣的是：我們想要讓判斷式為 `True` 的字元在排序完成後在比較前面的位置，所以根據結論(2)加了一個 `not`來讓符合的字元可以在前面．
