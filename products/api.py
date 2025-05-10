from django.shortcuts import get_list_or_404, get_object_or_404
from typing import List

from ninja import File, UploadedFile
from ninja_extra import Router
from ninja_jwt.authentication import JWTAuth

from .schemas import ProductInSchema, ProductOutSchema, TagInSchema, TagOutSchema
from .models import Product, Tags 

from images.models import Image

api = Router()

@api.get('products/', response=List[ProductOutSchema], tags=["products"])
def get_products(request):
    return get_list_or_404(Product)

@api.get('products/{product_id}', response=ProductOutSchema, tags=["products"])
def get_product(request, product_id : int):
    p = get_object_or_404(Product, id=product_id)
    imgs = Image.objects.filter(product=product_id)
    val = p.__dict__
    imgs_list = []
    for i in imgs:
        imgs_list.append(str(i.image))
        print(type(i.image))
    if imgs_list:
        val['images'] = imgs_list
    return val


# url example : pwt/1/2/3 => product with tags 1, 2 and 3
@api.get('products/tags/{path:tags_path}',
         response=List[ProductOutSchema],
         tags=["products"],
         description="get products with tags; Ex: pwt/1/3 => products with tags 1 AND 3")
def get_products_with_tags(request, tags_path : str):
    pathList = tags_path.split('/')
    qry = Product.objects
    for t in pathList:
        t = int(t)
        qry = qry.filter(tags=t)
    return qry 

@api.post('products/', auth = JWTAuth(), tags=["products"] )
def add_product(
    request,
    payload : ProductInSchema,
    thumbnail : File[UploadedFile] = None ,
    images : File[List[UploadedFile]] = None,
    ):
    return { "success" : payload.write(thumbnail, images).id }

#TODO: handle images and thumbnail updates
@api.put('products/{product_id}', auth = JWTAuth(), tags=["products"])
def update_product(request, 
                   product_id : int,
                   payload: ProductInSchema,
                   thumbnail : File[UploadedFile] = None,
                   ):
    return { "success" : payload.update(product_id) }

@api.delete('products/{product_id}', auth = JWTAuth(), tags=["products"])
def delete_product(request, product_id : int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return { "success" : True }


@api.get('tags/', response=List[TagOutSchema], tags=["tags"])
def get_tags(request):
    return get_list_or_404(Tags)

@api.get('tag/{tag_id}', response=TagOutSchema, tags=["tags"])
def get_tag(request, tag_id : int):
    return get_object_or_404(Tags, id=tag_id)

@api.post('tag/', auth = JWTAuth(), tags=["tags"])
def add_tag(request, payload:TagInSchema):
    return { "id" : payload.write().id }

@api.put('tag/{tag_id}', auth = JWTAuth(), tags=["tags"])
def update_tag(request, tag_id : int, payload : TagInSchema):
    return { "success" : payload.update(tag_id) }

@api.delete('tag/{tag_id}', auth = JWTAuth(), tags=["tags"])
def delete_tag(request, tag_id : int):
    tag = get_object_or_404(Tags, id=tag_id)
    tag.delete()
    return { "success" : True }

