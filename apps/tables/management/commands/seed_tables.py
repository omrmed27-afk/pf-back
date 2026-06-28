from django.core.management.base import BaseCommand
from apps.tables.models import Table
from apps.warehouses.models import Warehouse


TABLES = [
    # (number, capacity)
    (1,  6),
    (2,  6),
    (3,  6),
    (4,  6),
    (5,  6),
    (6,  6),
    (7,  6),
    (8,  6),
    (9,  6),
    (10, 6),
    (11, 6),
    (12, 6),
]


class Command(BaseCommand):
    help = 'Crea las 12 mesas del restaurante en el primer local registrado'

    def handle(self, *args, **options):
        warehouse = Warehouse.objects.first()
        if not warehouse:
            self.stdout.write(self.style.ERROR('No hay ningún local registrado. Creá uno primero en el admin.'))
            return

        self.stdout.write(f'Local: {warehouse.name}')
        created = 0
        for number, capacity in TABLES:
            table, is_new = Table.objects.get_or_create(
                warehouse=warehouse,
                number=number,
                defaults={'capacity': capacity, 'status': Table.AVAILABLE},
            )
            if is_new:
                created += 1
                self.stdout.write(f'  + Mesa {number} creada (capacidad {capacity})')
            else:
                self.stdout.write(f'  — Mesa {number} ya existe')

        self.stdout.write(self.style.SUCCESS(f'\n{created} mesas creadas. Total: {Table.objects.filter(warehouse=warehouse).count()} mesas en {warehouse.name}.'))
