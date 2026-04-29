from django.urls import path
from user.views import aboutpage, contactpage
from user.views import homepage
urlpatterns = [
    path('', homepage, name='home'),
    path('about/', aboutpage, name='about'),
    path('contact/', contactpage, name='contact')   
]