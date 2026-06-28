from django.core.management.base import BaseCommand
from apps.products.models import Product


PRODUCTS = [
    # --- Makis ---
    {
        'name': 'California Maki',
        'description': 'Langostino blanqueado, queso crema y palta, envuelto en ajonjolí.',
        'sku': 'MAKI-CAL-01',
        'unit_price': '25.90',
        'stock': 80,
        'is_featured': True,
        'ingredients': ['langostino', 'queso crema', 'palta', 'arroz de sushi', 'ajonjolí'],
        'image_url': 'https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=500',
    },
    {
        'name': 'Philadelphia Maki',
        'description': 'Trucha y queso crema, cubierto de ajonjolí blanco.',
        'sku': 'MAKI-PHI-02',
        'unit_price': '25.90',
        'stock': 70,
        'is_featured': False,
        'ingredients': ['trucha', 'queso crema', 'arroz de sushi', 'ajonjolí blanco'],
        'image_url': 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=500',
    },
    {
        'name': 'Acevichado Maki',
        'description': 'Roll de langostino empanizado y palta, con salsa acevichada.',
        'sku': 'MAKI-ACE-03',
        'unit_price': '20.90',
        'stock': 60,
        'is_featured': True,
        'ingredients': ['langostino empanizado', 'palta', 'salsa acevichada', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1617196034099-5ee8d7d52ae8?w=500',
    },
    {
        'name': 'Inka Maki',
        'description': 'Trucha salmonada y palta, cubierto con ajonjolí mixto.',
        'sku': 'MAKI-INK-04',
        'unit_price': '25.90',
        'stock': 60,
        'is_featured': False,
        'ingredients': ['trucha salmonada', 'palta', 'ajonjolí mixto', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1582125729809-8a0f88a2c78a?w=500',
    },
    {
        'name': 'Doragon Maki',
        'description': 'Roll cubierto con quinua tostada, topping de ebi furai.',
        'sku': 'MAKI-DOR-05',
        'unit_price': '25.90',
        'stock': 55,
        'is_featured': True,
        'ingredients': ['ebi furai', 'quinua tostada', 'palta', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1562802378-063ec186a863?w=500',
    },
    {
        'name': 'Passion Maki',
        'description': 'Ebi furai y palta, cubierto con trucha flameada.',
        'sku': 'MAKI-PAS-06',
        'unit_price': '25.90',
        'stock': 50,
        'is_featured': False,
        'ingredients': ['ebi furai', 'palta', 'trucha flameada', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?w=500',
    },
    {
        'name': 'Huancaína Maki',
        'description': 'Langostino empanizado y palta, cubierto con salsa huancaína.',
        'sku': 'MAKI-HUA-07',
        'unit_price': '25.90',
        'stock': 45,
        'is_featured': False,
        'ingredients': ['langostino empanizado', 'palta', 'salsa huancaína', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1534482421-64566f976cfa?w=500',
    },
    # --- Poke ---
    {
        'name': 'Poke Salmón Fresco',
        'description': 'Base de arroz sushi, salsa de ostión especial, dados de salmón.',
        'sku': 'POKE-SAL-08',
        'unit_price': '29.90',
        'stock': 40,
        'is_featured': True,
        'ingredients': ['arroz sushi', 'salmón', 'salsa ostión', 'alga', 'ajonjolí'],
        'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500',
    },
    {
        'name': 'Poke Atún Fresco',
        'description': 'Base de arroz sushi, salsa de ostión especial, dados de atún.',
        'sku': 'POKE-ATU-09',
        'unit_price': '29.90',
        'stock': 35,
        'is_featured': False,
        'ingredients': ['arroz sushi', 'atún', 'salsa ostión', 'alga', 'pepino'],
        'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500',
    },
    {
        'name': 'Poke Ebi Furai',
        'description': 'Arroz sushi, salsa ostión, langostinos empanizados crujientes.',
        'sku': 'POKE-EBI-10',
        'unit_price': '29.90',
        'stock': 35,
        'is_featured': False,
        'ingredients': ['arroz sushi', 'ebi furai', 'salsa ostión', 'palta'],
        'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500',
    },
    # --- Sashimi ---
    {
        'name': 'Sashimi de Salmón',
        'description': '04 cortes servidos con salsa shoyu, gari y wasabi.',
        'sku': 'SASH-SAL-11',
        'unit_price': '20.90',
        'stock': 30,
        'is_featured': True,
        'ingredients': ['salmón', 'salsa shoyu', 'gari', 'wasabi'],
        'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=500',
    },
    {
        'name': 'Sashimi de Trucha',
        'description': '04 cortes de trucha asalmonada con salsa shoyu.',
        'sku': 'SASH-TRU-12',
        'unit_price': '15.90',
        'stock': 30,
        'is_featured': False,
        'ingredients': ['trucha asalmonada', 'salsa shoyu', 'gari', 'wasabi'],
        'image_url': 'https://images.unsplash.com/photo-1617196034262-fd184f2d7df4?w=500',
    },
    # --- Entradas ---
    {
        'name': 'Ebi Furai',
        'description': 'Langostinos empanizados al panko, acompañados de salsa acevichada.',
        'sku': 'ENTR-EBI-13',
        'unit_price': '20.90',
        'stock': 60,
        'is_featured': True,
        'ingredients': ['langostino', 'panko', 'salsa acevichada'],
        'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500',
    },
    {
        'name': 'Gyozas de Pescado',
        'description': 'Empanaditas rellenas de pescado fresco y verduras, a la plancha.',
        'sku': 'ENTR-GYO-14',
        'unit_price': '17.90',
        'stock': 70,
        'is_featured': False,
        'ingredients': ['pescado fresco', 'verduras', 'pasta gyoza'],
        'image_url': 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=500',
    },
    # --- Ramen ---
    {
        'name': 'Chicken Ramen',
        'description': 'Caldo umami, fideo ramen, pollo, huevo y cebollines.',
        'sku': 'RAME-CHK-15',
        'unit_price': '20.90',
        'stock': 40,
        'is_featured': False,
        'ingredients': ['caldo umami', 'fideos ramen', 'pollo', 'huevo', 'cebollines'],
        'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500',
    },
    {
        'name': 'Ebi Ramen',
        'description': 'Caldo de langostinos con miso, fideos firmes y ebi furai.',
        'sku': 'RAME-EBI-16',
        'unit_price': '20.00',
        'stock': 35,
        'is_featured': True,
        'ingredients': ['caldo de langostinos', 'miso', 'fideos ramen', 'ebi furai'],
        'image_url': 'https://images.unsplash.com/photo-1623341214825-9f4f963727da?w=500',
    },
    # --- Bebidas ---
    {
        'name': 'Inca Kola 500ml',
        'description': 'La bebida de sabor nacional, sabor original.',
        'sku': 'BEBA-INC-17',
        'unit_price': '4.90',
        'stock': 200,
        'is_featured': False,
        'ingredients': [],
        'image_url': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500',
    },
    {
        'name': 'Coca-Cola 500ml',
        'description': 'Coca-Cola sabor original 500ml.',
        'sku': 'BEBA-COC-18',
        'unit_price': '4.90',
        'stock': 200,
        'is_featured': False,
        'ingredients': [],
        'image_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=500',
    },
]


class Command(BaseCommand):
    help = 'Carga productos del menú de Mr. Sushi en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Elimina todos los productos antes de sembrar')

    def handle(self, *args, **kwargs):
        if kwargs['clear']:
            count, _ = Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'{count} productos eliminados.'))

        created = 0
        updated = 0
        for data in PRODUCTS:
            sku = data.pop('sku')
            _, is_new = Product.objects.update_or_create(sku=sku, defaults=data)
            data['sku'] = sku
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'{created} productos creados, {updated} actualizados.'))
