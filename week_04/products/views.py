from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import category_service, product_service

# new imports
from .constants import HTTP_GET, HTTP_POST, HTTP_PUT, HTTP_DELETE, ERR_CATEGORY_NOT_FOUND, ERR_PRODUCT_NOT_FOUND, STATUS_MESSAGES
from .serializers import serialize_category, serialize_product

@csrf_exempt
def api_for_a_category(request, category_id=None):

    if request.method == HTTP_GET:
        if category_id:
            try:
                # renamed 'c' to 'category'
                category = category_service.get_category_by_id(category_id)
                if category:
                    # using the new serializer
                    return JsonResponse(serialize_category(category))
                return JsonResponse({
                    "error": STATUS_MESSAGES[404], 
                }, status=404)
            except Exception as e:
                #status code updated
                return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
        else:
            try:
                categories = category_service.get_all_categories()
                # using the serializer
                data = [serialize_category(cat) for cat in categories]
                return JsonResponse(data, safe=False)
            except Exception as e:
                return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
    
    elif request.method == HTTP_POST:
        try:
            data = json.loads(request.body)
            category = category_service.create_category(data['title'], data.get('description'))
            return JsonResponse({"id": str(category.id)})
        except Exception as e:
            return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
    
    elif request.method == HTTP_PUT:
        try:
            data = json.loads(request.body)
            updated_cat = category_service.update_category(category_id, data['title'], data.get('description'))
            
            if updated_cat:
                return JsonResponse({"status": "updated", "title": updated_cat.title})
            return JsonResponse({
                    "error": STATUS_MESSAGES[404],
                }, status=404)
        except Exception as e:
            return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
        
    elif request.method == HTTP_DELETE:
        try:
            success = category_service.delete_category(category_id)
            if success:
                return JsonResponse({"status": "deleted"})
            return JsonResponse({
                    "error": STATUS_MESSAGES[404],
                }, status=404)
        except Exception as e:
            return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)


@csrf_exempt
def api_for_a_product(request, product_id=None):

    if request.method == HTTP_GET:
        if product_id:
            try:
                # renamed 'p' to 'product'
                product = product_service.get_product_by_id(product_id)
                if product:
                    return JsonResponse(serialize_product(product))
                return JsonResponse({
                    "error": STATUS_MESSAGES[404],
                }, status=404)
            except Exception as e:
                return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
        else:
            try:
                products = product_service.get_all_products()
                data = [serialize_product(prod) for prod in products]
                return JsonResponse(data, safe=False)
            except Exception as e:
                return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
    
    if request.method == HTTP_POST:
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
             return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)

    if not product_id:
        return JsonResponse({"error": STATUS_MESSAGES[404],
                             "details":"product id is required for both delete and update",
                             }, status=400)

    # put only works if category_id is given and it is correct
    if request.method == HTTP_PUT:
        try:
            data = json.loads(request.body)
            category_id = data.get('category_id')
            
            product = product_service.add_product_to_category(product_id, category_id)
            if product:
                return JsonResponse({"status": "Success", "product": product.name, "category_id": str(product.category.id)})
            return JsonResponse({
                    "error": STATUS_MESSAGES[404], 
                }, status=404)
        except Exception as e:
             return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)

    elif request.method == HTTP_DELETE:
        try:
            product = product_service.remove_product_from_category(product_id)
            if product:
                return JsonResponse({"status": "Success", "message": f"{product.name} removed from category"})
            return JsonResponse({
                    "error": STATUS_MESSAGES[404], 
                }, status=404)
        except Exception as e:
             return JsonResponse({
                    "error": STATUS_MESSAGES[500], 
                    "details": str(e)
                }, status=500)
        
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