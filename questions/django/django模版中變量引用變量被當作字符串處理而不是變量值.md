# django 模版中變量引用變量被當作字符串處理而不是變量值

## 問題

問題：django 中模版變量引用變量，後面的變量被當作字串處理了，求解決方案。

代碼：

```python
li = ['a','b','c','d']
di = {'a':1,'b':2,'e':3,'f':5,'t':4}
```

```jinja
{% for i in li %}
    {{ di.i }}
{% endfor %}
```

這時候，`i` 沒有替換為列表中的內容，而是直接解析為字串 `i`，求解決方案。

問題出自 [segmentfault](https://segmentfault.com/q/1010000005615987), by [rongfeideng](https://segmentfault.com/u/rongfeideng)

## 回答

data:

```python
di = {'a':1,'b':2,'e':3,'f':5,'t':4}
items = di.items()
```

template:

```python
{% for key, value in items %}
    {{ value }}
{% endfor %}
```

----------

下面是我以前寫的筆記，你可以參考一下:

### for 標籤的限制

由於 `MTV (Model-View-Template)` 分工的關係，標籤(模板)語言受到了種種限制，所以對於 for 標籤來說，`break` 或是 `continue` 等方法是不存在的，我們只能透過在 view function 中整理出一個最貼切的資料。

另外特別要注意的是，for 標籤雖然能夠迭代 dictionary 的 key，但要由鍵取值是相當容易犯錯的，請看以下例子(假定我們的 view function 給定了一個字典 `dic={'1':'a','2':'b'}` ):

```jinja
{% for key in dic%}
    {{ key }} = {{ dic.key }}
{% endfor %}
```

我們將會發現，鍵會被輸出而對應的值不會，理由很簡單，變量的使用只會以變量的值取代變量的名稱(變量內的第一個名字)，往後的各種名稱都會以字面的意思解讀。有點難懂，以上例來說 `{{ key }}` 在兩次迴圈中會分別被代換成 1 跟 2，但是 `{{ dic.key }}` 卻會被試著解讀成 `dic['key']`、`dic.key`、`dic.key()`、`dic[key]`，也就是說變量中第二個以後的名字便不會被對應到值了，因為他不是變量，而是變量的屬性、方法或鍵(字面上！不會被真的代換)，`dic` 當然沒有叫做 `'key'` 的屬性。那你問我該怎麼辦，可以考慮在 view function 中提供`items = dic.items()`，以下有範例:

```jinja
{% for key, value in items %}
    {{ key }} = {{ value }}
{% endfor %}
```

或

```jinja
{% for item in items %}
    {{ item.0 }} = {{ item.1 }}
{% endfor %}
```
