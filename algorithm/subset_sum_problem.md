# Subset-Sum Problem

## 問題

給定一個值, 如100，給定一個 list，從 list 中挑選出 N 個元素，這 N 個元素相加也是 100，得到一種結果就行．

舉例: 給定一個 list：

```python
lst = [ 99.1 , 92.2 , 60 , 50 ,
        49.5 , 45.7 , 25.1 , 20 , 
        17.4 , 13 , 10 , 7 , 2.1 , 2 , 1 ]
```

找到和為100的數組元素：

```
[ 60 , 20 , 10 , 7 , 2 , 1 ]
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005696393/a-1020000005702007), by [輕逐微風](https://segmentfault.com/u/hare)

## 回答

來個 Python 版的:

```python
def subsetsum(elements, target):
    if target==0:
        return True, []
    elif not elements or target < 0:
        return False, None

    result, subset = subsetsum(elements[:-1], target-elements[-1])
    return (True, subset + [elements[-1]]) if result else subsetsum(elements[:-1], target)
```

思路很簡單，當我要問 `elements` 是否能加出 `target` 時，只有兩種可能:

1. 我要使用 `element[-1]` 才能加出 `target` -> 我要能夠使用 `elements[:-1]` 加出 `target-elements[-1]` 才行
2. 我不需要使用 `element[-1]` 就能加出 `target` -> 我要能夠使用 `elements[:-1]` 加出 `target` 才行

boundary condition 是:

1. 當 `target` 為 `0` 時，代表我什麼都不用就能加出來，所以 `return True, []`
2. 當 `elements` 為空或是 `target` 為負值時，代表永遠都加不出來了，所以 `return False, None`

**測試**:

```python
elements = [99.1, 92.2, 60, 50, 49.5, 45.7, 25.1, 20, 17.4, 13, 10, 7, 2.1, 2, 1]
target = 100
result, subset = subsetsum(elements, target)
print(result, subset)
```

**結果**:

```python
True [60, 20, 10, 7, 2, 1]
```

### 衍生問題

題外話，看到這個題目覺得超熟悉，如果還要考慮到解的速度等等會更有趣。

曾經做過這方面的研究，我提出一個變形的問題，大家可以思考看看:


>我們今天給定一個整數(代表負數也 ok )的 多重集 (多重集就是一個集合，但是允許元素重複出現)，叫做 ` elements`，在給定另外一個整數的 多重集 叫做 `targets`，試問是否存在若干個 子多重集，每個 子多重集 的元素和恰好有一個在 `targets` 中對應的 target。


定義看不懂沒差，我舉個例子:

```
elements = (1,4,6,4,1)
targets = (5,10,1)
```

這個例子是有解的:

```
(1,4) -> 5
(4,6) -> 10
(1) -> 1
```

注意，每個在 `elements` 中的元素只能被使用一次!
