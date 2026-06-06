from django.urls import path
from product.views import Products,Addproduct,EditProduct,delete_product,list_products,buy_product,product_transactions,error_404,error_500



urlpatterns= [path('',Products.as_view(), name='products'),
              path('add-product/',Addproduct.as_view(),name='add-product'),
              path('edit-product/<str:product_id>',EditProduct.as_view(),name='edit-product'),
              path('delete-product/<str:product_id>',delete_product, name = 'delete-product'),
              path('all',list_products, name='all_prod'),
              path('buy-product/<str:product_id>',buy_product,name='buy-product'),
              path('transactions/<str:product_id>',product_transactions,name='transactions-product'),
              


]