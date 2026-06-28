from .models import Customer


def get_all_customers():
    return Customer.objects.all().order_by('name')


def get_customer_by_id(customer_id):
    return Customer.objects.get(pk=customer_id)


def create_customer(data):
    return Customer.objects.create(**data)


def update_customer(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_customer(instance):
    instance.delete()
