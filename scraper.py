import io
import os
import numpy as np
from PIL import Image
import pytesseract
import cv2
from time import time
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

s = requests.Session()
# s.headers.update({"Cookie": "ID"})
correct = 0
total = 0
start_time = time()
for i in range(30000):
    t0 = time()

    r = s.get('https://d89ff86a985b72f37996b8873ebbf4f2.challenge.hackazon.org/craptcha.php', stream=True)
    im = Image.open(r.raw)

    # im.show()

    # im = im.crop((764, 443, 764 + 90, 443 + 30))

    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pixels[i, j][0] >= 200 and pixels[i, j][1] >= 200 and pixels[i, j][2] >= 200:
                pixels[i, j] = (255, 255, 255)

    img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (600, 200), fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    ret, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)

    cap = Image.fromarray(img)

    captcha = pytesseract.image_to_string(cap, config="-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 0 --psm 8")
    x = s.post('https://d89ff86a985b72f37996b8873ebbf4f2.challenge.hackazon.org/', data={'captcha': captcha.lower()})
    print(captcha.lower())
    response = x.content[:620] if len(x.content) > 620 else x.content
    if "Correct" in str(x.content):
        print("Correct!")
        correct += 1
    total += 1

    t1 = time()
    print("Time:", t1 - t0)
    print(correct, correct / total)
    if (t1 - start_time) > 30:
        correct = 0
        total = 0

    if correct == 100:
        print(x.content)
        break

