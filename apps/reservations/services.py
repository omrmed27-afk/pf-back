from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Reservation
from apps.tables.models import Table


def get_all_reservations():
    return Reservation.objects.select_related('customer', 'table').all().order_by('-date', '-time')


def get_reservation_by_id(reservation_id):
    return Reservation.objects.select_related('customer', 'table').get(pk=reservation_id)


@transaction.atomic
def create_reservation(data):
    table = data.get('table')
    if table and table.status != Table.AVAILABLE:
        raise ValidationError('La mesa no está disponible.')
    reservation = Reservation.objects.create(**data)
    if table:
        table.status = Table.RESERVED
        table.save()
    return reservation


def update_reservation(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


@transaction.atomic
def cancel_reservation(instance):
    if instance.status == Reservation.CANCELLED:
        raise ValidationError('La reserva ya está cancelada.')
    instance.status = Reservation.CANCELLED
    instance.save()
    table = instance.table
    if table.status == Table.RESERVED:
        table.status = Table.AVAILABLE
        table.save()
    return instance


def delete_reservation(instance):
    instance.delete()
