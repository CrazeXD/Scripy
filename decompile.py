import os
from PIL import Image
import sys

class ImageToDecompile:
    def __init__(self, imagepath):
        self.im = Image.open(imagepath)
        rgb_im = im.convert('RGB')
        pixels = []
