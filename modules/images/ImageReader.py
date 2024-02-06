from PIL import Image
import logging
from torchvision import transforms

class MaxResize(object):
    def __init__(self, max_size=800):
        self.max_size = max_size

    def __call__(self, image):
        width, height = image.size
        current_max_size = max(width, height)
        scale = self.max_size / current_max_size
        resized_image = image.resize((int(round(scale*width)), int(round(scale*height))))
        return resized_image

class ImageReader:

    def __init__(
            self,
            PIL_image: Image,
            device: str = 'cpu',
            verbose: bool = True,
            is_structure: bool = False,
            ):
        self.verbose = verbose
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        self.image = PIL_image
        self.device = device
        self.image_width, self.image_height = self.image.size
        self.image_pixels = self.image.load()
        # log
        logging.info('ImageReader initialized.')
        # transform
        # self._img_transform()
        if is_structure:
            self._img_structure_transform()
        else:
            self._img_detection_transform()
        logging.info('ImageReader transformed.')

    def __str__(self) -> str:
        _str = f"ImageReader for {self.image_path}"
        return _str
    
    # def _img_transform(
    #         self,
    #     ):
    #     self.detection_transform = transforms.Compose([
    #         MaxResize(800),
    #         transforms.ToTensor(),
    #         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    #     ])
    #     self.pixel_values_detect = self.detection_transform(self.image).unsqueeze(0)
    #     self.pixel_values_detect = self.pixel_values_detect.to(self.device)
    #     logging.info(self.pixel_values_detect.shape)
    #     self.structure_transform = transforms.Compose([
    #         MaxResize(1000),
    #         transforms.ToTensor(),
    #         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    #     ])
    #     self.pixel_values_structure = self.structure_transform(self.image).unsqueeze(0)
    #     self.pixel_values_structure = self.pixel_values_structure.to(self.device)
    #     logging.info(self.pixel_values_structure.shape)
    #     return self.pixel_values_detect, self.pixel_values_structure
    
    def _img_detection_transform(
            self,
        ):
        self.detection_transform = transforms.Compose([
            MaxResize(800),
            transforms.ToTensor(),
        ])
        self.pixel_values = self.detection_transform(self.image).unsqueeze(0)
        self.pixel_values = self.pixel_values.to(self.device)
        logging.info(self.pixel_values.shape)
        return self.pixel_values
    
    def _img_structure_transform(
            self,
        ):
        self.structure_transform = transforms.Compose([
            MaxResize(1000),
            transforms.ToTensor(),
        ])
        self.pixel_values = self.structure_transform(self.image).unsqueeze(0)
        self.pixel_values = self.pixel_values.to(self.device)
        logging.info(self.pixel_values.shape)
        return self.pixel_values