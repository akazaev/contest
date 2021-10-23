import os

from PIL import Image, ImageDraw

from converter import UPLOAD_PATH, db


def process_image(uuid, page, boxes):
    path = os.path.join(UPLOAD_PATH, uuid)
    pages_path = os.path.join(path, 'pages')
    page_file = os.path.join(pages_path, f'{page}.jpg')
    output_file = os.path.join(pages_path, f'{page}_new.jpg')

    with db.db() as connection:
        connection.execute(f"update nlp set status = 'obfuscation' where uuid = '{uuid}' and page = {page}")

    boxes = boxes['boxes']['nlp']
    with Image.open(page_file) as image:
        draw = ImageDraw.Draw(image)
        for box in boxes:
            x, y, w, h = box['x'], box['y'], box['w'], box['h']
            shape = (x, y, x + w, y + h)
            draw.rectangle(shape, fill="#000000", outline="black")
        image.save(output_file)

    with db.db() as connection:
        connection.execute(f"update nlp set status = 'obfuscated' where uuid = '{uuid}' and page = {page}")


if __name__ == '__main__':
    boxes = {'boxes': {
            'nlp': [
                {'x': 200, 'y': 100, 'w': 200, 'h': 200}
            ]
        }
    }
    process_image('a8ff28dc-ac7e-40da-9eec-5553c061d853', 2, boxes)
