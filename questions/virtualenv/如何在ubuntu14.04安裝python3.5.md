# 如何在 ubuntu14.04 安裝 python3.5

## 問題

ubuntu14 默認安裝了 python2.7.6 和 python3.4.3，因為某個項目要用 python3.5，想問一下如何在 ubuntu 上安裝 python3.5 而不產生衝突？

補充:

結果發現是阿里雲的ubuntu缺了zlib和openssl幾個依賴包，導致編譯python的時候pip沒裝上...orz

問題出自 [segmentfault](https://segmentfault.com/q/1010000005991779/a-1020000005991900), by [moling3650](https://segmentfault.com/u/moling3650)

## 回答

使用 [`virtualenv`](https://virtualenv.pypa.io/en/stable/)的概略指南:

1. 下載 Python
2. 編譯 Python ([實用的 compile 指南](http://www.kelvinwong.ca/2010/08/02/python-2-7-on-dreamhost/))
3. 使用 `virtualenv` 來建置新環境
 * (選擇 1) 利用新版本 Python 中的 `pip` 來安裝 `virtualenv` (Python 新版本安裝後我記得直接都有相對應版本的 `pip`)
 * (選擇 2) 利用新版本 Python 先安裝對應的 `pip` (`easy_install` or `get-pip.py`), 然後同 (選擇 1)
 * (選擇 3) 利用 option: `virtualenv -p <python path> [ENVNAME]` 來指定使用哪個 python 建置環境

你也可以試試看:

1. [pyenv](https://github.com/yyuu/pyenv)
2. [pythonbrew](https://github.com/utahta/pythonbrew) <- 有整合 `virtualenv`
