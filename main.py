import os
import sys
from pathlib import Path
from tkinter import filedialog

from app.app_window import AppWindow
from app.image_display import ImageDisplay
from app.image_manager import ImageManager
from app.image_processor import ImageProcessor

if __name__ == "__main__":
    image_manager = ImageManager()
    # image_manager.load_image("Images/1.bmp")
    image_manager.load_folder("Images")
    image_display = ImageDisplay(image_manager)
    image_processor = ImageProcessor(image_manager)
    app_window = AppWindow(image_manager, image_processor, image_display)
    app_window.run()
