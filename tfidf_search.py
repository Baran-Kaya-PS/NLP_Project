import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

# Charger les données à partir du fichier JSON
with open('tokenized_data_cleaned.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Regrouper les textes tokenisés par série (comme dans le code précédent)
series_tokenized_content = {}
for episode in data:
    series_name = episode['series_name']
    tokenized_content = episode['tokenized_content']
    if series_name not in series_tokenized_content:
        series_tokenized_content[series_name] = []
    # Assurez-vous que chaque élément de la liste tokenized_content est une chaîne de caractères
    tokenized_content = [str(phrase) for phrase in tokenized_content]
    series_tokenized_content[series_name].extend(tokenized_content)
    
# Initialiser le vectoriseur TF-IDF en dehors de la fonction
tfidf_vectorizer = TfidfVectorizer()

# Convertir les textes par série en vecteurs TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(episodes) for series, episodes in series_tokenized_content.items()])

# Fonction pour traduire la requête en anglais
def translate_to_english(query, source_lang='fr'):
    translator = Translator(from_lang=source_lang, to_lang="en")
    translation = translator.translate(query)
    return translation

# Fonction pour trouver les séries les plus similaires à la requête de l'utilisateur
def get_top_series(query, top_n=5):
    # Traduire la requête en anglais
    english_query = translate_to_english(query, source_lang='fr')

    # Convertir la requête en vecteur TF-IDF
    query_vector = tfidf_vectorizer.transform([english_query])

    # Calculer la similarité cosinus entre la requête et les séries
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Trier les indices des séries en fonction de leur similarité avec la requête
    similar_series_indices = cosine_similarities.argsort()[::-1]

    # Utiliser un ensemble pour stocker les séries uniques
    unique_series = set()

    # Récupérer les noms des séries les plus similaires
    for i in similar_series_indices:
        series_name = list(series_tokenized_content.keys())[i]
        # Ajouter la série à l'ensemble si elle n'est pas déjà présente
        if series_name not in unique_series:
            unique_series.add(series_name)
            # Si nous avons trouvé suffisamment de séries uniques, sortir de la boucle
            if len(unique_series) >= top_n:
                break

    # Renvoyer les noms des séries uniques
    return list(unique_series)

# Exemple d'utilisation
user_query = input("Entrez votre requête : ")
top_series = get_top_series(user_query)

print("Séries les plus similaires à votre requête :")
for series_name in top_series:
    print(f"Série : {series_name}")
