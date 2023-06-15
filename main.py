from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Store the paths to the image and watermark
image_path = ""
watermark_path = "horns_white.png"  # Replace with your watermark image path
img = None
canvas = None


def start_over():
    global canvas
    canvas.grid_forget()


def upload_file():
    global canvas, image_path
    f_types = [('Jpg Files', '*.jpg'), ("Png Files", "*.png")]
    image_path = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    if canvas is None:
        canvas = Canvas(window, height=img_tk.height(), width=img_tk.width())
        canvas.grid(row=4, column=1)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    # We have to keep a reference to img_tk
    canvas.img = img_tk


def create_watermark():
    global canvas, image_path, watermark_path
    watermark = Image.open(watermark_path).convert("RGBA")
    watermark = watermark.resize((80, 80))  # Or any other size
    watermark_with_transparency = Image.new("RGBA", watermark.size)
    for x in range(watermark.width):
        for y in range(watermark.height):
            r, g, b, a = watermark.getpixel((x, y))
            watermark_with_transparency.putpixel((x, y), (r, g, b, int(a * 0.5)))

    main = Image.open(image_path).convert("RGBA")
    main.paste(watermark_with_transparency, (main.width - watermark_with_transparency.width,
                                             main.height - watermark_with_transparency.height),
               watermark_with_transparency)

    main.save("watermarked.png")
    img_tk = ImageTk.PhotoImage(main)
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    # We have to keep a reference to img_tk
    canvas.img = img_tk


def add_text_watermark():
    global canvas, image_path
    watermark_text = watermark_entry.get()
    main = Image.open(image_path)
    draw = ImageDraw.Draw(main)
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
    textbbox = draw.textbbox((0, 0), watermark_text, font=font)
    textwidth, textheight = textbbox[2], textbbox[3]
    position = main.width - textwidth, main.height - textheight
    draw.text(position, watermark_text, font=font)
    main.save("watermarked.png")
    img_tk = ImageTk.PhotoImage(main)
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img = img_tk


window = Tk()
window.title("Image Watermarking App")

window.config(padx=50, pady=50)

upload_button = Button(text="Upload Picture File", width=30, command=upload_file)
upload_button.grid(row=1, column=1)

watermark_entry = Entry(width=30)
watermark_entry.grid(row=2, column=1)

add_text_watermark_button = Button(text="Add Text Watermark to Current Image", width=30, command=add_text_watermark)
add_text_watermark_button.grid(row=3, column=1)

add_image_watermark_button = Button(text="Add Image Watermark to Current Image", width=30, command=create_watermark)
add_image_watermark_button.grid(row=2, column=2)

clear_button = Button(text="Clear", width=10, command=start_over)
clear_button.grid(row=5, column=1)

window.mainloop()
