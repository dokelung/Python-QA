# Python 如何通過類方法創建實例方法？

## 問題

下面是Python 3.x language reference 中的一段話，大意是理解的，不過寫不出一個這樣的示例，求大神給個與這段話一致的示例：

> When an instance method object is derived from a class method object, the “class instance” stored in self will actually be the class itself, so that calling either xf(1) or Cf(1) is equivalent to calling f(C,1 ) where f is the underlying function.

問題出自 [segmentfault](https://segmentfault.com/q/1010000005690407/a-1020000005701043), by [xu_zhoufeng](https://segmentfault.com/u/inside)

## 回答

其實這個部分，你自己做做實驗就會明白。

我們從原文開始看起，分成兩段來討論，第一段說道:

>When an instance method object is called, the underlying function (__func__) is called, inserting the class instance (__self__) in front of the argument list. For instance, when C is a class which contains a definition for a function f(), and x is an instance of C, calling x.f(1) is equivalent to calling C.f(x, 1).

原文第一段說，當一個 `instance method object` 被調用時，`__func__` 的第一個參數先代入 `class instance` 後被調用，接著舉了一個例子:

```python
x.f(1) == C.f(x,1)  # x is an instance of C
```

我們用下面的範例來說明，在這裡我們有一個類 `Demo`，他底下有一個 function `foo` 和 function `bar`。

`Demo` class:

```python
class Demo:

    def foo(self, *args):
        return 'Call foo by instance' + repr(self) + 'with args' + repr(args)

    @classmethod
    def bar(cls, *args):
        return 'Call bar by class ' + repr(cls) + 'with args' + repr(args)
```

實際上呢:

1. Python 對於 `foo`，會產生一個 **一般的 function**，這個 function 會被 `Demo.foo` 所參考。
2. 當我們寫出 `demo.foo` 的時候，Python 會即時創造一個 **bound method object**: `demo.foo`，這個 method object 是個綁定的 method，綁定甚麼呢? 當然就是綁定 `demo` 這個 instance，所以 `demo.foo.__self__` 會參考到 `demo`, 同時 Python 也會把 `Demo.foo` 記在 `demo.foo.__func__` 中。
3. 所以當這個 `demo.foo` 被呼叫的時候(`demo.foo(1,2,3)`)，他其實會去呼叫 `demo.foo.__func__`，並且以 `demo.foo.__self__` (其實也就是 `demo` 自己) 當作第一個參數。

以我們寫的類來展示的話，他的例子變成:

```python
   x.f(1)   ==    C.f(x, 1) 
demo.foo(1) == Demo.foo(demo, 1) == demo.foo.__func__(demo.foo.__self__, 1) 
```

看看**代碼**:

```python
demo  = Demo()

print('=== Demo start ===\n')

print('demo.foo', ':', demo.foo)
print('    [type             ] ', type(demo.foo))
print('    [demo.foo.__self__] ', demo.foo.__self__)
print('    [demo.foo.__func__] ', demo.foo.__func__)
print('    [demo.foo(1,2,3)  ] ', demo.foo(1,2,3))
print()

print('Demo.foo', ':', Demo.foo)
print('    [type                 ] ', type(Demo.foo))
print('    [Demo.foo(demo, 1,2,3)] ', Demo.foo(demo, 1,2,3))
print()

print('demo.foo.__func__', ':',  demo.foo.__func__,)
print('    [type                          ] ', type(demo.foo.__func__))
print('    [demo.foo.__func__(demo, 1,2,3)] ', demo.foo.__func__(demo, 1,2,3))
print()

print('Demo.foo is demo.foo.__func__ --> ', Demo.foo is demo.foo.__func__)
```

**測試結果**:

```python
=== Demo start ===

demo.foo : <bound method Demo.foo of <__main__.Demo object at 0x7f413db47fd0>>
    [type             ]  <class 'method'>
    [demo.foo.__self__]  <__main__.Demo object at 0x7f413db47fd0>
    [demo.foo.__func__]  <function Demo.foo at 0x7f413db41840>
    [demo.foo(1,2,3)  ]  Call foo by instance<__main__.Demo object at 0x7f413db47fd0>with args(1, 2, 3)

Demo.foo : <function Demo.foo at 0x7f413db41840>
    [type                 ]  <class 'function'>
    [Demo.foo(demo, 1,2,3)]  Call foo by instance<__main__.Demo object at 0x7f413db47fd0>with args(1, 2, 3)

demo.foo.__func__ : <function Demo.foo at 0x7f413db41840>
    [type                          ]  <class 'function'>
    [demo.foo.__func__(demo, 1,2,3)]  Call foo by instance<__main__.Demo object at 0x7f413db47fd0>with args(1, 2, 3)

Demo.foo is demo.foo.__func__ -->  True
```

接著看第二段:

>When an instance method object is derived from a class method object, the “class instance” stored in self will actually be the class itself, so that calling either x.f(1) or C.f(1) is equivalent to calling f(C,1) where f is the underlying function.

第二段的大意是說，當 instance method object 是來自於 class method object 的時候，存在 `self` 裡的 **類實例** 會是 **類** 本身，之後又舉了一個例子:

```python
x.f(1) == C.f(1) == f(C,1)  # x is an instance of C
```

我們一樣用範例來說明:

1. Python 對於 bar, 會產生 `Demo.bar` ，他是一個來自於 **class method object** 的 **bound method object**，原本 `Demo.bar` 就跟 `Demo.foo` 一樣是個一般的 Python function，但是透過修飾器(`@classmethod` 修飾器)，他成為了一個 bound method object，若要觀察原本的 general function，只能在 `Demo.bar.__func__` 中看到，同時他綁定了 `Demo` 類，所以 `Demo.bar.__self__` 會參考到 `Demo` 類。
2. 所以當 `Demo.bar` 被呼叫的時候(`Demo.bar(1)`)，，他其實會去呼叫 `Demo.bar.__func__`，並且以 `Demo.bar.__self__` (其實也就是 `Demo` 自己) 當作第一個參數。

以我們寫的類來展示的話，他的例子變成:

```python
   x.f(1)   ==    C.f(1)   == f(C, 1)
demo.bar(1) == Demo.bar(1) == Demo.bar.__func__(Demo, 1) == Demo.bar.__func__(Demo.bar.__self__, 1) 
```

**測試代碼**:

```python
demo  = Demo()

print('=== Demo start ===\n')

print('Demo.bar', ':', Demo.bar)
print('    [type             ] ', type(Demo.bar))
print('    [Demo.bar.__self__] ', Demo.bar.__self__)
print('    [Demo.bar.__func__] ', Demo.bar.__func__)
print('    [Demo.bar(1,2,3)  ] ', Demo.bar(1,2,3))
print()

print('Demo.bar(1)               ', Demo.bar(1))
print('demo.bar(1)               ', demo.bar(1))
print('Demo.bar.__func__(Demo, 1)', Demo.bar.__func__(Demo, 1))
```

**測試結果**:

```python
=== Demo start ===

Demo.bar : <bound method type.bar of <class '__main__.Demo'>>
    [type             ]  <class 'method'>
    [Demo.bar.__self__]  <class '__main__.Demo'>
    [Demo.bar.__func__]  <function Demo.bar at 0x7f413db41950>
    [Demo.bar(1,2,3)  ]  Call bar by class <class '__main__.Demo'>with args(1, 2, 3)

Demo.bar(1)                Call bar by class <class '__main__.Demo'>with args(1,)
demo.bar(1)                Call bar by class <class '__main__.Demo'>with args(1,)
Demo.bar.__func__(Demo, 1) Call bar by class <class '__main__.Demo'>with args(1,)
```

### 結論

1. 在 Python3 中，class 內有兩種 funciton，一種是一般的 function object，另外一種是 bound method object
2. instance method 是一般的 function 綁定了 instance 所構成的 method object，class mehtod 是一般的 function 綁定了 class 所構成的 method object
3. bound method 被調用的時候，其實都是調用最原始的 function (記在 `__func__` 中)，但會以綁定的對象作為第一個參數(記在 `__self__` 中)。

### 參考資料

1. [Difference between methods and functions][1]
2. [Different way to create an instance method object in Python][2]


  [1]: http://stackoverflow.com/questions/20981789/difference-between-methods-and-functions
  [2]: http://stackoverflow.com/questions/37370578/different-way-to-create-an-instance-method-object-in-python
