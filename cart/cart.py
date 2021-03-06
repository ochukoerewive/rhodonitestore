from django.conf import settings

from product.models import Product

class Cart(object):
    """Session confirmation"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item
    
    def __len__(self):
        """Product adding all product cost"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product_id, quantity=1, update_quantity=False):
        """Product add/subtract quantity"""
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()
    
    def remove(self, product_id):
        """ if changing you mind in purchasing the item, it can be deleted"""
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """ self save"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        """ self delete section"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        """ getting the total cost of Item in cart """
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())