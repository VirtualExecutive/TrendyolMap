import folium
from folium import IFrame
import json
from database import Database
from log import Log 


class TrendyolMap:

    TURKEY_COORDINATS_JSON_FILE ="turkey.json" 
    TURKEY_COORDINATS_JSON={}

    turkeyMap = folium.Map(location=(39.925533, 32.866743), zoom_start=6)
    db = Database()
    log = Log()

    @classmethod
    def CreateMap(cls) -> None:
        cls.db.Log = cls.log
        cls.db.host="193.203.168.7"
        cls.db.database="u902215931_trendyolMap"
        cls.db.user="u902215931_yusuf"
        cls.db.password="yusufY.2002"
        cls.db.Connect()
        cls.GetTurkeyCoordinats()
        cls.GetShops()
        cls.PlaceShopsLocationDistricts()
        cls.PlaceLayoutController()

    
    @classmethod
    def SaveMap(cls):
        cls.turkeyMap.save("TrendyolMapp.html")
    
    @classmethod
    def GetTurkeyCoordinats(cls):
        with open(cls.TURKEY_COORDINATS_JSON_FILE,"r",encoding="utf-8") as file:
            cls.TURKEY_COORDINATS_JSON = json.load(file)


    @classmethod
    def AddMarker(cls,location,popup,tooltip,icon=None,add_to=None):

        # Marker'ı ilçe koordinatlarına yerleştir
        folium.Marker(
            location=location,
            popup=popup,
            tooltip=tooltip,
            icon=icon
        ).add_to(add_to)


    @classmethod
    def PlaceShopsLocationDistricts(cls):
        districtLayout = folium.FeatureGroup("İlçeler").add_to(cls.turkeyMap)
        for city, districts in cls.locationShops.items():
            for district, shops in districts.items():
                district = district.replace("i","İ").upper()
                location = cls.TURKEY_COORDINATS_JSON[city][district]
                
                shopList = []
                for shop in shops:
                    shopList.append({
                        "name":shop[1],
                        "ID":shop[0],
                        "cityName":city,
                        "districtName":district,
                        "address":shop[2]
                    })

                iframe = IFrame(html=cls.CreateHTMLPopup(shopList), width=500,height=520)
                popup = folium.Popup(iframe, max_width=2650)
                tooltip = f"{city}, {district}"
                cls.AddMarker(location, popup, tooltip,icon=folium.Icon("blue"),add_to=districtLayout)

    @classmethod
    def CreateHTMLPopup(cls,shop_details:list):
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
                <div class="shop-title shop-info"><a href=https://www.trendyol.com/magaza/a-m-{shop['ID']}?sst=0 target="_blank">{shop['name']}</a></div>
                <div class="shop-info">ID: {shop['ID']}</div>
                <div class="shop-info">Şehir: {shop['cityName']}</div>
                <div class="shop-info">İlçe: {shop['districtName']}</div>
                <div class="shop-info">Adres: {shop["address"]}</div>
            </div>
            """
        html += """
        </div>
        </body>
        </html>
        """
        return html

    @classmethod
    def PlaceLayoutController(cls):
        folium.LayerControl().add_to(cls.turkeyMap)

    @classmethod
    def GetShops(cls):
        cls.locationShops = {}
        shopsResult = cls.db.Execute("SELECT ID, name, cityName, districtName, address FROM shops")

        for shop in shopsResult:

            city = shop[2]
            district = shop[3]

            if city not in cls.locationShops:
                cls.locationShops[city] = {}

            if district not in cls.locationShops[city]:
                cls.locationShops[city][district] = []

            cls.locationShops[city][district].append((shop[0], shop[1],shop[4]))



TrendyolMap.CreateMap()
TrendyolMap.SaveMap()