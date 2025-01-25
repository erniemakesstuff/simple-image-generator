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
from PIL import ImageDraw


logger = logging.getLogger(__name__)

def download_image(url: str, watermark_text: str, file_path: Path) -> None:
    """Download a single image.

    Args:
        url: URL to download the image from.
        file_path: Path to save the image to.
    """
    req: Request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    # FIXME: This is a potential security issue
    raw_img = urlopen(req).read()  # noqa: S310
    tmp_file = str(random.randint(0, 1000)) + "tmp_image.jpg"
    with open(tmp_file, "wb") as f:
        f.write(raw_img)
        f.close()

    image = Image.open(tmp_file).convert("RGBA")
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
    transparency_value = 128
    draw.text((x + 75, y - 35), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((x - 100, y + 300), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((300, 100), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    draw.text((w - 300, h - 100), watermark_text, fill=(255, 255, 255, transparency_value), font=font, anchor='ms')
    combined_image = Image.alpha_composite(image, txt)
    combined_image.save(file_path)

    if Path(tmp_file).is_file():
        os.remove(tmp_file)


def get_image(query: str, content_lookup_key: str, filepath_prefix: str, watermark_text: str) -> Path:
    """Download random images that are relevant to the provided text.

    Args:
      query: Text used to find relevant images.
    Returns:
        A list of files path to the downloaded images.
    """
    safe_query: str = urllib.parse.quote(query.strip())
    lexica_url: str = f"https://lexica.art/api/v1/search?q={safe_query}"
    logger.info("Downloading Image From Lexica : %s", query)
    filename = filepath_prefix + content_lookup_key
    image_path: Path = Path(filename)
    if os.path.exists(image_path):
        logger.info("Image already exists : %s - %s", id, query)
        return image_path

    try:
        time.sleep(60) # avoid throttling from Lexica
        r: Response = requests.get(lexica_url, timeout=120)

        if not r.ok:
            logger.error("Lexica client response code error: " + str(r.status_code) + " " + r.reason)
        j: object = json.loads(r.text)
    except Exception as ex:
        logger.error("Error Retrieving Lexica Images: " + str(ex))
        return
    max_selection = len(j["images"])
    image_index = random.randint(0, max_selection) % 27 # select top 27
    if not os.path.exists(image_path):
        image_url: str = j["images"][image_index]["src"]
        download_image(image_url, watermark_text, image_path)

    return image_path