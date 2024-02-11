import os

folder_path = "assets/papers"
pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

for file in pdf_files:
    # Process each PDF file here
    print(file)
