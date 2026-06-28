from .models import Route, RouteStop


def get_all_routes():
    return Route.objects.select_related('origin_warehouse').prefetch_related('stops').all().order_by('name')


def get_route_by_id(route_id):
    return Route.objects.select_related('origin_warehouse').prefetch_related('stops').get(pk=route_id)


def create_route(data):
    return Route.objects.create(**data)


def update_route(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_route(instance):
    instance.delete()


def get_all_stops(route_id):
    return RouteStop.objects.filter(route_id=route_id).order_by('stop_order')


def create_stop(data):
    return RouteStop.objects.create(**data)


def update_stop(instance, data):
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


def delete_stop(instance):
    instance.delete()
