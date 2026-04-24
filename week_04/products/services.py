from .models import ProductCategory, Product
from .repositories import category_repo, product_repo

class CategoryService:    
    ## crud of category
    def create_category(self,title, description=None):
        category = ProductCategory(title=title, description=description)
        category.save()
        return category
    
    def get_category_by_id(self, category_id):
        return category_repo.get_category_by_id(category_id)

    def delete_category(self,category_id):
        category = category_repo.get_category_by_id(category_id)
        if category:
            category.delete()
            return True
        return False
    

    def get_all_categories(self):
        return category_repo.get_all_categories()
    
    def update_category(self,category_id, title=None, description=None):
        category = category_repo.get_category_by_id(category_id)
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
        return product_repo.get_all_products()

    def get_product_by_id(self, product_id):
        return product_repo.get_product_by_id(product_id)
    
    def add_product_to_category(self, product_id, category_id):
        product = product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product not found with id = {product_id}")

        category = category_repo.get_category_by_id(category_id)
        if not category:
            raise ValueError(f"Category not found with id = {category_id}") 
        
        product.category = category
        product.save()
        return product

    def get_products_by_category(self, category_id):
        category = category_repo.get_category_by_id(category_id)
        if category:
            return product_repo.get_products_by_category(category)
        return []

    def remove_product_from_category(self, product_id):
        product = product_repo.get_product_by_id(product_id)
        if product:
            product.category = None
            product.save()
        return product
    
    def create_product(self, name, brand, price, category_id=None):
        product = Product(name=name, brand=brand, price=price)
        
        if category_id:
            category = category_repo.get_category_by_id(category_id)
            if category:
                product.category = category

            # this line is important because else it will fail without returning any error if category id is wrong
            else:
                raise ValueError(f"Category not found with id = {category_id}")
                
        product.save()
        return product

category_service = CategoryService()
product_service = ProductService()