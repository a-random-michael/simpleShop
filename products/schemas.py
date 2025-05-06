from django.shortcuts import get_object_or_404
from ninja import Schema
from shop import settings
from images.models import Image
from .models import Product, Tags
from typing import List
from django.core.files.storage import FileSystemStorage

class TagOutSchema(Schema):
    id : int
    title : str = "default title"

# TODO: add tag thumbnail support.
class TagInSchema(Schema):
    title: str = "default title"

    def write(self):
        return Tags.objects.create(**self.dict())
    
    def update(self, tag_id):
        tag = get_object_or_404(Tags, id=tag_id)
        for attr, val in self.dict().items():
            setattr(tag, attr, val)
        tag.save()
        return True

class ProductOutSchema(Schema):
    id : int
    title : str
    price : float
    description : str = "Description not available"
    tags : List[TagOutSchema] = None
    thumbnail : str # no default as all items are assigned to default.png
    images : List[str] = None


class ProductInSchema(Schema):
    title : str = "default title"
    description : str = None
    price : int = 0
    tags : List[int] = None

    def write(self, thumbnail, images):
        product = Product(title=self.dict()['title'], description=self.dict()['description'])
        product.save()
        if self.dict()['tags'] is not None:
            product.tags.set(self.dict()['tags'])
        if thumbnail is not None :
            codec = thumbnail.name.split('.')[-1]
            product.thumbnail.name = 'thumbnails/' + str(product.id) + '.' +  codec 
            product.save()
            FileSystemStorage(location=settings.MEDIA_ROOT).save(product.thumbnail.name, thumbnail.file)
            #NOTE: further image processing could take place.
        if images is not None:
            for ix,i in enumerate(images):
                img = Image.objects.create(product = product)
                img.image.name = 'images/' + str(product.id) + '/' + str(ix+1) + '.png'
                img.save()
                FileSystemStorage(location=settings.MEDIA_ROOT).save(img.image.name, i.file)
        return product

    def update(self, product_id, thumbnail):
        product = get_object_or_404(Product, id=product_id)
        for attr, val in self.dict().items():
            setattr(product, attr, val)
        if thumbnail is not None:
            FileSystemStorage(location=settings.MEDIA_ROOT).save(product.thumbnail.name, thumbnail.file)
            #NOTE: no need to re-construct image name

        product.save()
        return True 

#NOTE: for ModelSchema:
# class mySchema(ModelsSchema):
# Meta : myModel
# fields : ['id', ....] or '__all__'
