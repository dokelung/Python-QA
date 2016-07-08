# jinja2 macro caller

## 問題

剛開始學用 jinja 來渲染 html, 遇到個 macro 調用 macro 的問題，就是用 call 來實現，按照官方的文檔的樣例寫的，但是一直報錯。

代碼是這樣的：

```jinja
{% macro dump_users(users) %}
     < ul >
    {% for user in users %}
        < li > {{ caller(user) }} </ li >
    {% endfor %}
    </ ul >
{% endmacro %}

{% call(user) dump_users(users) %}
    {{ user }}
{% endcall %}

   {{ dump_users(users) }}
```

錯誤信息：

```python
File "scorePage.html" , line 16 , in template
    <li>{{ caller (user) }}</li>

UndefinedError: No caller defined
```

查了好多資料，發現都是這麼寫的，，但是我這寫的就報錯。。真的被折磨了好久。。太菜了。。能不能告訴下到底哪裡出問題了。。十分十分感謝！！

問題出自 [segmentfault](https://segmentfault.com/q/1010000005352059/a-1020000005352912), by [leohujx](https://segmentfault.com/u/leohujx)

## 回答

```jinja
{% macro dump_users(users) %}
    <ul>
    {% for user in users %}
        <li>{{ caller(user) }}</li>
    {% endfor %}
    </ul>
{% endmacro %}

{% call(user) dump_users(users) %}
    {{ user }}
{% endcall %}

   {{ dump_users(users) }}
```

首先你會發現你定義的 macro `dump_users` 內部需要調用 `caller`

但是你在這行:

```jinja
{{ dump_users(users) }}
```

調用 `dump_users` 的時候並沒有利用 `call` 標籤來調用，既然 `dump_users` 不是被 "call" 的，自然也沒有 "caller" 讓他在內部調用囉。
