Supports doc, docx, xls, rtf.

Installation
============

Run:

    sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-rus
    pip3 install -r requirements.txt
    python3 -m spacy download ru_core_news_sm
    python3 -m spacy download ru_core_news_lg
    python3 init.py


Start
=====

Run:
    
    ./start.sh


Main page example
=================

    Upload form

    Documents conversion statuses

    [26] documents_oiv_svedeniya_o_raskhodakh_za_2014.docx [3/3 ready]
    [25] documents_oiv_svedeniya_o_raskhodakh_za_2014.docx [3/3 ready]

    Documents parsing statuses

    [26] documents_oiv_svedeniya_o_raskhodakh_za_2014.docx [3 pages]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 1/3 [ready]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 2/3 [ready]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 3/3 [ready]
    
    [25] documents_oiv_svedeniya_o_raskhodakh_za_2014.docx [3 pages]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 1/3 [ready]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 2/3 [ready]
       documents_oiv_svedeniya_o_raskhodakh_za_2014.docx page 3/3 [ready]


API
===

Get conversion progress
-----------------------
GET http://127.0.0.1:5000/progress?uuid={uuid}

Example

http://127.0.0.1:5000/progress?uuid=a07f0256-258f-4464-9f6b-d25d1d06676d

    {
        "files": [ 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/1.jpg",
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/2.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/3.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/4.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/5.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/6.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/7.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/8.jpg", 
            "http://127.0.0.1:5000/file/a07f0256-258f-4464-9f6b-d25d1d06676d/9.jpg"
        ],
        "pages": 9,
        "ready": 6,
        "status": "jpeg",
        "uuid": "a07f0256-258f-4464-9f6b-d25d1d06676d",
        "message": ""
    }

**Json fields description**

**files** - document pages urls;

**pages** - pages total number;

**ready** - ready pages total number;

**message** (additional data)

**status** - 
* new (not processed)
* pdf (pdf ready)
* pdf_failed (pdf processing failed)
* jpg (jpg conversion in progress)
* jpg_failed (jpg processing failed)
* ready (all the pages ready)

NLP progress check
------------------
GET http://localhost:5000/nlp/{uuid}/{page}

Example:

http://localhost:5000/nlp/88fb3490-f40e-47f3-9736-abb42606bfb3/1

    {
      "boxes": {
        "nlp": [
          {
            "h": 100, 
            "text": "\u043c\u043e\u0441\u043a\u0432\u0430", 
            "w": 660, 
            "x": 2006, 
            "y": 699,
            "propn": true
          }, 
            ...
          {
            "h": 32, 
            "text": "\u043c\u043e\u0441\u043a\u0432\u0430", 
            "w": 159, 
            "x": 3948, 
            "y": 5684,
            "propn": false
          }
        ]
      }, 
      "page": 1, 
      "status": "ready", 
      "uuid": "88fb3490-f40e-47f3-9736-abb42606bfb3"
    }

**Json fields description**

**boxes** - parsed text with x, y, h, w, propn (bool);

**page** - page number;

**status** - parsing status

**status** - 
* not_found (not found or process hasn't started yet)
* in_progress (parsing started)
* parsed (text parsed)  
* ready (parsing is completed)


Run image processing
--------------------

POST http://localhost:5000/process/{uuid}/{page}

Example:

http://localhost:5000/process/88fb3490-f40e-47f3-9736-abb42606bfb3/1

Bode example:

    {
      "boxes": {
        "nlp": [
          {
            "h": 100, 
            "text": "\u043c\u043e\u0441\u043a\u0432\u0430", 
            "w": 660, 
            "x": 2006, 
            "y": 699
          }, 
            ...
          {
            "h": 32, 
            "text": "\u043c\u043e\u0441\u043a\u0432\u0430", 
            "w": 159, 
            "x": 3948, 
            "y": 5684
          }
        ]
      }
    }


Tools
-----

* Include words to vocabulary

POST http://localhost:5000/inclide

Body example:

    {
        "words": ["word1", "word2""]
    }


* Exclude words from vocabulary

POST http://localhost:5000/exclude

Body example:

    {
        "words": ["word1", "word2""]
    }


Output
------

* Get JPEG page:

GET http://localhost:5000/file/<uuid>/<page>.jpg

* Get obfuscated JPEG page:

GET http://localhost:5000/file/<uuid>/<page>_new.jpg
