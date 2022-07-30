from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from decimal import Decimal

from profiles.models import UserProfile
from checkout.models import Order
from .models import Product, Collection, Review
from .forms import ProductForm, ReviewForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all().exclude(sale=True)
    query = None
    collections = None
    sort = None
    direction = None
    sale = None
    newprice = None
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'collection':
                sortkey = 'collection__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'collection' in request.GET:
            collections = request.GET['collection'].split(',')
            products = products.filter(collection__name__in=collections)
            collections = Collection.objects.filter(name__in=collections)

        if 'sale' in request.GET:
            sale = request.GET['sale']
            products = Product.objects.all()
            products = products.filter(sale=True)
            for product in products:
                percentage = 50
                discount = product.price * Decimal(percentage / 100)
                newprice = product.price - discount

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't search anything!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(details__icontains=query) | Q(collection__friendly_name__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'collections': collections,
        'sale': sale,
        'current_sorting': current_sorting,
        'newprice': newprice,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    percentage = 50
    discount = product.price * Decimal(percentage / 100)
    newprice = product.price - discount
    reviews = Review.objects.filter(product=product_id)
    review_form = None
    review = None

    if request.user.is_authenticated:
        profile = request.user.userprofile
        ordered = Order.objects.filter(user_profile=profile)
        has_purchased = False
        for order in ordered:
            for item in order.lineitems.all():
                if item.product.id == product.id:
                    has_purchased = True
                    break

        if has_purchased:
            review = Review.objects.filter(user=request.user, product=product_id)
            if review:
                review_form = None

            else:
                review_form = ReviewForm()

    context = {
        'product': product,
        'newprice': newprice,
        'reviews': reviews,
        'review': review,
        'review_form': review_form
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


def add_review(request, product_id):
    user = get_object_or_404(UserProfile, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product_id)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=product)
        form_data = {
            'comment': request.POST['comment']
            }

        review_form = ReviewForm(form_data)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.info(request, f'Thank you for posting a review for {product.name}.')
        else:
            messages.error(request, f'Sorry we were unable to post a review for {product.name}, try again.')
        return redirect(reverse('product_detail', args=(product_id,)))

    else:
        review_form = ReviewForm(instance=user)

    context = {
        "product": product,
        "reviews": reviews,
        "review_form": review_form
    }
    return render(request, 'products/product_detail.html', context)


def edit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = get_object_or_404(Review, user=request.user, product=product_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=user)
        if review_form.is_valid():
            review_form.save()
            messages.info(request, f'Review edited for {product.name}.')
            return redirect(reverse('product_detail', args=[product_id, ]))
        else:
            messages.error(request, f'Sorry an error has accoured, we cannot update your review for {product.name}, please try again.')
    else:
        review_form = ReviewForm(instance=user)

    template = 'products/product_review.html'
    context = {
        'product': product,
        'review_form': review_form,
    }
    return render(request, template, context)


def delete_review(request, product_id):
    review = get_object_or_404(Review, user=request.user, product=product_id)
    review.delete()
    messages.info(request, 'Your review has been removed.')
    return redirect(reverse('product_detail', args=(product_id,)))


