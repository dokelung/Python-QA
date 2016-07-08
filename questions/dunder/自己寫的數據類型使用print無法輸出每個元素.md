# 自己寫的數據類型使用 print 無法輸出每個元素

## 問題

估計是我問題沒有描述清楚，這樣吧，直接上代碼：

```python
class  Mylist : 
    def __init__(self) :
        self._mylist=list()

    def __len__(self) : 
        return len(self._mylist)

    def add(self,value) : 
        return self._mylist.append(value)
```

我自己模仿 list 的行為。寫了一個基本的 list，名字叫 Mylist, 並給他一個 `add` 方法用來添加其中的元素．

添加完之後，我想輸出其中的內容，然後我使用：

```python
list1=Mylist()
list1.add( 1 )
list1.add( 2 )
print(list1)
```

我以為print會顯示出 `list1` 中的每一項，但是發現實際沒有，顯示的為：

```python
<__main__.Mylist object at 0x0071A470>
```

怎麼樣能讓 `print(list1)` 顯示出的結果和真實 list 類型一樣呢？例如：

```
[1,2] 
```

`__str__` 具體怎麼實現，貌似這個只能為 str 類型, int 不行，而且我發現在 pycharm 裡面寫的時候，提示 __str__ 方法 "overrides method in object"

問題出自 [segmentfault](https://segmentfault.com/q/1010000005110206/a-1020000005113051), by [小燕smile](https://segmentfault.com/u/xiaoyansmile)

## 回答

你是用的是 "聚合" 的方式來建立自己的群集資料，這時候透過委託是個簡單的方法:

```python
class Mylist:
    def __init__(self):
        self._mylist=list()
    
    def __len__(self):
        return len(self._mylist)
    
    def add(self,value):
        return self._mylist.append(value)
    
    def __str__(self):
        return str(self._mylist)
```

`__str__` 是 Python 類中的特殊方法，他的回傳值就是使用 `str(x)` 所得到的值， 而 `print(x)` 其實就等於是 `print(str(x))`．其實再講細一點，當我們呼叫 `str(x)` 的時候其實是呼叫 `x.__str__()`．

也就是說我們可以這樣想像:

```python
print(x) === print(str(x)) === print(x.__str__())
```

一般我們 **自定義的類**，`__str__` 方法的回傳值是默認的字串．

比如說: `<__main__.Mylist object at 0x0071A470>` 用以說明 namespace, class name 和位置．如果要改變 `__str__` 的回傳值，我們必須要覆寫他．

這邊我們讓 `__str__` 的回傳值為 `MyList` 類中聚合的 list 的 `__str__`值，這樣就透過委託的方式讓 `__str__` 的輸出跟 list 一樣了．

多嘴補充一下，這種在 class 裡面 **以雙底線開頭且以雙底線結尾** 的 method (俗名叫做魔術方法或是特殊方法)，有個正式名稱叫做 **"dunder method"**，對於 `__str__`，我們可以唸作 "dunder string"．

> The frequent use of a double underscores in internal identifiers in Python gave rise to the abbreviation dunder; this was coined by Mark Jacksonand independently by Tim Hochberg, within minutes of each other, both in reply to the same question in 2002. --[wiki][1]

----------

下方評論問的問題我回答在這裡．

首先是不要被混淆，我們利用 `print` 印出來的內容都是 **字串**，即便你看到 `[1, 2]` 其實這也是一個字串 `'[1, 2]'`，只不過內建的幾種資料型態(或我們有覆寫過 `__str__` 的 class) 會想辦法輸出一個帶有該資料型態特徵的字串(通常會非常接近我們產生這些資料時所用的"字面")．

舉例，我們使用字面產生一個 list:

```python
lst = [1, 2]
```

當我們打印 `lst` 時，Python 是會製造一個長得像該資料型態字面(甚至一模一樣)的字串讓你印出:

```python
print(lst)

[1, 2] # 其實這是個字串，但是 lst 還是 list!
```

所以在這裡 `str(list)` 並沒有改變 list 中元素的 type，只不過將帶有其特徵的 "字串" 當成回傳值．

其次，如果想要在 Python shell (Python的互動介面)中能夠只利用變數名稱就展示用來表示 `Mylist` 的字串，光是 `__str__` 還不夠，這必須要覆寫 `__repr__`:

```python
class Mylist:
    
    def __init__(self):
        self._mylist=list()
    
    def __len__(self):
        return len(self._mylist)
    
    def add(self,value):
        return self._mylist.append(value)
    
    def __str__(self):
        return str(self._mylist)
            
    def __repr__(self):
        return str(self)
```

**結果**:

```python
>>> from test import Mylist
>>> lst = Mylist()
>>> lst.add(1)
>>> lst.add(2)
>>> lst
[1, 2]
```

  [1]: http://bit.ly/1Vm72Mf
