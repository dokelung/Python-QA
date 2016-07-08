# tk 程序中出現問題

這段代碼為什麼輸入框不顯示任何輸入，只有去掉 `validate = 'key'` 才可以，但是這樣又失去了驗證功能:

```python
from tkinter import *

master = Tk()

v1 = StringVar()
v2 = StringVar()
v3 = StringVar()

def test(content) :
    return content.isdigit()

testCMD = master.register(test)

e1 = Entry(master,textvariable = v1, validate = 'key',\
      validatecommand = (testCMD,'%p')).grid(row = 0,column =0)
      
Label(master,text = '+').grid(row = 0,column =1)

e2 = Entry(master, textvariable=v2, validate = 'key',\
           validatecommand=(testCMD, '%p')).grid(row = 0,column =2)
           
Label(master,text = '=').grid(row = 0,column =3)

e3 = Entry(master,textvariable = v3,state = 'readonly').grid(row = 0,column =4)

def calc() :
    result = int(v1.get()) + int(v2.get())
    v3.set(str(result))
    
Button(master,text = '计算结果',command = calc).grid(row = 1,column =2)

mainloop()
```

## 問題

問題出自 [segmentfault](https://segmentfault.com/q/1010000005590653), by [ice_sword](https://segmentfault.com/u/ice_sword)

## 回答

關鍵問題在於 valid percent substitutions 有誤，`validatecommand` 中的 **P 應該要大寫**: `%P` 而不是 `%p`．

另外補充一點，左右小括號 `(`, `)` 本身就允許代碼換行，不需要另外加上 `\` 了．

以上給你參考．
