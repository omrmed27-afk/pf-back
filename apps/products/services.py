from .models import Product


def get_all_products():
    return Product.objects.select_related('supplier').all().order_by('name')


def get_product_by_id(product_id):
    return Product.objects.select_related('supplier').get(pk=product_id)


def create_product(data):
    return Product.objects.create(**data)


def update_product(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_product(instance):
    instance.delete()
