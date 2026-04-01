import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("600x400")

# Configure grid


# Create frame to hold canvas and scrollbar
frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Create canvas with fixed height
canvas = tk.Canvas(frame, height=200, bg="lightgray")  # Fixed height of 200px
canvas.grid(row=0, column=0, sticky="nsew")

# Add scrollbar
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)

# Create frame inside canvas to hold the image
image_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=image_frame, anchor="nw")

# Load and display image
try:
    image = Image.open("lang_imgs/image.jpg")

    # Get original dimensions
    img_width, img_height = image.size

    # Option 1: Keep original size (will scroll if taller than canvas)
    photo = ImageTk.PhotoImage(image)

    # Option 2: Resize width to fit canvas (optional)
    # max_width = 500
    # if img_width > max_width:
    #     ratio = max_width / img_width
    #     new_size = (max_width, int(img_height * ratio))
    #     image = image.resize(new_size, Image.LANCZOS)
    #     photo = ImageTk.PhotoImage(image)

    img_label = tk.Label(image_frame, image=photo)
    img_label.pack()
    img_label.image = photo

    # Update scroll region
    image_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

except Exception as e:
    error_label = tk.Label(image_frame, text=f"Error loading image: {e}", fg="red")
    error_label.pack()

root.mainloop()