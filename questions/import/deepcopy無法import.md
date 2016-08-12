# deepcopy 無法 import

## 問題

![clipboard.png](https://segmentfault.com/img/bVzN19)

![clipboard.png](https://segmentfault.com/img/bVzN2v)

本來一個叫 `copy` 的文件，我後來改了名字還是這樣

問題出自 [segmentfault](https://segmentfault.com/q/1010000006111497/a-1020000006112397), by [yijiangnan](https://segmentfault.com/u/yijiangnan)

## 回答

看你的意思應該是原本的文件名叫做 `copy.py`:

然後出現:

```python
ImportError: cannot import name deepcopy
```

接著你改了名字還是這樣, 我不知道你的 **還是這樣** 是

1. 還是有問題     或是
2. 還是同一個問題

我整個給你以下建議:

1. 你自己寫的 .py 文件不要取名跟要使用到的 pkg 或 module 一樣
2. 刪除該目錄下的 .pyc 文件 (這可能是讓你 `import copy` 持續出錯的原因)
3. 你使用  `copy` 和 `deepcopy` 的方式有誤, 請參考 @prolifes  的用法

### prolifes 的說明

```python
import copy
c = copy.copy(d)
dc = copy.deepcopy(d)
```
