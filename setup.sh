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
mongoimport --type csv -d documents -c include --fields word converter/db/surnames.csv
mongoimport --type csv -d documents -c include --fields word converter/db/names.csv
mongoimport --type csv -d documents -c exclude --fields word converter/db/exclude.csv
