# 刪除xml文件的指定標籤

## 問題

有個xml文件的格式大致如下：

```xml
<re> 
<id>123</id> 
<name>abc</name> 
</re> 
<re> 
<id>126</id> 
<name>abc</name > 
</re> 
<re> 
<id>135</id> 
<name>abc</name> 
</re> 
<re> 
<id>147</id> 
<name>abc</name> 
</re >
```

然後另外一個 `delete.txt` 保存的是需要刪除的 re 標籤的 id。

假設 txt 內容如下：

```
126 
147
```

需要做的就是讀取這個 delete.txt 文件，然後在 xml 中找到這些 id 對應的 `<re> `標籤將其全部刪除，如上例的結果就是：

```xml
<re> 
<id>123 </id> 
<name>abc</name> 
</re>

<re> 
<id>135</id> 
<name>abc</name> 
</re>
```

請問是怎麼做的。。另外需要提到的是這個 xml 文件挺大的，有200多M。

問題出自 [segmentfault](https://segmentfault.com/q/1010000005077756/a-1020000005079269), by [starryer](https://segmentfault.com/u/starryer)

## 回答

你可以使用 `BeautifulSoup` 套件:

**安裝**:

```sh
$ pip install bs4
```

* 如果覺得 `html` 解析器不敷使用，參考[文檔][1]安裝其他適合的解析器。
* 如果想要詳細了解 `BeautifulSoup` 也請參考官方文檔(有中文版本)。
 
**測試檔**:

以下是我使用的測試文件:

delete.txt

```
126
147
``` 

test.xml

```xml
<re>
<id>123</id>
<name>abc</name>
</re>
<re>
<id>126</id>
<name>abc</name>
</re>
<re>
<id>135</id>
<name>abc</name>
</re>
<re>
<id>147</id>
<name>abc</name>
</re>
```
    
**代碼**:

```python
from bs4 import BeautifulSoup
    
with open('test.xml') as reader:
    xml = reader.read()
    
deleted_id = []
    
with open('delete.txt') as reader:
    for line in reader:
        line = line.strip()
        deleted_id.append(line)
    
def has_delete_id(tag):
    return tag.name=='re' and tag.id.string in deleted_id
    
soup = BeautifulSoup(xml, 'html.parser')
    
tags = soup(has_delete_id)
for tag in tags:
    tag.decompose()
    
print(soup.prettify())
```

**程式輸出**:

```xml
<re>
 <id>
  123
 </id>
 <name>
  abc
 </name>
</re>
<re>
 <id>
  135
 </id>
 <name>
  abc
 </name>
</re>
```

**代碼說明**:

首先我們從 `Beautiful Soup` 的套件中匯入 `BeautifulSoup` 類

```python
from bs4 import BeautifulSoup
```

接著分別從 `delete.txt` 和 `test.xml` 中讀出要刪除的 id 和主要的 xml 內容，下一步是實體化生成一個 `BeautifulSoup` 對象 `soup`， 我們採用 `html.parser` 解析器去解析 `xml`:

```python
soup = BeautifulSoup(xml, 'html.parser')
```

在此我們定義了一個用於過濾的 function `has_delete_id`，每一個在 `xml` 中的tag 只要是 `<re>` tag 且含有想要刪除的 `<id>` tag 就會被檢索出來:

```python
def has_delete_id(tag):
    return tag.name=='re' and tag.id.string in deleted_id
```

接著 `soup(has_delete_id)` 會幫助我們找到欲刪除的 tag，接著走訪搜索出來的這些 tag 並呼叫方法 `decompose()` 來從文件中刪除該標籤。

最後 `soup.prettify()`可以幫助我們輸出修改後的文件。

  [1]: https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id9

