# 關於 python * 和 ** 的問題

## 問題

`*` 和 `**` 為可變形參，但是平時在使用的時候感覺很少能有使用到的情況，有些不是很理解它們的用法和用處場景？
而且形參不是可以傳遞任意類型麼？這樣我寫成:

```python
a = (1,2,3,4)
def test(a):
    print a
    print a[1]
```

加不加 `*` 貌似沒什麼區別？字典也是一樣只不過變成 `print['keyname']` 而已。
那麼 `*` 和 `**` 這玩意到底有什麼用呢？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006075094/a-1020000006075616), by [msia121](https://segmentfault.com/u/msia121)

## 回答

這兩個東西可是相當有用的呢!

舉幾個例子示範一下

### 用於 function arguments 時

假設有個 function `intro`:

```python
def intro(name, age, city, language):
    print('I am {}. I am {} years old. I live in {}. I love {}'.format(
        name, age, city, language
    ))
```

今天我給你一組 list 的 data `lst` 和 dict 的 data `dic`:

```python
lst = ['dokelung', 27, 'Taipei', 'Python']
dic = {'name': 'dokelung', 'age': 27, 'city': 'Taipei', 'language': 'Python'}
```

不用 `*` 或 `**` 你可能要:

```python
test(lst[0], lst[1], lst[2], lst[3])
test(dic['name'], dic['age'], dic['city'], dic['language'])
```

使用 `*` 和 `**`:

```python
test(*lst)
test(**dic)
```

### 用於 function params 時

今天我們要寫一個加法 function:

```python
def add2(a, b):
    return a + b
```

如果要擴充到三個數相乘:

```python
def add3(a, b, c):
    return a + b + c
```

這邊有兩個問題: 
* 一個是參數列可能很長
* 一個是 Python 不允許多載, 所以不能使用同一個 function name

但是 `*` 可以解決這個問題:

```python
def add(*n):
    return sum(n)
```

當然你可能覺得這邊我也可以設計成參數是 list 或 tuple, 但有些時候這樣的做法比較方便, 你可以參考一下 `print` 的概念(Python3的):

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
      ^^^^^^^^
```

這邊的概念就是這樣

其次, 這個做法是寫 decorator 的基礎:

```python
def mydeco(func):
    def newfunc(*args, **kwargs):
        return func(*args, **kwargs)
    return newfunc
```

因為不使用這種做法, 你無法應對要修飾的 function 可能千奇百怪的參數

## 用於 tuple unpacking 時 (Python3)

這個功能很實用:

```python
>>> t = ('start', 1 ,2 ,3 ,4 ,5, 'end')
>>> s, *nums, e = t
>>> s, nums, e
('start', [1, 2, 3, 4, 5], 'end')
```

### 結論

其實妙處不只這些, 只等待你去發現!

### 補充

我覺得會有無用之感很大的一點在於我們常陷入一種思考情境:

> 寫 function 的人 跟 用 function 的人是同一人, 也就是我

因為如果寫跟用為同一人, 那麼介面怎麼設計當然可以很自由, 選用 `*` 或是直接用 list 都沒差

但當今天我們是使用別人的 API 或是要寫 function 給別人用時, 就沒那麼大的彈性了

這個時候, `*` 可以幫助我們許多
