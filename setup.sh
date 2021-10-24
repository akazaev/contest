# setup libraries
sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-rus
pip3 install -r requirements.txt
python3 -m spacy download ru_core_news_sm
python3 -m spacy download ru_core_news_lg

# create upload dir
mkdir upload

# init db
cat converter/db/database.sql | sqlite3 database.db
