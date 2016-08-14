# 如何交換兩個 shelve objects

## 問題

假定 `db1`, `db2` 是 `shelve` objects:

```python
if switch_d1_and_db2:
    func(db1, db2)
else:
    func(db2, db1)
```

怎麼才能改寫成：

```python
if switch_d1_and_db2:
    db1, db2 = db2, db1 # 错误写法
func(db1, db2)
```

`db1, db2 = db2, db1` 肯定是不行的，怎麼改寫呢?

所謂不行可以見以下範例:

`define.py`:

```python
import shelve
db1 = shelve.open('db1', writeback = True)
db2 = shelve.open('db2', writeback = True)
db1['name'] = 'db1'
db2['name'] = 'db2'
db1.close()
db2.close()
```

`switch.py`:

```python
import shelve
db1 = shelve.open('db1', writeback = True)
db2 = shelve.open('db2', writeback = True)
db1, db2 = db2, db1
print db1
print db2
db1.close()
db2.close()
```

`check.py`:

```python
import shelve
db1 = shelve.open('db1', writeback = True)
db2 = shelve.open('db2', writeback = True)
print 'db1:', db1
print 'db2:', db2
```

測試:

```
$ python define.py
$ python check.py
db1: {'name': 'db1'}
db2: {'name': 'db2'}
$ python switch.py
{'name': 'db2'}
{'name': 'db1'}
$ python check.py
db1: {'name': 'db1'}
db2: {'name': 'db2'}
```

雖然 switch 成功, 但是最後 check 還是失敗, 代表改變沒有正確反映在 db 中。

問題出自 [segmentfault](https://segmentfault.com/q/1010000006116287/a-1020000006119818), by [littlealias](https://segmentfault.com/u/littlealias)

## 回答

你好, 我研究這個問題一陣之後結論是:

1. 太難做到而且你想要使用的語法跟你要做的事情並不 match
2. 我覺得用原本的方法沒有什麼不好
3. 如果你想要做到你定義的這種交換, 那我有一個不算是太漂亮的替代方案, 你可以參考

以下針對上述三點說明:

對於第一點, 你想要:

```python
db1, db2 = db2, db1
```

這邊不論 `db1`, `db2` 是哪種 object, 這種交換式的意義在於

> 讓 `db1` 這個變數參考到原本 `db2` 所參考的 object, 並讓 `db2` 這個變數參考到原本 `db1` 所參考到的 object。

但是你想要做的事情是:

> 讓 `db1` 這個 file 和 `db2` 這個 file 的內容互換

仔細想一想, 這兩件事情並不相同, 換個方式來說, `db1, db2 = db2, db1`, 只會讓變數參考的東西互換(變數名稱不等於 db 的 file 名稱), 但是每個文件的內容還是沒有互換。

所以 **使用這種語法來互換跟你要達到的效果並不一致**。

第二點就不多說明了, 因為合理, 只是你可能不喜歡。

第三點我給了一個不怎麼漂亮的替代方案, 就是簡單定義一個 `shelf` 的代理類 `ShelfProxy`, 這個類盡量模擬 `Shelf` 類的行為(僅是介面上相似), 並且重載了運算符 `^` 定義為交換:

```python
import shelve

class ShelfProxy:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.file = args[0]
        self.loaddb()

    @classmethod
    def open(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.dic, name)

    def __setitem__(self, name, value):
        self.dic[name] = value

    def __getitem__(self, name):
        return self.dic[name]

    def __xor__(self, other):
        self.dic, other.dic = other.dic, self.dic
        return True

    def __str__(self):
        return str(self.dic)

    def loaddb(self):
        db = shelve.open(*self.args, **self.kwargs)
        self.dic = dict(db.items())
        db.close()

    def close(self):
        newdb = shelve.open(self.file, *self.args[1:], **self.kwargs)
        for key in newdb.keys():
            del newdb[key]
        for key, value in self.dic.items():
            newdb[key] = value
        newdb.close()
```

我將 `^` 定義為 **內容上的交換**, 之所以選 `^` 只是因為我想不到比較適合的符號, 一般來說重載不會這樣進行, 而且也不太會返回其他類的實例, 不過我這邊為求方便且針對你想要一個簡單介面這一點, 出此下策。 

接著我們定義一些測試的 function:

```python
def define():
    db1 = ShelfProxy.open('db1', writeback=True)
    db2 = ShelfProxy.open('db2', writeback=True)
    db1['name'] = 'db1'
    db2['name'] = 'db2'
    db1.close()
    db2.close()

def check():
    db1 = ShelfProxy.open('db1', writeback=True)
    db2 = ShelfProxy.open('db2', writeback=True)
    print('db1:', db1)
    print('db2:', db2)
    db1.close()
    db2.close()

def switch():
    print('switch')
    db1 = ShelfProxy.open('db1', writeback=True)
    db2 = ShelfProxy.open('db2', writeback=True)
    db1 ^ db2
    db1.close()
    db2.close()
```

測試代碼:

```python
if __name__ == '__main__':
    define()
    check()
    switch()
    check()
```

結果:

```
db1: {'name': 'db1'}
db2: {'name': 'db2'}
switch
db1: {'name': 'db2'}
db2: {'name': 'db1'}
```

### 結論

大部分的時候, 你可以用跟 `Shelf` 相同的介面來操作 `ShelfProxy`, 整體效果也類似, 但是你不覺得寫了那麼多, 還是使用一開始的方法比較簡單嗎XD
