#!/bin/bash

# setup libraries
sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-rus mongodb-org poppler-utils
pip3 install pillow
pip3 install -r requirements.txt
python3 -m spacy download ru_core_news_lg

# create upload dir
mkdir upload

# init db
mongoimport --type csv --mode upsert -d documents -c include --fields word converter/db/surnames.csv
mongoimport --type csv --mode upsert -d documents -c include --fields word converter/db/names.csv
mongoimport --type csv --mode upsert -d documents -c exclude --fields word converter/db/exclude.csv
