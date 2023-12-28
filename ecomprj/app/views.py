from django.db.models import Count
from django.shortcuts import render
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from .models import Product,Customer
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,"app/home.html")
def about(request):
    return render(request,"app/about.html")
def contact(request):
    return render(request,"app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetails(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk) #beacuse we only need one product
        return render(request,"app/productdetail.html",locals())
    
class customerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation! User Register Successfully")
        else:
            messages.warning(request,"Error! Please Check Your Input Data")
        return render(request,'app/customerregistration.html',locals())
    
class profileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Profile save successfully!")
        else:
            messages.warning(request,"Please correct the errors.")
        return render(request, 'app/profile.html',locals())
    
def address(request):
    address = Customer.objects.filter(user=request.user) 
    return render(request, 'app/address.html',locals())