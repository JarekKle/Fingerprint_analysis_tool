from app.image_manager import ImageManager


class ImageProcessor:
    def __init__(self, manager: ImageManager):
        self.manager = manager

    def change_pixel_color(self, coords):
        self.manager.handler.change_pixel_color(coords)

    def convert_to_grayscale(self):
        self.manager.handler = self.manager.handler.convert_to_grayscale()

    def restore_original(self):
        self.manager.restore_original()

    def adjust_brightness(self):
        option = self.manager.handler.ask_adjust_brightness_option()
        self.manager.handler.adjust_brightness(option)

    def display_histogram(self):
        self.manager.handler.display_histogram()

    def stretch_histogram(self):
        self.manager.handler.stretch_histogram()

    def equalize_histogram(self):
        self.manager.handler.equalize_histogram()

    def linear_filter(self):
        kernel, convert_to_grayscale = self.manager.handler.ask_linear_filter_parameters()
        if convert_to_grayscale:
            self.convert_to_grayscale()
        self.manager.handler.linear_filter(kernel)

    def median_filter(self):
        size = self.manager.handler.ask_median_mask_size()
        self.manager.handler.median_filter(size)

    def apply_binarization(self):
        self.manager.handler = self.manager.handler.convert_to_grayscale()
        method = self.manager.handler.ask_binarization_method()
        self.manager.handler.apply_binarization(method)

    def undo_change(self):
        self.manager.handler.undo_change()
        if self.manager.is_image_grayscale(self.manager.handler.img_modified):
            self.manager.handler = self.manager.handler.convert_to_grayscale()

    def change_image(self, step):
        ord = self.manager.current_handler_ord
        count = len(self.manager.handlers)
        new_ord = (ord + step) % count
        new_handler = self.manager.handlers[new_ord - 1]
        self.manager.handler = new_handler
        self.manager.current_handler_ord = new_ord