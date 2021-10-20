Supports doc, docx, xls, rtf.

Main page example
=================

    Upload form
    
    [6] documents_oiv_svedeniya_o_raskhodakh_za_2014.docx [1/3 jpg]
    [5] documents_oiv_svedeniya_o_dokhodakh_df_2016_god.xlsx [?/? pdf]
    [4] documents_oiv_svedeniya_o_dokhodakh_df_2016_god.xlsx [24/24 ready]
    [3] documents_oiv_svedeniya_o_dokhodakh_df_2016_god.xlsx [24/24 ready]
    [2] documents_oiv_svedeniya-o-dokhodakh-za-2014(2).pdf [9/9 ready]
    [1] documents_oiv_svedeniya_o_dokhodakh_raskhodakh_s_1_yanvarya_20_15_g_po_31.doc [5/5 ready]

API
===

Get conversion progress
-----------------------
http://127.0.0.1:5000/progress?uuid={uuid}

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
http://localhost:5000/nlp/{uuid}/{page}.json

Example:

http://localhost:5000/nlp/88fb3490-f40e-47f3-9736-abb42606bfb3/1.json

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
      }, 
      "page": 1, 
      "status": "ready", 
      "uuid": "88fb3490-f40e-47f3-9736-abb42606bfb3"
    }

**Json fields description**

**boxes** - parsed text with x, y, h, w;

**page** - page number;

**status** - parsing status

**status** - 
* not_found (not found or process hasn't started yet)
* in_progress (parsing started)
* ready (parsing is completed)
