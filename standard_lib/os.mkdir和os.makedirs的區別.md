# os.mkdir 和 os.makedirs 的區別

## 問題

* 語言: Python2.7
* IDE: Pycharm
* os: Linux

用Python做的爬蟲 :

* 第一個建立在project folder下用os.mkdir('home/img/')創建文件夾存儲數據,文件夾正常建立
* 第二個加入RedisQueue，爬蟲程序放在/usr/lib/python2.7 , rq主體放在project folder下面,在爬蟲程序裡面用os.mkdir('home/img/')報錯，用os.makedirs( 'home/img/')正常建立。

為什麼第一個沒有報錯？

thx in advance

問題出自 [segmentfault](https://segmentfault.com/q/1010000005770628/a-1020000005770966), by [shuanglu1993](https://segmentfault.com/u/shuanglu1993)

## 回答

[os.mkdir][1] 與 [os.makedirs][2] 的差別在於 `os.makedirs` 會遞迴地去建立目錄，也就是說連同中繼的目錄也會一起建立，就類似於 Linux 中的 `mkdir -p`．

```python
>>> import os
>>> os.mkdir('foo/bar')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 2] No such file or directory: 'foo/bar'
>>> os.makedirs('foo/bar')
```

使用 `os.mkdir` 時，如果你給定的 path 參數是個多層的 path，如果某個中繼的目錄不存在(比如說上例中的 `foo`), Python 將會報錯．

但如果使用 `os.makedirs` 則 Python 會連同中間的目錄一起建立．但有一點值得注意，當 path 末端的目錄已經存在的話，`os.makedirs` 也是會引發例外．

我想你的問題就在這裡，你可以檢查 `home` 目錄一開始是否存在．

要注意的是，這邊的路徑認定是要看你啟動 Python 直譯器的地方，也就是說你要確定你運行 `python` 所在的目錄下面要有 `home` 才能避免 `os.mkdir` 出錯．

  [1]: https://docs.python.org/2/library/os.html#os.mkdir
  [2]: https://docs.python.org/2/library/os.html#os.makedirs
