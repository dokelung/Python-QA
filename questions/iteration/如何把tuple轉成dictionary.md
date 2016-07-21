# 如何把 tuple 轉成 dictionary

## 問題

我有一個 tuple list:

![clipboard.png](https://segmentfault.com/img/bVzgCO)

現在我想把這組 tuples 變成 dictionary 的 list, 類似的效果是這樣:

```python
meat = [
    {
    "地區詞":"深圳福田區",
    "品牌詞":"TTM全身體檢",
    "疑問詞":"地址怎麼走",
    "價格詞":"價格要多少錢"
    },
    {
    "地區詞":"深圳保安區",
    "品牌詞":"TTM全身體檢",
    "疑問詞":"地址怎麼走",
    "價格詞":"要做多少項目"
    },
    .....
        ]
```

有什麼比較方便的方法?

問題出自 [segmentfault](https://segmentfault.com/q/1010000005983046/a-1020000005983077), by [jqlts1](https://segmentfault.com/u/jqlts1)

## 回答

```python
names = 'area brand question price'.split()
lst = [{name:value for name, value in zip(names, t)} for t in tlst]
```

測試:

```python
tlst = [('a1','b1','q1','p1'),
        ('a2','b2','q2','p2'),
        ('a3','b3','q3','p3')]
 
names = 'area brand question price'.split()
lst = [{name:value for name, value in zip(names, t)} for t in tlst]

print(lst)
```

結果:

```python
[{'brand': 'b1', 'area': 'a1', 'question': 'q1', 'price': 'p1'}, {'brand': 'b2', 'area': 'a2', 'question': 'q2', 'price': 'p2'}, {'brand': 'b3', 'area': 'a3', 'question': 'q3', 'price': 'p3'}]
```

改良(by [hsfzxjy](https://segmentfault.com/u/hsfzxjy):

```python
names = 'area brand question price'.split()
lst = [dict(zip(names, t)) for t in tlst]
```
