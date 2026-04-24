def serialize_category(category):
    if not category:
        return None
    return {
        "id": str(category.id),
        "title": category.title,
        "description": category.description
    }

def serialize_product(product):
    if not product:
        return None
    return {
        "id": str(product.id),
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "category_id": str(product.category.id) if product.category else None
    }