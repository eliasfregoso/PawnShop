from pdf2image import convert_from_path
from rpalib.parallel_utils import multiprocessing
import os


def get_pdfs_folder() -> str:
    for x in os.listdir('.'):
        if os.path.isdir(x):
            for file in os.listdir(x):
                if file.endswith(".pdf"):
                    return x
    raise Exception("There is no folder in the current directory with at least 1 pdf file")


# Get pdfs_folder name
pdfs_folder: str = get_pdfs_folder()


def pdf_to_img(pdf: str) -> None:
    pages = convert_from_path(f"{pdfs_folder}\\{pdf}")
    for i, page in enumerate(pages):
        page.save(f"images\\{pdf.strip('.pdf')}_{i+1}.jpg", 'JPEG')


if __name__ == "__main__":
    # Initialize images folder
    if "images" not in os.listdir('.'):
        os.mkdir("images")
    else:
        for f in os.listdir("images"):
            os.remove(f"images\\{f}")

    # Read pdf files name
    pdfs: list = [x for x in os.listdir(pdfs_folder) if x.startswith("03") or x.startswith("04")]

    # Convert pdf to img using multiprocessing
    multiprocessing(pdf_to_img, pdfs, max_workers=os.cpu_count()-1)
