首先你寫在 class 裡面但不在 method 裡面的 variable 是 class variable

這個 variable 對於該類別及其子類別的類別和實體而言都只有一份, 看下面這個例子:

```python
class A:
    _dict = {}
    def __init__(self):
        self._dict.update({'a':'a'})
        
class B(A):

    def __init__(self):
        self._dict.update({'b':'b'})
        
if __name__=='__main__':
    a = A()
    b = B()
    print(a._dict)
    print(b._dict)
    print(A._dict)
    print(B._dict)
```

```
{'b': 'b', 'a': 'a'}
{'b': 'b', 'a': 'a'}
{'b': 'b', 'a': 'a'}
{'b': 'b', 'a': 'a'}
```

這裡你看到的所有 `_dict` 都參考到同一個物件

但是下面這個情況就不太一樣了:

```python
class A:
    _dict = {}
    def __init__(self):
        self._dict = {}
        self._dict.update({'a':'a'})
        
class B(A):

    def __init__(self):
        self._dict.update({'b':'b'})
        
class C(A):

    def __init__(self):
        super().__init__()
        self._dict.update({'c':'c'})
        
if __name__=='__main__':
    a = A()
    b = B()
    c = C()
    print(a._dict)
    print(b._dict)
    print(c._dict)
    print(A._dict)
    print(B._dict)
    print(C._dict)
```

```
{'a': 'a'}
{'b': 'b'}
{'c': 'c', 'a': 'a'}
{'b': 'b'}
{'b': 'b'}
{'b': 'b'}
```

咦?! 怎麼變成這樣了呢? 這邊如果搞懂的話就全盤皆通了:

首先 A 及其子類別都共有一個 class variable, 叫做 `_dict`

當我們初始化 a 的時候, `self._dict = {}` 會讓 a 裡面新產生一個變數叫做 `_dict`, 因為這次 `self._dict` 出現在等號左邊。注意! 這裡我們已經有兩個不同的東西了, 一個是 class variable `_dict`, 另一個是 instance variable `_dict`, 從此以後, a 裡面拿 `self._dict` 的時候就都是拿到 instance variable 了!

接著看 b, b 並沒有讓 variable 出現在等號左邊, 所以沒有建立新的變數, 現在 b 中的 `self._dict` 仍然指涉 class variable `_dict`

c 的情況就比較特別了, 藉由 `super` 他呼叫了 A 的 `__init__`, 上面說過了, 這會讓 c 中新建立一個 instance variable `_dict`, 這個變數因為 `A.__init__` 和 `C.__init__`, 所以會有兩個鍵值對


最後 `A._dict`, `B._dict` 和 `C._dict` 就很容易理解了, 他們都是參考到同一個 class variable, 所以值都一樣。

### 小結

讓我們來整理一下, 這邊一共會有 3 個 `_dict`:

1. class variable `_dict`
2. instance variable of a
3. instance variable of c
