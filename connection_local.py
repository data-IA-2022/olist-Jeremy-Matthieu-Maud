import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Environnement : source env_ecommerce/bin/activate


files=['olist_customers_dataset', 'olist_geolocation_dataset', 'olist_order_items_dataset', 
       'olist_order_payments_dataset', 'olist_orders_dataset', 'olist_products_dataset', 
       'olist_sellers_dataset', 'product_category_name_translation', 'olist_order_reviews_dataset'] #'olist_order_reviews_dataset',

# Paramètres de connexion à la base de données local
host_local = 'localhost'
port_local = 32768
dbname_local = 'postgres'
user_local = 'postgres'
password_local = 'postgrespw'

# Connexion à la base de données
conn_str_local = f"postgresql://{user_local}:{password_local}@{host_local}:{port_local}/{dbname_local}"

try:
 
    # Création d'un objet engine
    engine_local = create_engine(conn_str_local)

    # Test de connexion
    conn_local = engine_local.connect()
    print("\n-------------------------------------------------------------------------------------------")
    print("|                                   Connexion réussie !                                   |")
    print("===========================================================================================")

    for name in files:
        print("-------------------------------------------------------------------------------------------")
        print(f"| Chargement {name}")
        df = pd.read_csv(f"/home/mikaleff/Bureau/Brazilian_ecommerce/{name}.csv", sep=',')
        print(f"| {df.shape} ")
        print("-------------------------------------------------------------------------------------------")

        df.to_sql(name.replace('.', '_'), engine_local, if_exists='replace') # , index=False


    # Fermeture de la connexion
    conn_local.close()
    print("-------------------------------------------------------------------------------------------")
    print("|                                   Connexion fermée !                                    |")
    print("===========================================================================================\n")
    
except Exception as error:
    print("Erreur lors de la connexion à la base de données :", error)