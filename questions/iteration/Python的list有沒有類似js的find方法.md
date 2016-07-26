# Python 的 list 有沒有類似 js 的 find 方法

## 問題

js 的 array 中的 `find` 寫法很帥

假設我有一個 array, 是 array of objects:

```javascript
sample_list = [{key: 1, value: 'a'}, {key: 2, value: 'b'}]
```

js 可以這樣找到 `key=1` 的元素:

```javascript
sample_list.find((data)=>{return data.key == 1})
```

python 有沒有類似的東西呢? 
我只看到了 `index`, 但是這個 `index` 只能找值類型的,引用類型的用 `index` 很麻煩. 
有沒有比較好的辦法呢?

我現在知道的方法有這幾個:

```python
[i for i in sample_list if i.get('key')==1][0]
```

還有:

```python
find_it = None
for i in sample_list:
    if i.get('key')==1: 
        find_it = i
        break
```

但總覺的不如 js 爽.

問題出自 [segmentfault](https://segmentfault.com/q/1010000006013101/a-1020000006013138), by [daimon](https://segmentfault.com/u/daimon)

## 回答

### 分析與比較

我們來看一下你給的例子:
(如果我 js 有地方講不對, 請你指正我)

```javascript
sample_list.find((data)=>{return data.key == 1})
```

* `sample_list` 是一個 js array
* `data` 是 js object

然後這邊的手法是 `array.find` 配上 arrow function

然後 Python 這邊對應的手法是(我改了一下比較好對照):

```python
[data for data in sample_list if data.get('key')==1][0]
```

* `sample_list` 是 python list
* `data` 是 python dictionary

手法是 list comprehension

其實 js 的 arrow function 就類似於 Python 的 lambda function, `find` 手法也類似於 `filter`:

```python
filter(lambda data: data.get('key')==1, a)[0]       # Python2
list(filter(lambda data: data.get('key')==1, a))[0] # Python3
```

首先, 基本上手法所差無幾, 再來, 用 Python 的人都應該知道 list comprehension 的表達力比起 `filter` 是好上不少, 所以其實我覺得:

```python
[data for data in sample_list if data.get('key')==1][0]
```

的閱讀性其實更佳, 而且其實這樣的寫法你會發現你少寫了一個 lambda function(arrow function)

### 結論

我覺得這樣沒有比較差啊!

### 題外話(寫給 Python 愛好者)

Python 的 list 的確沒有直接相等於 js `array.find` 的方法, 所以多數時候的 **filter 查找** 都必須依賴 `filter` 或 list comprehension 或 generator expression.

但是如果我們只是要查找第一個符合條件的元素, 使用 list comprehension 似乎有一點點浪費(但其實 90% 的情況其實都無關緊要), 可是如果我們使用 generator expression 或是 Python3 的 `filter` 的話( Python3 的  filter 會返回一個 generator), 要怎麼取得第一個符合條件的項目呢?

如果你把他轉成 list 再取第一個:

```python
list((data for data in sample_list if data.get('key')==1))[0]
```

這樣等於是耗盡了 generator 這個 iterater, 簡單來說你已經 iterate 過所有的項目才找出答案。這樣就跟 list comprehension 沒什麼不同了

這邊有一個 trick 是這樣的:

```python
next((data for data in sample_list if data.get('key')==1))
```

這樣做我們就可以只產生第一個項目, 這也代表了查找會找到第一個找到就停止不會繼續下去走完整個 list

這邊如果查找失敗會引發一個 `StopIteration`, 為了處理這種狀況我們可以加一個 default value 用以指出查找失敗:

```python
next((data for data in sample_list if data.get('key')==1), None) # 查找失敗會返回 `None`
```
