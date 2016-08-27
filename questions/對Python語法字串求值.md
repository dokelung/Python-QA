# 對 Python 語法字串求值

## 問題

讀 csv 文件的時候讀到這樣的 str：

```python
["item1", "item2", "item3"]
```

顯然這是一個 list 
可是我該如何把它轉化成 list 呢?
用 `list()` 的話每個字符會被當成一個 item 
用切詞的方法也應該可以但會麻煩
但是有沒有直接的方法呢？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006152237/a-1020000006152877), by [persona](https://segmentfault.com/u/persona)

## 回答

使用 `eval`, 不過要小心他的風險：

```python
In [1]: s = '["item1", "item2", "item3"]'

In [2]: lst = eval(s)

In [3]: lst
Out[3]: ['item1', 'item2', 'item3']
```

* [Python doc - eval](https://docs.python.org/3/library/functions.html#eval)

對於 Python 的 subset 進行求值, 使用 `ast.literal_eval` 是對的。


```python
# by manong
>>> import ast
>>> ast.literal_eval('["item1", "item2", "item3"]')
['item1', 'item2', 'item3']
```

下面文章值得一讀:

[Using python's eval() vs. ast.literal_eval()?](http://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval)
