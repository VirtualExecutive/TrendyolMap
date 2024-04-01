from log import Log
import traceback

from bs4 import BeautifulSoup

import undetected_chromedriver as uc

class Browser():
    Log:Log
    
    minerID=-1
    minerName:str
    url=""
    browser:uc.Chrome
    request:None

    def __init__(self) -> None:
        pass

    def OpenWeb(self):
        self.Log.Write("INFO","Browser","BrowserOpen",self.minerName,f"Tarayıcı açılıyor.")
        options = uc.ChromeOptions()
        options.user_data_dir = self.minerName
        self.browser = uc.Chrome(headless=True,use_subprocess=True)

    def Request(self):
        self.Log.Write("INFO","Browser","BrowserRequest",self.minerName,f"Siteye istek gönderiliyor: {self.url}")
        try:
            self.request = self.browser.get(self.url)
        except Exception as err:
            self.Log.Write("ERROR","Browser","BrowserRequestFailed",self.minerName,f"İstek gönderimi başarısız.","\n"+traceback.format_exc())
            self.Request()
        self.Log.Write("INFO","Browser","BrowserRequestSuccesfully",self.minerName,f"İstek başarıyla tamamlandı.")

    
    def WriteContent(self):
        self.Log.Write("INFO","Browser","BrowserWriteContent",self.minerName,f"Site içeriği yazdırıldı.")
        with open("result.html", "w", encoding="utf-8") as f:
            f.write(self.content)
        return self    

    def SetUrl(self, url):
        self.url = url

    
    def GetContent(self):
        self.Log.Write("INFO","Browser","BrowserGetContent",self.minerName,f"Site içeriği alındı.")
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")
        self.content = str(self.soup.contents)

    def GetAllElements(self):
        return self.soup.find_all()
    


