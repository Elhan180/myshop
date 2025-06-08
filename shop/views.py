import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.db.models import Q
from .cart import Cart
from django.views.decorators.http import require_POST
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CartAddProductForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/index.html', {'products': products})




def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    search_query = request.GET.get('search')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
    else:
        # Только товары, помеченные как популярные
        products = Product.objects.filter(available=True, is_featured=True)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'products': products,
        'selected_category': category,
        'search_query': search_query,
    })




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=False)
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


@login_required
def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('shop:order_payment', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'shop/order_create.html', {'cart': cart, 'form': form})


@login_required
def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # создаём Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Заказ №{order.id}',
                },
                'unit_amount': int(order.get_total_cost() * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payment/success/'),
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    return render(request, 'shop/payment_success.html')


def payment_cancel(request):
    return render(request, 'shop/payment_cancel.html')


@login_required
def profile(request):
    orders = request.user.orders.all().order_by('-created')
    return render(request, 'shop/profile.html', {'orders': orders})




from django.db import connection

def clear_order_history(request):
    orders = request.user.orders.all()
    orders.delete()
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='shop_order'")
    
    messages.success(request, "История заказов успешно очищена.")
    return redirect('shop:profile')


def about(request):
    return render(request, 'shop/about.html')

def contacts(request):
    return render(request, 'shop/contacts.html')

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'form': form})
