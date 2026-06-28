from .models import Transport


def get_all_transports():
    return Transport.objects.all().order_by('license_plate')


def get_transport_by_id(transport_id):
    return Transport.objects.get(pk=transport_id)


def create_transport(data):
    return Transport.objects.create(**data)


def update_transport(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_transport(instance):
    instance.delete()
