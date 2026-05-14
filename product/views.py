from django.shortcuts import render,redirect,resolve_url
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from user.views import homepage



class Products(LoginRequiredMixin,View):
    def get(self,request):
        all_products = Product.objects.all().order_by("-created_at")
        context = {
            'all_prod':all_products
        }
        return render (request,'products.html',context)
    
class Addproduct(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'add_product.html')
    def post (self,request):
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        image=request.FILES.get('image')
        if not name or not description or not price or not quantity or not image:
            messages.error(request,"all field required")
            return redirect(resolve_url('add-product'))
        try:
            price = int(price)
            quantity=int(quantity)
        except:
            messages.error(request,'price and quantity must be intergers')
            return redirect(resolve_url('add-product'))
        if price < 1:
                messages.error(request,"price too low")
        if quantity < 1:
                messages.error(request,"quantity too low")
        Product.objects.create(name=name, description=description, price=price, quantity=quantity,image=image,
                                   user=request.user)
        messages.success(request,'product listed successfully')
        return redirect(resolve_url('add-product'))
            
class EditProduct(LoginRequiredMixin,View):
     def get(self,request,product_id):
          product=Product.objects.filter(id=product_id).first()
          if not product:
               return redirect(resolve_url(Products))
          if product.user !=request.user:
               return redirect(resolve_url(Products))
          context={'product':product}
          return render(request,'edit_products.html',context)
     def post (self,request,product_id):
          product=Product.objects.filter(id=product_id).first()
          if not product:
               return redirect(resolve_url(Products))
          if product.user !=request.user:
               return redirect(resolve_url(Products))
          name=request.POST.get('name')
          description=request.POST.get('description')
          price=request.POST.get('price')
          if price and price< 1:
               messages.error(request,'price too low')
          quantity=request.POST.get('quantity')
          if quantity and quantity < 1:
               messages.error(request,'quantitiy too low')
          image=request.FILES.get('image')
          product.name=name or product.name
          product.description=description or product.description
          product.price=price or product.price
          product.quantity=quantity or product.quantity
          product.image=image or product.image
          product.save()
          messages.success(request,'product successfully updated')
          return redirect(resolve_url('products'))
     


@login_required    
def delete_product(request,product_id):
     product=Product.objects.filter(id=product_id).first()
     if not product:
          return redirect(resolve_url('products'))
     if product.user != request.user:
          return redirect(resolve_url('products'))
     product.delete()
     messages.success(request,'product deleted successfully')
     return redirect(resolve_url('products'))
          
               
     
    
          






    
    



# Create your views here.
