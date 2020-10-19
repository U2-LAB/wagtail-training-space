from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from duplicate.models import Collage, CustomImage


class Command(BaseCommand):
    help = 'Clean DB'

    def handle(self, *args, **options):

        ImageModel = get_image_model()
        for image in ImageModel.objects.all():
            image.delete()
        for c_image in CustomImage.objects.all():
            print('Delete CustomImage - ',c_image)
            c_image.delete()
        
        for collage in Collage.objects.all():
            print('Delete collage - ',collage)
            collage.delete()
        
        
        
