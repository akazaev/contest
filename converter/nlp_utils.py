import json
import os

import cv2
import pytesseract
from pytesseract import Output
import spacy
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from converter import UPLOAD_PATH, db

# download stopwords corpus, you need to run it once
nltk.download("stopwords")


def nlp_analysis(args):
    uuid, page = args
    # Create lemmatizer and stopwords list

    with db.db() as connection:
        connection.execute(f"insert or replace into nlp (uuid, page, status, json)"
                           f" values('{uuid}', {page}, 'in_progress', '')")
        include = connection.execute(f"select word from include").fetchall()
        exclude = connection.execute(f"select word from exclude").fetchall()

    exclude = set(word for word in exclude)
    include = set(word for word in include)
    image_path = os.path.join(UPLOAD_PATH, f'{uuid}/pages', f'{page}.jpg')

    os.environ['OMP_THREAD_LIMIT'] = '1'
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")

    def preprocess_text(text):
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens
                  if token not in russian_stopwords and token != " " and
                  token.strip() not in punctuation]

        text = " ".join(tokens)
        return text

    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(image_path)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (1,1), 0)
    # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #
    # # Morph open to remove noise and invert image
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # invert = 255 - opening
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('opening', opening)
    # cv2.imshow('invert', invert)

    # Perform text extraction
    custom_tessaract_config = r'-l rus'
    parsed_data = pytesseract.image_to_data(image, output_type=Output.DICT,
                                            config=custom_tessaract_config)
    # print(parsed_data)

    with db.db() as connection:
        connection.execute(f"update nlp set status = 'parsed' where uuid = '{uuid}' and page = {page}")

    nlp = spacy.load("ru_core_news_lg")
    rect_thickness = -1

    boxes = {'nlp': []}
    n_boxes = len(parsed_data['text'])
    for i in range(n_boxes):
        # print(parsed_data['conf'][i])
        if float(parsed_data['conf'][i]) > 10:
            # parse text by nlp
            parsed_fio = nlp(preprocess_text(parsed_data['text'][i]))
            # print([(w.text, w.pos_) for w in parsed_fio])
            text = str(parsed_fio).lower()
            if text.isspace():
                continue

            propn = text not in exclude and(text in include or 'PROPN' in {w.pos_ for w in parsed_fio})
            # print(str(parsed_fio))
            x, y, w, h = (parsed_data['left'][i],
                          parsed_data['top'][i],
                          parsed_data['width'][i],
                          parsed_data['height'][i])
            # image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), rect_thickness)
            boxes['nlp'].append({
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'propn': propn,
                'text': text
            })

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    with db.db() as connection:
        connection.execute(f"update nlp set status = 'ready', json = '{json.dumps(boxes)}' where "
                           f"uuid = '{uuid}' and page = {page}")


if __name__ == '__main__':
    nlp_analysis(('45b9d57f-1a0d-4b7b-87b2-835ab5dd7536', 1))
