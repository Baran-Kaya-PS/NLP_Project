import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

# Charger les données à partir du fichier JSON
with open('tokenized_data_cleaned.json.', 'r', encoding='utf-8') as file: # Changer selon le chemin du fichier
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

# Obtenir la liste des mots dans l'ordre à partir du vectoriseur TF-IDF
feature_names = tfidf_vectorizer.get_feature_names_out()

# Créer une matrice JSON pour stocker les TF-IDF de chaque mot en fonction de la série
tfidf_matrix_json = {}

# Remplir la matrice JSON
for i, series_name in enumerate(series_tokenized_content.keys()):
    tfidf_matrix_json[series_name] = {}
    # Obtenir les TF-IDF pour la série actuelle
    tfidf_values = tfidf_matrix[i].toarray().flatten()
    # Remplir la matrice JSON avec les TF-IDF de chaque mot
    for j, feature_name in enumerate(feature_names):
        tfidf_matrix_json[series_name][feature_name] = float(tfidf_values[j])

# Enregistrer la matrice JSON dans un fichier
with open('tfidf_matrix.json', 'w', encoding='utf-8') as json_file:
    json.dump(tfidf_matrix_json, json_file, ensure_ascii=False, indent=4)

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

    # Afficher le classement et les valeurs de similarité
    print("Classement du top 5 séries similaires:")
    for rank, i in enumerate(similar_series_indices[:top_n]):
        series_name = list(series_tokenized_content.keys())[i]
        similarity_value = round(cosine_similarities[i], 5)
        print(f"{rank + 1}. Série : {series_name}, Similarité : {similarity_value}")

        # Ajouter la série à l'ensemble si elle n'est pas déjà présente
        if series_name not in unique_series:
            unique_series.add(series_name)

    # Renvoyer les noms des séries uniques
    return list(unique_series)

# Exemple d'utilisation
# user_query = input("Entrez votre requête : ") 
# top_series = get_top_series(user_query)
