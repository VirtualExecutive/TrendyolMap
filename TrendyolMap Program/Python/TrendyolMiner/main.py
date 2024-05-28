from database import Database
from miner import Miner
from log import Log
from browser import Browser
from trendyol import Trendyol
import json

import sys

class Main():
    Log = Log()
    STOPFILE= "STOP"
    

    def __init__(self) -> None:
        Main.Log.Write("INFO","Main","MainInit","Program başlatılıyor.")
        Miner.Log = Main.Log
        Miner.STOPFILE = self.STOPFILE
        Database.Log = Main.Log
        Browser.Log = Main.Log
        Trendyol.Log = Main.Log
        
        Database.host="193.203.168.7"
        Database.database="u902215931_trendyolMap"
        Database.user="u902215931_yusuf"
        Database.password="yusufY155"
        self.Database = Database()

        


    def Start(self):
        self.Log.Write("INFO","Main","MainStarted","Program başlatıldı.")
        # print("Seçeneklerden birini seçiniz:")
        # print("0 | Exit")
        # print("1 | Mining yap")
        # print("2 | Araştırma yap")

        # u_input= str(input(">>| ")).strip()
        u_input="1"
        match u_input:
            case "0":
                self.Log.Write("INFO","Main","SelectedExit","Çıkış yapılıyor.")
            case "1":
                self.Log.Write("INFO","Main","SelectedMining","Mining seçildi.")
                self.CreateMiner()
            case "2":
                self.Log.Write("INFO","Main","SelectedResearchSpecial","Özel araştırma seçildi.")
                self.Research()



        # self.WaitStop()
        

        


    def CreateMiner(self):
        self.Log.Write("INFO","Miner","CreatedMiner","Yeni Miner oluşturuldu.")
        Miner().Start()

    def Research(self):
        self.Database.Connect()
        products = self.Database.Execute("SELECT productDetail FROM `products` WHERE `productDetail` != 'false' ")
        self.Database.Disconnect()
        dataTemplate={} 

        def analyzeJson(data:dict,parentData:dict):

            if isinstance(data,dict):

                for key,value in data.items():
                    types=str(type(value))
                    if key in parentData:
                        if types not in parentData[key]["type"]:
                            parentData[key]["type"].append(types)
                        parentData[key]["count"] +=1
                    else:
                        parentData[key]={}
                        parentData[key]["type"]=[types]
                        parentData[key]["count"]=1
                    
                    if isinstance(value,dict):
                        for key_,value_ in value.items():
                            if key_ not in parentData[key]:
                                parentData[key][key_] = {}
                            parentData[key][key_] = analyzeJson(value_,parentData[key][key_])

            elif isinstance(data,list):
                for i,item in enumerate(data):
                    types = str(type(item))
                    i = str(i)
                    if i  in parentData:
                        if types not in parentData[i]["type"]:
                            parentData[i]["type"].append(types)
                        parentData[i]["count"]+=1
                    else:
                        parentData[i]={}
                        parentData[i]["type"]=[types]
                        parentData[i]["count"]=1
                    
                    if isinstance(item,dict):
                        for key_,value_ in item.items():
                            if key_ not in parentData[i]:
                                parentData[i][key_] = {}
                            parentData[i][key_] = analyzeJson(value_,parentData[i][key_])
            else:
                    if isinstance(parentData,dict):
                        types=str(type(data))
                        if not parentData:
                            parentData["type"] = [types]
                            parentData["count"] =1
                        else:
                            if types not in parentData["type"]:
                                parentData["type"].append(types)
                            parentData["count"]+=1

            return parentData

        for product in products:
            productDetail = json.loads(product[0])
            productDetail:dict
            dataTemplate = analyzeJson(productDetail,dataTemplate)
                    


        with open("templateProduct.json","w",encoding="utf-8") as f:
            json.dump(dataTemplate,f, indent=4)



if  __name__ == "__main__":
    inputs=sys.argv[1:]
    
    Miner.inputs=inputs
    Main().Start()
