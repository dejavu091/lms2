from django.shortcuts import render,redirect,resolve_url
from product.models import Product,ProductTransactions
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import JsonResponse



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


def list_products(request):
     all_products = Product.objects.all()
     data=[{'name' : x.name,'id': x.id , 'quantity': x.quantity , 'image':x.image.url}for x in all_products]
     return JsonResponse(data,safe=False)


@login_required
def buy_product(request,product_id):
     product=Product.objects.filter(id=product_id).first()
     if not product:
          return redirect(resolve_url('products'))
     if product.user == request.user:
          messages.error(request,'why are you buying your own product!')
          return redirect(resolve_url('products'))
     if request.method=='POST':
          quantity=request.POST.get('quantity')
          try:
               quantity=int(quantity)
          except:
               messages.error(request,'quantity must be integer')
               return redirect(resolve_url('products'))
     
          if product.quantity < quantity:
           messages.error(request,'quantity more than what we have in stock')
           return redirect(resolve_url('products'))
          product.quantity = product.quantity - quantity
          product.sold+=quantity
          ProductTransactions.objects.create(
               quantity=quantity,
               quantity_after=product.quantity,
               user=request.user,
               price=product.price
          )
          product.save()
          messages.success(request,'product bought successfully! ')
          return redirect(resolve_url('products'))
     return render(request,'buy_product.html')



@login_required
def product_transactions(request,product_id):
     product=Product.objects.filter(id=product_id).first()
     if not product:
          return redirect(resolve_url('products'))
     if product.user != request.user:
          return redirect(resolve_url('products'))
     transactions=ProductTransactions.objects.filter(product=product).order_by('-created_at')
     context={'transactions':transactions}
     return render(request,'products')


def error_404(request,exception):
     return render(request,'error_404.html')

def error_500(request):
     return render(request,'error_500.html')
     


     

               
     
    
          






    
    



# Create your views here.
