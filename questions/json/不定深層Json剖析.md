# 不定深層 Json 剖析

## 問題

現有如下數據結構:

```python
{
  "date": {

  "doc_count_error_upper_bound": 0,
  "sum_other_doc_count": 0,
  "buckets": [
    {
      "key": "2015-02-01",
      "doc_count": 547,
      "shop": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "A",
            "doc_count": 251,
            "sum_qty": {
              "value": 36927
            },
            "sum_amt": {
              "value": 3651755
            }
          },
          {
            "key": "B",
            "doc_count": 178,
            "sum_qty": {
              "value": 12115
            },
            "sum_amt": {
              "value": 436019
            }
          },
          {
            "key": "C",
            "doc_count": 118,
            "sum_qty": {
              "value": 8896
            },
            "sum_amt": {
              "value": 1310549
            }
          }
        ]
      }
    },
    {
      "key": "2015-03-01",
      "doc_count": 524,
      "shop": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "A",
            "doc_count": 354,
            "sum_qty": {
              "value": 212909
            },
            "sum_amt": {
              "value": 18620841
            }
          },
          {
            "key": "B",
            "doc_count": 86,
            "sum_qty": {
              "value": 40109
            },
            "sum_amt": {
              "value": 5105368
            }
          },
          {
            "key": "C",
            "doc_count": 84,
            "sum_qty": {
              "value": 28156
            },
            "sum_amt": {
              "value": 938102
            }
          }
        ]
      }
    }
  ]
  }
}
```

想要剖析成：

```python
lst = [
    {'date': '2015-02-01', 'shop': 'A', 'sum_qty': 5, 'sum_amt': 10},
    {'date': '2015-02-01', 'shop': 'B', 'sum_qty': 5, 'sum_amt': 10},
    {'date': '2015-02-01', 'shop': 'C', 'sum_qty': 5, 'sum_amt': 10},
    {'date': '2015-03-01', 'shop': 'A', 'sum_qty': 20, 'sum_amt': 100},
    {'date': '2015-03-01', 'shop': 'B', 'sum_qty': 20, 'sum_amt': 100},
    {'date': '2015-03-01', 'shop': 'C', 'sum_qty': 20, 'sum_amt': 100}
]
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000006078915), by [prolifes](https://segmentfault.com/u/prolifes)

## 回答

寫了一個 class, 結果應該跟你要的一樣:

```python
from collections import abc

class CoolJSON:

    def __init__(self, key, mapping):
        """
        key is the main key of this CoolJSON
        mapping is the total data
        """
        self.key = key
        self.mapping = dict(mapping)


    def collect_bucket_item(self, item):
        """ used to handle single bucket item"""
        dic = {}
        lst = [{}]

        for key, value in item.items():
            if key=='key':
                dic[self.key] = value
            elif isinstance(value, abc.MutableMapping):
                if 'buckets' in value:      
                    lst = CoolJSON(key, value).collect()
                elif 'value' in value:
                    dic[key] = value['value']

        for item in lst:
            item.update(dic)

        return lst


    def collect(self):
        """used to collect results from all bucket items"""
        results = []
        for item in self.mapping['buckets']:
            results.extend(self.collect_bucket_item(item))
        return results
```

測試:

```python
# 測資使用 prolife 在評論下方新給的測資

lst = CoolJSON('date', data['date']).collect()

for item in lst:
    print(item)
```

結果:

```python
{'sum_amt': 3651755, 'sum_qty': 36927, 'date': '2015-02-01', 'shop': 'A'}
{'sum_amt': 436019, 'sum_qty': 12115, 'date': '2015-02-01', 'shop': 'B'}
{'sum_amt': 1310549, 'sum_qty': 8896, 'date': '2015-02-01', 'shop': 'C'}
{'sum_amt': 18620841, 'sum_qty': 212909, 'date': '2015-03-01', 'shop': 'A'}
{'sum_amt': 5105368, 'sum_qty': 40109, 'date': '2015-03-01', 'shop': 'B'}
{'sum_amt': 938102, 'sum_qty': 28156, 'date': '2015-03-01', 'shop': 'C'}
```
