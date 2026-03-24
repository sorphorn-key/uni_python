import sys

import pytesseract
from PIL import Image

import tkinter as tk
from tkinter import filedialog

from deep_translator import GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename(
        title="Select a file",
        initialdir="D:/",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    )
    root.destroy()
    return file_path

def extract_text(image):
    try:
        text = pytesseract.image_to_string(image, lang="khm+chi_sim+eng+rus").strip()
        if text:
            translated = GoogleTranslator(source='auto', target='en').translate(text)

            print("\n### Extracted Text ###\n")
            print(f"@@@ Original: {text}\n")
            print(f"@@@ Translated: {translated}\n")
            return
        else:
            print("\nCannot detect!\n")
            return
    except Exception as e:
        print(f"\nError: {e}\n")
        return

while True:
    cmd = input("s > select, f > fill, x > exit\n"
                "Option: ")
    if cmd.lower() == "x":
        print("Exiting...")
        sys.exit()
    elif cmd.lower() == "s":
        file_image = select_file()
    elif cmd.lower() == "f":
        file_image = input("Enter filename: ")
    else:
        print("Error: invalid command!\n")
        continue

    if not file_image:
        print("\nBruh you're not selecting anything!\n")
        continue

    try:
        image = Image.open(file_image)
    except Exception as e:
        print(f"\nError: {e}\n")
        continue

    extract_text(image)


