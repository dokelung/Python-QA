# Python如何向文件最開始插入一個字串

## 問題

Python 如何向文件最開始插入一個字串，在 **盡量保證性能** 的情況下。

問題出自 [segmentfault](https://segmentfault.com/q/1010000005890090/a-1020000005894627), by [galaxy_21](https://segmentfault.com/u/galaxy_21)

## 回答

分兩點來探討這個問題:

1. 如何有效率的來插入內容到檔案的頭或中間，有效率指的是較少的時間(較快的速度)與資源利用．
2. 如何能夠寫出足夠 pythonic 的 code 來處理這件事

我先說我的結論(如果有任何其他看法歡迎討論，也許我是錯的):

1. 做不到
2. 只要不是寫得太糟或太難閱讀，我覺得平庸一點或是較長的 code 也無妨(甚至更好)

引大神的話來佐證一下:

> Python makes a lot of things easy and contains libraries and wrappers for a lot of common operations, but the goal is not to hide fundamental truths.
>
> The fundamental truth you are encountering here is that you generally can't prepend data to an existing flat structure without rewriting the entire structure. This is true regardless of language.
>
> There are ways to save a filehandle or make your code less readable, many of which are provided in other answers, but none change the fundamental operation: You must read in the existing file, then write out the data you want to prepend, followed by the existing data you read in.
>
> By all means save yourself the filehandle, but don't go looking to pack this operation into as few lines of code as possible. In fact, never go looking for the fewest lines of code -- that's obfuscation, not programming.
>
> By ***Nicholas Knight***

參考資料：

[Prepend a line to an existing file in Python](http://stackoverflow.com/questions/4454298/prepend-a-line-to-an-existing-file-in-python)
