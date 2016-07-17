# Python 代碼怎麼打包

## 問題

python 代碼怎麼打包(製作成套件)。像 java 一樣打個包共別人引用

問題出自 [segmentfault](https://segmentfault.com/q/1010000005942981/a-1020000005943604), by [進西米大](https://segmentfault.com/u/jinximida)

## 回答

參考我寫的 [It's Django](http://www.books.com.tw/products/0010676433) 一書中的 [教學](http://dokelung-blog.logdown.com/posts/243281-notes-django-python-modules-and-kits)

我直接節錄相關這段給你看:

### 上傳自己的套件

我們看了、用了那麼多別人寫的套件，自己會不會很想寫一個呢？本章前面的內容已經足夠讓大家了解如何自己撰寫一個套件並在本地端使用，但是我們要如何將這個套件分享給全世界呢？那當然就是要把套件上傳到PyPI囉!(這樣子所有人都可以用pip來下載和安裝你的套件呢)。這個小節就是要教大家怎麼作。

> 如果打算要上傳自己的套件，那要先去PyPI上註冊取得帳號跟密碼喔。

首先，大家要知道，如果自己的Python專案不只想要能從現行或相對的資料夾中匯入，而想要能夠安裝到Python環境中，一定要在專案的目錄底下撰寫`setup.py`檔。這邊針對還要上傳到PyPI，來客製化我們的setup.py，我們先來檢視一下一個待上傳的專案結構和和我們要加入的幾個設定檔位置:

```
MyProject/
├── README
├── pkgA
│   ├── __init__.py
│   ├── modA_1.py
│   └── modA_2.py
├── pkgB
│   ├── __init__.py
│   └── modB.py
├── runner
├── .pypirc  # 加入.pypirc
└── setup.py  # 加入setup.py
```

我們注意到原本該專案底下有兩個套件`pkgA`、`pkgB`(通常我們一個專案裡面會有數個套件，而我們在上傳專案的同時要將所屬的套件全數上傳)，裡面分別有數個模組跟標示其為套件結構的`__init__.py`。接著我們會有一個說明檔`README`(用來介紹該專案的結構與使用方式，在此便不細談)和一個執行檔(整個專案的執行腳本碼)`runner`。

接著我們要在原本的專案中加入兩個設定檔，分別是`setup.py`和`.pypirc`檔，我們會逐一介紹這些檔案該如何撰寫。

首先來看到`setup.py`:

```python
from distutils.core import setup

setup(
	name = 'MyProject',
	packages = ['pkgA', 'pkgB'],
	scripts = ['runner'],
	version = '1.0',
	description = 'My first project',
	author = 'dokelung',
	author_email = 'dokelung@gmail.com',
	keywords = ['Good Project'],
	classifiers = [],
)
```

我們必須要從`distutils.core`(distutils是Python內建的套件)中匯入`setup`函式，此函式會幫助我們進行安裝，讓我們來了解一下此函式中每個參數的意義:
 
| 欄位名稱 | 描述 |
|---|---|
| name | 專案名稱(與專案目錄同名) |
| packages | 要安裝的套件名稱 |
| scripts | script名稱，通常代表一個執行檔，不一定有 |
| version | 版本 |
| description | 專案描述 |
| author | 作者 |
| author_email | 作者信箱 |
| keywords | 這個專案的一些關鍵字 |

這邊稍微解釋一下`scripts`，這邊要寫在scripts裡的是整個專案的執行檔，他可能用到了專案裡面的套件。為了要將該檔案同時也裝到使用者的系統上，我們需要把他也標註上去，否則後面我們利用pip安裝的時候就只會安裝package而不會安裝執行檔了。而這邊所謂對執行檔的安裝，其實也就是把指定的scripts放到一個可執行路徑裡，例如`/usr/bin/`中，如此使用者在安裝完後可在任何地方運行該script(其實我們能夠指定安裝的路徑，但如果只給script名稱，那他會被放在預設的位置)。這邊有一點一定要注意，script的名字千萬不要跟他要匯入的pakcage同名了，這會導致一些匯入上的失誤。

至此，已經擁有一個漂亮的安裝檔了(同時也能支援PyPI發佈)。

接著，我們來看看`.pypirc`檔，唯有建立此設定檔才能讓我們傳東西到PyPI上面:

```python
[distutils]
index-servers =
    pypi 

[pypi] 
repository: https://pypi.python.org/pypi
username: (此處填帳號)
password: (此處填密碼)
```

如果是Windows的使用者，請打開終端機(命令提示字元)，進行環境變數的設定:

```sh
set HOME=C:\Users\Owner\
```

接著將我們在C槽的使用者資料夾(其實就是`C:\Users`)裡面新增一個子目錄`Owner`，把我們的`.pipyrc`複製一份放到該資料夾下，就算設定完成囉。

如果是Linux或是Mac的使用者，也請將`.pypirc`複製到家目錄底下:

```sh
$ cp .pypirc ~/.pypirc
```

上述設定檔備妥後，就到了最後一個階段，首先註冊:

```sh
$ python setup.py register -r pypi
```

接著上傳:

```sh
$ python setup.py sdist upload -r pypi
```

太好了，你成功的讓全世界都能看到你的作品了，上PyPI看看你的package頁面吧。終於，我們嘗到了甜美的果實，緊接著利用`pip`下載我們的專案(和裡面的套件)並安裝到自己的電腦看看:

```sh
$ pip install MyProject
```

> 如果讀者有用pip在自己的電腦上安裝了上傳的專案，該專案底下的套件就可以在本機端任何地方匯入了。

然後你就可以昭告天下，你也是Python的貢獻者了。
