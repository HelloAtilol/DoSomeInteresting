# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image


def recognize(picture):
    image = Image.open(picture)
    code = pytesseract.image_to_string(image)
    print(code)


if __name__ == '__main__':
    recognize('pic/794129035968223444.jpg')