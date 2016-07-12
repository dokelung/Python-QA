# python 爬蟲 beautifulsoup string 抓取問題

## 問題

![图片描述][1]

  [1]: https://segmentfault.com/img/bVyY2I

我要的是這個藍色部分的內容，但是 beautifulsoup 裡兩個方法，一個 `.strings` 還有一個 `get_text()` 都不行，他們會把下面 `span` 裡的 `string：Good Sister-in-lwa:Forbidden love` 這些都抓取。

`.string` 直接抓不到，因為這個方法無法判斷該抓取哪個 string。

所以我該怎麼解決標籤里內嵌標籤的抓取字符串問題

問題出自 [segmentfault](https://segmentfault.com/q/1010000005915466/a-1020000005915727), by [yikosudo](https://segmentfault.com/u/yikosudo)

## 回答

@洛克 的想法不錯，把不要的標籤淬出或是移除，再取字串:

```python
>>> from bs4 import BeautifulSoup
>>> html = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
>>> soup = BeautifulSoup(html)
>>> a_tag = soup.a
>>> i_tag = soup.i.extract()
>>> a_tag.string
'I linked to '
```

或是像 @cloverstd 說的:

```
>>> from bs4 import BeautifulSoup
>>> html = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
>>> soup = BeautifulSoup(html)
>>> a_tag = soup.a
>>> list(a_tag.strings)
[u'I linked to ', u'example.com']
>>> list(a_tag.strings)[0]
'I linked to '
>>> a_tag.contents[0]
'I linked to '
```

總之方法很多，任意組合囉...
