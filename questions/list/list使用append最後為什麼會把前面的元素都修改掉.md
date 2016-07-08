# list 使用 append 最後為什麼會把前面的元素都修改掉

## 問題

一個簡單的循環解包，寫成字典後向後添加到列表中。

前面六步都沒問題，可是最後一次append會把前面六個元素都修改掉，這是為什麼呢？

```Python
items_index = range(7)
value = [10, 40, 30, 50, 35, 40, 30]
weight = [35, 30, 60, 50, 40, 10, 25]

item = {}
items = []
for i in range(len(items_index)):
    item['index'] = items_index[i] + 1
    item['value'] = value[i]
    item['weight'] = weight[i]
    items.append(item)
    print('第'+str(i+1)+'次：')
    print(items)
print('最后结果：')
print(items)
```

結果如下：

![img](https://segmentfault.com/img/bVvGGT)

問題出自 [segmentfault](https://segmentfault.com/q/1010000005129927/a-1020000005138271), by [KCN_5](https://segmentfault.com/u/kcn_5)

## 回答

這個問題的癥結點，之前幾位大大都已經點明了，就在於 `item` 的初始化應置放於迴圈內，否則每次 `append`到 `items` 中的都是同一個字典，到最後 `items` 中的每一個元素都參考到同一個字典。

----------

接下來就是我多嘴的部分了，希望能夠好好討論一些想法，給大家當作參考囉．

在 Python 中，我們應該盡量避免:

 1. 用 index 來循環 list
 2. 用 key 來循環 dictionary

不是說不可以，只是有更簡明的寫法，上述兩種用法的缺點都在於，在循環內我們必須多做一個取值的動作:

 1. `item = lst[index]`
 2. `item = dic[key]`

取而代之，我們應該直接去 iterate list 或 dictionary 中的元素。

在 list 中:

```python
>>> lst = ['a', 'b', 'c']
>>> for item in lst:
...     print(item)
... 
a
b
c
```

很簡單地，完全不透過 index 的控制我們就能依序取出 `lst` 中的元素．
至於在某些情況下我們也想要同時得到 index 值，我們也應該使用 `enumerate()` 方法:

```python
>>> lst = ['a', 'b', 'c']
>>> for index, item in enumerate(lst):
...     print(index, item)
... 
0 a
1 b
2 c
```

在 dictionary 中，使用 `items()` 方法是個好主意:

``` python
>>> dic = {'name':'dokelung', 'age':27}
>>> for key, item in dic.items():
...     print(key, item)
... 
age 27
name dokelung
```

以上這些寫法的好處都在於，**循環內不需要一個取值的干擾動作**，比較乾淨簡明．

----------

另外，BeginMan大點出了一個漂亮又簡明的想法，不過在某些情況下可能會有些問題，我舉個例子:

```python
value = [10, 40, 30, 50, 35, 40, 30, 50]
weight = [35, 30, 60, 50, 40, 10, 25, 50]

data = zip(value, weight)
items = map(lambda x: {"value": x[0], "weight": x[1], "index": data.index(x)+1}, data)

for item in items:
    print(item)
```

結果:

```
{'index': 1, 'weight': 35, 'value': 10}
{'index': 2, 'weight': 30, 'value': 40}
{'index': 3, 'weight': 60, 'value': 30}
{'index': 4, 'weight': 50, 'value': 50}
{'index': 5, 'weight': 40, 'value': 35}
{'index': 6, 'weight': 10, 'value': 40}
{'index': 7, 'weight': 25, 'value': 30}
{'index': 4, 'weight': 50, 'value': 50}
```

最後一個元素的 `index` 成為 4 了，這是因為利用 `data.index(x)` 永遠會找到 `data` 中第一個出現的 `x` 的 index 值，所以當 `data` 中有兩個相同的元素時便會有一些小問題

以這個case來說我的小建議是，我們不需要保留一個 `index` 值在 `item`中，因為最後所有的 `item` 會被保存在一個 list 中，這代表 `index` 就是 `item` 在 `items` 中的 index．

可以簡單改成下面的樣子:

```python
data = zip(value, weight)
items = map(lambda x: {"value": x[0], "weight": x[1]}, data)

for index, item in enumerate(items):
    print(index, item)
```

如果堅持一定要在每個字典中保持一個 `index`，那可以改成:

```python
items = map(lambda (index, item): {"index": index, "value": item[0], "weight": item[1]}, enumerate(data))
```

結果:

```
{'index': 0, 'weight': 35, 'value': 10}
{'index': 1, 'weight': 30, 'value': 40}
{'index': 2, 'weight': 60, 'value': 30}
{'index': 3, 'weight': 50, 'value': 50}
{'index': 4, 'weight': 40, 'value': 35}
{'index': 5, 'weight': 10, 'value': 40}
{'index': 6, 'weight': 25, 'value': 30}
{'index': 7, 'weight': 50, 'value': 50}
```

----------

接著來討論一下泛函編程中常見的 `map`(映射), `filter`(過濾) 和 `reduce`(精煉)．

在過去，Python 要撰寫泛函風格的代碼，上述三個 function 是必要中的必要，但現在，Python 的 list comprehension 和 generation expression 可以取代 map 和 filter 的角色，同時，許多內建的 **歸納函式** 也可以更好地取代 `reduce`，不過這邊不講那麼多，稍微講一下 `map`．

現在，`map` 我們應該盡量使用串列生成式來取代，比如以剛剛的例子:

```python
data = zip(value, weight)
items = map(lambda x: {"value": x[0], "weight": x[1]}, data)
```

使用 list comprehension 會更好理解些:

```python
data = zip(value, weight)
items = [{"value": value, "weight": weight} for value, weight in data]

for index, item in items:
    print(index, item)
```

如果有效率上的考量，使用 generator 會更好:

```python
data = zip(value, weight)
gen = ({"value": value, "weight": weight} for value, weight in data)

for item in gen:
    print(item)
```
