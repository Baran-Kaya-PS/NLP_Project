import os
import json
import nltk
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


if __name__ == '__main__':
    main()
