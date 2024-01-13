import os
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Tokenizer:
    def __init__(self, data_path, stopwords_fr_path, stopwords_en_path):
        # Chargement des données et des listes de mots vides
        with open(data_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        with open(stopwords_fr_path, 'r', encoding='utf-8') as file:
            self.stopwords_fr = set(json.load(file))
        with open(stopwords_en_path, 'r', encoding='utf-8') as file:
            self.stopwords_en = set(json.load(file))

    @staticmethod
    def tokenize_text_simple(text):
        # Tokenisation simple du texte
        return word_tokenize(text)

    @staticmethod
    def tokenize_text_with_stopwords(text, language="english"):
        # Tokenisation avec suppression des mots vides
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words(language))
        return [token for token in tokens if token.lower() not in stop_words]

    def tokenize_data(self):
        # Tokenisation des données de chaque série
        for series in self.data:
            language = series.get("language", "english")
            if language == "VO":
                language = "english"
            elif language == "VF":
                language = "french"
            series['tokenized_content'] = self.tokenize_text_simple(series['content'])

    def save_tokenized_data(self, tokenized_path):
        # Sauvegarde des données tokenisées
        with open(tokenized_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        print("Tokenization completed and saved to tokenized_data.json")

    def clean_data(self):
        # Nettoyage des données tokenisées
        token_frequency = defaultdict(int)
        total_series = len(self.data)

        for series in self.data:
            for token in series["tokenized_content"]:
                token_frequency[token] += 1

        for series in self.data:
            content = series["tokenized_content"]
            language = series["language"].lower()
            stopwords = self.stopwords_fr if language == "french" else self.stopwords_en

            series["tokenized_content"] = [
                token for token in content
                if token not in stopwords
                and token_frequency[token] < 0.85 * total_series
                and token_frequency[token] > 5
            ]

        cleaned_path = os.path.join(os.getcwd(), 'tokenized_data_cleaned.json')
        with open(cleaned_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        print("Nettoyage terminé.")

    def execute(self):
        # Exécute les étapes de tokenisation et de nettoyage
        self.tokenize_data()
        tokenized_path = os.path.join(os.getcwd(), 'tokenized_data.json')
        self.save_tokenized_data(tokenized_path)
        self.clean_data()

if __name__ == '__main__':
    json_path = os.path.join(os.getcwd(), 'structured_data.json')
    stopwords_fr_path = os.path.join(os.getcwd(), 'stop_words_french.json')
    stopwords_en_path = os.path.join(os.getcwd(), 'stop_words_english.json')

    tokenizer = Tokenizer(json_path, stopwords_fr_path, stopwords_en_path)
    tokenizer.execute()
