from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import category_service, product_service

@csrf_exempt
def api_for_a_category(request, category_id=None):

    if request.method == 'GET':
        if category_id:
            try:
                c = category_service.get_category_by_id(category_id)
                if c:
                    return JsonResponse({"title": c.title, "description": c.description})
                return JsonResponse({"error": "Category not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            try:
                categories = category_service.get_all_categories()
                data=[]
                for c in categories:
                    data.append({"id":str(c.id),"title":str(c.title)})
                return JsonResponse(data, safe=False)
            except Exception as e:
                return JsonResponse({"error": str(e)})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            c = category_service.create_category(data['title'], data.get('description'))
            return JsonResponse({"id": str(c.id)})
        except Exception as e:
            return JsonResponse({"error":str(e)})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_cat = category_service.update_category(category_id, data['title'], data.get('description'))
            
            if updated_cat:
                return JsonResponse({"status": "updated", "title": updated_cat.title})
            return JsonResponse({"error": "category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)})
        
    elif request.method == 'DELETE':
        try:
            success = category_service.delete_category(category_id)
            if success:
                return JsonResponse({"status": "deleted"})
            return JsonResponse({"error": "category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)})




@csrf_exempt
def api_for_a_product(request, product_id=None):

    if request.method == 'GET':
        if product_id:
            try:
                p = product_service.get_product_by_id(product_id)
                if p:
                    return JsonResponse({
                        "id": str(p.id),
                        "name": p.name,
                        "brand": p.brand,
                        "price": p.price,
                        "category_id": str(p.category.id) if p.category else None
                    })
                return JsonResponse({"error": "product not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                products = product_service.get_all_products()
                data = [{
                    "id": str(p.id), 
                    "name": p.name, 
                    "brand": p.brand, 
                    "price": p.price,
                    "category_id": str(p.category.id) if p.category else None
                } for p in products]
                return JsonResponse(data, safe=False)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = product_service.create_product(
                name=data['name'],
                brand=data['brand'], 
                price=data.get('price'),
                category_id=data.get('category_id')
            )
            
            cat_id_str = str(product.category.id) if product.category else None
            
            return JsonResponse({
                "status": "Created", 
                "id": str(product.id),
                "name": product.name,
                "category_id": cat_id_str
            })
        except Exception as e:
             return JsonResponse({"error": str(e)})

    if not product_id:
        return JsonResponse({"error": "product id is required for both delete and update"}, status=400)

    # put only works if category_id is given and it is correct
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category_id = data.get('category_id')
            
            product = product_service.add_product_to_category(product_id, category_id)
            if product:
                return JsonResponse({"status": "Success", "product": product.name, "category_id": str(product.category.id)})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
             return JsonResponse({"error": str(e)})

    elif request.method == 'DELETE':
        try:
            product = product_service.remove_product_from_category(product_id)
            if product:
                return JsonResponse({"status": "Success", "message": f"{product.name} removed from category"})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
             return JsonResponse({"error": str(e)})
        


import csv

@csrf_exempt
def bulk_upload_products(request):
    csv_text = request.body.decode('utf-8').splitlines()
    reader = csv.DictReader(csv_text)
    
    for row in reader:
        product_service.create_product(
            name=row['name'],
            brand=row['brand'],
            price=float(row['price']) if row['price'] else 0,
            category_id=row.get('category_id')
        )
        
    return JsonResponse({"status": "Bulk upload complete"})