# Top K Frequent Elements

## 問題

```
[('d', 100), ('c', 99), ('a', 89), ('b', 86)]
```

如何快速得出:

```
['d', 'c', 'a', 'b']
```

感覺好 low, 有什麼好的辦法嗎？
其實在用 Python 中在刷 leetcode 來學習
[題目](https://leetcode.com/problems/top-k-frequent-elements/)

```python
class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]          
        :type k: int
        :rtype: List[int]
        """
        items = {}
        for item in nums:
            if items.has_key(item):
                items[item]+=1
            else:
                items[item]=1
        arr1 = sorted(items.iteritems(), key=lambda asd:asd[1], reverse=True)
        arr2 = []
        for key in range(len(arr1)):
            arr2.append(arr1[key][0])
        return arr2[0:k]
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005087747/a-1020000005088335), by [cosde](https://segmentfault.com/u/cosde)

## 回答

很簡單，使用 list comprehension 即可:

```python
arr1 = [('d', 100), ('c', 99), ('a', 89), ('b', 86)]
arr2 = [pair[0] for pair in arr1]
```

看了一下你原本的問題，寫了一個簡潔的版本，可以參考一下:
(適用於 Python2.7+, Python3)

```python
from collections import Counter
    
def top_k_frequent(lst, k):
    return [key for key, count in Counter(lst).most_common(k)]
```

**使用**:

```python
lst = [1, 1, 1, 2, 3, 4, 4]
print(top_k_frequent(lst, 2))
```

**效果**:

```
[1, 4]
``` 

**說明**:

Python2.7+之後的版本，在 `collections` 庫裡有一種類 `Counter` 可以用。
詳細的操作方法請參考[Counter object][1]
    
利用 `Counter(lst)` 可以輕鬆得到一個 `Counter`實例，裡面已經對 `lst` 中的元素作過統計了。
之後利用 `most_common(k)` 方法可以輕鬆得到一個排序過的 list of tuple，而且只會剩下前出現頻率前k高的項目，最後用 `list comprehension` 取出元素本身:

```python
>>> from collections import Counter
>>> counter = Counter([1, 1, 1, 2, 3, 4, 4])
>>> counter
Counter({1: 3, 4: 2, 2: 1, 3: 1})
>>> most_items = counter.most_common(2)
>>> most_items
[(1, 3), (4, 2)]
>>> [key for key, count in most_items]
[1, 4]
```

  [1]: https://docs.python.org/2/library/collections.html#counter-objects
