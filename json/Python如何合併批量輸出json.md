# Python如何合併批量輸出json

## 問題

A文件夾裡面有:

```
1.json 
2.json 
3.json 
.....
```

格式為:

```json
{
   "hello": "hello",
   "data": [
        {
            "id": "123456",
            "create_time": "2016-03-28 11:41:00",
            "phone": "138888****",
            "name": "aaa"
        },
        {
            "id": "456789",
            "create_time": "2016-03-28 11:41:00",
            "phone": "137777****",
            "name": "bbb"
        }
    ]
}
```

遍歷 A 文件夾
合併 data 內容
輸出 1 個 json 和 csv

問題出自 [segmentfault](https://segmentfault.com/q/1010000004893778/a-1020000005151029), by [monkey_cici](https://segmentfault.com/u/monkey_cici)

## 回答

Python2:

```python
import os
import csv
import glob
import json

data = []

for fname in glob.glob(os.path.join('A', '*.json')):
    with open(fname) as f:
        jf = json.loads(f.read())
        data.extend(jf['data'])

with open('output.json', 'w') as f:
    print >>f, json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([key for key, value in data[0].items()])
    for d in data:
        writer.writerow([value for key, value in d.items()])
```

Python3:
```python
import os
import csv
import glob
import json

data = []

for fname in glob.glob(os.path.join('A', '*.json')):
    with open(fname) as f:
        jf = json.loads(f.read())
        data.extend(jf['data'])

with open('output.json', 'w') as f:
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')), file=f)

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([key for key, value in data[0].items()])
    for d in data:
        writer.writerow([value for key, value in d.items()])
```

1. 對於你說的合併，我這邊僅僅是將資料一筆一筆的疊加上去，並沒有作 id 檢查等處理。
2. csv 的輸出要求，可能也要視你想要的格式進行調整。

下面是相關的一些文檔，看完後對你會很有幫助:

* [glob][1]
* [csv][2]
* [os.path][3]
* [json][4]


  [1]: https://docs.python.org/2/library/glob.html
  [2]: https://docs.python.org/2/library/csv.html
  [3]: https://docs.python.org/2/library/os.path.html
  [4]: https://docs.python.org/2/library/json.html
