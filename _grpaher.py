from neo4j import GraphDatabase
import csv

# Neo4j veritabanına bağlan
uri = "neo4j+s://40768e4d.databases.neo4j.io" # Neo4j URI'si
username = "neo4j" # Neo4j kullanıcı adı
password = "4Xl9qNpe3nuCU0jdCqtMVU1I9qlEIMXG-q6AtKi3sPE" # Neo4j şifresi
driver = GraphDatabase.driver(uri, auth=(username, password))

# CSV dosyalarının yolunu belirtin
products_csv = "products.csv"
category_csv = "category.csv"
brand_csv = "brand.csv"
shops_csv = "shops.csv"
seller_csv = "seller.csv"

# Düğümleri oluşturma işlevi
def create_nodes(tx, csv_file, label):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tx.run(f"CREATE (n:{label}) SET n += $data", data=row)

# İlişkileri oluşturma işlevi
def create_relationships(tx, csv_file, rel_name, start_label, end_label, start_id, end_id):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tx.run(f"MATCH (a:{start_label} {{ {start_id}: $start_id }}), (b:{end_label} {{ {end_id}: $end_id }}) "
                   f"CREATE (a)-[:{rel_name}]->(b)", start_id=row[start_id], end_id=row[end_id])

# Veritabanına düğümleri ve ilişkileri ekleme işlemi
with driver.session() as session:
    # Ürünleri ekleyin
    session.write_transaction(create_nodes, products_csv, "Product")
    
    # Kategorileri ekleyin
    session.write_transaction(create_nodes, category_csv, "Category")
    
    # Markaları ekleyin
    session.write_transaction(create_nodes, brand_csv, "Brand")
    
    # Satıcıları ekleyin
    session.write_transaction(create_nodes, shops_csv, "Shop")
    
    # Ürünlerin kategori ve marka ilişkilerini ekleyin
    session.write_transaction(create_relationships, products_csv, "BELONGS_TO_CATEGORY", "Product", "Category", "categoryID", "categoryID")
    session.write_transaction(create_relationships, products_csv, "MANUFACTURED_BY", "Product", "Brand", "brandID", "brandID")
    
    # Satıcı ve ürün ilişkilerini ekleyin
    session.write_transaction(create_relationships, seller_csv, "SELLS", "Seller", "Product", "productID", "productID")
