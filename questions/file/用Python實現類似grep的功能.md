# 用 Python 實現類似 grep 的功能

## 問題

一個草圖：

![图片描述][1]

現實現在文件夾和子文件夾下查找目標字串，
但不知如何提取包含目標字符的字串，並寫入到新文件中。
  [1]: https://segmentfault.com/img/bVyX2e

```python
#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys
import fnmatch

listonly = False
skipexts = ['.js']
def visitfile(fname,searchkey):
	global fcount,vcount
	try:
		if not listonly:
			if os.path.splitext(fname)[1] in skipexts:
				if open(fname).read().find(searchkey) != -1:
					print '%s has %s '%(fname,searchkey)
					fcount+=1
	except: pass
	vcount +=1

def visitor(args,directoryName,filesInDirectory):
	for fname in filesInDirectory:
		# 返回文件所在路径和文件名
		fpath = os.path.join(directoryName,fname)
		if not os.path.isdir(fpath):

			visitfile(fpath,args)

def searcher(startdir,searchkey):
	global fcount,vcount
	fcount = vcount = 0
	os.path.walk(startdir,visitor,searchkey)

if __name__=='__main__':
	# root=raw_input("type root directory:")
	root = '/home/jiangbin/findJS'
	key=raw_input("type key:")
	searcher(root,key)
	print 'Found in %d files,visited %d'%(fcount,vcount)

```

run

```
type key:JSQ
/home/jiangbin/findJS/XXX.js has JSQ 
/home/jiangbin/findJS/JSQ.js has JSQ 
Found in 2 files,visited 19
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005911595/a-1020000005912159), by [jiangbingo](https://segmentfault.com/u/jiangbingo)

## 回答

如果你用的是 linux，那我建議你用 `grep` 就好了:

```
$ ls mydir
a.js  b.js  c.js
```
```
$ grep JSQ mydir/*.js
mydir/a.js:abcdefg JSQ abcdefg
mydir/a.js:JSQ abcdefg abcdefg
mydir/a.js:abcdefg abcdefg JSQ
mydir/c.js:abcdefg JSQ abcdefg
mydir/c.js:JSQ abcdefg abcdefg
mydir/c.js:abcdefg abcdefg JSQ
```

(上面的例子裡，第一行的顯示有點問題，應該是這樣:`grep JSQ mydir/*.js`)

你也可以導到文件裡:

```
$ grep JSQ mydir/* > results.txt
```

然後你再從 `results.txt` 中去整理和統計數據。

如果你堅持想要使用 Python，我寫了一個應該是比較優化的代碼，你可以參考一下:

```python
import os
import glob

def search(root, key, ftype='', logname=None):
    ftype = '*.'+ftype if ftype else '*'
    logname = logname or os.devnull
    symbol = os.path.join(root, ftype)
    fnames = glob.glob(symbol)
    vc = len(fnames)
    fc = 0

    with open(logname, 'w') as writer:
        for fname in fnames:
            found = False
            with open(fname) as reader:
                for idx, line in enumerate(reader):
                    line = line.strip()
                    if key in line.split():
                        line = line.replace(key, '**'+key+'**')
                        found = True
                        print('{} -- {}: {}'.format(fname, idx, line), file=writer)
            if found:
                fc = fc + 1
                print('{} has {}'.format(fname, key))

    return vc, fc
```

`search(root, key, ftype='', logname=None)`
* 會在 `root` 這個 path 底下
* 尋找副檔名為 `ftype` 的文件(如果沒給則全部的文件都接受)
* 在裡面搜尋是否包含 `key` 這個關鍵字
* 如果有給 `logname`，則會輸出關鍵字前後用 `'**'` highlight 的 log 文件，內容是包含該關鍵字的每一行

實際上可以這樣用(`search.py`):

```python
if __name__=='__main__':
    root = 'mydir'
    key = input("type key: ")
    vc, fc = search(root, key, 'js', logname='results')
    print('Found in {} files, visited {}'.format(fc, vc))
```

運行:

```
$ python3 search.py
type key: JSQ
mydir/c.js has JSQ
mydir/a.js has JSQ
Found in 2 files, visited 3
```

logfile `results`:

```
mydir/c.js -- 0: abcdefg **JSQ** abcdefg
mydir/c.js -- 1: **JSQ** abcdefg abcdefg
mydir/c.js -- 2: abcdefg abcdefg **JSQ**
mydir/a.js -- 0: abcdefg **JSQ** abcdefg
mydir/a.js -- 1: **JSQ** abcdefg abcdefg
mydir/a.js -- 2: abcdefg abcdefg **JSQ**
```
