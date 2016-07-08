# Python 中字串的 bitwise or 怎麼實現？

## 問題

```
a="1000111000" 
b="1000000001" 
```

`a` 和 `b` 為字串

a bitwise or b 得到 `1000111001`

除了一位一位的處理，有沒有什麼方便的方法?

問題出自 [segmentfault](https://segmentfault.com/q/1010000005097274/a-1020000005099056), by [ffaniu](https://segmentfault.com/u/ffaniu)

## 回答

**代碼**:

```python
a = "1000111000"
b = "1000000001"
    
c = int(a, 2) | int(b, 2)
    
print('{0:b}'.format(c))
```

**結果**:

```
1000111001
```

**分析**:

運算符 `|` 本身就可以執行 bitwise 的運算，所以我們只要知道如何將 *字串* 轉為 *2進位整數* 以及如何將運算完的 *整數* 結果以 *2進位字串* 表示即可．

`int(a, 2)` 可以將整數或字串 `a` 轉為2進位整數(精準來說應該是讓 `a` 以 `2進位` 為基底進行整數轉換)，接著利用 `|` 進行 bitwise or，最後 `'{0:b}'.format(c)` 方法可以讓我們將數值進行 2進位 的格式化處理．

----------

**其他想法**:

有趣的是，如果我們一位一位處理，利用 generator comprehension 加上其他的一些 functional programming style 的技巧也能用簡短的一行完成任務:

```python
a = "1000111000"
b = "1000000001"
    
c = ''.join(str(int(ba) | int(bb)) for ba, bb in zip(a, b))
print(c)
```
