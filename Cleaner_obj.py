import os
import zipfile
import re
from unidecode import unidecode

class Cleaner:
    def __init__(self, path):
        self.path = path

    def unzip_files(self):
        for root, dirs, files in os.walk(self.path):
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

    def clean_subtitles(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
        except PermissionError:
            print(f"Skipping {file_path} due to a permission error.")
            return

        content = re.sub(r'\W+', ' ', content)
        content = re.sub(r'^\d+\s*$', '', content)
        content = re.sub(r'{\d+}{\d+}', '', content)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except PermissionError:
            print(f"Skipping {file_path} due to a permission error.")
            return

    def process_files(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.srt') or file.endswith('.sub'):
                    file_path = os.path.join(root, file)
                    self.clean_subtitles(file_path)
                    print(f"Processed {file_path}")

    def remove_numbers_from_files(self):
        processed_files = 0
        total_files = sum([len(files) for _, _, files in os.walk(self.path)])
        print(f"Found {total_files} files in the directory.")

        for root, _, files in os.walk(self.path):
            for file in files:
                file_ext = os.path.splitext(file)[1]
                if file_ext not in ['.srt', '.sub', '.txt']:
                    continue

                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                cleaned_content = re.sub(r'\d+', '', content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                processed_files += 1
                print(f"Processed {file_path}. {processed_files}/{total_files} files processed.")
        print(f"Finished processing {processed_files} out of {total_files} files.")

    def remove_accents_from_files(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                file_ext = os.path.splitext(file)[1]
                if file_ext in ['.srt', '.sub', '.txt']:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    content_without_accents = unidecode(content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content_without_accents)
                    print(f"Removed accents from {file_path}")

    def execute(self):
        self.unzip_files()
        self.remove_accents_from_files()
        self.process_files()
        self.remove_numbers_from_files()

if __name__ == '__main__':
    cleaner = Cleaner(os.path.join(os.getcwd(), 'sous-titres'))
    cleaner.execute()
