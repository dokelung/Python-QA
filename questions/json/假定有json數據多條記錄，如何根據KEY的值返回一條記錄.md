# 假定有 json 數據多條記錄，如何根據 KEY 的值返回一條記錄?

## 問題

比如說給一個 json 數據：

```python
[
  {
    "Name": "A1", 
    "No": "3111", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "B2", 
    "No": "2222", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "C3", 
    "No": "1444", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "C4", 
    "No": "0542", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }
]
```

我想要 `No` 為 `"0542"` 的一條記錄：

```python
{
  "Name": "C4", 
  "No": "0542", 
  "createDate": "9999/12/31 00:00:00", 
  "lastUpdDate": "9999/12/31 00:00:00"
}
```

如果用 python3 應該怎麼實現？

我網上搜索了類似代碼, 比如:

```python
data = list（filter(lambda d: d['No'] == "0542", jsondata)）
```

改來改去，總是報各種類型錯誤，抓狂了……所以請教下大家，應該怎麼寫，謝謝！

問題出自 [segmentfault](https://segmentfault.com/q/1010000008793933/a-1020000008795741), by [Nix](https://segmentfault.com/u/nix)

## 回答

假設有 json string 如下:

```python
s = """
[
  {
    "Name": "A1", 
    "No": "3111", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "B2", 
    "No": "2222", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "C3", 
    "No": "1444", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }, 
  {
    "Name": "C4", 
    "No": "0542", 
    "createDate": "9999/12/31 00:00:00", 
    "lastUpdDate": "9999/12/31 00:00:00"
  }
]
"""
```

代碼:

```python
# code for python3

import json

def search(json_str, no):
    return [datum for datum in json.loads(s) if datum['No']==no]

datum = search(s, '0542')
print(datum)
```

結果:

```python
[{'Name': 'C4', 'No': '0542', 'createDate': '9999/12/31 00:00:00', 'lastUpdDate': '9999/12/31 00:00:00'}]
```
