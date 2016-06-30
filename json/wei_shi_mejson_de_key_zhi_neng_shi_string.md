# 為什麼json的key只能是string？

## 問題

在 python 中，字典的 key 可以是任意 immutable 對象，但 json 的 key 卻只能是 string。

在 stackoverflow 上搜到的相關問題，Why JSON allows only string to be a key?

最佳答案是說 json 是為了數據在不同程序之間相互傳遞，所以 string 能保證不同的程序語言都能支持這種數據結構。但我還是不明白為什麼 int、float 之類的不行。

```python
json.dumps({ 1 : 1 , 2 : 2 })
 '{"1": 1, "2": 2}
```

by user of segmentfault morriaty_the_murderer

## 回答

你好，針對你的問題，我覺得你自己貼的那篇 stack overflow 的文章已經說得很清楚了。

補充一下我對於 json 中 object key 的看法:

首先你可以看到 [json.org][1] 中對於 json **object** 和 **string** 的定義:

> **object**: An object is an unordered set of name/value pairs. An object begins with { (left brace) and ends with } (right brace). Each name is followed by : (colon) and the name/value pairs are separated by , (comma).

> **string**: A string is a sequence of zero or more Unicode characters, `wrapped in double quotes`, using backslash escapes. A character is represented as a single character string. A string is very much like a C or Java string.

同時我們可以在 [The application/json Media Type for JavaScript Object Notation (JSON)][2] 中看到以下的敘述:

> An object is an unordered collection of zero or more name/value pairs, where `a name is a string` and a value is a string, number, boolean, null, object, or array.

我們可以清楚了解到，json 用來表述 object 用 string (雙引號夾住的字符集) 當作 key 的唯一選擇。

這說明了在 json 的定義或是 spec 中是明顯規範了 key 的型態跟表達方式，這可能出於`某些設計哲學上的考量`，也可能只是`某些實作上的選擇`，當然我們可以去追究當中的意涵，但是:

> 對於一般的使用者而言，能夠認識到這一點以避免設計上的問題應該是更為重要的。

就像是我們未必會去深究 Python 為何不使用 `else if` 而要使用 `elif`，為什麼我們複製 tuple 卻拿不到副本，而是拿到同一個對象等等。

----------

當然這可能不能滿足我們的求知欲，所以我試圖提出一些觀點(還有真正大師的觀點)

>P.S. 我在這裡並不打算說服你，因為我自認為我完全不是個 json 專家(笑)。

如果你嘗試使用過 javascript 去建立一個 object，你會發現，以下的敘述語句是行得通的:

```
var obj = {hello:1, world:2}
```

這相等於:

```
var obj = {"hello":1, "world":2}
```

可見在 js 中，object 的 key 有沒有雙引號在 evaluate 的時候都是一樣的。 甚至目前的 js object 用整數或是 js 關鍵字也能當作 key ...

但在 json 中，key 不但要是 string，還必須以雙引號夾住，所以很多人的疑問反而是，為什麼 js 中可以不用雙引號，但是 json 卻要? 我覺得這是一個重點，當雙引號的規則被使用的時候，不是 string 的東西也會變成 string 了(因為非得用雙引號不可)，那所以為什麼要用雙引號咧?

關於這一點，你可以參考一下 Douglas Crockford (json 標準創造者) 在某個演講上面的一段說詞:

> That was when we discovered the unquoted name problem. It turns out ECMA Script 3 has a whack reserved word policy. Reserved words must be quoted in the key position, which is really a nuisance. When I got around to formulizing this into a standard, I didn't want to have to put all of the reserved words in the standard, because it would look really stupid.

> At the time, I was trying to convince people: yeah, you can write applications in JavaScript, it's actually going to work and it's a good language. I didn't want to say, then, at the same time: and look at this really stupid thing they did! So I decided, instead, let's just quote the keys. That way, we don't have to tell anybody about how whack it is. That's why, to this day, keys are quoted in JSON.

總而言之，大意是說，為了避免 `json 因為要避免使用它的語言發生問題` 所導致的過度複雜的標準(比如說考慮所有關於那個語言的關鍵字在作為 key 的情況)，那乾脆用個簡單的法則來解決所有可能的意外，那就是加上雙引號拉。

以上不知道有沒有讓你有一些想法呢? 其實很多人覺得只能使用 string key 是為了不同語言使用 json 上面的穩定性我覺得也很有道理，我覺得能找個理由說服自己就很不錯了，畢竟怎麼理解他這樣設計可以有千千萬萬種解讀，至於真正的原因，也就只有他的創造者或標準的維護者知道了。

----------

**總之，簡單而明確的規則不是很不錯嗎!**

參考資料:
[in JSON, Why is each name quoted?][3]
[Is there any practical reason to use quoted strings for JSON keys?][4]
[Converting a JSON Text to a JavaScript Object][5]
[Object Equality in JavaScript][6]

----------
(以下是題外話)

對於你一開始的這個敘述:

> 在 Python 中，字典的 key 可以是任意 immutable 对象

稍微有點不精確，分享我自己的看法。

關於甚麼樣的對象可以作為字典的鍵，我們應該這樣說:

> 在 Python 中，字典的 key 必須要是 hashable 的

有人可能會覺得很奇怪，immutable 的對象不應該都是 hashable 的嗎?

其實並不盡然，我們看一個例子:

```
>>> a = ([1, 2, 3], 4, 5)
>>> hash(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> dic = {}
>>> dic[a] = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
``` 

`a` 是一個 tuple，我想我們應該都同意他是 immutable 的對象，可是這個 tuple 含有一個 mutable 的 list 元素，導致他自己成為一個非 hashable 對象，這就不能當作字典 `dic` 的鍵了。

這是非常容易被忽略的一點:

> tuple 只有在他的元素都是 hashable 的情況下，才會是 hashable 的

所以其實有些 tuple 可以當作字典的鍵:

```
>>> b = (1,2,3)
>>> dic[b] = 0
```

那我們到底要如何判斷一個對象是否為 hashable 的(也就是他可以作為字典的鍵)呢? (第三點針對 Python3)

1. 基本的 immutable builtin type 都是 hashable 的，除非他們包含了 mutable 的元素(見規則2)，ex: str, bytes, ...
2. tuple 只有在所有元素都是 hashable 的對象時，他才是 hashable 的
3. 自定義的類基本上都是 hashable 的，因為他們的 hash 值是由他們的 id 值推導出來的。但假如我們有實作它的 `__eq__` 方法，因為要維持 hash 跟 equality 的一致性，所以如果我們沒有一併重新實作 `__hash__`，則該類也會變成 unhashable 的。

以上幾點可參考:

1. [Types that define `__eq__` are unhashable in Python 3.x?][7]
2. [Python doc - Glossary][8]


  [1]: http://www.json.org/
  [2]: http://tools.ietf.org/html/rfc4627
  [3]: http://stackoverflow.com/questions/2067974/in-json-why-is-each-name-quoted
  [4]: http://stackoverflow.com/questions/4201441/is-there-any-practical-reason-to-use-quoted-strings-for-json-keys
  [5]: http://www.w3schools.com/js/js_json.asp
  [6]: http://adripofjavascript.com/blog/drips/object-equality-in-javascript.html
  [7]: http://stackoverflow.com/questions/1608842/types-that-define-eq-are-unhashable-in-python-3-x
  [8]: https://docs.python.org/3/glossary.html#term-hashable