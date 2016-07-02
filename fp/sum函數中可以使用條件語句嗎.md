# sum 函數中可以使用條件語句嗎

## 問題

我在學習協同過濾，遇到這樣一段代碼

```python
def sim_distance(prefs,person1,person2):
    # Get the list of shared_items
    si={}
    for item in prefs[person1]: 
        if item in prefs[person2]: si[item]=1
    
    # if they have no ratings in common, return 0
    if len(si)==0: 
        return 0
    
    # Add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                        for item in prefs[person1] if item in prefs[person2]])
    
    return 1/(1+sum_of_squares)
```

比較困惑的是下面這段代碼，為什麼sum裡面可以寫for 循環呢，這個是什麼意思，為什麼我寫了個類似的函數就會報錯

```python
sum([pow(prefs[person1][item]-prefs[person2][item],2) 
      for item in prefs[person1] if item in prefs[person2]])
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005666851/a-1020000005669415), by [pennyboarding](https://segmentfault.com/u/pennyboarding)

## 回答

這邊的 `for` 或是 `if` 都跟 `sum` 本身沒有什麼關係，如同 @大鹌鹑 所說，`sum` 接受一個可迭代的對象作為參數．

至於這個例子中的可迭代對象就一個 **使用 list comprehension 產生的 list**。

### list comprehension

那就稍為介紹一下 list comprehension(串列產生式) 好了。

這是一個帶有 **functional programming** 味道的語法，直覺而優雅。

顧名思義，他是為了產生 **串列** 而被使用。

因此有一個重要的原則就是: 

> 當今天代碼的目的是為了要生成一個 list ，那我們應當考慮使用他，否則完全不應該使用

我們來看一下用法，非常簡單的，為了生成串列，所以我們字面上使用兩個成對的中括號 `[]` ( list 的字面產生語法)，夾住一個 `for...in...` 迭代式，利用 `for` 走訪到的元素會被依序用來製造 list 中的各個元素。

讓我們看例子，假設今天我們有一個整數的串列 `lst`，我們想要製造另外一個串列 `lst2`，其中的每個元素都是 `lst` 中元素的平方:

```python
lst = [1, 2, 3, 4]
lst2 = []

for i in lst:
    lst2.append(i**2)
``` 

我們使用了一個標準的 `for...in...` 迴圈來作到這件事，但同樣的事情，我們能夠用 **list comprehension** 作得更簡潔更優雅:

```python
lst = [1, 2, 3, 4]
lst2 = [i**2 for i in lst]
``` 

在這個例子中，`for i in lst` 會依序取出 `lst` 中的元素進行平方運算後成為 `lst2` 的新元素。 

### map

這讓人聯想到 `map` function，我們同樣可以使用 **映射** 來作到類似的效果:

```python
lst = [1, 2, 3, 4]
lst2 = map(lambda x:x**2, lst)  # Python2
lst2 = list(map(lambda x:x**2, lst))  # Python3
```

`map` 會依序走訪他第二個參數(一個可迭代對象)中的元素，並且將元素作為引數，調用他的第一個參數(一個單參數函數)，也就是會依序取出 1, 2, 3 ,4 然後將之當成參數 `x` 調用匿名函數 `lambda x:x**2`。

但我們可以發現 list comprehension 更加直覺，我們可以說 list comprehension 中的 `for`述句就是在 `map` 的良好替代品。

### filter

說到 `map` 就會想到 `filter`，他會對可迭代物件進行過濾的動作。

比如說我想讓 `lst2` 裡面只出現奇數:

```python
lst = [1, 2, 3, 4]
lst2 = filter(lambda x:x%2!=0, map(lambda x:x**2, lst))  # Python2
lst2 = list(filter(lambda x:x%2!=0, map(lambda x:x**2, lst)))  # Python3
```

`filter` 一樣會去走訪他的第二個參數(一個可迭代對象)，並依序取出當成引數，調用他的第一個參數(一個單參數函數)，若運算的結果為真( `True` )，則保留此回傳值作為新的元素，反之( `False` )會被過濾掉。

而現在 `filter` 也有了替代品，就是 list comprehension，我們可以這樣寫:

```python
lst = [1, 2, 3, 4]
lst2 = [i**2 for i in lst if i%2!=0]
```

同樣也是簡單許多! 我們可以說 list comprehension 中的 `if` 述句就是 `filter` 的良好替代品。

看到這裡，相信你已經明白:

```python
sum([pow(prefs[person1][item]-prefs[person2][item],2) 
        for item in prefs[person1] if item in prefs[person2]])
```

這段代碼，是先執行了一個含有 `for...in...` 述句和 `if` 述句的 list comprehension 來產生 list 後，才以該 list 作為引數調用 `sum` 函數。

### 結論

1. `for...in...` 和 `if` 與 `sum` 沒有直接關係。
2. `for...in...` 和 `if` 是 list comprehension 的關鍵語法。
3. list comprehension 可以幫助我們使用可迭代對象產生 list。
4. list comprehension 是 `map` 和 `filter` 的良好替代品。
