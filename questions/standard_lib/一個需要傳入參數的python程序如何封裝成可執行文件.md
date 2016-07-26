# 一個需要傳入參數的 python 程序，如何封裝成可執行文件

## 問題

我已經寫好一個 python 程序功能是搜索一段時間範圍內的信息，程序需要傳入參數，即開始和結束的時間。

目前想把這個程序封裝成一個可執行文件，這樣其他人拿到程序後在自己電腦上就可以直接跑了，以前用 pyinstaller 試過將 .py 文件轉換成 .exe 文件，不過碰到需要傳參數的情況好像就不適用了。
想請問大家是否有相關的教程或者工具，將 .py 文件轉化為一個可手動輸入參數(比如時間）的可執行文件？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006008157), by [desertfoxx](https://segmentfault.com/u/desertfoxx)

## 回答

command line 介面下簡單來說三種方法:

1. 用 `input` 去問使用者
2. 用 `sys.argv`
3. 用一些 package/module, 像是 [argparse](https://docs.python.org/3.5/library/argparse.html) 或 [clime](http://clime.mosky.tw/)

示範一下 **第二點**:

假設你的 python file 叫 `test.py`

```python
import sys
print(sys.argv)
```

運行:

```
$ python test.py hello world 2016-07-01 12:30
['test.py', 'hello', 'world', '2016-07-01', '12:30']
```
