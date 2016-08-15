# 為什麼這兩段 python lambda 出現不同的結果

## 問題

寫了這樣一段代碼:

```python
[i(4) for i in [(lambda y: print('y=', y, '; x=', x, ' ; n + x = ', y + x)) for x in range(10)]]
```

發現輸出如下:

```
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
```

修改了一下:

```python
import functools
    
[f(4) for f in [functools.partial(lambda x, y: print('y=', y, '; x=', x, ' ; y + x = ', y + x), y) for y in range(10)]]
```

輸出如下:

```
y= 4 ; x= 0  ; y + x =  4
y= 4 ; x= 1  ; y + x =  5
y= 4 ; x= 2  ; y + x =  6
y= 4 ; x= 3  ; y + x =  7
y= 4 ; x= 4  ; y + x =  8
y= 4 ; x= 5  ; y + x =  9
y= 4 ; x= 6  ; y + x =  10
y= 4 ; x= 7  ; y + x =  11
y= 4 ; x= 8  ; y + x =  12
y= 4 ; x= 9  ; y + x =  13
```

不知道為什麼會有這樣的差異，請指教

問題出自 [segmentfault](https://segmentfault.com/q/1010000006121417/a-1020000006121940), by [kavlez](https://segmentfault.com/u/kavlez)

## 回答

你問的這個問題不是那麼好理解, 不過我慢慢說看看能接受多少。

### 第一段 code

首先我們看到你寫的第一段 code:

```python
[i(4) for i in [(lambda y: print('y=', y, '; x=', x, ' ; n + x = ', y + x)) for x in range(10)]]
```

我們先專心看內層的 list comprehension:

```python
funclist1 = [(lambda y: print('y=', y, '; x=', x, ' ; n + x = ', y + x)) for x in range(10)]
```

這段我們可以寫成一段等價的 code:

```python
def produce_functions():
    funclist = []
    for x in range(10):
        def ld(y):
            print('y=', y, '; x=', x, ' ; n + x = ', y + x)
        funclist.append(ld)
    return funclist
    
funclist2 = produce_functions()
```

我們隨意地來測試一下:

```python
>>> funclist1[0](4)
y= 4 ; x= 9  ; n + x =  13

>>> funclist2[0](4)
y= 4 ; x= 9  ; n + x =  13
```

希望大家看到這裡可以接受兩者除了一個用 lambda funciton 一個用 normal function 但是其實行為上是一致的。

接著請大家仔細看上面那段等價的 code, 你想到了甚麼呢? 沒錯! decorator 裡面會出現的 **閉包(closure)** !! 在這裡 `x` 不就是 **free variable** 嗎? 所以 `x` 並不會被綁死在 `ld` 中, 他參考到一個非全域的變數 `x`。我要說的是, 製造出來的 10  個 function 全部都參考到同一個 `x`, `for x in range(10)` 很容易誤導大家, 以為有十個不同的 `x` 然後製造了 10 個不同的 function。其實你跟我都明白, 這裡只有一個 `x` 變數, 只是他的值在改變, 但是說到底 `x` 就那麼一個。

為了避免空口說白話, 我證明我說的給大家看:

```python
>>> funclist1[0].__code__.co_freevars
('x',)
>>> funclist2[0].__code__.co_freevars
('x',)
```

好, 那 `x` 的值在製造完之後究竟是多少呢?

```python
>>> funclist2[0].__closure__
(<cell at 0x7f6e8ba22df8: int object at 0x9a34e0>,)

>>> funclist2[0].__closure__[0]
<cell at 0x7f6e8ba22df8: int object at 0x9a34e0>

>>> funclist2[0].__closure__[0].cell_contents
9
```

沒錯, 是 9 !, 所有所有製造出來的 function 全部都會參考到這個 `x`, 所以他們的 `x` 值就是 9 !

所以, 出現這個結果也就不意外了:

```python
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
y= 4 ; x= 9  ; n + x =  13
...
```

### 第二段 code

接著我們來看第二段 code (一樣 focus 在內層):

```python
import functools

[functools.partial(lambda x, y: print('y=', y, '; x=', x, ' ; y + x = ', y + x), y) for y in range(10)]
```

`partial(func, a)` 會凍結 `func` 的第一個引數(會綁定 a 值)

所以上面這段 code 會從 0~9 凍結這個 lambda function 的第一個引數, 這邊不同於 free variables, 這裡不是讓第一個引數 `x` 參考到同一個人, 而是直接綁死(代定) 0~9, 所以這裡每一個製造出來的 functions 全部都不一樣, 且可以當成 x 指定為 0~9。

經過上述講解, 應該大致可以明白兩者不同之處了。

### 結論

* `partial` 會直接凍結引數, 使變數代入定值
* 一般的 function 會直接參考到 free variable 而不是代入定值
