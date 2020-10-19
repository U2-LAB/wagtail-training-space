from celery import shared_task
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.models import F
from wagtail.images.models import Image
from wagtail.images import get_image_model
from progress.bar import Bar

from duplicate.logic import collage_funcs, duplicate_funcs
from duplicate.models import Collage, CustomImage

def work_with_collage(compare_first_image):
    all_collages = Collage.objects.all()
    for collage in all_collages:
        if duplicate_funcs.compare_two_images(
            collage.main_image.image.file.url,
            compare_first_image.image.file.url
            ):
            compare_first_image.collage = collage
            compare_first_image.collage.save()
            return True
    return False

@shared_task
def find_duplicates():
    ImageModel = get_image_model()
    for c_image in CustomImage.objects.all():
        c_image.delete()
    for collage in Collage.objects.all():
        collage.delete()

    for image in ImageModel.objects.all():
        CustomImage.objects.create(image=image)
    bar = Bar('Processing',max=CustomImage.objects.count()) 
    for first_image in CustomImage.objects.all():
        if work_with_collage(first_image):
            bar.next()
            continue
        for second_image in CustomImage.objects.filter(~Q(pk=first_image.id) & Q(collage=None)):
            if duplicate_funcs.compare_two_images(second_image.image.file.url,first_image.image.file.url):
                if not first_image.main:
                    collage_count = Collage.objects.count()
                    new_collage = Collage.objects.create(title=f'Duplicate #{collage_count+1}',main_image=first_image)
                    first_image.collage = new_collage
                    second_image.collage = new_collage
                    first_image.main = True

                    first_image.save()
                    second_image.save()
                else:
                    first_collage = first_image.collage
                    second_image.collage = first_collage
                    first_image.save()
                    second_image.save()
        bar.next()
    bar.finish()
    for collage in Collage.objects.all():
        count_image = len(CustomImage.objects.filter(collage=collage.id))
        collage.image_count=count_image
        collage.save()