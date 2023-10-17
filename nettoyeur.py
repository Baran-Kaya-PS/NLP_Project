import os
import json
from collections import defaultdict

class Nettoyeur:

    def __init__(self, data_path, stopwords_fr_path, stopwords_en_path):
        with open(data_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        with open(stopwords_fr_path, 'r', encoding='utf-8') as file:
            self.stopwords_fr = set(json.load(file))

        with open(stopwords_en_path, 'r', encoding='utf-8') as file:
            self.stopwords_en = set(json.load(file))

    def clean_data(self):
        token_frequency = defaultdict(int)
        total_series = len(self.data)

        # Calculer la fréquence de chaque token
        for series in self.data:
            for token in series["tokenized_content"]:
                token_frequency[token] += 1

        # Supprimer les tokens en fonction de la fréquence et des stopwords
        for series in self.data:
            content = series["tokenized_content"]
            language = series["language"].lower()
            stopwords = self.stopwords_fr if language == "french" else self.stopwords_en

            series["tokenized_content"] = [
                token for token in content
                if token not in stopwords
                and token_frequency[token] < 0.85 * total_series
                and token_frequency[token] > 5  # Supprimer les tokens qui apparaissent moins de 5 fois
            ]

        # Mise à jour du fichier
        with open(os.path.join(os.getcwd(), 'tokenized_data_cleaned.json'), 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

        print("Nettoyage terminé.")

if __name__ == "__main__":
    cleaner = Nettoyeur(
        data_path=os.path.join(os.getcwd(), 'tokenized_data.json'),
        stopwords_fr_path=os.path.join(os.getcwd(), 'stop_words_french.json'),
        stopwords_en_path=os.path.join(os.getcwd(), 'stop_words_english.json')
    )
    cleaner.clean_data()
