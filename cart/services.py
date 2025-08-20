

def in_basket(request):
    cart = request.session.get("cart", {})
    quantities_list = []

    for product_code, product in cart.items():
        quantity = product["quantity"]
        quantities_list.append(quantity)

    in_cart = sum(quantities_list)    
    
    return in_cart
