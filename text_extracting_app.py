import re
import tkinter as tk
from tkinter import filedialog

import pytesseract
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator

import os
import pyperclip
from langdetect import detect, LangDetectException

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

title_font = ("arial", 12)
font = ("arial", 10)
ori_img = None
ori_img_path = None
h_scroll = None
v_scroll = None
lang_map = {
    "English": "en",
    "Khmer": "km",
    "Chinese": "zh-CN",
    "Russian": "ru"
}
lang_name = {v: k for k, v in lang_map.items()}

def on_resize(event=None):
    global h_scroll, v_scroll

    if ori_img is None:
        return
    if event is not None and event.widget != root:
        return

    if v_scroll:
        img_screen.configure(yscrollcommand="")
        v_scroll.destroy()
        v_scroll = None
    if h_scroll:
        img_screen.configure(xscrollcommand="")
        h_scroll.destroy()
        h_scroll = None

    w = left_frame.winfo_width()
    h = left_frame.winfo_height()

    if w <= 1 or h <= 1:
        return

    iw, ih = ori_img.size

    scale = max(w/iw, h/ih)
    niw = int(iw * scale)
    nih = int(ih * scale)

    if w/iw > h/ih:
        req_h_scroll = False
        req_v_scroll = nih > h
    else:
        req_h_scroll = niw > w
        req_v_scroll = nih > w

    resize_img = ori_img.resize((niw,nih), Image.Resampling.LANCZOS)
    photo_img = ImageTk.PhotoImage(resize_img)

    img_screen.delete("all")
    img_screen.create_image(0, 0, anchor="nw", image=photo_img)
    img_screen.img = photo_img

    img_screen.config(scrollregion=(0, 0, niw, nih))

    if req_v_scroll:
        v_scroll = tk.Scrollbar(left_frame, orient="vertical",
                                command=img_screen.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        img_screen.config(yscrollcommand=v_scroll.set)

    if req_h_scroll:
        h_scroll = tk.Scrollbar(left_frame, orient="horizontal",
                                command=img_screen.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        img_screen.config(xscrollcommand=h_scroll.set)

def load_image(img_path):
    global ori_img
    global ori_img_path
    ori_img_path = img_path
    ori_img = Image.open(img_path)
    on_resize()

def txt_op(text, tag):
    output.tag_config("error", foreground="red")
    output.tag_config("normal", foreground="white")

    output.configure(state="normal")
    output.insert(tk.END, f"{text}\n\n", tag)
    output.see(tk.END)
    output.configure(state="disabled")

def translate_text():
    lang = sl_lang.get()
    tar = lang_map.get(lang, "en")
    text = txt_screen.get(1.0, tk.END).strip()

    try:
        detected = detect(text)
        if detected == tar:
            txt_op("Language already matched.", "normal")
            return
    except LangDetectException:
        pass

    if not txt_screen.get(1.0, tk.END).strip():
        txt_op("Error: translate fail, cannot detected text.", "error")
        return

    txt_op(f"Translating text to {lang}....", "normal")
    convert(tar)

def convert(tar_lang=None):
    global ori_img

    if not ori_img:
        return

    try:
        text = pytesseract.image_to_string(ori_img, lang="eng+khm+chi_sim+rus", config="--oem 1 --psm 6").strip()

        if not text:
            txt_op("Error: converting fail, no text detected.", "error")
            return

        result = GoogleTranslator(source="auto", target=tar_lang).translate(text) if tar_lang else text

        txt_screen.configure(state="normal")
        txt_screen.delete(1.0, tk.END)
        txt_screen.insert(tk.END, result)
        txt_screen.configure(state="disabled")

        if not tar_lang:
            data = pytesseract.image_to_data(ori_img, lang="eng+khm+chi_sim+rus", config="--oem 1 --psm 6",
                                             output_type=pytesseract.Output.DICT)
            text = " ".join([t for t in data["text"] if t.strip()])
            confidences = [int(c) for c in data["conf"] if int(c) != -1]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0

            try:
                detected = detect(text)
                lang_text = f"Language detected: {lang_name.get(detected, detected)}"
            except LangDetectException:
                lang_text = "Language detected: Unknown"

            op_text = (f"File: {ori_img_path}\n"
                       f"Characters detected: {len(text)}\n"
                       f"{lang_text}\n"
                       f"Confidence: {avg_conf:.1f}%")

            txt_op(op_text, "normal")
    except Exception as e:
        txt_op(f"{e}", "error")

def select_image():
    DEFAULT_DIR = "D:/Meow-Meow/Python/uni_py_projects/lang_imgs"
    os.makedirs(DEFAULT_DIR, exist_ok=True)

    img_path = filedialog.askopenfilename(
        title="Select an image",
        initialdir=DEFAULT_DIR,
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )

    if img_path:
        load_image(img_path)
        convert()

def save_file():
    global ori_img
    DEFAULT_DIR = "D:/Meow-Meow/Python/uni_py_projects/lang_texts"
    os.makedirs(DEFAULT_DIR, exist_ok=True)

    if not ori_img:
        txt_op("Error: no image selected.", "error")
        return

    file_path = filedialog.asksaveasfilename(
        title="Save text file",
        defaultextension=".txt",
        initialdir=DEFAULT_DIR,
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(txt_screen.get(1.0, tk.END))
    txt_op(f"File saved: {file_path}", "normal")

def copy_text():
    text = txt_screen.get(1.0, tk.END).strip()

    if not text:
        txt_op("Error: copy fail, cannot detected text.", "error")
        return

    pyperclip.copy(text)
    txt_op("Text copied.", "normal")

# init
root = tk.Tk()
root.geometry("600x450")
root.config(padx=10, pady=10)
root.minsize(600, 450)

root.bind("<Configure>", on_resize)
root.after(100, on_resize, None)

# for scaling size
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=1)

# title of the app
tlabel = tk.Label(root, text="An app 4 something", font=title_font)
tlabel.grid(columnspan=2, row=0, column=0, pady=(0, 10))

# screen for displaying image
left_frame = tk.Frame(root, width=285, highlightthickness=1, highlightbackground="green")
left_frame.grid(column=0, row=1, padx=(0, 3), sticky="nsew")
left_frame.grid_propagate(False)
left_frame.rowconfigure(0, weight=1)
left_frame.columnconfigure(0, weight=1)

img_screen = tk.Canvas(left_frame)
img_screen.grid(row=0, column=0, sticky="nsew")

# screen for displaying text
right_frame = tk.Frame(root, width=285)
right_frame.grid(column=1, row=1, padx=(3, 0), sticky="nsew")
right_frame.grid_propagate(False)
right_frame.rowconfigure(0, weight=1)
right_frame.columnconfigure(0, weight=1)

txt_screen = tk.Text(right_frame, padx=5, pady=5, state="disabled", font=font)
txt_screen.grid(row=0, column=0, sticky="nsew")

# for output detail
op_frame = tk.Frame(root)
op_frame.grid(columnspan=2, row=2, column=0, sticky="nsew")
op_frame.columnconfigure(0, weight=1)
op_frame.rowconfigure(0, weight=1)

output = tk.Text(op_frame, state="disabled", bg="black", height=3, padx=5, pady=5)
output.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

# frame for containing buttons
left_btn_frame = tk.Frame(root)
left_btn_frame.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=(30, 20))

select_btn = tk.Button(left_btn_frame, text="Select Image", font=font, command=select_image)
select_btn.grid(column=0, row=0, padx=3)
save_btn = tk.Button(left_btn_frame, text="Save as File", font=font, command=save_file)
save_btn.grid(column=1, row=0, padx=3)
copy_btn = tk.Button(left_btn_frame, text="Copy Text", font=font, command=copy_text)
copy_btn.grid(column=2, row=0, padx=3)

# frame for translate buttons
right_btn_frame = tk.Frame(root)
right_btn_frame.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(30, 20))

sl_lang = tk.StringVar()
sl_lang.set("Select a Language")
sl_lang.set("English")
langs = tk.OptionMenu(right_btn_frame, sl_lang, "English", "Khmer", "Russian", "Chinese")
langs.config(font=font)
langs.grid(column=1, row=0, padx=3)
tran_btn = tk.Button(right_btn_frame, text="Translate", font=font, command=translate_text)
tran_btn.grid(column=0, row=0, padx=3)

root.mainloop()

