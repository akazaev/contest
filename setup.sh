#!/bin/bash

# setup libraries
sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-rus sqlite3 poppler-utils
pip3 install pillow
pip3 install -r requirements.txt
python3 -m spacy download ru_core_news_sm
python3 -m spacy download ru_core_news_lg

# create upload dir
mkdir upload

# init db
cat converter/db/database.sql | sqlite3 documents.db
cat converter/db/surnames.sql | sqlite3 documents.db
cat converter/db/names.sql | sqlite3 documents.db
