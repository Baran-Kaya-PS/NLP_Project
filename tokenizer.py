import os
import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def tokenize_text_simple(text):
    """
    Tokenizes the given text using NLTK's word_tokenize.
    """
    return word_tokenize(text)


def tokenize_text_with_stopwords(text, language="english"):
    """
    Tokenise le texte donné en supprimant les stopwords.
    :param text: Texte à tokeniser.
    :param language: Langue du texte (par défaut : anglais).
    :return: Liste de tokens.
    """
    # Tokenisation
    tokens = word_tokenize(text)

    # Suppression des stopwords
    stop_words = set(stopwords.words(language))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    return tokens


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


def main():
    # Define the path to the JSON data
    json_path = os.path.join(os.getcwd(), 'structured_data.json')

    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Tokenize the content for each series
    for series in data:
        language = series.get("language", "english")
        if language == "VO":
            language = "english"
        elif language == "VF":
            language = "french"

        # Since you've already removed stopwords, we'll use the simple tokenizer
        series['tokenized_content'] = tokenize_text_simple(series['content'])

    # Save the tokenized data to a new JSON file
    tokenized_path = os.path.join(os.getcwd(), 'tokenized_data.json')
    with open(tokenized_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Tokenization completed and saved to tokenized_data.json")

    # Clean the tokenized data
    cleaner = Nettoyeur(
        data_path=os.path.join(os.getcwd(), 'tokenized_data.json'),
        stopwords_fr_path=os.path.join(os.getcwd(), 'stop_words_french.json'),
        stopwords_en_path=os.path.join(os.getcwd(), 'stop_words_english.json')
    )
    cleaner.clean_data()


if __name__ == '__main__':
    main()
