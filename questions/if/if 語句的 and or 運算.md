# if 語句的 and or 運算

## 問題

最近想提取出特定的 URL，遇到問題為預期提取出 URL 中帶有 `webshell` 或者 `phpinfo` 字段的 URL，但是全部 URL 都匹配出來了：

```python
for url in urls:
	  if "webshell" or "phpinfo" in url:
		  print url
```

![图片描述][1]

改成 and 語句也不符合預期，只提取出了含有 `phpinfo` 的 url：

```python
for url in urls:
	  if "webshell" and "phpinfo" in url:
		  print url
```

![图片描述][2]

  [1]: https://segmentfault.com/img/bVzaNa
  [2]: https://segmentfault.com/img/bVzaNH

問題出自 [segmentfault](https://segmentfault.com/q/1010000005960652/a-1020000005960714), by [daisydydy](https://segmentfault.com/u/daisydydy)

## 回答

```python
if "webshell" or "phpinfo" in url:
```

這樣做的意思是 `if "webshell"` or `if "phpinfo" in url` 而前者恆成立。

```python
if "webshell" and "phpinfo" in url:
```

這樣做的意思是 `if "phpinfo" in url` 因為 `if "webshell"` 恆成立。

解法基本上如 @洛克 所說:

```python
for url in urls:
    if "webshell" in url or "phpinfo" in url:
        print url 
```

如果今天用來匹配的 word 很多的話:

```python
urls = [
    'https://www.example.com/aaa',
    'https://www.example.com/bbb',
    'https://www.example.com/ccc',
]


def urlcontain(url, lst):
    return any(seg for seg in url.split('/') if seg and seg in lst)

for url in urls:
    if urlcontain(url, ['aaa', 'bbb']):
        print(url)
```

結果:

```
https://www.example.com/aaa
https://www.example.com/bbb
```

`urlcontain(url, lst)` 可以問 `url` 裡面是不是有 `lst` 裡面的任何一個 string

這樣子要比對十個關鍵字也不會寫出太長的 if 述句。

當然要用 `re` 也可以，只是我個人不太喜歡 `re` 就是了...
