# pip 無法在命令行運行

## 問題

```
$ pip install pyinstaller
```

後運行:

```
$ pyinstaller - F文件
```

pyinstaller無法在命令行運行，會提示報錯：

```
failed to create process.
```

問題出自 [segmentfault](https://segmentfault.com/q/1010000005615543/a-1020000005616501), by [hongfeiyu](https://segmentfault.com/u/hongfeiyu)

## 回答

我了解了一下感覺上應該是 `pip` 的一個 bug [Spaces in Python path make pip-installed launchers fail on Windows][1]

### 原因分析

簡單來說就是 shebang line (script 裡面指定 python path 的那一行) 裡面有空白導致的，可能就是安裝 Python 的路徑上有空白而且 `pip` 在安裝的時候沒正確幫你加上引號，例如你的 Python 在:

```
C:\Program Files (x86)\Python35-32\python.exe
          ^     ^           
          空白惹事
```

然後用 `pip` 安裝的 Pyinstaller 的 script 裡面對於路徑上的空白沒有正確的用 **引號** 處理好:

```
#!C:\Program Files (x86)\Python35-32\python.exe  <-- 這個 shebang line 有問題，因為空白
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.1.1','console_scripts','pyinstaller'
```

### 解決辦法

有一些 workaround 的方式可以解決，第一個是你直接去 pyinstaller 的 script 裡面利用引號把空白問題給搞定(在 Python 目錄下的 Script 子目錄下):

```
#!"C:\Program Files (x86)\Python35-32\python.exe"  <-- 這個 shebang line 有問題，因為空白，我們補上前後的引號
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.1.1','console_scripts','pyinstaller'
```

或是直接用 Python 運行 script (不透過 shebang line 了):

```
C:>"C:\Program Files (x86)\Python35-32\python.exe" "C:\Program Files (x86)\Python35-32\Scripts\pyinstaller-script.py" script_to_compile.py
```

我查到還有人用一招，重裝 Python 在路徑沒有空白的地方(笑)，真的也是一招。

  [1]: https://github.com/pypa/pip/issues/2783
