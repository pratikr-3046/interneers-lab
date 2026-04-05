from django.urls import path
from . import views

urlpatterns = [
    # api_for_a_category
    path('categories/', views.api_for_a_category),
    path('categories/<str:category_id>/', views.api_for_a_category),
    
    #bulk post
    # here there can be a problem if i write this below the product with product id. it may think bulk-upload is the product id
    path('products/bulk-upload/', views.bulk_upload_products),


    # api_for_a_product
    path('products/<str:product_id>/', views.api_for_a_product),
    path('products/',views.api_for_a_product),

]