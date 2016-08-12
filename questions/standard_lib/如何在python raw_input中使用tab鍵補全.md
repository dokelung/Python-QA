# 如何在 python raw_input 中使用 tab 鍵補全

## 問題

如何在 python raw_input 中使用 tab 鍵補全？

問題出自 [segmentfault](https://segmentfault.com/q/1010000006090261/a-1020000006094141), by [caimaoy](https://segmentfault.com/u/caimaoy)

## 回答

### 拋磚

用 readline, 以下是一個簡單的小範例:

```python
import readline

CMD = ['foo1', 'foo2', 'bar1', 'bar2', 'exit']

def completer(text, state):
    options = [cmd for cmd in CMD if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

while True:
    cmd = raw_input('==> ')
    if cmd=='exit':
        break
    print(cmd)
```

測試:

```
==> <TAB><TAB>
bar1  bar2  exit  foo1  foo2
==> b<TAB>
==> bar
==> bar<TAB><TAB>
bar1  bar2  
==> bar1
bar1
==> exit
```

### 參考資料

* [python - readline](https://docs.python.org/2.7/library/readline.html)
* [GNU Readline Library](http://tiswww.case.edu/php/chet/readline/readline.html)


### 引玉

其實我沒有完全理解 completer 的作用原理, 尤其是 `state` 的部分, 希望有高手可以闡釋, 十分感謝!
