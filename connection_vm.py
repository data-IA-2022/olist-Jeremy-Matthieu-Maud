import pg8000
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import paramiko

# Environnement : source env_ecommerce/bin/activate
# Tunnel ssh : ssh -L 5432:localhost:5432 greta@gretap2-mjm.francecentral.cloudapp.azure.com / MDP : @greta*2023!
# Tunnel ssh : ssh -L 5432:172.17.0.2:5432 greta@gretap2-mjm.francecentral.cloudapp.azure.com

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='gretap2-mjm.francecentral.cloudapp.azure.com', username='greta', password='@greta*2023!')

files=['olist_customers_dataset', 'olist_geolocation_dataset', 'olist_order_items_dataset', 
       'olist_order_payments_dataset', 'olist_orders_dataset', 'olist_products_dataset', 
       'olist_sellers_dataset', 'product_category_name_translation', 'olist_order_reviews_dataset'] #'olist_order_reviews_dataset',

# Paramètres de connexion à la base de données distance
host_dist = 'localhost'
port_dist = 5432
dbname_dist = 'postgres'
user_dist = 'postgres'
password_dist = 'greta2023'

# Connexion à la base de données
conn_str_dist = f"postgresql://{user_dist}:{password_dist}@{host_dist}:{port_dist}/{dbname_dist}"

try:
 
    # Création d'un objet engine
    engine_dist = create_engine(conn_str_dist)

    # Test de connexion
    conn_dist = engine_dist.connect()
    print("\n-------------------------------------------------------------------------------------------")
    print("|                                   Connexion réussie !                                   |")
    print("===========================================================================================")

    for name in files:
        print(f"| Chargement {name}")
        df = pd.read_csv(f"/home/mikaleff/Bureau/Brazilian_ecommerce/{name}.csv", sep=',')
        print(f"| {df.shape} ")
        print("-------------------------------------------------------------------------------------------")

        df.to_sql(name.replace('.', '_'), engine_dist, if_exists='replace', index=False) # , index=False


    # Fermeture de la connexion
    conn_dist.close()
    print("-------------------------------------------------------------------------------------------")
    print("|                                   Connexion fermée !                                    |")
    print("===========================================================================================\n")
    
    # Fermer la connexion SSH
    ssh.close()

except Exception as error:
    print("Erreur lors de la connexion à la base de données :", error)