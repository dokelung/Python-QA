# Python 獲取文件路徑及文件目錄(`__file__` 的使用方法)

## 問題

我正在學習Python，不過遇到一些問題，想請教:

`os` module 中的 `os.path.dirname(__file__)` 和 `os.path.abspath(__file__)`

運行 `os.path.dirname(__file__)` 時候，為什麼返回的是空白呢? 是不是因為他運行的是相對路徑???

如果是的話: 

1. 我怎麼能夠知道，括號內的文件是以相對路徑還是絕對路徑被運行的?
2. 為什麼我運行下面例子腳本的時候，這個文件是以相對路徑被運行的呢?

比如我下面的例子:

```python
import os
    
print (os.path.dirname(__file__))
print (os.path.abspath(__file__))
print (os.path.abspath(os.path.dirname(__file__)))
print (os.path.dirname(os.path.abspath(__file__)))
```

![测试][1]
  [1]: https://segmentfault.com/img/bVzRXy

PS:附加問題
`os.path.abspath(os.path.dirname(__file__))` 和 `os.path.dirname(os.path.abspath(__file__))` 性質是否一樣呢？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006126582/a-1020000006127638), by [nodinner](https://segmentfault.com/u/nodinner)

## 回答

建議你可以稍微瀏覽一下 Python doc: [os.path](https://docs.python.org/3.5/library/os.path.html), 你就會明白囉:

我放上跟你問題相關的幾個條目:

* `os.path.abspath(path)`
 * Return a normalized absolutized version of the pathname path. On most platforms, this is equivalent to calling the function normpath() as follows: normpath(join(os.getcwd(), path)).

* `os.path.normpath(path)`
 * Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase().

* `os.path.dirname(path)`
  * Return the directory name of pathname path. This is the first element of the pair returned by passing path to the function split().

* `os.path.split(path)`
 * Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty. Trailing slashes are stripped from head unless it is the root (one or more slashes only). In all cases, join(head, tail) returns a path to the same location as path (but the strings may differ). Also see the functions dirname() and basename().

我們做以下觀察:

`test.py`

```python
import os

print(__file__)
print(os.path.dirname(__file__))
print(os.path.abspath(__file__))
print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
```

運行:

```
$ pwd
/home/dokelung
$ python test.py
```

結果:

```
test.py

/home/dokelung/test.py
/home/dokelung
/home/dokelung
```

首先 `__file__` 的值其實就是在命令列上 invoke Python 時給的 script 名稱:

```python
$ python test.py          # 此時 __file__ 是 test.py
$ python ../test.py       # 此時 __file__ 是 ../test.py
$ python hello/../test.py # 此時 __file__ 是 hello/../test.py
```

在這裡, 因為 `__file__` 的值為 `test.py`, 所以 `print(__file__)` 的結果是 `test.py` 也就不意外了。

接著, `os.path.dirname(__file__)`之所以得出空白(空字串), 是因為 `__file__` 就只是一個單純的名稱(非路徑) 且 `dirname` 也只是很單純的利用 `os.path.split()` 來切割這個名稱(這當然沒甚麼好切的, 連路徑分割符都沒有):

```python
>>> import os
>>> os.path.split('test.py')
('', 'test.py')
>>> os.path.split('test.py')[0]
''
```

我分會發現切出來的 `head` 是空字串, 所以 `dirname` 的結果是空白。

`abspath` 動用了 `os.getcwd()` 所以即便給定的是單純的名稱, 也能返回路徑:

```python
>>> os.getcwd()
'/home/dokelung'

>>> os.path.join(os.getcwd(), 'test.py')
'/home/dokelung/test.py'

>>> os.path.normpath(os.path.join(os.getcwd(), 'test.py'))
'/home/dokelung/test.py'
```

而 `os.path.abspath(os.path.dirname(__file__))` 的結果就等於是 `os.getcwd()` 的結果去接上 `dirname` 得到的空字串:

```python
>>> os.path.dirname('test.py')
''

>>> os.path.join(os.getcwd(), os.path.dirname('test.py'))
'/home/dokelung/'
```

最後, `os.path.dirname(os.path.abspath(__file__))` 的結果是這麼來的:

```python
>>> os.path.abspath('test.py')
'/home/dokelung/test.py'

>>> os.path.split(os.path.abspath('test.py'))
('/home/dokelung', 'test.py')

>>> os.path.split(os.path.abspath('test.py'))[0]
'/home/dokelung'
```

希望講到這裡有讓你明白!

## 結論
現在簡要的回答你的問題

1. 為什麼 `dirname` 出現空白?
 * 因為你運行的時候給的是單純的名稱, 所以 `__file__` 是單純的名字非路徑

2. 我怎么能够知道，括号内的文件是以相对路径还是绝对路径被运行的？
 * 很簡單, 就看你怎麼運行 Python 的

3. 为什么我运行下面例子脚本的时候，这个文件是以相对路径被运行的呢？
 * 因為 `$ python 1.py` 你自己給了相對路徑

4. `os.path.abspath(os.path.dirname(__file__))` 和 `os.path.dirname(os.path.abspath(__file__))` 性质是否一样呢？
 * 基本上一樣
