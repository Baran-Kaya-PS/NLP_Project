import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

# Fonction pour charger la matrice TF-IDF depuis le fichier JSON
def load_tfidf_matrix(file_path='tfidf_matrixtest.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        tfidf_matrix_json = json.load(file)

    # Vérifier la structure du fichier JSON
    for series, tfidf_values in tfidf_matrix_json.items():
        if not isinstance(tfidf_values, dict):
            raise ValueError(f"La série '{series}' n'est pas représentée comme un dictionnaire dans le fichier JSON.")

    return tfidf_matrix_json

# Fonction pour traduire la requête en anglais
def translate_to_english(query, source_lang='fr'):
    translator = Translator(from_lang=source_lang, to_lang="en")
    translation = translator.translate(query)
    return translation

# Fonction pour effectuer une recherche basée sur la matrice TF-IDF
def search_series(query, tfidf_matrix_json, tfidf_vectorizer):
    # Traduire la requête en anglais
    english_query = translate_to_english(query, source_lang='fr')

    # Ajuster le vectoriseur TF-IDF sur les données de séries TV
    tfidf_vectorizer.fit_transform([" ".join(episodes) for series, episodes in tfidf_matrix_json.items()])

    # Convertir la requête en vecteur TF-IDF
    query_vector = tfidf_vectorizer.transform([english_query])

    # Liste pour stocker les résultats de la recherche
    search_results = []

    # Parcourir toutes les séries dans la matrice TF-IDF
    for series_name, tfidf_values in tfidf_matrix_json.items():
        # Créer un vecteur avec les TF-IDF de chaque mot pour la série actuelle
        series_vector = [tfidf_values.get(word, 0.0) for word in tfidf_vectorizer.get_feature_names_out()]
        series_vector = [float(value) for value in series_vector]
        series_vector = [series_vector]

        # Calculer la similarité cosinus entre la requête et la série actuelle
        similarity = cosine_similarity(query_vector, series_vector).flatten()[0]

        # Ajouter la série et sa similarité à la liste des résultats
        search_results.append({'series_name': series_name, 'similarity': similarity})

    # Trier les résultats par similarité décroissante
    search_results = sorted(search_results, key=lambda x: x['similarity'], reverse=True)

    return search_results

# Fonction pour obtenir des recommandations basées sur une série donnée
def recommandation(watched_series, keywords_file='series_keywords.json'):
    # Charger les mots-clés depuis le fichier JSON
    with open(keywords_file, 'r', encoding='utf-8') as file:
        series_keywords = json.load(file)

    # Dictionnaire pour stocker les résultats de la recommandation
    recommendation_results = {}

    # Parcourir les séries regardées
    for series in watched_series:
        # Vérifier si la série a des mots-clés associés
        if series in series_keywords:
            # Récupérer les mots-clés de la série
            series_keywords_list = series_keywords[series]

            # Effectuer une recherche basée sur les mots-clés
            search_results = search_series(" ".join(series_keywords_list), tfidf_matrix_json, tfidf_vectorizer)

            # Parcourir les résultats de la recherche
            for result in search_results:
                series_name = result['series_name']
                similarity = result['similarity']

                # Mettre à jour le dictionnaire avec la plus grande similarité pour chaque série
                # Ne pas ajouter la série si elle a déjà été regardée
                if series_name not in watched_series and (series_name not in recommendation_results or similarity > recommendation_results[series_name]):
                    recommendation_results[series_name] = similarity

    # Trier le dictionnaire par similarité décroissante
    sorted_results = sorted(recommendation_results.items(), key=lambda x: x[1], reverse=True)

    return sorted_results

# Fonction pour revoir les séries déjà regardées
def review_watched_series(watched_series):
    return watched_series

# Initialiser le vectoriseur TF-IDF en dehors de la fonction
tfidf_vectorizer = TfidfVectorizer()

# Charger la matrice TF-IDF
tfidf_matrix_json = load_tfidf_matrix()

# Liste pour stocker les séries regardées
watched_series = []

while True:
    user_action = input("Que voulez-vous faire? (recherche/recommandations/revoir/quitter): ").lower()

    if user_action == 'quitter':
        break

    elif user_action == 'recherche':
        user_query = input("Entrez votre requête : ")
        search_results = search_series(user_query, tfidf_matrix_json, tfidf_vectorizer)

        # Afficher les résultats de la recherche
        print("Résultats de la recherche :")
        for result in search_results:
            print(f"Série : {result['series_name']}, Similarité : {result['similarity']}")
        
        # Demander si l'utilisateur veut ajouter une série à sa liste de séries regardées
        add_to_watched = input("Voulez-vous ajouter une série à votre liste de séries regardées? (oui/non): ").lower()
        if add_to_watched == 'oui':
            series_to_add = input("Entrez le nom de la série à ajouter : ")
            watched_series.append(series_to_add)
            print(watched_series)

    elif user_action == 'recommandations':
        if not watched_series:
            print("Aucune série regardée pour obtenir des recommandations.")
        else:
            recommendations = recommandation(watched_series)
        print("Recommandations de séries similaires basées sur les mots-clés des séries regardées:")
        for series, similarity in recommendations:
            print(f"Série : {series}, Similarité : {similarity}")
            
    elif user_action == 'revoir':
        watched_series_review = review_watched_series(watched_series)
        print("Séries déjà regardées :")
        for series in watched_series_review:
            print(series)

    else:
        print("Action non reconnue. Veuillez entrer 'recherche', 'recommandations', 'revoir' ou 'quitter'.")
