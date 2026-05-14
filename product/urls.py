from django.urls import path
from product.views import Products,Addproduct



urlpatterns= [path('',Products.as_view(), name='products'),
              path('add-product/',Addproduct.as_view(),name='add-product'),

]