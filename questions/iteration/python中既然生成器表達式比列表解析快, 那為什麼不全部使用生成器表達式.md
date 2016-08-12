# python 中既然生成器表達式比列表解析快, 那為什麼不全部使用生成器表達式

## 問題

python 中既然生成器表達式比列表解析快？那為什麼不全部使用生成器表達式？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006099706), by [昌维001](https://segmentfault.com/u/changwei)

## 回答

generator 的 lazy evaluation (惰性求值) 當然是能盡量用就盡量用, 但有的時候這是不太有意義的, 比如說:

1. 最後你還是要一個列表
2. 你需要排序

關於第一點很好明白, generator 只能夠 iterate 卻不具備大部分的 list 能力:

```python
>>> I = [5 ,3, 1, 6, 2]
>>> genexp = (i for i in I)

>>> genexp[0]  # generator 不支援 __getitem__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'generator' object has no attribute '__getitem__'

>>> genexp + [9, 9, 9]  # generator 不支援列表串接
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'generator' and 'list'
```

諸如此類...

那可能觀眾會想問, 那這樣就好了阿:

```python
>>> list(genexp)
```

那這樣子跟直接用 list comprehension 有差嗎? (還真的有差! 你白做工了)

其實第二點跟第一點類似, 不過你可能會想要反駁:

```python
>>> sorted(genexp)
[1, 2, 3, 5, 6]
```

這不是好好的嗎? 沒錯, sorted 支援任何 iterables 的輸入, 但是

> 要排序, 所有的項目都必須要被求值

也就是說, 惰性求值完全沒有派上用場, 這個時候還不如直接用 list 來的乾脆。

最後 @Maslino 有提到一很重要的一點, generator 是會耗盡的, 是一次使用性的, 所以要反覆使用多次的話只能夠依靠 generator function:

```python
def gen():
    for i in range(10):
        yield i
```

或者 return genexp 的 function:

```python
def gen():
    return (i for i in range(10))
```

然後:

```python
for i in gen():
    print(i)
```

這樣就可以反覆多次使用了

但這樣做是好還是壞還要看情況而定, 大多數的時候直接用 list 會比較容易

### 結論 (有點複雜, 如果看不懂可以再討論)

**generator** (這裡指一般的 generator 而非 genexp) 用在:

1. 追求效率所以希望使用惰性求值, on-the-fly 的 evaluate, 省空間也避免一口氣過多求值
2. 對於無限無窮的 iteration, 一般的 iterables 是辦不到的
3. generator 可以憑空生出值來, 一般的 iterator 不行 (generator 也是 iterator)

關於 2, 3 兩點我覺得比較不適用在 generator expression 上面, generator expression 我想最大的用途就在於上述的第一點!

撇開這三點, 使用 list 可能是比較簡單的, 但 **如果是 list comprehension 跟 generator expression 比** , 那我覺得只需要考慮第一點的情況來決定就好。

觀念澄清一下:

> generator 是 iterator, 反之不一定, iterator 是 iterables, 反之不一定 
