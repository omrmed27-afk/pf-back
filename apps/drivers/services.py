from django.contrib.auth.models import User
from django.db import transaction
from .models import Driver


def get_all_drivers():
    return Driver.objects.select_related('user').all().order_by('user__last_name')


def get_driver_by_id(driver_id):
    return Driver.objects.select_related('user').get(pk=driver_id)


@transaction.atomic
def create_driver_with_user(user_data, driver_data):
    password = user_data.pop('password')
    user = User.objects.create_user(password=password, **user_data)
    driver = Driver.objects.create(user=user, **driver_data)
    return driver


def update_driver(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_driver(instance):
    instance.delete()
