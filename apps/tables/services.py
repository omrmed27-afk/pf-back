from django.core.exceptions import ValidationError
from .models import Table

VALID_TRANSITIONS = {
    Table.AVAILABLE: [Table.RESERVED],
    Table.RESERVED: [Table.OCCUPIED, Table.AVAILABLE],
    Table.OCCUPIED: [Table.AVAILABLE],
}


def get_all_tables():
    return Table.objects.select_related('warehouse').all().order_by('warehouse', 'number')


def get_table_by_id(table_id):
    return Table.objects.select_related('warehouse').get(pk=table_id)


def create_table(data):
    return Table.objects.create(**data)


def update_table(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_table(instance):
    instance.delete()


def change_status(instance, new_status):
    allowed = VALID_TRANSITIONS.get(instance.status, [])
    if new_status not in allowed:
        raise ValidationError(
            f"Transición inválida: {instance.status} → {new_status}. Permitidas: {allowed}"
        )
    instance.status = new_status
    instance.save()
    return instance
