# Python 如何讀取 json 中的數據

## 問題

```json
{
  "errno": "0",
  "data": {
    "hi_info": {
      "login_ip": "127.0.0.1",
      "license": {
        "id": "123456",
        "name": "hello",
        "sex": "",
        "status": "1"
      },
      "hello_info": {
        "model": "3",
        "license": {
          "id": "123456",
          "license_no": ""
        },
        "upgrade": 1
      }
    }
  }
}
```

如何讀取自己想要的數據

比如:

* `hi_info` 中的 `login_ip`
* `license` 中的 `name`
* `license` 中的 `id`

以及 `data` 裡面所有的數據

問題出自 [segmentfault](), by [monkey_cici](https://segmentfault.com/u/monkey_cici)

## 回答

```python
import json

with open('ex.json' , 'r') as reader:
    jf = json.loads(reader.read())

print(jf['data']['hi_info']['login_ip'])
```
