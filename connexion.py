import psycopg2

#vm MJM
try:
    conn = psycopg2.connect(
        user = "postgres",
        password = "greta2023",
        host = "localhost",
        port = "5433",
        database = "postgres"
    )
    cur = conn.cursor()





    # Afficher la version de PostgreSQL
    cur.execute("SELECT version();")
    print("co reussie")
    version = cur.fetchone()
    print("Version : ", version,"\n")

    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")

except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)


#local
try:
    conn1 = psycopg2.connect(
        user = "postgres",
        password = "greta2023",
        host = "localhost",
        port = "5432",
        database = "postgres"
    )
    cur1 = conn1.cursor()

    # Afficher la version de PostgreSQL
    cur1.execute("SELECT version();")
    print("co reussie")
    version = cur1.fetchone()
    print("Version : ", version,"\n")

    #fermeture de la connexion à la base de données
    cur1.close()
    conn1.close()
    print("La connexion PostgreSQL est fermée")

except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)