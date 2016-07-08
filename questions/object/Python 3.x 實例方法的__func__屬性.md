# Python 3.x 實例方法的 `__func__`屬性

## 問題

看 Python 3.x 的文檔，涉及到實例方法特殊屬性的內容，有這麽一段話描述 instance method 的 `__func__` 屬性：

>When an instance method object is created by retrieving a user-defined function object from a class via one of its instances, its self attribute is the instance, and the method object is said to be bound. The new method’s func attribute is the original function object.

>When a user-defined method object is created by retrieving another method object from a class or instance, the behaviour is the same as for a function object, except that the func attribute of the new instance is not the original method object but its func attribute.

甚是不解，主要是不明白前後兩段中對instance method object的創建方式的描述到底有何不同？ 還請大神賜教

問題出自 [segmentfault](https://segmentfault.com/q/1010000005175248/a-1020000005178655), by [xu_zhoufeng](https://segmentfault.com/u/inside)

## 回答

class(object, instance) 中的 function 我們稱為 method，而一個 method 是一個 bound (綁定的) function，綁定什麼呢? 自然是綁定 instance．

我們看下面這個作為範例的 `Test` class:

```python
class Test:
    
    def __init__(self):
        self.name = 'hello'

    def func(self):
        return self.name
```

他有一個 method `func`，如果我們使用該類產生實例 `test1` 和 `test2`：

```python
>>> test1 = Test()
>>> test2 = Test()
>>> test1.func
<bound method Test.func of <test.Test object at 0x7f15d0703eb8>>
```

我們會發現 `test1.func` 是一個 bound method，這代表了他與 `test1` 綁定，這個綁定最重要的一點就是 `test1.func` 的 `self` 屬性是 `test1`．

這看起來很 trivial，不過這中間有個很重要的概念，就是一個 class 中的某個 method 其實只有一個實體，也就是說無論今天我們用 `Test` 產生了多少個 instances，他們都是共用同一個 function `func`，但是每個 instance 都會有一個將 `func` 綁定到自己的 bound method `func`，那我們要如何觀察到真正的(unbound) function呢? 很簡單，這個真正的 function object 被記錄在 bound method 的 `__func__` 屬性：

```python
>>> test1.func # instance 中的 func
<bound method Test.func of <test.Test object at 0x7f15d0703eb8>>
>>> test2.func # instance 中的 func
<bound method Test.func of <test.Test object at 0x7f15d0703320>>
>>> test1.func.__func__ # unbound function
<function Test.func at 0x7f15d0671048>
>>> test2.func.__func__ # unbound function
<function Test.func at 0x7f15d0671048>
>>> Test.func # unbound function
<function Test.func at 0x7f15d0671048>
>>> test1.func.__func__ is test2.func.__func__
True
```

由上可知，雖然每個 instance 有自己的 bound method，但這些其實只是將原本的 function 綁定了不同的 instance 後所產生的 functions．

----------

接著稍微來分析一下 Python 的指派(assignment)，我其實覺得 Python 的指派其實就可以很簡單地想成讓等號左邊的變數參考到等號右邊所運算出來的 instance．

也就是說一個簡單地不帶其他運算的指派:

```
a = b
```

很直覺地可以解讀成 a 參考到 b 所參考的 instance．

----------

讓我們回到原本的問題，

今天我們如果做了下面這樣的指派:

```python
myfunc = test1.func
＃或是
myfunc = test2.func
```

很明顯地 `myfunc` 現在和 `test1.func` 參考到同一個 unbound method，也很自然地，他們的`__func__` 屬性必然會一樣，也就是參考到 `Test.func`．

### 結論

其實他想要告訴大家的事情是:

像是 `myfunc` 這樣的 object，他的 `__func__` 並不會是 `test1.func`(應該說 `myfunc` 根本就是 `test1.func`)，而他的 `__func__` 屬性自然就是 `test1.func` 的 `__func__` 屬性．
