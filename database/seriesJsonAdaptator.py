import json

# The name of your input and output files
input_json_filename = 'tfidf_matrixtest.json'
output_json_filename = 'transformed_tfidf_matrix.json'

# Function to load the existing JSON data
def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save the transformed data to a new JSON file
def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Transform the existing data to the desired structure
def transform_data(existing_data):
    transformed_data = []
    series_id = 1
    for series_name, tfidf_values in existing_data.items():
        series_data = {
            "id": series_id,
            "title": series_name,
            "tfidf_vectors": tfidf_values
        }
        transformed_data.append(series_data)
        series_id += 1  # Incrémenter l'ID pour la prochaine série
    return transformed_data


def main():
    # Load the existing data
    existing_data = load_json(input_json_filename)

    # Transform the data
    transformed_data = transform_data(existing_data)

    # Save the transformed data
    save_json(transformed_data, output_json_filename)

    print(f"Transformation complete. Data saved to '{output_json_filename}'.")

if __name__ == "__main__":
    main()