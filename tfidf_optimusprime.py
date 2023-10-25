import json
import optuna
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

# Charger les données à partir du fichier JSON
with open('tokenized_data_cleaned.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Charger le fichier JSON des mots-clés
with open('series_keywords.json', 'r', encoding='utf-8') as file:
    keywords_data = json.load(file)

series_tokenized_content = {}
for episode in data:
    series_name = episode['series_name']
    tokenized_content = episode['tokenized_content']
    if series_name not in series_tokenized_content:
        series_tokenized_content[series_name] = []
    tokenized_content = [str(phrase) for phrase in tokenized_content]
    series_tokenized_content[series_name].extend(tokenized_content)

# Fusionner les mots-clés avec le contenu tokenisé
for series_name, keywords in keywords_data.items():
    if series_name in series_tokenized_content:
        series_tokenized_content[series_name].extend(keywords)


def objective(trial):
    ngram_range_choice = trial.suggest_categorical('ngram_range', [(1, 1), (1, 2), (2, 2)])
    use_idf_choice = trial.suggest_categorical('use_idf', [True, False])
    norm_choice = trial.suggest_categorical('norm', ['l1', 'l2'])

    tfidf_vectorizer = TfidfVectorizer(ngram_range=ngram_range_choice, use_idf=use_idf_choice, norm=norm_choice)
    tfidf_matrix = tfidf_vectorizer.fit_transform(
        [" ".join(episodes) for series, episodes in series_tokenized_content.items()])

    correct_matches = 0
    total_keywords = sum(len(v) for v in keywords_data.values())

    print(
        f"\nEssai {trial.number + 1} - Paramètres : ngram_range = {ngram_range_choice}, use_idf = {use_idf_choice}, norm = {norm_choice}")

    def translate_to_english(query, source_lang='fr'):
        translator = Translator(from_lang=source_lang, to_lang="en")
        translation = translator.translate(query)
        return translation

    def get_top_series_with_scores(query, top_n=5):
        english_query = translate_to_english(query, source_lang='fr')
        query_vector = tfidf_vectorizer.transform([english_query])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        similar_series_indices = cosine_similarities.argsort()[::-1]
        return [list(series_tokenized_content.keys())[i] for i in similar_series_indices[:top_n]]

    for idx, (series_name, keywords) in enumerate(keywords_data.items(), 1):
        for keyword in keywords:
            top_series = get_top_series_with_scores(keyword)
            if series_name in top_series:
                correct_matches += 1
        print(f"Traitement de la série {series_name} ({idx}/{len(keywords_data)})")

    accuracy = correct_matches / total_keywords
    print(f"Précision pour cet essai : {accuracy:.4f}")
    return accuracy


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

print("\nRésultat final de l'optimisation :")
print("Meilleure précision :", study.best_value)
print("Meilleurs hyperparamètres :", study.best_params)
