from django.db import models
import uuid
from django.contrib.auth.models import User




class product(models.Model):
 id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)   
 name=models.CharField(max_length=250)
 decription=models.TextField()
 price=models.PositiveBigIntegerField()
 quantity=models.PositiveIntegerField()
 sold=models.PositiveIntegerField(default=0)
 image=models.ImageField(upload_to='product/')
#  user deleltes profile, products delete too
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
def __str__(self):
        return f' name= {self.name} description= {self.decription} price={self.price} quantity={self.quantity}'

#  user deletes profile, products remain
# user=models.ForeignKey(User, on_delete=models.SET_NULL)
#  user deletes profile, products transfers to a default user
# user=models.ForeignKey(User, on_delete=models.SET_DEFAULT)
# Create your models here.
