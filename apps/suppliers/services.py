from .models import Supplier


def get_all_suppliers():
    return Supplier.objects.all().order_by('name')


def get_supplier_by_id(supplier_id):
    return Supplier.objects.get(pk=supplier_id)


def create_supplier(data):
    return Supplier.objects.create(**data)


def update_supplier(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_supplier(instance):
    instance.delete()
