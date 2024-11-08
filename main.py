import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw
import os

program = TkinterDnD.Tk()
program.minsize(width=800, height=600)
program.title("Image Watermarking App")

image_path = None
original_img = None
save_path = None
font_path = None

def on_drop(event):
    global image_path
    global original_img
    global font_path

    file_path = event.data[1:-1]

    # print(file_path)

    # print(os.path.isfile(file_path))

    # print(file_path[-3:])

    if os.path.isfile(file_path):
        if(file_path[-3:] == "otf"):
            font_path = file_path
        else:
            abs_path = os.path.abspath(file_path)
            label.config(text=f"Absolute Path:\n{abs_path}")
            image_path = abs_path
            original_img = Image.open(image_path).convert("RGBA")
            messagebox.showinfo("Image Loaded", f"Image loaded from:\n{abs_path}")
    else:
        label.config(text="Please drop a valid file.")

def show_image():
    if original_img:
        original_img.show()
    else:
        messagebox.showwarning("No Image", "Please load an image first.")

def show_watermarked_image():
    global save_path
    if save_path:
        watermarked_img = Image.open(save_path)
        watermarked_img.show()
    else:
        messagebox.showwarning("No Image", "Please load an image first.")

def drag_and_drop_image():
    global original_img
    original_img = None
    label.config(text="Drag an image here to see its absolute path")

def add_watermark():
    global original_img
    global image_path
    global save_path

    if not image_path:
        messagebox.showwarning("No Image", "Please load an image first.")
        return

    watermark_text = watermark_entry.get()

    if not watermark_text:
        messagebox.showwarning("No Text", "Please enter watermark text.")
        return

    txt = Image.new("RGBA", original_img.size, (255, 255, 255, 0))

    # Ensure you are using the correct font file path
    try:
        font = ImageFont.truetype(font_path, 50)  # Use raw string or double backslashes
    except IOError:
        messagebox.showerror("Font Error", "Font file not found or unable to load.")
        return

    draw = ImageDraw.Draw(txt)

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = original_img.width - text_width - 15  # 15px from the right edge
    y = original_img.height - text_height - 15  # 15px from the bottom edge

    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    watermarked = Image.alpha_composite(original_img, txt)
    watermarked = watermarked.convert("RGB")

    save_path = os.path.splitext(image_path)[0] + "_watermarked.jpg"
    watermarked.save(save_path, "JPEG")

    messagebox.showinfo("Watermark Added", f"Watermarked image saved as:\n{save_path}")

# GUI setup
welocme_label = tk.Label(program, text="Welcome to Image Watermarking App :)", font=("Arial", 24, "bold"), padx=10, pady=10)
welocme_label.place(x=100, y=0)

label = tk.Label(program, text="Drag an image here to see its absolute path", padx=10, pady=10, wraplength=300)
label.place(x=100, y=300)

show_original_img_button = tk.Button(program, text="Show Original Image", command=show_image, width=20, height=2, font=("Arial", 10, "bold"))
show_original_img_button.place(x=315, y=100)

change_img_button = tk.Button(program, text="Change Image", command=drag_and_drop_image, width=20, height=2, font=("Arial", 10, "bold"))
change_img_button.place(x=50, y=100)

show_watermarked_img_button = tk.Button(program, text="Show Watermarked Image", command=show_watermarked_image, width=20, height=2, font=("Arial", 10, "bold"))
show_watermarked_img_button.place(x=570, y=100)

watermark_lable = tk.Label(program, text="Input watermark text :", width=20, font=("Arial", 10, "bold"))
watermark_lable.place(x=300, y=390)

watermark_entry = tk.Entry(program, width=20, font=("Arial", 10, "bold"))
watermark_entry.place(x=310, y=420)

watermark_button = tk.Button(program, text="Add Watermark", command=add_watermark, font=("Arial", 10, "bold"))
watermark_button.place(x=330, y=450)

program.drop_target_register(DND_FILES)
program.dnd_bind('<<Drop>>', on_drop)

program.mainloop()
