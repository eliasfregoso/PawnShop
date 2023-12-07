from rpalib.parallel_utils import multiprocessing
from rpalib.utils import log
from PIL import Image
import pytesseract
import os
import re


def get_needed_rotation(img):
    out: str = pytesseract.image_to_osd(img)
    return int(re.search(r'(?<=Rotate: )\d+', out).group(0))


def img_to_text(img_name: str) -> None:
    with Image.open(f"images\\{img_name}") as img:
        rot_degrees = get_needed_rotation(img)
        if rot_degrees != 0:
            img = img.rotate(-rot_degrees, expand=True)
        text = pytesseract.image_to_string(img)
        log(f"text\\{img_name.strip('.jpg')}.txt", text)


if __name__ == "__main__":
    # Initialize text folder
    if "text" not in os.listdir('.'):
        os.mkdir("text")
    else:
        for f in os.listdir("text"):
            os.remove(f"text\\{f}")

    # Read image files name
    img_names: list = os.listdir("images")

    # Convert img to text using ocr and multiprocessing
    multiprocessing(img_to_text, img_names, max_workers=os.cpu_count()-1)

