import os
import sys
from pathlib import Path
from tkinter import filedialog

from app.app_window import AppWindow
from app.image_display import ImageDisplay
from app.image_manager import ImageManager
from app.image_processor import ImageProcessor
from pipeline import Pipeline

if __name__ == "__main__":
    # image_manager = ImageManager()
    # # image_manager.load_image("Images/1.bmp")
    # image_manager.load_folder("Images")
    # image_display = ImageDisplay(image_manager)
    # image_processor = ImageProcessor(image_manager)
    # app_window = AppWindow(image_manager, image_processor, image_display)
    # app_window.run()
    pipeline = Pipeline()
    pipeline.load_folder("Images")
    for i, handler in enumerate(pipeline.manager.handlers, start=1):
        img_title = handler.img_title
        pipeline.manager.set_current_handler(i - 1)  # ustawiamy aktualny handler

        # przetwarzamy obraz
        pipeline.process_image()

        # zapisujemy przetworzony obraz
        pipeline.save_image(f"Processed/processed_{img_title}.bmp")