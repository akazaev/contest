from datetime import datetime
import json
import os
os.environ['OMP_THREAD_LIMIT'] = '1'

import cv2
import pytesseract
from pytesseract import Output
import spacy
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
import regex
from string import punctuation

from converter import UPLOAD_PATH
from converter.db.managers import NlpManager, IncludeManager, ExcludeManager


# download stopwords corpus, you need to run it once
nltk.download("stopwords")


def nlp_analysis(uuid, page):
    # Create lemmatizer and stopwords list

    NlpManager.upsert({'uuid': uuid, 'page': page, 'status': 'in_progress',
                       'json': '', 'final': '', 'timestamp': datetime.now()})
    include = IncludeManager.get()
    exclude = ExcludeManager.get()

    exclude = set(word['word'].lower() for word in exclude)
    include = set(word['word'].lower() for word in include)
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
    custom_tessaract_config = r'-l rus+eng'
    parsed_data = pytesseract.image_to_data(image, output_type=Output.DICT,
                                            config=custom_tessaract_config)

    NlpManager.upsert({'uuid': uuid, 'page': page}, {'status': 'parsed'})
    nlp = spacy.load("ru_core_news_lg")

    boxes = {'nlp': []}
    c = n = 0
    data = []
    full_text = []
    for i in range(len(parsed_data['text'])):
        if float(parsed_data['conf'][i]) > 10:
            data.append({
                'text': parsed_data['text'][i],
                'left': parsed_data['left'][i],
                'top': parsed_data['top'][i],
                'width': parsed_data['width'][i],
                'height': parsed_data['height'][i],
            })
            full_text.append(parsed_data['text'][i])
    full_text = ' '.join(full_text)

    persons = set()
    parsed = nlp(preprocess_text(full_text))
    for named_entity in parsed.ents:
        if named_entity.label_ == 'PER':
            for part in named_entity.text.lower().strip().split():
                persons.add(part)

    print(persons)

    for i in range(len(data)):
        # text text by nlp
        parsed = nlp(preprocess_text(data[i]['text']))
        # print([(w.text, w.pos_) for w in parsed_fio])
        text = str(parsed).lower().strip()
        if not text or text.isspace():
            # skip empty strings
            continue
        if not regex.match(r'^\p{IsCyrillic}+$', text):
            # skip non-cyrillic strings
            continue

        person = False
        if text not in exclude and text in include:
            n += 1
            c += 1
            person = True

        if text not in exclude and text in persons:
            n += 1
            person = True

        boxes['nlp'].append({
            'x': data[i]['left'],
            'y': data[i]['top'],
            'w': data[i]['width'],
            'h': data[i]['height'],
            'propn': person,
            'text': text
        })

    boxes['value'] = c/n if n else 0

    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    NlpManager.upsert({'uuid': uuid, 'page': page}, {'status': 'ready', 'json': json.dumps(boxes)})
    return boxes


if __name__ == '__main__':
    uuid = 'c680467b-88ef-4544-930e-d29f0e305b66'
    page = 1

    nlp_analysis(uuid, page)

    nlp = NlpManager.get_first(uuid=uuid, page=page)
    boxes = json.loads(nlp.json)

    image_path = os.path.join(UPLOAD_PATH, f'{uuid}/pages', f'{page}.jpg')
    image = cv2.imread(image_path)
    print(boxes['value'])

    words = boxes['nlp']
    block = 19
    i = 0
    for word in words:
        x = word['x']
        y = word['y']
        w = word['w']
        h = word['h']
        #print(b)
        #if block != b:
        #    continue
        propn = word['propn']
        if propn:
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
        else:
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 0)
        i += 1
        # if i > 54:
        #     break
    image_path = os.path.join(UPLOAD_PATH, f'{uuid}/pages', f'{page}_test.jpg')
    cv2.imwrite(image_path, image)
