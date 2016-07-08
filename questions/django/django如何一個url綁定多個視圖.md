# django 如何一個 url 綁定多個視圖

## 問題

問題很簡單,我有2個url規則,但是可能會有衝突

```python
url(r'^(?P<category>\w+)/$',
            CategoryView.as_view(), name='category-detail-view'),


url(r'^(?P<url>\w+)/$',CustomView.as_view(),name="custm"),
```

簡單的看來就是這樣的,這2條url,其實目的的是一樣,為了訪問
www.baidu.com/xxx/ 這樣的分類,只是有一個是自定頁面. 
這樣設置不行, 只能取其中一個.

我想問問, django 有沒有辦法讓同一個url規則綁定多個不同的視圖? 這樣就很靈活了~

問題出自 [segmentfault](https://segmentfault.com/q/1010000005773535/a-1020000005773924), by [jqlts1](https://segmentfault.com/u/jqlts1)

## 回答

一個 url pattern 如果可以綁定多個視圖，我覺得 Django 也不知道怎麼處理這個 request 了 (到底要派發給哪個 view )。

但你現在的問題是:

> 符合同一個 pattern 的不同 url 需要不同的處理

這聽起來怪怪的，如果說真有這種情形，那大概代表你的 pattern 不應該這樣寫，你應該試圖將原本的 url pattern 拆開寫成多個可區別的 pattern。

當然，很有可能是 url pattern 很難拆開來，以你的例子，也許的確難以區別:

```
(domain name)/category1/
```

和

```
(domain name)/www.google.com.tw/
```

因為這兩種 url 提取出來的 pattern 如你所講的，根本一模一樣。

以下是幾種可能的作法:

1. 如果 category 的種類不多，可以考慮將 category 的部份直接拆開來寫 url pattern
2. 就使用一種 url pattern，但是先用一個統一個 view 來處理，再根據 url 中截取到的參數轉發給不同的 view 處理

### 結論

url 截取參數就是為了這種需求阿:

> 同樣形式的 url pattern 要能夠處理符合該 pattern 但實際上還是有區別的各個 url
