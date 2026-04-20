from django.contrib import admin
from .models import Products, CartModel, Order


# ==================================
# SHOPSPHERE ADMIN BRANDING
# ==================================

admin.site.site_header = "ShopSphere Admin Panel"
admin.site.site_title = "ShopSphere Admin"
admin.site.index_title = "Welcome to ShopSphere Dashboard"


# ==================================
# PRODUCTS ADMIN
# ==================================

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'pname',
        'pcategory',
        'price',
        'trending',
        'offer'
    )

    search_fields = (
        'pname',
        'pcategory'
    )

    list_filter = (
        'pcategory',
        'trending',
        'offer'
    )

    list_editable = (
        'price',
        'trending',
        'offer'
    )

    ordering = ('id',)


# ==================================
# CART ADMIN
# ==================================

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'pname',
        'host',
        'quatity',
        'totalprice'
    )

    search_fields = (
        'pname',
        'host__username'
    )

    list_filter = (
        'pcategory',
    )

    ordering = ('-id',)


# ==================================
# ORDER ADMIN
# ==================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'price',
        'status',
        'created_at'
    )

    search_fields = (
        'user__username',
        'product__pname'
    )

    list_filter = (
        'status',
        'created_at'
    )

    list_editable = (
        'status',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
    )