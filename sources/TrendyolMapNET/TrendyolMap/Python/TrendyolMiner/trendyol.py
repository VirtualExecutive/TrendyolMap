
from bs4 import BeautifulSoup
from log import Log
from browser import Browser

class Trendyol():
    Log : Log
    url = "https://www.trendyol.com/"

    Browser:Browser

    def __init__(self) -> None:
        pass

    def GetAllUrl(self):
        result=[]
        self.Log.Write("INFO","Trendyol","TrendyolGetAllUrl",self.Browser.minerName,f"Site içeriğindeki bütün linkler elde ediliyor.")
        for tag in self.Browser.GetAllElements():
            if tag.has_attr("href"):
                href = tag.get("href")
                href:str
                
                if "?" in href:
                        href = href[:href.index("?")] 

                if href.endswith("/yorumlar"):
                    href = href[:0-len("/yorumlar")]
                elif href.endswith("/saticiya-sor"):
                    href = href[:0-len("/saticiya-sor")]
                
                if href not in result:
                    if(self.isValidUrl(href)):
                        result.append(href)
                        self.Log.Write("INFO","Trendyol","TrendyolFoundHref",self.Browser.minerName,href)
            
            if tag.has_attr("src"):
                src = tag.get("src")
                src:str
                if "?" in src and "?shopId" not in src:
                    src = src[:src.index("?")]      
                if"&" in src and "?shopId" in src:
                    src = src[:src.index("&")]
                if "?gag" in src:
                    src = src[:src.index("?gag")]
                elif "?boutiqueId" in src:
                    src = src[:src.index("?boutiqueId")]

                if src not in result:
                    if(self.isValidUrl(src)):
                        result.append(src)
                        self.Log.Write("INFO","Trendyol","TrendyolFoundSrc",self.Browser.minerName,src)
        return result


    def isValidUrl(self,url:str):
        if (url.startswith("http")  ):
            if(url.startswith(self.url)):
                pass
            else:
                return False
        if(url.endswith("webp")):
            return False
        if(url.endswith(".js")):
            return False
        if(url.endswith(".svg")):
            return False
        if(url.endswith(".svg\n")):
            return False
        if(url.endswith(".jpg")):
            return False
        if(url.startswith("data:image")):
            return False

        if(url.startswith("tel:")):
            return False
        if(url=="#"):
            return False
        if(".com" in url and "trendyol.com" not in url):
            return False
        if(not url.startswith("/")):
            return False
        elif(url=="/"):
            return False
        elif(url.startswith("//")):
            return False
        elif(url.startswith("/sr?")):
            return False
        elif(url.startswith("/koleksiyonlar/")):
            return False
        elif(url.startswith("/sanaozel/")):
            return False
        elif(url.startswith("/cok-satanlar")):
            return False
        elif(url.startswith("/_ui/")):
            return False
        return True