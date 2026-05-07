from django.urls import path
from authz.views import Signup

urlpatterns=[
    path('signup/',Signup.as_view(), name='signup')
]