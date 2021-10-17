API url example
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
  "uuid": "a07f0256-258f-4464-9f6b-d25d1d06676d"
}

files - document pages
pages - pages total number
ready - ready pages total number
status - 
* new (not processed)
* pdf (pdf ready)
* jpeg (jpeg convertation in progress)
* ready (all the pages ready)
