# 會php和python的大神進來幫忙轉換一段代碼

## 問題

求把這段php代碼轉成python的代碼，謝謝！



```php
//倒序排序
function my_sort($a,$b)
{
    if ($a==$b) return 0;
   return ($a<$b)?1:-1;
}


$arr = array('aaa'=>5,'bbb'=>3,'ccc'=>4);

usort($arr,"my_sort");

echo json_encode($arr);
```

簡單說就是數組倒序排序，然後轉成json格式。

問題出自 [segmentfault](https://segmentfault.com/q/1010000005106649/a-1020000005107260), by [御風獨行豬](https://segmentfault.com/u/yufengduxingzhu)

## 回答

PHP 中的 associative array 是一種 ordered mapping (有序映射)．
這代表了 Python 中的 dictionary 並非完全相等於 associative array．

其次, json 據我所知並不支援 ordered mapping，所以如果你想要完成這項任務可能要:

1. 使用 Python 中的有序映射對象: `OrderedDict` (請參考[OrderedDict][1])
2. 將 `OrderedDict` 轉為 `list` 再轉為 `json`
3. 到時候要使用該項資料時，必須從 `json` 中 load 進 `list` 再轉回 `OrderedDict`

----------

以下是 *Python3* 的代碼讓你參考:

**代碼**:

```python
import json
from collections import OrderedDict
    
# using OrderedDict
arr = {"aaa":5,"bbb":3,"ccc":4, "ddd":7}
arr = OrderedDict(sorted(arr.items(), key=lambda item: item[1], reverse=True))
# or you can create an OrderedDict directly:
# arr = OrderedDict([('aaa', 5), ('bbb', 3), ('ccc', 4), ('ddd', 7)])
print(arr)
    
# list
arr = list(arr.items())
print(arr)
    
# json dump
json_arr = json.dumps(arr)
print(json_arr)
    
# json load
arr = OrderedDict(json.loads(json_arr))
print(arr)
```

**結果**:

```python
OrderedDict([('ddd', 7), ('aaa', 5), ('ccc', 4), ('bbb', 3)])
[('ddd', 7), ('aaa', 5), ('ccc', 4), ('bbb', 3)]
[["ddd", 7], ["aaa", 5], ["ccc", 4], ["bbb", 3]]
OrderedDict([('ddd', 7), ('aaa', 5), ('ccc', 4), ('bbb', 3)])
```

  [1]: https://docs.python.org/2/library/collections.html#ordereddict-objects
