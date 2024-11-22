import tkinter
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageChops, ImageEnhance, ImageOps
import numpy as np

global base_img
base_img = None
global cur_img
cur_img = None
global label1 
label1 = None


def btn_upload_image():
    global base_img
    fileTypes = [("Image files", ";*.png;*.jpg;*.jpeg")]
    path = tkinter.filedialog.askopenfilename()

    if len(path):
        img = Image.open(path)
        drow_img(img)
        base_img = img


def btn_save_image():
    global cur_img
    if cur_img is not None:
        fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        save_path = tkinter.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=fileTypes)

        if save_path:
            cur_img.save(save_path)


def drow_img(img):
    global label1
    global cur_img

    if label1 is not None:
        label1.destroy()

    cur_img = img

    img = resize_img(img)
    test = ImageTk.PhotoImage(img)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label_x = (1080 - img.size[0]) / 2
    label1.place(x=label_x, y=100)


def resize_img(img, max_width=600, max_height=600):
    width, height = img.size
    width_ratio = max_width / float(width)
    height_ratio = max_height / float(height)
    ratio = min(width_ratio, height_ratio)
    
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img


def original():
    global base_img
    img = base_img
    drow_img(img)


def blur():
    global base_img    
    img = base_img.filter(ImageFilter.BoxBlur(20))
    drow_img(img)


def noise(noise_level=50):
    global base_img
    img_array = np.array(base_img)
    noise = np.random.randint(-noise_level, noise_level, img_array.shape)
    noisy_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(noisy_array)
    drow_img(img)


def negative():
    global base_img
    img = ImageOps.invert(base_img)
    drow_img(img)


def chromatic_aberration(shift_x=5, shift_y=5, intensity=2.0):
    global base_img
    r, g, b = base_img.split()
    r_shifted = ImageChops.offset(r, shift_x, shift_y)
    b_shifted = ImageChops.offset(b, -shift_x, -shift_y)
    r_final = Image.blend(r, r_shifted, intensity)
    b_final = Image.blend(b, b_shifted, intensity)

    img = Image.merge("RGB", (b_final, g, r_final))
    drow_img(img)


root = tkinter.Tk()
root.geometry("1080x720")
frame = tkinter.Frame(root)

label = tkinter.Label(frame, text="Фильтры изображения").grid(row=1, column=1)

btn_upload = ttk.Button(text="Загрузить", command=btn_upload_image)
btn_save = ttk.Button(text="Сохранить", command=btn_save_image)

btn_original = ttk.Button(text="Original", command=original)
btn_blur = ttk.Button(text="Blur", command=blur)
btn_noise = ttk.Button(text="Noize MC", command=noise)
btn_negative = ttk.Button(text="Negative", command=negative)
btn_chromatic_aberration = ttk.Button(text="Chromakopia", command=chromatic_aberration)

btn_upload.place(x=380, y=20, width=150, height=50)
btn_save.place(x=550, y=20, width=150, height=50)

# Расположение кнопок фильтров под картинкой
btn_original.grid(row=2, column=0, padx=10, pady=10)
btn_blur.grid(row=2, column=1, padx=10, pady=10)
btn_noise.grid(row=2, column=2, padx=10, pady=10)
btn_negative.grid(row=2, column=3, padx=10, pady=10)
btn_chromatic_aberration.grid(row=2, column=4, padx=10, pady=10)

root.mainloop()
