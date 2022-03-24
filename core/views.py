from django.shortcuts import render

from product.models import Product

#Import Pagination
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    """ creating view page for newest product"""
    #newest_products = Product.objects.all()[0:10]
    newest_products = Product.objects.all()[0:10]

    #Setup paginaion
    p = Paginator(Product.objects.all(), 4)
    page = request.GET.get('page')
    newest_products = p.get_page(page)
    
    return render(request, 'index.html', {'newest_products': newest_products })

def contact(request):
    """ creating view page for contact us"""
    return render(request, 'contact.html')
    