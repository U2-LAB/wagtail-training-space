import os
from django.db.models.aggregates import Count
from django.db.models.enums import Choices
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from .models import Collage, CustomImage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.utils.html import format_html, urlencode
from django.urls import reverse
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


class PermissionCollage(PermissionHelper):
    def user_can_create(self, user):
        return False
    def user_can_delete_obj(self, user, obj):
        return False

class PermissionCustomImage(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        return False
    def user_can_create(self, user):
        return False


class CollageAdmin(ModelAdmin):
    model = Collage
    list_display = ('title', 'get_main_image', 'get_all_duplicates')
    search_fields = ('title',)
    ordering = ('-image_count',)
    # list_filter = ('Duplicates',)
    permission_helper_class = PermissionCollage

    def get_main_image(self,obj):
        if custom_img:=obj.main_image:
            return format_html(f'<img src="{custom_img.image.file.url}" align="center" style="margin: 5px; height: 120px;" width="120px" />')
        else:
            return format_html(f'<img src="{CustomImage.objects.filter(collage=obj.pk)[0].image.file.url}" align="center" style="margin: 5px; height: 120px;" width="120px" />')
            # return '---'
        
    def get_metadata(self,obj):
        parser = createParser(os.getcwd() + obj.image.file.url)
        if not parser:
            return ' ---- '
        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception:
                return ' ---- '
        if not metadata:
            return ' ---- '
        return metadata.exportDictionary()['Metadata']

    def get_all_duplicates(self, obj):
        url = ImageAdmin().url_helper.index_url + '?' + urlencode({'collage__id': obj.id})
        duplicate_html = ''
        all_images = CustomImage.objects.filter(collage=obj.pk)
        for image in all_images[:3]:
            duplicate_html+="""
            <div style="display: flex; flex-direction: column; width: 120px; text-align: center">
                <img src="{}" width="90px" align="center" style="margin: 5px; height: 90px;">
                <span style="">{}</span>
                <small>{} x {}</small>
                <small style="">{:.1f} kB</small>
                
            </div>
            """.format(
                image.image.file.url, 
                self.get_metadata(image)['Comment'], 
                self.get_metadata(image)['Image width'].split()[0],
                self.get_metadata(image)['Image height'].split()[0],
                image.image.file.size / 1024
                )
        if len(all_images) > 3:
            duplicate_html+=f"""
                <div style="display: flex; flex-direction: column;">
                    <a class='button button-small button-secondary' style="margin-top: 70px;" href={url}> Show more ...</a>
                </div>
                """
        html = f"""
            <div style="display:flex;">
                {duplicate_html}
            </div>
        """
        
        return format_html(html)

    # def get_count(self,obj):
        # return self.images.count()

    # get_count_image = get_count(self.obj)

    get_main_image.short_description = 'Main Image'
    get_all_duplicates.short_description = 'Duplicates'
    # image_count.short_description = 'Count of duplicates'

    panels = [
       ImageChooserPanel('main_image')
    ]
    
class ImageAdmin(ModelAdmin):
    model = CustomImage
    list_display = ('show_img', 'collage', 'show_quality',)
    list_filter = ('collage', )
    menu_label = 'customimages'
    # menu_order=-1
    # permission_helper_class = PermissionCustomImage
    def show_img(self, obj):
        return format_html(f'<img src="{obj.image.file.url}" width=100px >')
    
    def show_quality(self,obj):
        parser = createParser(os.getcwd() + obj.image.file.url)
        if not parser:
            return ' ---- '
        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception:
                return ' ---- '
        if not metadata:
            return ' ---- '
        return metadata.exportDictionary()['Metadata']['Comment']

    panels = []

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(CollageAdmin)
modeladmin_register(ImageAdmin)


# Hooks
from wagtail.core import hooks

@hooks.register('construct_main_menu')
def hide_customimages(request, menu_items):
    """
    Hook that hides custom images side bar.
    """
    menu_items[:] = [item for item in menu_items if item.name != 'customimages']