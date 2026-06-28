from django.core.management.base import BaseCommand
from apps.warehouses.models import Warehouse
from apps.tables.models import Table


TABLES = [
    {'number': 1,  'capacity': 2},
    {'number': 2,  'capacity': 2},
    {'number': 3,  'capacity': 4},
    {'number': 4,  'capacity': 4},
    {'number': 5,  'capacity': 2},
    {'number': 6,  'capacity': 4},
    {'number': 7,  'capacity': 2},
    {'number': 8,  'capacity': 4},
    {'number': 9,  'capacity': 4},
    {'number': 10, 'capacity': 4},
    {'number': 11, 'capacity': 6},
    {'number': 12, 'capacity': 6},
]


class Command(BaseCommand):
    help = 'Carga las mesas del restaurante en la base de datos'

    def handle(self, *args, **kwargs):
        warehouse, _ = Warehouse.objects.get_or_create(
            name='Dragon Rojo - Local Principal',
            defaults={
                'address': 'Av. Japón 123',
                'city': 'Lima',
                'country': 'Perú',
                'capacity': 48,
                'floors': 1,
            }
        )

        created = 0
        skipped = 0
        for data in TABLES:
            _, is_new = Table.objects.get_or_create(
                warehouse=warehouse,
                number=data['number'],
                defaults={'capacity': data['capacity']},
            )
            if is_new:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'{created} mesas creadas, {skipped} ya existían.'))
