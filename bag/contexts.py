from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    View to handle the contents of the bag
    """
    bag_items = []
    total = 0
    total2 = 0
    saletotal = 0
    item_after_discount = 0
    subtotal = 0
    product_count = 0
    discount = 0
    checkout_total = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.sale is True:
            for size, quantity in item_data["items_by_size"].items():
                total2 += quantity * product.price
                product_count += quantity
                saletotal = total2
                item_after_discount = product.price * Decimal(50 / 100)
                discount = saletotal * Decimal(50 / 100)
                subtotal = discount
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                    }
                )
        else:
            for size, quantity in item_data["items_by_size"].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                    }
                )

    delivery = (total + total2) * Decimal(
        settings.STANDARD_DELIVERY_PERCENTAGE / 100
    )

    grand_total = (delivery + total + total2) - subtotal
    checkout_total = total + total2
    total = total + total2 - subtotal
    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "grand_total": grand_total,
        "subtotal": subtotal,
        "item_after_discount": item_after_discount,
        "discount": discount,
        "checkout_total": checkout_total,
    }

    return context
