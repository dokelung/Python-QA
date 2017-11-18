# Python 多重繼承屬性問題

## 問題

Python 類的繼承,怎麽讓一個子類 `C`, 同時繼承父類 `A`, `B` 的屬性?

先定義兩父類:

```python
    class A(object):
        def __init__(self, a1,a2):
            # super(ClassName, self).__init__()
            self.a1 = a1
            self.a2 = a2
    
        def funa(self):
            print("I'm funa")

    class B(object):
        def __init__(self, b1):
            # super(ClassName, self).__init__()
            self.b1 = b1
    
        def funb(self):
            print("I'm funb")
```

那麽子類 `C` 應該如何寫? 才能讓初始化後具有 `A`, `B` 中的 `a1`, `a2`, `b1` 屬性和 `funa`, `funb` 方法?

```python
    class C(A,B):
        # ????????????????????
        def __init__(self):
            super().__init__()
        #?????????????????????
        pass
```
感覺是很基本的問題,求各位大佬解答,謝謝!

問題出自 [segmentfault](), by [Andykim](https://segmentfault.com/u/andykim)

## 回答

假設你要多重繼承的 **各個父類關係是平行的**, 多重繼承用於 **組合各父類的成員** (**Mixin** 的概念), 那你可以考慮下面這個例子, 而為了展示通用性, 下面的例子中有三個可能被用來繼承的父類 `A`, `B`, `C`, 而其子類 (例如 `X`, `Y`)可以用任意順序來組合任意數量個父類:

```python
# base classes

class A:
    def __init__(self, a1, a2, **kwargs):
        super().__init__(**kwargs)
        self.a1 = a1
        self.a2 = a2

    def funa(self):
        print("I'm funa")

class B:
    def __init__(self, b1, **kwargs):
        super().__init__(**kwargs)
        self.b1 = b1

    def funb(self):
        print("I'm funb")
        
class C:
    def __init__(self, c1, c2, c3, **kwargs):
        super().__init__(**kwargs)
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    def func(self):
        print("I'm func")
```

```python
# derived classes

class X(B, A, C):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class Y(A, B):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
```

使用範例:

```python
x = X(a1=1, a2=2, b1=3, c1=4, c2=5, c3=6)
y = Y(a1=1, a2=2, b1=3)
print(x.a1, x.a2, x.b1, x.c1, x.c2, x.c3)
x.funa()
y.funb()
print(dir(x))
print(dir(y))
```

結果:

```python
1 2 3 4 5 6
I'm funa
I'm funb
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a1', 'a2', 'b1', 'c1', 'c2', 'c3', 'funa', 'funb', 'func']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'a1', 'a2', 'b1', 'funa', 'funb']
```
