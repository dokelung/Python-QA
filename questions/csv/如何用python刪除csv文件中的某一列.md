# 如何用 python 刪除 csv 文件中的某一列

## 問題

如何用python刪除csv文件中的某一列？

比如名為 `a.csv`中的數據：

```
index ABC 
0 1 3 5 
1 2 4 6 
2 7 8 9
```

想要刪除第二列（ B 列）該如何刪除呢？代碼該如何編寫呢？
求大神！萬分感謝！！！

問題出自 [segmentfault](https://segmentfault.com/q/1010000005958613/a-1020000005959134), by [tammy](https://segmentfault.com/u/qqqqqq123)

## 回答

如果問題很單純，甚至連 `csv` 都可以不使用:

```python
with open('old.csv') as reader, open('new.csv', 'w') as writer:
    for line in reader:
        items = line.strip().split()
        print(' '.join(items[:2]+items[3:]), file=writer)
```

寫個 general 的:

```python
import csv

def del_cvs_col(fname, newfname, idxs, delimiter=' '):
    with open(fname) as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)

del_cvs_col('a.csv', 'b.csv', [2])
```

`del_cvs_col` 會將 `fname` 轉成 `newfname` 用 `delimiter` 來做分割字元，且會去除掉在 `idxs`中指定的列。
