from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


def login(identifier, password):
    # intenta por username directo
    user = authenticate(username=identifier, password=password)
    if user is None:
        # intenta por email
        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass
    if user is None:
        return None
    token, _ = Token.objects.get_or_create(user=user)
    return token


def logout(user):
    Token.objects.filter(user=user).delete()


def get_all_users():
    return User.objects.all().prefetch_related('groups').order_by('date_joined')


def create_user(data):
    user = User.objects.create_user(
        username=data['username'],
        password=data['password'],
        email=data.get('email', ''),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
    )
    if data.get('is_superuser'):
        user.is_superuser = True
        user.is_staff = True
        user.save()
    return user


def update_user(user, data):
    for field in ['email', 'first_name', 'last_name', 'is_active']:
        if field in data:
            setattr(user, field, data[field])
    if 'is_superuser' in data:
        user.is_superuser = data['is_superuser']
        user.is_staff = data['is_superuser']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    user.save()
    return user


def assign_group(user, group_id, action='add'):
    group = Group.objects.get(pk=group_id)
    if action == 'remove':
        user.groups.remove(group)
    else:
        user.groups.add(group)
    return user


def get_all_groups():
    return Group.objects.all().order_by('name')


def create_group(name):
    group, _ = Group.objects.get_or_create(name=name.strip())
    return group


def delete_group(group_id):
    Group.objects.filter(pk=group_id).delete()


def register_customer(data):
    from django.db import transaction
    from apps.customers.models import Customer
    with transaction.atomic():
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        Customer.objects.get_or_create(
            email=data['email'],
            defaults={'name': f"{data['first_name']} {data['last_name']}"},
        )
        token, _ = Token.objects.get_or_create(user=user)
        return token
