import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

class MatrixGenerator:
    def __init__(self, data_path, output_path):
        self.data_path = data_path
        self.output_path = output_path

    def load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def generate_series_tokenized_content(self, data):
        series_tokenized_content = {}
        for episode in data:
            series_name = episode['series_name']
            tokenized_content = episode['tokenized_content']
            if series_name not in series_tokenized_content:
                series_tokenized_content[series_name] = []
            tokenized_content = [str(phrase) for phrase in tokenized_content]
            series_tokenized_content[series_name].extend(tokenized_content)
        return series_tokenized_content

    def generate_tfidf_matrix(self, series_tokenized_content):
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(episodes) for series, episodes in series_tokenized_content.items()])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        return tfidf_matrix, feature_names

    def create_tfidf_json(self, series_tokenized_content, tfidf_matrix, feature_names):
        tfidf_matrix_json = {}
        for i, series_name in enumerate(series_tokenized_content.keys()):
            tfidf_matrix_json[series_name] = {}
            tfidf_values = tfidf_matrix[i].toarray().flatten()
            for j, feature_name in enumerate(feature_names):
                tfidf_value = float(tfidf_values[j])
                if tfidf_value != 0.0:
                    tfidf_matrix_json[series_name][feature_name] = tfidf_value
        return tfidf_matrix_json

    def save_json(self, tfidf_matrix_json):
        with open(self.output_path, 'w', encoding='utf-8') as json_file:
            json.dump(tfidf_matrix_json, json_file, ensure_ascii=False, indent=4)

    def execute(self):
        data = self.load_data()
        series_tokenized_content = self.generate_series_tokenized_content(data)
        tfidf_matrix, feature_names = self.generate_tfidf_matrix(series_tokenized_content)
        tfidf_matrix_json = self.create_tfidf_json(series_tokenized_content, tfidf_matrix, feature_names)
        self.save_json(tfidf_matrix_json)

if __name__ == '__main__':
    data_path = 'tokenized_data_cleaned.json'  # Change according to the file path
    output_path = 'tfidf_matrix.json'
    matrix_generator = MatrixGenerator(data_path, output_path)
    matrix_generator.execute()
