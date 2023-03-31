import pandas as pd
import time
from deep_translator import GoogleTranslator
from sqlalchemy import create_engine, text, MetaData

# Paramètres de connexion à la base de données local
host_dist = 'localhost'
port_dist = 5432
dbname_dist = 'olist_brazilian_ecommerce'
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

    name="product_category_name_translation"
    df = pd.read_csv(f"/home/mikaleff/Bureau/Brazilian_ecommerce/{name}.csv", sep=',')

    # Fonction de traduction
    def translate_category_name(name, target_lang="fr"):
        translation = GoogleTranslator(source='auto', target=target_lang).translate(name)
        return translation

    # Application de la traduction aux noms de catégorie de produits
    start_time = time.time()
    df['product_category_name_french'] = df['product_category_name_english'].apply(translate_category_name)

    # Affichage du résultat
    print(df)
    end_time = time.time()
    training_time = end_time - start_time
    print(f"\n------------------------------------------------------- Traduction fini => {training_time:.2f} seconds")

    # Upload des données
    training_time=0
    start_time = time.time()

    df.to_sql(name, engine_dist, if_exists='replace', index=False)

    end_time = time.time()
    training_time = end_time - start_time
    print(f"\n------------------------------------------------------- Upload fini => {training_time:.2f} seconds")

    # Fermeture de la connexion
    conn_dist.close()
    print("-------------------------------------------------------------------------------------------")
    print("|                                   Connexion fermée !                                    |")
    print("===========================================================================================\n")
    
except Exception as error:
    print("Erreur lors de la connexion à la base de données :", error)