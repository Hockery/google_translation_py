import urllib.request    
from HandleJs import Py4Js    
    
def open_url(url):    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}      
    req = urllib.request.Request(url = url,headers=headers)    
    response = urllib.request.urlopen(req)    
    data = response.read().decode('utf-8')    
    return data    
    
def translate(content,tk):    
    if len(content) > 4891:    
        print("翻译的长度超过限制！！！")    
        return     
        
    content = urllib.parse.quote(content)    
        
    url = "http://translate.google.cn/translate_a/single?client=t"+ "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca"+"&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1"+"&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s"%(tk,content)    
        
    result = open_url(url)    
    return result   
    
def main():    
    js = Py4Js()    
        
    while 1:    
        content = input("输入待翻译内容：")    
            
        if content == 'q!':    
            break    
            
        tk = js.getTk(content)    
        translate(content,tk)    
        
if __name__ == "__main__":    
    main()