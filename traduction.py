import pandas as pd
from translate import Translator

# Chargement du fichier CSV
df = pd.read_csv("/home/matthieu/Formation_IA/Briefs/olist-Jeremy-Matthieu-Maud/archive/product_category_name_translation.csv")

# Fonction de traduction
def translate_category_name(name, target_lang="fr"):
    translator = Translator(to_lang=target_lang)
    translation = translator.translate(name)
    return translation

# Application de la traduction aux noms de catégorie de produits
df['product_category_name_fr'] = df['product_category_name_english'].apply(translate_category_name)
df.to_csv('/home/matthieu/Formation_IA/Briefs/olist-Jeremy-Matthieu-Maud/archive/product_category_name_translation_fr.csv', index=False)

# Affichage du résultat
print(df)
