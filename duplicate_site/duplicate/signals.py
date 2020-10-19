from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from wagtail.images.models import Image
from duplicate.models import CustomImage, Collage

from duplicate.logic.collage_funcs import add_collage
from wagtail.core import hooks


######################
# NEED TO BE CHANGED #
######################

# @receiver(post_save, sender=Image)
# def create_custom_image(sender, instance, created, **kwargs):
#     if created:

#         valid_collage = add_collage(instance)

#         CustomImage.objects.create(image=instance, collage=valid_collage)

@receiver(pre_delete, sender=Image)
def delete_custom_image(sender, instance, **kwargs):
    # pass
    sender.objects.get(title=instance)
    custom_image = CustomImage.objects.get(image=instance)
    try:
        id_current_collage = custom_image.collage.id
        if len(CustomImage.objects.filter(collage=id_current_collage)) < 2:
            custom_image.collage.delete()
    except AttributeError:
        pass
    
    custom_image.delete()
    

    
    

@receiver(pre_delete,sender=CustomImage)
def delete_c_image(sender,instance,**kwargs):
    pass
    # if len(CustomImage.objects.filter(collage=id_current_collage)) < 2:
        # current_img.collage.delete()
        
######################


@hooks.register('construct_image_chooser_queryset')
def show_my_uploaded_images_only(images, request):
    collage_id = request.headers['Referer'].split('/')[-2]
    return images.filter(customimage__collage = collage_id)