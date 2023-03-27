import pg8000

# Paramètres de connexion à la base de données
host = 'localhost'
port = 32769
dbname = 'postgres'
user = 'postgres'
password = 'postgrespw'

try:
    # Connexion à la base de données
    conn = pg8000.connect(host=host, port=port, database=dbname, user=user, password=password)
    print("Connexion réussie !")
    
    # Fermeture de la connexion
    conn.close()
    print("Connexion fermée.")
    
except (Exception, pg8000.Error) as error:
    print("Erreur lors de la connexion à la base de données :", error)