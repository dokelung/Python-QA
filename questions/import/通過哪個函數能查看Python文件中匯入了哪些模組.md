# 通過哪個函數能查看 Python 文件中匯入了哪些模組？

## 問題

通過哪個函數能查看 Python 文件中匯入了哪些模組？

```python
from A import B
from AA import BB
```

如以上代碼，我如何在這個腳本中通過函數，返回

```python
[B, BB]
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005673457/a-1020000005675400), by [yangeren](https://segmentfault.com/u/hanz)

## 回答

定義如下的 function:

```python
def find_import():
    return {key:value for key, value in globals().items()
            if isinstance(value, type(sys)) and not key.startswith('__')}
```

函數 `find_import()` 會返回一個字典，以被匯入的:

* **module name**為 key
* **module instance**為 value。

**測試**:

```python
import sys
from os import path

def find_import():
    return {key:value for key, value in globals().items()
            if isinstance(value, type(sys)) and not key.startswith('__')}

for key, value in find_import().items():
    print key, value
```

**結果**:

```python
sys <module 'sys' (built-in)>
path <module 'posixpath' from '(your python path)/lib/python2.7/posixpath.pyc'>
```
