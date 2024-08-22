from django.urls import path, include
from core import views

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),

    # category
    path('category/', views.category_list_view, name="category-list"),
    path('category_product/<cid>', views.category_product_list, name="category-products-list"),

    # vendor
    path('vendors/', views.vendor_list_view, name="vendor"),
    path('vendor_details/<vid>', views.vendor_detail_view, name="vendor-detail"),

    # products
    path('products/', views.product_list_view, name="product-list"),
    path('products_details/<pid>', views.product_detail_view, name="product-detail"),

    # tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),

    # add
    path("ajax-add-review/<int:pid>/", views.ajax_add_review, name="ajax-add-review"),

    path("search/", views.search_view, name="search"),

    path("filter_product/", views.filter_product, name="filter-product"),

    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),

    path("cart/", views.cart_view, name="cart"),

    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),

    path("update-cart/", views.update_from_cart, name="update-cart"),

    path("checkout/", views.checkout_view, name="checkout-page"),

    # paypal integration url
    path("paypal/",include('paypal.standard.ipn.urls')),

    # payment
    path("payment-completed/", views.payment_completed_view, name="payment-completed"),

    path("payment-failed/", views.payment_failed_view, name="payment-failed"),

    # customer dashboard
    path("customer_dashboard/", views.customer_dashboard,name="dashboard"),

    # order detail
    path("order_detail/<int:id>", views.order_details,name="order-detail"),

    # make default
    path("make-default-address/",views.make_address_default,name="make-default-address"),
]
