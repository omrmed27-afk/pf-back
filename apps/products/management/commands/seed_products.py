from django.core.management.base import BaseCommand
from apps.products.models import Product


PRODUCTS = [
    {
        'name': 'Sashimi Salmón',
        'description': 'Finas láminas de salmón fresco premium servidas con wasabi y jengibre encurtido.',
        'sku': 'SASH-SAL-01',
        'unit_price': '18.90',
        'stock': 50,
        'is_featured': True,
        'ingredients': ['salmón', 'wasabi', 'jengibre encurtido', 'salsa de soya'],
        'image_url': 'https://images.unsplash.com/photo-1534482421-64566f976cfa?w=500',
    },
    {
        'name': 'Sashimi Atún',
        'description': 'Láminas de atún rojo seleccionado, suave y de sabor intenso.',
        'sku': 'SASH-ATU-02',
        'unit_price': '20.50',
        'stock': 40,
        'is_featured': True,
        'ingredients': ['atún rojo', 'wasabi', 'jengibre encurtido', 'salsa de soya'],
        'image_url': 'https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?w=500',
    },
    {
        'name': 'Dragon Roll',
        'description': 'Roll cubierto con aguacate en forma de dragón, relleno de camarón tempura y pepino.',
        'sku': 'ROLL-DRA-03',
        'unit_price': '16.50',
        'stock': 60,
        'is_featured': True,
        'ingredients': ['camarón tempura', 'pepino', 'aguacate', 'arroz de sushi', 'alga nori'],
        'image_url': 'https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=500',
    },
    {
        'name': 'Philadelphia Roll',
        'description': 'Clásico roll con salmón, queso crema y pepino, sin alga por fuera.',
        'sku': 'ROLL-PHI-04',
        'unit_price': '14.90',
        'stock': 70,
        'is_featured': False,
        'ingredients': ['salmón', 'queso crema', 'pepino', 'arroz de sushi'],
        'image_url': 'https://images.unsplash.com/photo-1617196034099-5ee8d7d52ae8?w=500',
    },
    {
        'name': 'Spicy Tuna Roll',
        'description': 'Roll picante de atún con salsa sriracha, pepino y cebollín.',
        'sku': 'ROLL-SPI-05',
        'unit_price': '15.50',
        'stock': 55,
        'is_featured': False,
        'ingredients': ['atún', 'sriracha', 'pepino', 'cebollín', 'arroz de sushi', 'alga nori'],
        'image_url': 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=500',
    },
    {
        'name': 'Ramen Tonkotsu',
        'description': 'Caldo cremoso de hueso de cerdo con fideos ramen, chashu, huevo marinado y nori.',
        'sku': 'RAME-TON-06',
        'unit_price': '17.90',
        'stock': 35,
        'is_featured': True,
        'ingredients': ['caldo tonkotsu', 'fideos ramen', 'chashu', 'huevo marinado', 'nori', 'cebollín', 'bambú'],
        'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500',
    },
    {
        'name': 'Gyoza',
        'description': 'Empanadillas japonesas rellenas de cerdo y verduras, a la plancha con salsa ponzu.',
        'sku': 'GYOZ-CER-07',
        'unit_price': '10.50',
        'stock': 80,
        'is_featured': False,
        'ingredients': ['cerdo molido', 'repollo', 'jengibre', 'ajo', 'salsa ponzu'],
        'image_url': 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=500',
    },
    {
        'name': 'Edamame',
        'description': 'Vainas de soya verde al vapor con sal marina. Aperitivo clásico japonés.',
        'sku': 'EDAM-SOY-08',
        'unit_price': '6.90',
        'stock': 100,
        'is_featured': False,
        'ingredients': ['soya verde', 'sal marina'],
        'image_url': 'https://images.unsplash.com/photo-1535140728325-a4d3707eee61?w=500',
    },
    {
        'name': 'Tempura de Camarón',
        'description': 'Camarones en tempura crujiente servidos con salsa tentsuyu.',
        'sku': 'TEMP-CAM-09',
        'unit_price': '19.90',
        'stock': 45,
        'is_featured': True,
        'ingredients': ['camarón', 'masa tempura', 'salsa tentsuyu', 'rábano rallado'],
        'image_url': 'https://images.unsplash.com/photo-1617196034262-fd184f2d7df4?w=500',
    },
    {
        'name': 'Miso Soup',
        'description': 'Sopa tradicional de miso con tofu, alga wakame y cebollín.',
        'sku': 'SOUP-MIS-10',
        'unit_price': '5.90',
        'stock': 120,
        'is_featured': False,
        'ingredients': ['pasta miso', 'tofu', 'alga wakame', 'cebollín'],
        'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500',
    },
    {
        'name': 'California Roll',
        'description': 'Roll invertido con cangrejo, aguacate y pepino, cubierto de semillas de sésamo.',
        'sku': 'ROLL-CAL-11',
        'unit_price': '13.90',
        'stock': 75,
        'is_featured': False,
        'ingredients': ['cangrejo', 'aguacate', 'pepino', 'arroz de sushi', 'sésamo'],
        'image_url': 'https://images.unsplash.com/photo-1602827114285-2f1269f2c4ed?w=500',
    },
    {
        'name': 'Nigiri Mix',
        'description': 'Selección de 8 piezas de nigiri: salmón, atún, camarón y pez blanco.',
        'sku': 'NIGI-MIX-12',
        'unit_price': '22.90',
        'stock': 30,
        'is_featured': True,
        'ingredients': ['salmón', 'atún', 'camarón', 'pez blanco', 'arroz de sushi', 'wasabi'],
        'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500',
    },
    {
        'name': 'Yakitori',
        'description': 'Brochetas de pollo a la parrilla glaseadas con salsa tare dulce.',
        'sku': 'YAKI-POL-13',
        'unit_price': '12.90',
        'stock': 60,
        'is_featured': False,
        'ingredients': ['pollo', 'salsa tare', 'cebolla de verdeo'],
        'image_url': 'https://images.unsplash.com/photo-1604909052743-94e838986d24?w=500',
    },
    {
        'name': 'Sake (Copa)',
        'description': 'Sake japonés tradicional servido frío o caliente.',
        'sku': 'BEBA-SAK-14',
        'unit_price': '9.90',
        'stock': 200,
        'is_featured': False,
        'ingredients': ['sake japonés'],
        'image_url': 'https://images.unsplash.com/photo-1582337557373-a0e1d65b57cc?w=500',
    },
    {
        'name': 'Matcha Latte',
        'description': 'Té verde matcha premium con leche vaporizada.',
        'sku': 'BEBA-MAT-15',
        'unit_price': '7.50',
        'stock': 150,
        'is_featured': False,
        'ingredients': ['matcha premium', 'leche', 'azúcar'],
        'image_url': 'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500',
    },
]


class Command(BaseCommand):
    help = 'Carga productos del menú en la base de datos'

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0
        for data in PRODUCTS:
            _, is_new = Product.objects.get_or_create(sku=data['sku'], defaults=data)
            if is_new:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'{created} productos creados, {skipped} ya existían.'))
