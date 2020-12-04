import imagehash
import math
import operator
import os

from functools import reduce
from PIL import Image, ImageChops


# The result of each function is compared with specific value.
# Depends on this value, the similarity of two images can be changed.
# There are no one similar value for all functions, because all functions have
# different range of returned function, so this value needs to be different for
# all the functions. 

def compare_hash_codes(first_img_url: str, second_img_url: str) -> bool:
    """
    Get hash-funcs of two images and compare them. If the result is less than 1 then they are similar.
    """
    first_img_hash = imagehash.average_hash(Image.open(os.getcwd()+first_img_url))
    second_img_hash = imagehash.average_hash(Image.open(os.getcwd()+second_img_url))
    
    return abs(first_img_hash - second_img_hash) < 5

def compare_color_histograms(first_img_url: str, second_img_url: str) -> bool:
    """
    Function that calculate color histograms of first img (f_img) and second img (s_img) and compare them.
    """
    first_img = Image.open(os.getcwd()+first_img_url)
    second_img = Image.open(os.getcwd()+second_img_url)
    # print('first_img url ',first_img_url )
    # print(os.getcwd())
    # try:
    h = ImageChops.difference(first_img.convert('1'), second_img.convert('P')).histogram()
    # except ValueError:
        # return False
    
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
        ) / (float(first_img.size[0]) * first_img.size[1])) < 5