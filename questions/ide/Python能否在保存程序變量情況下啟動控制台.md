# Python 能否在保存程序變量情況下啟動控制台

## 問題

類似於 matlab 可以在程序完成後直接在控制台操作變量，而不是啟動一個獨立的控制台程序，不知道有沒有哪款 Python 的 ide 支持這種行為

問題出自 [segmentfault](https://segmentfault.com/q/1010000005897684/a-1020000005906439), by [mzmssg](https://segmentfault.com/u/mzmssg)

## 回答

Python 自帶的 IDLE 就可以做到了，你開啟一個 python file 後 run module，你會發現主控台上可以操控 file 中的 variable 

-----

Pycharm 的部分我自己試了一下，你進到 `Run/Edit Configurations...`

![图片描述][1]

然後把 `Interpreter options` 加入 `-i` 的選項:

![图片描述][2]

之後運行 script 完畢，shell 會 keep 在那邊不會結束

-----

其實不需要 ide 就可以做到你想做的了

假設你有一個 python script `test.py`

```python
a = 5
b = [1, 2, 3]
```

直接用:

```
$ python -i test.py
```

運行 `test.py` 完畢後，Python 會停在 console 中可以繼續互動

或是用:

```
$ python
```

開啟 python shell 後，用 `import` 匯入 test 並執行，接著你就可以操控 variable 了:

```
>>> from test import *
>>> a
5
>>> b
[1, 2, 3]
```

這也有同樣效果

  [1]: https://segmentfault.com/img/bVyYF6
  [2]: https://segmentfault.com/img/bVyYFI
