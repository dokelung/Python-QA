# Python 的 staticmethod 在什麼情況下用

## 問題

如題。

問題出自 [segmentfault](https://segmentfault.com/q/1010000005943821/a-1020000005944785), by [PG](https://segmentfault.com/u/pg_577221f2caf96)

## 回答

### 特色與使用情境 

來講講講 `staticmethod` 好了，被 staticmethod 修飾的 method 並不會接收特殊的第一項引數 (一般的 instance method 和被 `classmethod` 修飾過的 **類別方法** 分別會接受實例和類別的參考作為第一項參數)，這讓靜態方法就像是個一般的 function，只是他剛好被定義在 class 裡而不是直接定義在 module level。

所以他的 **使用情境**就是: 當某個類裡面的函數不需要像是 `self` 或是 `cls` 等實例或類的參考時，使用靜態方法可以比較簡明且有效率地完成工作。

1. 簡明的部分在於不需要多接收一個無關緊要的引數
2. 效率在於一般的實例方法是 bound method (是個 object) 且是在我們要使用他的時候才生成，這會花上多一點點的 cost，而靜態方法並不會

### 實用/不實用?

但我覺得他並不實用，首先與類有直接關係的函數我們可以用 `classmethod` 就好，在代碼之中我們依靠第一項引數提供的 class 參考能夠完成與類有關的操作 (比如說 `__init__` 的替代物 或是 做為一個調度更多子 `staticmethod` 的上層方法)。

若非與類有關(而又與實例無關)，那我們需要類別靜態方法的目的，我暫時只想的到一個: 為了調用上能夠有一個抽象的層級 (沒錯，我說的就是 **namespace**) 而此函數雖然不會直接接觸類但是卻與類有關。

但是在 Python 之中，使用 `namespace` 是很容易的事情，我們不如將原先想要定義成靜態方法的函數定義在 module 層級，且盡可能地放在有關類別的附近，我想就非常足夠了([Luciano Ramalho](https://www.linkedin.com/in/lucianoramalho) 的觀點)。

### 反思

就在我打完上面這段之後，我特意看了一次 Julien Danjou 的一篇超棒的文章:
[The definitive guide on how to use static, class or abstract methods in Python](https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods)
我強力推薦任何想弄清楚 Python method 的人看這篇文章。

這篇文章提出了兩點 `staticmethod` 的優點，第一點我在上面已經有提到了，靜態方法比起實例方法來的簡明與有效率。第二點是靜態方法 **雖然與類無關但是屬於類的** ，這代表他可以客製化地為類服務。這有點難懂，我們看一個例子好了( Julien Danjou 文章中例子):

```python
class Pizza(object):
    @staticmethod
    def mix_ingredients(x, y):
        return x + y
 
    def cook(self):
        return self.mix_ingredients(self.cheese, self.vegetables)
```

我們想像一下，如果我們把 `mix_ingredients` 定義在 module level，那當我們在處理繼承 `Pizza` 的子類時，勢必無法藉由改動 `mix_ingredients` 來更動 mix ingredients 的行為 (因為該函數有別的類在使用)，那我們只好複寫 `cook` 了。

這個理由有一點點讓我改觀，起碼他指出了一個靜態方法跟一般方法的最大不同，**靜態方法是單屬於某一類的**。

不過我還是比較堅持原先的想法，因為也許 `mix_ingredients` 可以寫得更好，又或者是對於 Pizza 這種非抽象類別根本是不要去繼承他的，又或是繼承的時候複寫方法是不好的，甚至我可以覺得更動 `mix_ingredients` 跟更動 `cook` 同樣都是個負擔。

### 小結

以上都是 **我覺得**，也許哪一天 `staticmethod` 讓我真正優雅地派上用場了，我可能會承認今天我愚昧而膚淺的認識吧。至於你呢? 我覺得你可以有自己的想法，只要你在了解夠多的情況下還能說服自己，那我覺得沒有任何立場是錯誤的 :)
