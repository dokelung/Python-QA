# 使用 Python 如何按行數拆分文件

## 問題

假設我有1個類似這樣方式生成的文件:

```python
with open('my-file.txt','wb') as f:
    for x in xrange(300000):
        f.write('hello,world\n')
```
        
現在我們想按照每個文件1000行的方式對之前生成的文件進行拆分,該如何處理?

問題出自 [segmentfault](https://segmentfault.com/q/1010000005357402/a-1020000005359339), by [我勒個去](https://segmentfault.com/u/yafeile)

## 回答

```python
with open('my-file.txt', 'r') as reader:
    counter = 0
    findex = 0
    for line in reader:
        if counter==0:
            writer = open('file-'+str(findex), 'w')
        print >> writer, line.strip()
        counter += 1
        if counter >= 1000:
            writer.close()
            counter = 0
            findex += 1
```

其實，Linux 的 `split` 指令就可以作到這件事了:

```bash
$ split -l 1000 my-file.txt
```
