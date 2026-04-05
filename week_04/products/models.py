from django.db import models
from mongoengine import Document,StringField,FloatField,ReferenceField

class ProductCategory(Document):
    title=StringField(max_length=100,required=True)
    description = StringField(max_length=300)

    meta={
        'collection':'product categories'
    }

class Product(Document):
    name = StringField(required=True)
    price = FloatField()
    brand = StringField(required=True, default="Unknown")
    # 2 means nullify if product category is deleted
    category = ReferenceField(ProductCategory, reverse_delete_rule=2)
