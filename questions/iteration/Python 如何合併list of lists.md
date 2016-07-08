# Python 如何合併list of lists

## 問題

```python
for i in  open (v):
    _temp = i.split('-')
	self._i= gen.gen(_temp[0], _temp[1])
```

`self._i` 中是 list of lists，怎樣合併成一個?

問題出自 [segmentfault](https://segmentfault.com/q/1010000005904259), by [懒洋洋](https://segmentfault.com/u/lanyangyang)

## 回答

如果你的意思是要合併多個 list 為一個，那使用 `itertools.chain` 來串接是最好的，以下是個簡單的範例:

```python
>>> from itertools import chain
>>> a = [1,2,3]
>>> b = [4,5,6]
>>> c = [7,8,9]
>>> chain(a,b,c)
<itertools.chain object at 0x7f2915465c10>
>>> list(chain(a,b,c))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

對於你的 case 而言:

```python
from itertools import chain
lst = list(chain(*self._i))
```

---

以下題外話。

@松林 的方法是可行的，而且效能不會差，在 python 中 **擴增(增強)運算** 和 **一般運算** 的行為不見得完全一模一樣，在這裡我們使用 `+` 來討論。

我們看一個例子:

```python
>>> lst1 = [1,2,3]
>>> lst2 = [4,5,6]
>>> id(lst1)
139814427362656
>>> id(lst1 + lst2)
139814427363088
>>> lst1 += lst2
>>> id(lst1)
139814427362656
``` 

由本例可以發現，`lst1 + lst2` 會產生一個新的 list，但是 `lst1 += lst2` 則不會，因為對於擴增運算，Python **大部分** 會依循以下規則:

1. 不可變的型態會經由運算後產生一個新的 object，並且讓變數參考到該 object
2. 可變的型態會採用 **就地(in-place)運算** 的方式來擴充或更新變數原本參考的 object

也就是說 `lst1 += lst2` 等價於 `lst1.extend(lst2)`

這取決於該型態是否有實作 `__iadd__`(或 `__imul__` ...) 而不是只有實作 `__add__` (或 `__mul__` ...)

對於沒有實作 `__iXXX__` 的型態，Python 會改呼叫 `__XXX__` 代替，這一定會運算出新的 object，但是 `__iXXX__` 則會就地更新原 object

也就是說 **大部分** 的:

1. 不可變型態都不會實作 `__iXXX__`，因為更新不可變型態的 object 是沒有道理的
2. 可變型態會實作 `__iXXX__` 來就地更新

為什麼我一直強調大部分呢?

因為 CPython 中優化了 `str` 的擴增運算，`str += other` 實在太常用了，在串接時，Python 並不會每次都複製字串
