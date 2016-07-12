# Python timeit 測量代碼運行時間問題

## 問題

```python
def is_unique_char(string):
    if len(string) > 256:
        return True
    
    record = 0L
    
    for ch in string:
        # print record
        ch_val = ord(ch)
    
        if (record & (1 << ch_val)) > 0:
            return False
    
        record |= (1 << ch_val)
    
    return True
    
    
import string
s1 = string.ascii_letters + string.digits
    
    
if __name__ == '__main__':
    import timeit
    print is_unique_char(s1)
    print timeit.timeit("is_unique_char(s1)",
            setup="from __main__ import is_unique_char, s1")
```

代碼如上, `is_unique_char` 就是一個包含位運算的函數(具體作用不重要) 
運行代碼,秒出 `print is_unique_char(s1)` 的結果,但是 `timeit` 測量需要 30 多秒。

這是為什麼呢？會不會是因為位運算? 呃，先感謝大家解答🙏

問題出自 [segmentfault](https://segmentfault.com/q/1010000005924858/a-1020000005925103), by [neo1218](https://segmentfault.com/u/neo1218)

## 回答

簡單來說，`timeit` 會執行代碼 `1000000` 次...，當然要花很久囉。

這個 function 是用來測量某段代碼的平均運行時間，所以你必須除以他執行的次數。

我改了一下你的代碼並且用 `time.time` 測了一下:

```python
# uc.py

import string

def is_unique_char(string):
    if len(string) > 256:
        return True

    record = 0L

    for ch in string:
        # print record
        ch_val = ord(ch)

        if (record & (1 << ch_val)) > 0:
            return False

        record |= (1 << ch_val)

    return True

s1 = string.ascii_letters + string.digits
```

```python
import timeit
import time
from uc import is_unique_char, s1

if __name__ == '__main__':
    btime = time.time()
    is_unique_char(s1)
    etime = time.time()
    print etime - btime
    print timeit.timeit("is_unique_char(s1)", setup="from uc import is_unique_char, s1")/1000000
```

結果:

```
4.91142272949e-05
2.89517600536e-05
```

結果是單次的運行差不多...
