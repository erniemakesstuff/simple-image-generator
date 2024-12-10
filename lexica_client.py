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


logger = logging.getLogger(__name__)

def download_image(url: str, file_path: Path) -> None:
    """Download a single image.

    Args:
        url: URL to download the image from.
        file_path: Path to save the image to.
    """
    req: Request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    # FIXME: This is a potential security issue
    raw_img = urlopen(req).read()  # noqa: S310

    with open(file_path, "wb") as f:  # noqa: SCS109
        f.write(raw_img)
        f.close()


def get_image(query: str, content_lookup_key: str, filepath_prefix: str) -> Path:
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
        download_image(image_url, image_path)

    return image_path