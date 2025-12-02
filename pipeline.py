from app.base_image_handler import BinarizationMethods
from app.image_processor import ImageProcessor
from app.image_manager import ImageManager
class Pipeline:
    def __init__(self, processor = None):
        self.manager = ImageManager()
        self.processor = processor or ImageProcessor(self.manager)
    def load_image(self, img):
        self.manager.load_image(img)

    def save_image(self, name):
        self.manager.save_image(name)

    def load_folder(self, path):
        self.manager.load_folder(path)

    def process_image(self):
        self.processor.apply_clahe()
        self.processor.median_filter(3)
        self.processor.gabor_filter()
        self.processor.apply_binarization(BinarizationMethods.OTSU)
        self.processor.apply_thinning()
        self.processor.apply_crossingnumber()
        self.processor.draw_minutiae()

