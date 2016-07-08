# Python 如何實現並行查找關鍵字所在的行

## 問題

我有幾十萬個關鍵字放在文件 `4.txt` 中，想提取文件 `3.txt` 中含有關鍵字的行，保存到文件 `5.txt` 中. 
文件 3 有 200 萬行，我使用下面的代碼可以實現我的要求，但是非常慢，一個下午還沒運行完，誰有快一點的方法？
使用並行改如何改造呢？我看到這裡有個[並行的帖子](http://www.oschina.net/translate/python-parallelism-in-one-line)，與我的不同的事，我要同時讀以及查詢同一個文件，上述鏈接可以並行操作多個文件。

```python
with open('3.txt', 'r') as f3, open('4.txt', 'r') as f4, open('result.txt', 'w') as f5:
    a = [line.strip() for line in f4.readlines()]
    for li in f3.readlines():
        new_line = li.strip().split()[1][:-2]
        for i in a:
            if i in new_line:
                f5.writelines(li)
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005137716/a-1020000005138325), by [biopython](https://segmentfault.com/u/biopython)
  
## 回答

因為沒有實際的文件，沒有辦法給你一個百分之百的保證，不過對於你的 code，我有一些些效率改進上的建議:

(也許你會發現改進後的代碼根本不需要使用並行的解決的方案)

首先一個很大的問題是 `readlines()`，這個方法會一口氣讀取 file objects 中的所有行，這對於效率和資源的使用顯然是極差的，幾十萬行幾百萬行的東西要一口氣讀**完**了，這可是非常恐怖的．

詳細的分析和討論請參考[Never call readlines() on a file][1]

(文章中的這段話幾乎可當作是警語了)
> There are hundreds of questions on places like StackOverflow about the readlines method, and in every case, the answer is the same.
> "My code is takes forever before it even gets started, but it's pretty fast once it gets going."
> **That's because you're calling readlines**.
> "My code seems to be worse than linear on the size of the input, even though it's just a simple loop."
> **That's because you're calling readlines**.
> "My code can't handle giant files because it runs out of memory."
> **That's because you're calling readlines**.

結論是: **建議所有使用 `readlines` 的地方全部改掉**．

範例:

```python
with open('XXX', 'r') as f:
    for line in f.readlines():
       # do something...
```

一律改成:

```python
with open('XXX', 'r') as f:
    for line in f:
       # do something...
```

直覺上效率會好很多．

其次，你使用了 list 來查找關鍵字，這也是相當沒效率的:

```python
for i in a:
    if i in new_line:
```

為了確認 `new_line` 中是否有關鍵字 `i`，這邊走訪了一整個關鍵字 list: `a`，對於一般的情況可能還好，但是數十萬的關鍵字比對，對每一行都走訪一次 `a` 會造成大量的時間浪費，假設 `a` 裡面有 x 個關鍵字，`f3` 中有 y 行，每行有 z 個字，這邊要花的時間就是 `x*y*z`(根據你文件的行數，這個數量級極為驚人)．

如果簡單地利用一些使用 hash 來查找的容器肯定會好一些，比如說 `dictionary` 或是 `set`．

最後是關於你的查找部分:

```python
for li in f3.readlines():
    new_line = li.strip().split()[1][:-2]
    for i in a:
        if i in new_line:
            f5.writelines(li)
```

這邊我不是很懂，`new_line` 看起來是一個子字串，然後現在要用這個字串去比對關鍵字？

不過先撇開這個不談，關於含有關鍵字的 `new_line` 在印出後，似乎不該繼續循環 `a`，除非你的意思是 `new_line` 中有幾個關鍵字我就要印 `line` 幾次． 否則加上一個 `break` 也是可以加快速度．

建議你的code改為:

```python
with open('3.txt') as f3, open('4.txt') as f4, open('result.txt', 'w') as f5:
    keywords = set(line.strip() for line in f4)
    for line in f3:
        new_line = line.strip().split()[1][:-2]
        for word in new_line:
            if word in keywords:
                print(line, file=f5)
                break
```

如果我有弄錯你的意思，歡迎跟我說，我們再來討論一下，直覺上應該不必使用到並行就可以解決你的問題

  [1]: http://stupidpythonideas.blogspot.tw/2013/06/readlines-considered-silly.html
