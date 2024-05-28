import pandas as pd
import mysql.connector

# MySQL bağlantısı
connection = mysql.connector.connect(
    host="193.203.168.7",
    user="u902215931_yusuf",
    password="yusufY155",
    database="u902215931_trendyolMap"
    )

tables =[
    "products",
    "category",
    "brand",
    "shops",
    "seller"
]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}",con=connection)
    df.to_csv(f"{table}.csv",index=False)
