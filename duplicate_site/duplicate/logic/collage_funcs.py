from duplicate.models import Collage
from duplicate.logic.duplicate_funcs import compare_two_images

from PIL import Image


def add_collage(image: Image) -> Collage:
    """
    Search for existed valid collage.
    If return None -> create new collage.
    """
    for collage in Collage.objects.all():
        if compare_two_images(image.file.path, collage.images.first().image.file.path):
            return collage
        
    latest_number = Collage.objects.count() + 1

    return Collage.objects.create(title=f'Duplicate #{latest_number}')