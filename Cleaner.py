import os
import zipfile
import re
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

    # Overwrite the original file with the cleaned content
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
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

def remove_accents_from_files(path):
    """
    Removes accents from all .srt, .sub, and .txt files in the given directory and its subdirectories.
    """
    for root, _, files in os.walk(path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in ['.srt', '.sub', '.txt']:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Retry opening the file with UTF-8 encoding if an exception occurs
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                content_without_accents = unidecode(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content_without_accents)
                print(f"Removed accents from {file_path}") 
                
def main():                
    Path = os.path.join(os.getcwd(), 'sous-titres')

    # Unzip all files in the directory
    unzip_files(Path)
    
    # Remove accents from all files in the directory
    remove_accents_from_files(Path)
    
    # Process all .srt and .sub files in the directory
    process_files(Path)

    # Clean all subtitles in the directory
    clean_subtitles(Path)
    
    # Remove numbers from all files in the directory
    remove_numbers_from_files(Path)

if __name__ == '__main__':
    main()
