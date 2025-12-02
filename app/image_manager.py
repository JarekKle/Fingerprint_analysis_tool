import io
import os
from pathlib import Path
from tkinter import filedialog

import cairosvg
import numpy as np
from PIL import Image, ImageOps

from app.color_image_handler import ColorImageHandler
from app.grayscale_image_handler import GrayscaleImageHandler


class ImageManager:
    def __init__(self):
        self.handlers = []
        self.handler = None
        self.current_handler_ord = 0
        self.original_handler = None


    def load_image(self, img_name=None, folder_mode=False):
        if img_name is None:
            img_name = filedialog.askopenfilename(
                title="Wybierz plik obrazu",
                filetypes=[("Image files", ".jpg .jpeg .png .tiff .bmp .svg")]
            )

        if not img_name:
            raise FileNotFoundError("Nie wybrano żadnego pliku.")

        if img_name.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp")):
            img = Image.open(img_name).resize((320, 480))
            img_title = Path(img_name).stem
        elif img_name.lower().endswith(".svg"):
            png_bytes = cairosvg.svg2png(url=img_name)
            img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            img_title = Path(img_name).stem
        else:
            return None

        handler = self._create_handler(img, img_title)

        if not folder_mode:
            self.handlers = [handler]
            self.handler = handler
            self.original_handler = handler
            return handler.img_modified

        return handler

    def _create_handler(self, img, img_title):
        if self.is_image_grayscale(img):
            return GrayscaleImageHandler(img, img_title)
        else:
            return ColorImageHandler(img, img_title)
    def set_current_handler(self, index):
        if 0 <= index < len(self.handlers):
            self.handler = self.handlers[index]
            self.current_handler_ord = index
    def load_folder(self, folder_name=None):
        if folder_name is None:
            folder_name = filedialog.askdirectory(mustexist=True, initialdir=os.getcwd())

        if not folder_name:
            raise FileNotFoundError("Nie wybrano folderu.")

        self.handlers = []
        self.handler = None
        self.original_handler = None

        for file in os.listdir(folder_name):
            path = os.path.join(folder_name, file)
            try:
                handler = self.load_image(path, folder_mode=True)
                if handler:
                    self.handlers.append(handler)
                    self.originals.append(handler.img_original)
            except:
                pass

        if self.handlers:
            self.handler = self.handlers[0]
            self.original_handler = self.handlers[0]

        return self.handlers

    def replace_image(self, new_img):
        self._assign_handler(new_img)

    def _assign_handler(self, img):
        if self.is_image_grayscale(img):
            self.handler = GrayscaleImageHandler(img)
        else:
            self.handler = ColorImageHandler(img)

    def save_image(self, path):
        if self.handler.img_modified:
            self.handler.img_modified.save(path)
            print(f"Obraz zapisany do {path}")
        else:
            print("Brak obrazu do zapisania")

    def convert_to_grayscale(self):
        new_handler = self.handler.convert_to_grayscale()
        if new_handler is not self.handler:
            self.handler = new_handler

    def restore_original(self):
        self.handler.restore_original()

    @staticmethod
    def is_image_grayscale(img):
        if img.mode == "L":
            return True
        if img.mode in ("RGB", "RGBA"):
            arr = np.array(img)
            return np.allclose(arr[..., 0], arr[..., 1]) and np.allclose(arr[..., 1], arr[..., 2])
        return False

    @staticmethod
    def is_image_binarized(img):
        if not ImageManager.is_image_grayscale(img):
            return False
        img_arr = np.array(img)
        img_size = img_arr.size
        w, b = 0, 0
        for row in img_arr:
            for pixel in row:
                if pixel == 255:
                    w += 1
                if pixel == 0:
                    b += 1
        if w+b == img_size:
            return True
        return False
