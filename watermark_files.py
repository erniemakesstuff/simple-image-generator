"""Functions used to process and download images."""
import json
import logging
import os
import time
import urllib
from pathlib import Path
from typing import List
from urllib.request import Request, urlopen
from requests import Response
import requests
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, ImageFilter
from os import listdir
from os.path import isfile, join
import uuid


logger = logging.getLogger(__name__)

def watermark_image(file_path: str, image_name: str, watermark_text: str, save_path: str) -> None:
    """Download a single image.

    Args:
        url: URL to download the image from.
        file_path: Path to save the image to.
    """

    image = Image.open(file_path + "/" + image_name).convert("RGBA")
    txt = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    w, h = image.size
    x, y = int(w / 2), int(h / 2)
    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x
    
    font = ImageFont.truetype("arial.ttf", int(font_size/12))
    transparency_value = 50
    draw.text((x + 75, y - 35), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((x - 100, y + 300), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((300, 100), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((w - 300, h - 100), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')

    interference_text = ImageFont.truetype("arial.ttf", int(font_size/5))
    interference_transparency = 7
    for ny in range(100, h - 100):
        if ny % 285 != 0: # and y % 400 != 0 and y % 500 != 0
            continue
        draw.text((x - 15, ny), watermark_text, fill=(255, 255, 255, interference_transparency), font=interference_text, anchor='ms')
    for ny in range(100, h - 100):
        if ny % 400 != 0: # and y % 400 != 0 and y % 500 != 0
            continue
        draw.text((x + 75, ny), watermark_text, fill=(255, 255, 255, interference_transparency), font=interference_text, anchor='ms')

    combined_image = Image.alpha_composite(image, txt)
    combined_image.save(Path(save_path + "/" + str(uuid.uuid4()) + ".png"))

    thumbnail_size = 256, 256
    combined_image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
    combined_image.save(Path(save_path + "/thumb_" + str(uuid.uuid4()) + ".png"))

def blur_image(file_path: str, image_name: str, save_path: str) -> None:
    """Download a single image.

    Args:
        url: URL to download the image from.
        file_path: Path to save the image to.
    """

    image = Image.open(file_path + "/" + image_name).convert("RGBA")

    thumbnail_size = 800, 800
    image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
    filtered_image = image.filter(ImageFilter.GaussianBlur)
    filtered_2 = filtered_image.filter(ImageFilter.BLUR)
    filtered_3 = filtered_2.filter(ImageFilter.BoxBlur(10))
    filtered_3.save(Path(save_path + "/thumb_" + str(uuid.uuid4()) + ".png"))

"""

path = "/Users/owner/Documents/0 Copper - misc, behind the scenes"
path2 = "/Users/owner/Documents/1 Silver - sensual"
save_path = "/Users/owner/Documents/processed"
watermark_text = "BityFan.com/noraK"

print('watermarking images...')
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for f in onlyfiles:
    if f.startswith("."):
        continue
    watermark_image(path, f, watermark_text, save_path)

onlyfiles = [f for f in listdir(path2) if isfile(join(path2, f))]
for f in onlyfiles:
    if f.startswith("."):
        continue
    watermark_image(path2, f, watermark_text, save_path)

"""

save_path = "/Users/owner/Documents/"
blur_image("/Users/owner/Documents/", "daddy.png", save_path)
blur_image("/Users/owner/Documents/", "boyfriend.png", save_path)
blur_image("/Users/owner/Documents/", "fan.png", save_path)
print('done')