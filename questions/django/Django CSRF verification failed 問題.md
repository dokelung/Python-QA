# Django CSRF verification failed 問題

## 問題

**urls.py**

```python
from django.conf.urls import url
from django.contrib import admin
from blog import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.index),
	url(r'^abc$',views.handler),
]
```

**views.py**

```python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,"index.html")


def handler(request):
	return HttpResponse("<p>name:</p>" + request.POST['username'])
```

**index.html**

```python
<!doctype html>
<html>
	<head>
		<meta charset="UTF-8"/>
		<title>index page</title>
	</head>
	<body>
       <form action="abc" method="POST">
       		<input type="text" name="username">
       		<button id="btn">提交</button>
       </form>
	</body>
</html>

```

我在谷歌瀏覽器下點擊這個提交後出現了:
![图片描述][1]

我又直接打開abc網站出現了:
![图片描述][2]

請問這是什麼問題啊要怎麼解決啊？


  [1]: https://segmentfault.com/img/bVz3ih
  [2]: https://segmentfault.com/img/bVz3iq

問題出自 [segmentfault](https://segmentfault.com/q/1010000006170144/a-1020000006171703), by [dzxczxsb](https://segmentfault.com/u/dzxczxsb)

## 回答

在 Django 中, 使用 post 的時候很可能會出現以下錯誤:

```python
Forbidden(403):
CSRF verification failed. Request aborted.
Reason given for failure:
    CSRF token missing or incorrect.
```

這是因為 Django 幫我們啟動了 **CSRF攻擊** 的防護，CSRF(cross-site request forgery) 是惡意的跨站請求或偽裝使用者的攻擊，攻擊者會欺騙用戶的瀏覽器去訪問一個認證過的網站並且執行一些惡意的操作。由於用戶的瀏覽器已經被該網站認證過了，所以該網站會放心的讓這些操作被執行(即便這些操作並非該網站要求的或是不是用戶自願的)。

所以我們的伺服器需要一些有保護的措施。常見的一種防護手段，就是使用一個伺服器產生的亂數 token，夾帶在送給客戶端的表單中，當客戶端送回表單時，伺服器檢查這個 token 是不是自己發出，便可以防止攻擊。

由於在 `settings.py` 檔中的 `MIDDLEWARE_CLASSES` 中有預設的 `'django.middleware.csrf.CsrfViewMiddleware'`，所以 Django 在這裡便會要求 CSRF token 驗證，為了讓我們的網站更安全，我們還是照著遊戲規則一步一步來吧!

在html的`<form>`中加入`{% csrf_token %}`如下：

```html
...
         <form action="" method="post"> {% csrf_token %}
...
```

就可以解決問題了
