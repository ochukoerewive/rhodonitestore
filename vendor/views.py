from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Vendor
from product.models import Product
from .forms import ProductForm
from order.models import OrderItem
#from cart.views import cart_detail

 
# Create your views here.
def become_vendor(request):
    """
    Here we will check if the form has been submitted, if not POST will be GET. also to validate user and direct to front page
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.filter(created_by=user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    """ product and ordering section"""
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})


@login_required
def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()
    
    return render(request, 'vendor/add_product.html', {'form': form})


def deleteProduct(request,pk):
    """function for deleting a particular item in store"""
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('vendor_admin')


@login_required
def edit_vendor(request):
    """ posting information """
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')
    
    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})

    #showing all vendor
def vendors(request):
    """ Showing all vendor """
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

# to show products of each vendordef vendors(request):

# to show products of each vendor
def vendor(request, vendor_id):
    """  to show products of each vendor """
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendors})


@login_required
def edit_product(request, product_id):
    """ Updating product already added in the store"""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect('vendor_admin')
        else: 
            messages.error(request, 'Failed to update product. Please ensure form is valid.')
    else:
        
        
        form = ProductForm(instance=product)
   
    
    return render(request, 'vendor/edit_product.html', {'form': form, 'product': product})


def order_history(request, order_id):
    order = get_object_or_404(Order, order_number=order_number)

    return render(request,' order_history.html', { 'order': order} )