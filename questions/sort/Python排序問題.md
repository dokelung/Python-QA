# Python排序問題

## 問題

下面是題目要求: 

用 Python 實現函數 `count_words()`，該函數輸入字符串 `s` 和數字 `n`，返回 `s` 中 `n` 個出現頻率最高的單詞。返回值是一個元組列表，包含出現次數最高的 `n` 個單詞及其次數,即 [(<單詞1>, <次數1>), (<單詞2>, <次數2>), ... ] ，按出現次數降序排列。

您可以假設所有輸入都是小寫形式，並且不含標點符號或其他字符（只包含字母和單個空格）。如果出現次數相同，則按字母順序排列。

例如：

```python
print(count_words( "betty bought a bit of butter but the butter was bitter" , 3 ))
```

輸出：

```python
[('butter', 2 ), ('a', 1 ), ('betty', 1 )]
```

我已經按照單詞出現頻率排好了順序，但是怎麼在這基礎上再實現字母排序？

問題出自 [segmentfault](https://segmentfault.com/q/1010000005821181/a-1020000005822587), by [marsggbo](https://segmentfault.com/u/marsggbo)

## 回答

這應該滿足你的條件，只是我自認為寫得很醜，等有時間再優化吧:

(改了一下 code 這樣做比較好!)

```python
import collections

def count_words(s, n):
    lst = collections.Counter(s.split()).most_common()
    lst.sort(key=lambda t: t[0])
    lst.sort(key=lambda t: t[1], reverse=True)
    return lst[0:n]

print(count_words("betty bought a bit of butter but the butter was bitter", 3))
```

想了一想，覺得下面更好:

```python
import collections

def count_words(s, n):
    lst = collections.Counter(s.split()).most_common()
    lst.sort(key=lambda t: (-t[1], t[0]))
    return lst[0:n]

print(count_words("betty bought a bit of butter but the butter was bitter", 3))
```
