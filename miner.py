from browser import Browser
from trendyol import Trendyol
from database import Database
from log import Log
from mysql.connector import IntegrityError
import traceback
import json
import os
import time

class Miner():
    Log:Log

    minerCount=0
    minerID:int
    minerName:str

    isStop=False

    STOPFILE ="STOP"



    def  __init__(self) -> None:
        self.SetID()
        self.minerName= self.GetMinerName()
        self.Log.Write("INFO","Miner","MinerInitializing",self.minerName,"Başlatılıyor.")

        self.Browser = Browser()
        self.Browser.minerID=self.minerID
        self.Browser.minerName=self.minerName

        self.Trendyol=Trendyol()
        self.Trendyol.Browser = self.Browser

        self.Database=Database()
        self.Database.minerName=self.minerName


    def Start(self):
        self.Log.Write("INFO","Miner","MinerStarted",self.minerName,"Başlatıldı.")
        self.Database.Connect()
        self.CreateTables()
        Urls.CreateTableUrls(self)
        Urls.CreateTableVurls(self)
        self.Log.Write("INFO","Miner","MinerCheckedTables",self.minerName,"Tabloları kontrol etti.")
        self.Browser.OpenWeb()
        self.ScanTrendyolPage(Trendyol.url)
        
        while Urls.isHaveAnyUrl(self) and not self.IsStop():
            try:
                self.ScanTrendyolPage(Urls.GetRandomUrl(self))
            except:
                print("Hata", traceback.format_exc())
                continue

    def IsStop(self):
        self.Database.Connect()
        try:
            result=self.Database.Execute("SELECT value FROM settings WHERE `key` = 'isStop'; ")[0][0]
        except TypeError as e:
            result = False
        # self.Database.Disconnect()
        try:
            with open(self.STOPFILE,"r") as f:
                resultfile=True
        except:
            resultfile= False 
        return resultfile or int(result)
    
    def Stop(self):
        if os.path.exists(self.STOPFILE):
            self.Log.Write("INFO","Main","StoppedWithStopFile","Stop File ile işlemler durduruldu.")
            os.remove(self.STOPFILE)
        else:
            self.Log.Write("INFO","Main","StoppedWithDatabase","Veritabanı ile işlemler durduruldu.")
        self.Log.Write("INFO","Main","Stopped","İşlemler durduruldu.")
        Miner.isStop =True
    
    

    def ScanTrendyolPage(self,url:str):
        url_=url
        if url.startswith("/"):
            url = self.Trendyol.url+url
        self.Log.Write("INFO","Miner","TrendyolScanningPage",self.minerName,f"Trendyol sayfası taranıyor URL: {url} ")
        self.Browser.SetUrl(url)
        self.Browser.Request()
        self.Browser.GetContent()
        Urls.AddNotVisitedLinks(self,self.Trendyol.GetAllUrl())
        self.IfProductAddToProductTable(url_)
        Urls.SetAsVisitedUrl(self,url_)

    def IfProductAddToProductTable(self, url):
        if Urls.isProductUrl(self, url):
            productDetail = self.GetDataJson()
            if not productDetail: return

            product = productDetail["product"]

            productOrderCount = product.get("socialProof", {}).get("orderCountL365D")
            productFavoriteCount = product.get("favoriteCount")
            productAvgScore = product.get("ratingScore", {}).get("averageRating")
            productTotalRate = product.get("ratingScore", {}).get("totalRatingCount")
            productCommentCount = product.get("ratingScore", {}).get("totalCommentCount")
            productGroupID = product.get("productGroupId")
            productCategoryID = product.get("category", {}).get("id")
            productCategoryName = product.get("category", {}).get("name")
            productBrandID = product.get("brand", {}).get("id")
            productBrandName = product.get("brand", {}).get("name")



            productID = product.get("id")
            productName = product.get("name")


            try:
                self.Database.Execute("INSERT INTO category (ID,Name) VALUES (%s,%s)",(productCategoryID,productCategoryName))
            except:
                pass
            try:
                self.Database.Execute("INSERT INTO brand (ID,Name) VALUES (%s,%s)",(productBrandID,productBrandName))
            except:
                pass
            Product.AddProduct(self,productID,productName,productOrderCount,productFavoriteCount,productAvgScore,productTotalRate,productCommentCount,productGroupID,productCategoryID,productBrandID,None)
            
            for merchant in product["merchantListings"]:
                merchantID = merchant.get("merchant", {}).get("id")
                merchantScore = merchant.get("merchant", {}).get("sellerScore")
                merchantName = merchant.get("merchant", {}).get("name")
                merchantOfficalName = merchant.get("merchant", {}).get("officialName")
                merchantCityName = merchant.get("merchant", {}).get("cityName")
                merchantDistrictName = merchant.get("merchant", {}).get("districtName")
                merchantAddress = merchant.get("merchant", {}).get("address")
                price = merchant.get("variants", [{}])[0].get("price", {}).get("sellingPrice")

                try:
                    self.Database.Execute("INSERT INTO shops (ID,score,name,officialName,cityName,districtName,address) VALUES (%s,%s,%s,%s,%s,%s,%s)",(merchantID,merchantScore,merchantName,merchantOfficalName,merchantCityName,merchantDistrictName,merchantAddress))
                except:
                    pass
                try:
                    self.Database.Execute("INSERT INTO seller (sellerID,productID,price) VALUES (%s,%s,%s)",(merchantID,productID,price))
                except:
                    pass

    def CreateTables(self):
            self.Database.Execute("""
CREATE TABLE IF NOT EXISTS category (
    ID INT,
    Name VARCHAR(255),
    UNIQUE (ID)
);
            """)
            self.Database.Execute("""
CREATE TABLE IF NOT EXISTS brand (
    ID INT,
    Name VARCHAR(255),
    UNIQUE (ID)
);
            """)
            self.Database.Execute("""
CREATE TABLE IF NOT EXISTS products (
    productID INT,
    productName LONGTEXT,
    orderCount INT,
    favoriteCount INT,
    averageScore FLOAT,
    totalCount INT,
    commentCount INT,
    productGroupID INT,
    categoryID INT,
    brandID INT,
    data LONGTEXT,
    UNIQUE (productID),
    FOREIGN KEY (categoryID) REFERENCES category(ID),
    FOREIGN KEY (brandID) REFERENCES brand(ID)
);
            """)
            self.Database.Execute("""
CREATE TABLE IF NOT EXISTS shops (
    ID INT,
    score FLOAT,
    name VARCHAR(255),
    officialName TEXT,
    cityName VARCHAR(255),
    districtName VARCHAR(255),
    address TEXT,
    UNIQUE (ID)
);
            """)
            self.Database.Execute("""
CREATE TABLE IF NOT EXISTS seller (
    sellerID INT,
    productID INT,
    price FLOAT,
    FOREIGN KEY (productID) REFERENCES products(productID),
    FOREIGN KEY (sellerID) REFERENCES shops(ID)
);


        """)
    def IfMagazaAddToMagazeTable(self,url):
        if Urls.isMagazaUrl(self,url):
            magazaID = Magaza.GetMagazaID(self,url)
            Magaza.AddMagazaIDToTableShops(self, magazaID)

    def SetID(self):
        self.minerID = Miner.minerCount
        self.Log.Write("INFO","Miner","MinerDidSetID",f"Miner'e ID:{self.minerID} verildi.")
        Miner.minerCount +=1

    def GetMinerName(self):
        return f"Miner({self.minerID})"
    
    def GetDataJson(self):
        scripts = self.Browser.soup.find_all("script",type="application/javascript")
        for script in scripts:
            content = script.contents[0]
            try:
                content = content[len("window.__PRODUCT_DETAIL_APP_INITIAL_STATE__="):content.index(";window.TYPageName")]
                return json.loads(content)
            except Exception as err:
                self.Log.Write("ERROR","Browser","BrowserGetDataJsonError",self.minerName,"Bilinmeyen hata: \n"+ traceback.format_exc())
            break
        return False


class Urls(Miner):

    def AddNotVisitedLinks(self, urls):

        allUrls = Urls.GetUrls(self).union(Urls.GetVurls(self))
        newUrls = [url for url in urls if url not in allUrls]

        self.Database.Connect()
        addUrlQuey='INSERT IGNORE INTO urls (url) VALUES (%s)'
        try:
            self.Database.ExecuteMany(addUrlQuey,[(url,) for url in newUrls])
        except IntegrityError as err:
            self.Log.Write("ERROR","Database","AddNotVisitedLinksIntegrityError",self.minerName,"Ziyaret edilmeyen siteler eklenemedi: "+ traceback.format_exc())
            self.Log.Write("DEBUG","Database","AddNotVisitedLinksIntegrityError",self.minerName,"Siteler:\n"+"\n".join(newUrls))

        except Exception as err:
            self.Log.Write("ERROR","Database","AddNotVisitedLinksError",self.minerName,"Ziyaret edilmeyen siteler eklenemedi: "+ traceback.format_exc())
            self.Log.Write("DEBUG","Database","AddNotVisitedLinksError",self.minerName,"Siteler:\n"+"\n".join(newUrls))

        # self.Database.Disconnect()
        self.Log.Write("INFO","Database","AddedNotVisitedLinks",self.minerName,"Ziyaret edilmeyen siteler eklendi:\n"+"\n".join(newUrls))

    def SetAsVisitedUrl(self, url):
        self.Database.Connect()
        try:
            try:
                self.Database.Execute("DELETE FROM urls WHERE url = %s",(url,))
            except:
                pass
            self.Database.Execute("INSERT INTO vurls (vurl) VALUES (%s)",(url,))
        except IntegrityError:
            self.Log.Write("ERROR","Database","AddingSomeVisitedLink",self.minerName,"Aynı link eklemeye çalışıldı: "+url)

        # self.Database.Disconnect()    
        self.Log.Write("INFO","Database","AddedVisitedLink",self.minerName,"Site ziyaret edildi olarak ayarlandı: "+url)

    def GetRandomUrl(self):
        self.Database.Connect()
        self.Database.cursor.execute("SELECT url FROM urls ORDER BY RAND() LIMIT 1")
        result = self.Database.cursor.fetchone()[0]
        # self.Database.Disconnect()
        self.Log.Write("INFO","Miner","GetRandomURL",self.minerName,f"URL: {result}")
        if not result:
            self.Log.Write("INFO","Miner","GetRandomURL",self.minerName,f"URL: {result}")
        return result

    def GetUrls(self):
        self.Database.Connect()
        addUrlQuey="SELECT url FROM urls"
        result = self.Database.Execute(addUrlQuey)
        urls = set(url[0] for url in result)
        # self.Database.Disconnect()
        return urls

    def GetVurls(self):
        self.Database.Connect()
        addUrlQuey="SELECT vurl FROM vurls"
        vurls = set(vurl[0] for vurl in self.Database.Execute(addUrlQuey))
        # self.Database.Disconnect()
        return vurls

    def CreateTableUrls(self):
        self.Database.Connect()
        createTableQuery = '''
        CREATE TABLE IF NOT EXISTS urls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL UNIQUE
        )
        ''' 
        self.Database.Execute(createTableQuery)
        # self.Database.Disconnect()

    def CreateTableVurls(self):
        self.Database.Connect()
        createTableQuery = '''
        CREATE TABLE IF NOT EXISTS vurls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vurl VARCHAR(255) NOT NULL UNIQUE
        )
        ''' 
        self.Database.Execute(createTableQuery)
        # self.Database.Disconnect()

    def isProductUrl(self,url):
        numbers="0123456789"
        if url[-1] not in numbers:
            return False
        
        mode=0
        for char in url[::-1]:

            if mode==0:

                if char in numbers:
                    continue
                elif char == "-":
                    mode=1
                    continue
                else:
                    return False
                
            elif mode==1:
                if char =="p":
                    mode=2
                    continue
                else:
                    return False

            elif mode==2:
                if char =="-":
                    return True
                else:
                    return False
                
            else:
                return False
        return False
    
    def isMagazaUrl(self,url):
        if url.endswith("?sst=0"):
            url = url[:url.index("?")]
        numbers="0123456789"
        if url[-1] not in numbers:
            return False
        
        mode=0
        for char in url[::-1]:

            if mode==0:

                if char in numbers:
                    continue
                elif char == "-":
                    mode=1
                    continue
                else:
                    return False
                
            elif mode==1:
                if char =="m":
                    mode=2
                    continue
                else:
                    return False

            elif mode==2:
                if char =="-":
                    return True
                else:
                    return False
                
            else:
                return False
        return False

    def isHaveAnyUrl(self):
        self.Database.Connect()
        resultUrls = self.Database.Execute("SELECT COUNT(*) FROM urls;")[0][0]
        resultVurls = self.Database.Execute("SELECT COUNT(*) FROM vurls;")[0][0]
        # self.Database.Disconnect()

        self.Log.Write("INFO","Database","UrlCounted",self.minerName,"\nKalan url sayısı: "+str(resultUrls)+" | Tamamlanan url sayısı: "+str(resultVurls)+"\n"+str((resultVurls/(resultUrls+resultVurls))*100))
        return resultUrls


class Magaza(Miner):
    def AddMagazaIDToTableShops(self,magazaID):
        self.Database.Connect()
        try:
                self.Database.Execute("INSERT INTO shops (id) VALUES (%s)",int(magazaID))
        except Exception as e:
            self.Log.Write("ERROR", "Database", "DatabaseMagazaError", self.minerName, "Sorgu yürütülürken hata oluştu.","\nERROR: " + traceback.format_exc())
        # self.Database.Disconnect()

    def GetMagazaID(self,url):
        if url.endswith("?sst=0"):
            url = url[:url.index("?")]
        numbers="0123456789"
        result=""
        for number in url[::-1]:
            if number in numbers:
                result+=str(number)
            else : break
        return result[::-1]

    def CreateTableShops(self):
        self.Database.Connect()
        createTableQuery = '''
            CREATE TABLE IF NOT EXISTS shops (
                ID INT PRIMARY KEY,
                score FLOAT,
                name VARCHAR(255),
                officialName VARCHAR(255),
                cityName VARCHAR(255),
                districtName VARCHAR(255),
                address TEXT
            );
        ''' 
        self.Database.Execute(createTableQuery)
        # self.Database.Disconnect()

class Product(Miner):

    def AddProduct(self, *args):
        self.Database.Connect()
        sql = """
            INSERT INTO products (
                productID, productName, orderCount, favoriteCount, averageScore, totalCount, commentCount,
                productGroupID, categoryID, brandID, data
            ) VALUES (
                %(productID)s, %(productName)s, %(orderCount)s, %(favoriteCount)s, %(averageScore)s, %(totalCount)s,
                %(commentCount)s, %(productGroupID)s, %(categoryID)s, %(brandID)s, %(data)s
            )
        """
        product_data = {
            "productID": args[0],
            "productName": args[1],
            "orderCount": args[2],
            "favoriteCount": args[3],
            "averageScore": args[4],
            "totalCount": args[5],
            "commentCount": args[6],
            "productGroupID": args[7],
            "categoryID": args[8],
            "brandID": args[9],
            "data": args[10]
        }
        try:
            self.Database.Execute(sql, product_data)        
        except Exception as e:
            self.Log.Write("ERROR", "Database", "DatabaseProductError", self.minerName, "Sorgu yürütülürken hata oluştu.","\nERROR: " + traceback.format_exc())
        
        # self.Database.Disconnect()

    def GetProductID(self,url):
        numbers="0123456789"
        if url[-1] not in numbers:
            return False
        
        result=""
        for char in url[::-1]:
            if char in numbers:
                result+=char
            else:
                break
        return result[::-1]
 
    def CreateTableProducts(self):
        self.Database.Connect()
        createTableQuery =  '''
            CREATE TABLE IF NOT EXISTS products (
                productID INT PRIMARY KEY,
                orderCount INT,
                favoriteCount INT,
                averageScore FLOAT,
                totalCount INT,
                commentCount INT,
                productGroupID INT,
                categoryID INT,
                brandID INT,
            );
        ''' 
        self.Database.Execute(createTableQuery)
        # self.Database.Disconnect()
    def CreateTableBrand(self):
        createTableQuery =  '''
            CREATE TABLE IF NOT EXISTS brand (
                ID INT PRIMARY KEY,
                Name VARCHAR(255)
            );
        ''' 
        self.Database.Execute(createTableQuery)
    def CreateTableCategory(self):
        createTableQuery =  '''
            CREATE TABLE IF NOT EXISTS category (
                ID INT PRIMARY KEY,
                Name VARCHAR(255)
            );
        ''' 
        self.Database.Execute(createTableQuery)