from django.db import models
from django.db.models.query_utils import Q

from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.images.models import AbstractImage, AbstractRendition, Image 


class Collage(models.Model):
    """
    Model that containes duplicated images.
    """
    title = models.CharField(max_length=255)
                                 
    main_image = models.ForeignKey(
        'duplicate.CustomImage',
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='current_collage'
    )

    image_count = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.title


class CustomImage(models.Model):
    """
    Model that is the link for Wagtail Image model and Collage.
    Image -> CustomImage -> Collage
    This model was created to avoid changing the default Image model.
    """
    collage = models.ForeignKey('duplicate.Collage', 
                                null=True, 
                                blank=True, 
                                on_delete=models.SET_NULL, 
                                related_name='images')
    image = models.OneToOneField(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
    )

    main = models.BooleanField(null=True)
    
    def __str__(self):
        return self.image.title