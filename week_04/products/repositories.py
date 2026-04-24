from .models import ProductCategory, Product

class CategoryRepository:
    def get_by_id(self, category_id):
        return ProductCategory.objects(id=category_id).first()

    def get_all(self):
        return ProductCategory.objects()

class ProductRepository:
    def get_by_id(self, product_id):
        return Product.objects(id=product_id).first()

    def get_all(self):
        return Product.objects()
        
category_repo = CategoryRepository()
product_repo = ProductRepository()