# Python 如何優雅的處理大量異常語句

## 問題

我需要用 bs4 來分析一個 html，需要寫很多提取語句，大概幾十條，格式如下:

```python
twitter_url = summary_soup.find('a','twitter_url').get('href')
facebook_url = summary_soup.find('a','facebook_url').get('href')
linkedin_url = summary_soup.find('a','linkedin_url').get('href') 
name = summary_soup.find('div', class_='name').find('a').string
```

但是每個語句都有可能出異常，如果每個語句都加上 `try/except` 就太繁瑣了，有沒有什麼好的方法處理每條語句，出異常賦值為 `None`，不中斷程序

問題出自 [segmentfault](https://segmentfault.com/q/1010000005868327/a-1020000005894846), by [ider](https://segmentfault.com/u/ider)

## 回答

我在問題的評論裡面有提出一個小問題，如果能有回答，大家比較好掌握你的需求．

如果不想太多，純粹要避免掉 `get` 的時候可能會產生的錯誤，有個比較偷雞的方式，如果沒有太多奇怪的狀況要處理，也許你可以試試:

```python
twitter_url = (summary_soup.find('a','twitter_url') or {}).get('href')
```

如果說 bs 的 `find` 沒有找到東西的話，會 `return None`，此時我們利用先利用 `or` 來完成一個 trick 使得 `get` 永遠不會失敗．再利用字典的 `get` 與 bs tag 的 `get` 相似的特性就可以處理掉異常，對變數賦值為 `None`．

如果要寫的穩固一點的話，參考 @prolifes 的建議滿有幫助的．
