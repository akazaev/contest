import json
import os

from PIL import Image, ImageDraw

from converter import UPLOAD_PATH
from converter.db.managers import NlpManager


def process_image(uuid, page, boxes):
    path = os.path.join(UPLOAD_PATH, uuid)
    pages_path = os.path.join(path, 'pages')
    page_file = os.path.join(pages_path, f'{page}.jpg')
    output_file = os.path.join(pages_path, f'{page}_new.jpg')

    NlpManager.upsert({'uuid': uuid, 'page': page}, {'status': 'obfuscation'})

    boxes = boxes['boxes']['nlp']
    with Image.open(page_file) as image:
        draw = ImageDraw.Draw(image)
        for box in boxes:
            x, y, w, h = box['x'], box['y'], box['w'], box['h']
            shape = (x, y, x + w, y + h)
            draw.rectangle(shape, fill="#000000", outline="black")
        image.save(output_file)

    NlpManager.upsert({'uuid': uuid, 'page': page}, {'status': 'obfuscated'})


if __name__ == '__main__':
    # boxes = {'boxes': {
    #         'nlp': [
    #             {'x': 200, 'y': 100, 'w': 200, 'h': 200}
    #         ]
    #     }
    # }
    uuid = '7a7b8d3f-3850-49b7-a080-80dff1a5aac4'
    page = 2
    nlp = NlpManager.get_first(uuid=uuid, page=page)
    boxes = json.loads(nlp.json)
    boxes['nlp'] = [box for box in boxes['nlp'] if box['propn']]

    process_image(uuid, page, {'boxes': boxes})
