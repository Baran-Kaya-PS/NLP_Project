import os
import zipfile
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from unidecode import unidecode



def unzip_files(path):
    """
    Unzips all .zip files in the given directory and its subdirectories.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                    print(f"Extracted {file_path}")
                except zipfile.BadZipFile:
                    print(f"Skipped {file_path} as it's not a valid zip file.")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def process_files(path):
    """
    Processes all .srt and .sub files in the given directory and its subdirectories.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.srt') or file.endswith('.sub'):
                file_path = os.path.join(root, file)
                # Here, you can add any additional processing steps if needed.
                print(f"Processed {file_path}")


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words(['english', 'french']))


def clean_subtitles(file_path):
    """
    Cleans the subtitles in the given file by removing non-alphanumeric characters,
    stopwords, and lemmatizing the words.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except PermissionError:
        print(f"Skipping {file_path} due to a permission error.")
        return

    # Remove non-alphanumeric characters
    content = re.sub(r'\W+', ' ', content)
    
    # Remove the specified patterns
    content = re.sub(r'^\d+\s*$', '', content)  # Removes lines containing only digits
    content = re.sub(r'{\d+}{\d+}', '', content)  # Removes lines containing {digits}{digits}

    # Tokenize, remove stopwords, and lemmatize
    words = word_tokenize(content)
    words = [lemmatizer.lemmatize(word) for word in words if word.lower() not in stop_words]

    # Join the cleaned words back into a string
    cleaned_content = ' '.join(words)

    # Overwrite the original file with the cleaned content
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
    except PermissionError:
        print(f"Skipping {file_path} due to a permission error.")
        return


def process_files(path):
    """
    Processes all .srt and .sub files in the given directory and its subdirectories.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.srt') or file.endswith('.sub'):
                file_path = os.path.join(root, file)
                clean_subtitles(file_path)
                print(f"Processed {file_path}")
                

def unzip_single_file(path, filename):
    """
    Unzips a single file located at the given path.
    """
    file_path = os.path.join(path, filename)
    if file_path.endswith('.zip'):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(path)
            print(f"Extracted {file_path}")
        except zipfile.BadZipFile:
            print(f"Skipped {file_path} as it's not a valid zip file.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def removeNumberFromFiles(path):
    """
    Removes numbers from all files in the given directory and its subdirectories.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.srt') or file.endswith('.sub'):
                file_path = os.path.join(root, file)
                try:
                    os.rename(file_path, os.path.join(root, file.replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '')))
                    print(f"Cleaned {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


def remove_numbers_from_files(path):
    """
    Removes numbers from all .srt, .sub, and .txt files in the given directory and its subdirectories.
    """
    processed_files = 0
    total_files = sum([len(files) for _, _, files in os.walk(path)])
    print(f"Found {total_files} files in the directory.")

    for root, _, files in os.walk(path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext not in ['.srt', '.sub', '.txt']:
                print(f"Skipping {file} with extension {file_ext}.")
                continue

            file_path = os.path.join(root, file)

            print(f"Reading {file_path}...")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Use regex to remove numbers
            cleaned_content = re.sub(r'\d+', '', content)

            # Overwrite the original file with the cleaned content
            print(f"Removing numbers from {file_path}...")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            processed_files += 1
            print(f"Processed {file_path}. {processed_files}/{total_files} files processed.")

    print(f"Finished processing {processed_files} out of {total_files} files.")


def tokenize_text(text):
    # Sentence tokenization
    sentences = sent_tokenize(text)

    # Word tokenization, removing punctuation, and lowercasing
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    tokenized_sentences = [[word.lower() for word in sentence if word.isalpha()] for sentence in tokenized_sentences]

    # Removing stop words (optional)
    stop_words = set(stopwords.words('english'))  # Change 'english' to your desired language if needed
    tokenized_sentences = [[word for word in sentence if word not in stop_words] for sentence in tokenized_sentences]

    return tokenized_sentences


def remove_accents_from_files(path):
    """
    Removes accents from all .srt, .sub, and .txt files in the given directory and its subdirectories.
    """
    for root, _, files in os.walk(path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in ['.srt', '.sub', '.txt']:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                content_without_accents = unidecode(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content_without_accents)
                print(f"Removed accents from {file_path}")