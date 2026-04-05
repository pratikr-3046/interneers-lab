from .models import ProductCategory,Product

class CategoryService:    
    ## crud of category
    def create_category(self,title, description=None):
        category = ProductCategory(title=title, description=description)
        category.save()
        return category
    
    # objects() is a special funciton written in the original document class from which ProductCategory is inherited
    # we  can use it without intantiating the class
    def get_category_by_id(self, category_id):
        return ProductCategory.objects(id=category_id).first()

    def delete_category(self,category_id):
        category = ProductCategory.objects(id=category_id).first()
        if category:
            category.delete()
            return True
        return False
    

    def get_all_categories(self):
        return ProductCategory.objects()
    
    def update_category(self,category_id, title=None, description=None):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return None
        
        if title:
            category.title = title
        if description is not None:
            category.description = description
            
        category.save()
        return category





class ProductService():

    def get_all_products(self):
        return Product.objects()

    def get_product_by_id(self, product_id):
        return Product.objects(id=product_id).first()
    
    def add_product_to_category(self, product_id, category_id):
        product = Product.objects(id=product_id).first()
        if not product:
            raise ValueError("product not found")

        category = ProductCategory.objects(id=category_id).first()
        if not category:
            raise ValueError("category not found") 
        
        product.category = category
        product.save()
        return product

    def get_products_by_category(self, category_id):
        category = ProductCategory.objects(id=category_id).first()
        if category:
            return Product.objects(category=category)
        return []

    def remove_product_from_category(self, product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.category = None
            product.save()
        return product
    
    def create_product(self, name, brand, price, category_id=None):
        product = Product(name=name, brand=brand, price=price)
        
        if category_id:
            category = ProductCategory.objects(id=category_id).first()
            if category:
                product.category = category

            # this line is important because else it will fail without returning any error if category id is wrong
            else:
                raise ValueError("Category cannot be found in the original list")
                
        product.save()
        return product

category_service = CategoryService()
product_service = ProductService()