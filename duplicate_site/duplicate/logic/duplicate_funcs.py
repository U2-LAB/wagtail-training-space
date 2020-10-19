import importlib
from django.conf import settings


def compare_two_images(first_img_url: str, second_img_url: str) -> bool:
    """
    Function, that grabs options from settings.IMAGE_COMPARISON_OPTIONS and use them
    to compare duplicates.
    """
    for option_path in settings.IMAGE_COMPARISON_OPTIONS:
        module_path, func = option_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        if getattr(module, func)(first_img_url, second_img_url):
            # If it is true, then we got the duplicate
            return True

    return False