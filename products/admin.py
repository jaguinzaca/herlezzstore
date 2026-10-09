from django.contrib import admin

from .models import Product, ProductBenefit


class ProductBenefitInline(admin.TabularInline):
    model = ProductBenefit
    extra = 1
    fields = ("position", "icon", "text")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    search_fields = ("name", "slug", "description")
    list_filter = ("is_active", "includes_case", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active",)
    inlines = (ProductBenefitInline,)
