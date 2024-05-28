import folium
from folium import IFrame
import json
from database import Database
from log import Log 
import matplotlib.colors as mcolors
import webbrowser

import sys

class TrendyolMap:

    TURKEY_COORDINATS_JSON_FILE ="turkey.json" 
    TURKEY_COORDINATS_JSON={}
    TURKEY_MAP_FILE = "TrendyolMap.html"

    turkeyMap = folium.Map(location=(39.925533, 32.866743), zoom_start=6)
    db = Database()
    log = Log()
    locationShops:dict

    inputs:list

    @classmethod
    def CreateMap(cls) -> None:
        cls.db.Log = cls.log
        cls.db.host="193.203.168.7"
        cls.db.database="u902215931_trendyolMap"
        cls.db.user="u902215931_yusuf"
        cls.db.password="yusufY155"
        cls.db.Connect()
        cls.GetTurkeyCoordinats()

    
    @classmethod
    def SaveMap(cls):
        cls.turkeyMap.save(cls.TURKEY_MAP_FILE)
    
    @classmethod
    def GetTurkeyCoordinats(cls):
        with open(cls.TURKEY_COORDINATS_JSON_FILE,"r",encoding="utf-8") as file:
            cls.TURKEY_COORDINATS_JSON = json.load(file)


    @classmethod
    def AddMarker(cls,location,popup,tooltip,icon=None,add_to=None):

        folium.Marker(
            location=location,
            popup=popup,
            tooltip=tooltip,
            icon=icon
        ).add_to(add_to)


    @classmethod
    def PlaceLocationAllShops(cls,groupName,add_to=turkeyMap):
        districtLayout = folium.FeatureGroup(groupName).add_to(add_to)
        for city, districts in cls.locationShops.items():
            for district, shops in districts.items():
                district = district.replace("i","İ").upper()
                cityUpper = city.replace("i","İ").upper()
                location = cls.TURKEY_COORDINATS_JSON[city][district]
                
                shopList = []
                for shop in shops:
                    shopList.append(shop)

                iframe = IFrame(html=cls.CreateHTMLPopupAllShops(shopList), width=500,height=520)
                popup = folium.Popup(iframe, max_width=2650)
                tooltip = f"{cityUpper}, {district}"
                cls.AddMarker(location, popup, tooltip,icon=folium.Icon("blue"),add_to=districtLayout)

    @classmethod
    def  PlaceLocationSomeProductSellerShop(cls,groupName,add_to=turkeyMap,methodColor="min", isShowLine=True):
        """methodColor = min | max | avg"""

        def create_colormap():
            colors = ["green", "yellow", "red"]
            return mcolors.LinearSegmentedColormap.from_list("custom_gradient", colors)

        def getColor(price,min_price,max_price):
            price = float(price)
            norm = mcolors.Normalize(vmin=min_price, vmax=max_price)
            colormap = create_colormap()
            hexCode = mcolors.to_hex(colormap(norm(price)))
            # print(f"Price:{price} | Vmin: {min_price} | Vmax: {max_price} | HexCode: {hexCode}")
            return hexCode
        
        districtLayout = folium.FeatureGroup(groupName).add_to(add_to)
        minPrice = None
        maxPrice = None
        pricesDistricts = {}
        for city, districts in cls.locationShops.items():
            pricesDistricts[city] ={}
            for district, shops in districts.items():
                pricesDistricts[city][district] ={}
                lminPrice=None
                lmaxPrice=None

                pricesDistricts[city][district]["totalPrice"] = 0

                for shop in shops:
                    price = float(shop["Fiyat"])
                    pricesDistricts[city][district]["totalPrice"] +=price

                    if not lminPrice:
                        lminPrice = price
                        lmaxPrice = price

                    if not minPrice:
                        minPrice = price
                        maxPrice = price

                    if minPrice > price: minPrice = price
                    if maxPrice < price : maxPrice = price
                    if lminPrice > price: lminPrice = price
                    if lmaxPrice < price : lmaxPrice = price
                
                pricesDistricts[city][district]["minPrice"] = lminPrice
                pricesDistricts[city][district]["maxPrice"] = lmaxPrice

        colorsDistrict={}
        for city, districts in cls.locationShops.items():
            colorsDistrict[city] = {}
            for district, shops in districts.items():
                colorsDistrict[city][district]={}
                match methodColor:
                    case "min":
                        price = pricesDistricts[city][district]["minPrice"]
                        iconColor = getColor(price,minPrice,maxPrice)
                    case "max":
                        price = pricesDistricts[city][district]["maxPrice"]
                        iconColor = getColor(price,minPrice,maxPrice)
                    case "avg":
                        price = pricesDistricts[city][district]["totalPrice"]/len(shops)
                        iconColor = getColor(price,minPrice,maxPrice)

                colorsDistrict[city][district]["Color"] = iconColor
                colorsDistrict[city][district]["Price"] = price
        
        if isShowLine:
            sorted_districts = sorted([(city, district, info) for city, districts in colorsDistrict.items() for district, info in districts.items()], key=lambda x: x[2]['Price'])
            for i in range(len(sorted_districts)-1):
                start_city, start_district, _ = sorted_districts[i]
                start_districtU = start_district.replace("i","İ").upper()
                end_city, end_district, _ = sorted_districts[i+1]
                end_districtU = end_district.replace("i","İ").upper()
                start_loc = cls.TURKEY_COORDINATS_JSON[start_city][start_districtU]
                end_loc = cls.TURKEY_COORDINATS_JSON[end_city][end_districtU]
                start_color = colorsDistrict[start_city][start_district]["Color"]
                end_color = colorsDistrict[end_city][end_district]["Color"]


                color_gradient = mcolors.LinearSegmentedColormap.from_list("custom", [start_color, end_color])
                line_color = mcolors.to_hex(color_gradient(0.5)) 

                # Çizgiyi çiz
                folium.PolyLine(locations=[start_loc, end_loc], color=line_color, weight=3).add_to(districtLayout)



        for city, districts in cls.locationShops.items():
            for district, shops in districts.items():

                shopList=[]
                for shop in shops:
                    shop_ = shop.copy()
                    shop_["Color"] = getColor(shop["Fiyat"],minPrice,maxPrice)
                    shopList.append(shop_)
                


                districtU = district.replace("i","İ").upper()
                cityUpper = city.replace("i","İ").upper()
                location = cls.TURKEY_COORDINATS_JSON[city][districtU]

                iframe = IFrame(html=cls.CreateHTMLPopupSomeProductSellerShops(shopList), width=500,height=520)
                popup = folium.Popup(iframe, max_width=2650)
                tooltip = f"{cityUpper}, {districtU}"
                cls.AddMarker(location, popup, tooltip,icon=folium.Icon(color="white",icon_color=colorsDistrict[city][district]["Color"]),add_to=districtLayout)

    @classmethod
    def PlaceLayoutController(cls):
        folium.LayerControl().add_to(cls.turkeyMap)

    @classmethod
    def GetShops(cls,prompt):
        cls.locationShops = {}
        return cls.db.Execute(prompt)
        


    @classmethod
    def OpenMap(cls):
        webbrowser.open_new_tab(cls.TURKEY_MAP_FILE)

    @classmethod
    def CreateHTMLPopupAllShops(cls,shop_details:list):
        html = """
        <html>
        <head>
        <style>
            .shop-info { font-size: 14px; font-family: Rubik, sans-serif; padding: 5px; }
            .shop-title { font-weight: bold;}
            .carousel { display: flex; flex-direction: column; overflow-y: auto; max-height: 500px; }
            .shop-card { flex: 0 0 auto; margin: 2px; background: #f0f0f0; border-radius: 5px; width: 440px; }    
            .shop-title a { color:black; text-decoration: none;}
        </style>
        </head>
        <body>
        <div class="carousel">
        """
        for shop in shop_details:
            html += f"""
            <div class="shop-card">
                <div class="shop-title shop-info"><a href=https://www.trendyol.com/magaza/a-m-{shop['ID']}?sst=0 target="_blank">{shop['Name']}</a></div>
                <div class="shop-info">Kişi&Kurum: {shop['OfficalName']}</div>
                <div class="shop-info">ID: {shop['ID']}</div>
                <div class="shop-info">Şehir: {shop['Şehir']}</div>
                <div class="shop-info">İlçe: {shop['İlçe']}</div>
                <div class="shop-info">Adres: {shop["Address"]}</div>
            </div>
            """
        html += """
        </div>
        </body>
        </html>
        """
        return html

    @classmethod
    def PlaceAllShops(cls):
        shops = cls.GetShops("SELECT ID, name, cityName, districtName, address, officialName FROM shops")
        for shop in shops:
            Id = shop[0]
            name = shop[1]
            city = shop[2]
            district = shop[3]
            address = shop[4]
            officialName= shop[5]


            if city not in cls.locationShops:
                cls.locationShops[city] = {}

            if district not in cls.locationShops[city]:
                cls.locationShops[city][district] = []

            cls.locationShops[city][district].append({
                "ID": Id,
                "Name":name,
                "OfficalName":officialName,
                "Şehir":city,
                "İlçe":district,
                "Address":address
                })
        cls.PlaceLocationAllShops("İLÇELER")

    @classmethod
    def CreateHTMLPopupSomeProductSellerShops(cls,shop_details:list):
        html = """
        <html>
        <head>
        <style>
            .shop-info { font-size: 14px; font-family: Rubik, sans-serif; padding: 5px; }
            .shop-title { font-weight: bold;}
            .carousel { display: flex; flex-direction: column; overflow-y: auto; max-height: 500px; }
            .shop-card { flex: 0 0 auto; margin: 2px; background: #f0f0f0; border-radius: 5px; width: 415px; }    
            .shop-title a { color:black; text-decoration: none;}
        </style>
        </head>
        <body>
        <div class="carousel">
        """
        for shop in shop_details:
            html += f"""
            <div class="shop-card" style="box-shadow: 0px 0px 16px 1px {shop["Color"]}; margin:20px; border:4px solid {shop["Color"]}">
                <div class="shop-title shop-info"><a href=https://www.trendyol.com/magaza/a-m-{shop['ID']}?sst=0 target="_blank">{shop['Name']}</a></div>
                <div class="shop-info">Kişi&Kurum: {shop['OfficalName']}</div>
                <div class="shop-info">ID: {shop['ID']}</div>
                <div class="shop-info">Şehir: {shop['Şehir']}</div>
                <div class="shop-info">İlçe: {shop['İlçe']}</div>
                <div class="shop-info">Adres: {shop["Address"]}</div>
                <div class="shop-info">Fiyat: {shop["Fiyat"]}</div>
            </div>
            """
        html += """
        </div>
        </body>
        </html>
        """
        return html
    
    @classmethod
    def PlaceSomeProductSellerShops(cls, productID,methodColor,isShowLine=True):
        shops = cls.GetShops(f"""
        SELECT s.ID, s.name, s.cityName, s.districtName, s.address, s.officialName, sel.price
        FROM shops s
        JOIN seller sel ON s.ID = sel.sellerID
        JOIN products p ON sel.productID = p.productID
        WHERE p.productID = {productID};
        """)

        for shop in shops:
            Id = shop[0]
            name = shop[1]
            city = shop[2]
            district = shop[3]
            address = shop[4]
            officialName= shop[5]
            price= shop[6]


            if city not in cls.locationShops:
                cls.locationShops[city] = {}

            if district not in cls.locationShops[city]:
                cls.locationShops[city][district] = []

            cls.locationShops[city][district].append({
                "ID": Id,
                "Name":name,
                "OfficalName":officialName,
                "Şehir":city,
                "İlçe":district,
                "Address":address,
                "Fiyat":price
                })
        cls.PlaceLocationSomeProductSellerShop(f"ProductID:{productID} {methodColor}",methodColor=methodColor,isShowLine=isShowLine)

if __name__ == "__main__":
    inputs=sys.argv[1:]
    TrendyolMap.inputs = inputs
    TrendyolMap.CreateMap()
    if(inputs):
        ProductID = inputs[0]
    else:
        ProductID = input("Ürün ID'si girin: ")
    if not ProductID.isnumeric():
        index = ProductID.find("?")
        if(index!=-1):
            ProductID = ProductID[:ProductID.find("?")]
        ProductID = ProductID[ProductID.find("-p-")+3:]
    ProductID = int(ProductID)

    if(inputs):
        method = inputs[1]
    else:
        method = input("Fiyat hesaplama yöntemini seçiniz ( min | avg | max ):")
        

    # TrendyolMap.PlaceAllShops()   
    # TrendyolMap.PlaceSomeProductSellerShops(85074,methodColor="min",isShowLine=True)
    # TrendyolMap.PlaceSomeProductSellerShops(100398,methodColor="min")
    # TrendyolMap.PlaceSomeProductSellerShops(100398,methodColor="avg")
    # TrendyolMap.PlaceSomeProductSellerShops(100398,methodColor="max")
    TrendyolMap.PlaceSomeProductSellerShops(ProductID,methodColor=method) 
    # TrendyolMap.PlaceSomeProductSellerShops(820326336,methodColor="min")
    
    TrendyolMap.PlaceLayoutController()
    TrendyolMap.SaveMap()
    TrendyolMap.OpenMap()