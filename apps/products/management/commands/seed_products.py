from django.core.management.base import BaseCommand
from apps.products.models import Product

PRODUCTS = [
    # ── MAKIS ──────────────────────────────────────────────────────────────
    {
        'sku': 'MAK-001', 'name': 'Acevichado Maki',
        'description': 'Roll de langostino empanizado y palta, cubierto con láminas frescas de pescado blanco',
        'unit_price': '20.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/xL89gzB5ez2PA2MAz-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'MAK-002', 'name': 'California Maki',
        'description': 'Roll relleno de langostino blanqueado, queso crema y palta',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/uzTynC2gG7dY3GfGm-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'MAK-003', 'name': 'Philadelphia Maki',
        'description': 'Roll relleno de trucha y queso crema, cubierto de ajonjolí blanco',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/s8YGoc2ehe2Yuupak-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'MAK-004', 'name': 'Furai Maki',
        'description': 'Roll empanizado al panko y frito, relleno de queso crema, palta y trucha',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/bNcuKaRawnENBGCYm-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'MAK-005', 'name': 'Inka Maki',
        'description': 'Roll relleno de trucha salmonada y palta fresca, cubierto con ajonjolí mixto',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/CgmqfE9HZdSHcHbzx-300-x.webp',
    },
    {
        'sku': 'MAK-006', 'name': 'Passion Maki',
        'description': 'Roll relleno de ebi furai y palta, cubierto con trucha flameada',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/7gSnbZrqtdSwAu2vw-300-x.webp',
    },
    {
        'sku': 'MAK-007', 'name': 'Tuna Crispy',
        'description': 'Roll relleno de queso crema con pescado dulce deshidratado y palta',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/dQWv63MGBGJLvPjHu-300-x.webp',
    },
    {
        'sku': 'MAK-008', 'name': 'Ceviche Maki',
        'description': 'Roll relleno de pescado marinado en jugo de ceviche y langostino empanizado',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/kbtnawrmFMJEHLdM2-300-x.webp',
    },
    {
        'sku': 'MAK-009', 'name': 'Tartar Maki',
        'description': 'Roll empanizado y frito con langostinos y palta, coronado con tartar de trucha',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/9cr466rvmcbsybQQy-300-x.webp',
    },
    {
        'sku': 'MAK-010', 'name': 'Doragon Maki',
        'description': 'Roll cubierto con quinua tostada, topping de ebi furai con salsa acevichada',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/tvLFm9twaShTzvaTp-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'MAK-011', 'name': 'Lomo Saltado Maki',
        'description': 'Roll relleno de bastones de carne en tempura y papas al hilo',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Y8qrC3SWdfGK3WBhj-300-x.webp',
    },
    {
        'sku': 'MAK-012', 'name': 'Yakuza Maki',
        'description': 'Roll relleno de langostino empanizado y queso crema, cubierto de palta y ajonjolí',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Bum5uJHb7usPFYCoz-300-x.webp',
    },

    # ── POKE BOWLS ─────────────────────────────────────────────────────────
    {
        'sku': 'POK-001', 'name': 'Poke de Trucha',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y trucha fresca',
        'unit_price': '27.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Ydrv4AgzHxpmJkJ4n-300-x.webp',
        'is_featured': True,
    },
    {
        'sku': 'POK-002', 'name': 'Poke Salmón Fresco',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y salmón fresco',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Z7NvgrHgp7gJNr9Gv-300-x.webp',
    },
    {
        'sku': 'POK-003', 'name': 'Poke Ebi Furai',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y langostinos empanizados',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/XMHRtBkDsPAPDBoRb-300-x.webp',
    },
    {
        'sku': 'POK-004', 'name': 'Poke Tartar de Trucha',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y tartar de trucha',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/rdAaDdXgZ5guJXpWY-300-x.webp',
    },

    # ── POKE BOWLS adicionales ─────────────────────────────────────────────
    {
        'sku': 'POK-005', 'name': 'Poke Atún Fresco',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y atún fresco',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/u6zbbYZ4AQ6Qo5cSR-300-x.webp',
    },
    {
        'sku': 'POK-006', 'name': 'Poke Langostino Cocido',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y langostinos blanqueados',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/KZKDGWGfzm4StG7vg-300-x.webp',
    },
    {
        'sku': 'POK-007', 'name': 'Poke Pulpa Mix',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y crema de cangrejo',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/8snqM7gF8PoDxkQfE-300-x.webp',
    },
    {
        'sku': 'POK-008', 'name': 'Poke Sakana Furai',
        'description': 'Base de arroz sushi, salsa de ostión, col morada, zanahoria, pepino, palta y bastones de pescado frito',
        'unit_price': '29.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/v8dmAaWEzLeNjm3Mp-300-x.webp',
    },

    # ── ENTRADAS FRÍAS ─────────────────────────────────────────────────────
    {
        'sku': 'GUN-001', 'name': 'Gunkan Sushi de Kani',
        'description': 'Arroz envuelto en nori, relleno de pulpa de cangrejo y salsa especial',
        'unit_price': '15.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/FDeXRyReZnXLf4GDE-300-x.webp',
    },
    {
        'sku': 'GUN-002', 'name': 'Gunkan Sushi de Langostinos',
        'description': 'Arroz envuelto en nori, relleno de tartar de langostinos, palta y salsa especial',
        'unit_price': '14.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/eEekaqAyZJuf2WnED-300-x.webp',
    },
    {
        'sku': 'GUN-003', 'name': 'Gunkan Sushi de Trucha',
        'description': 'Arroz envuelto en nori, relleno de trucha asalmonada, palta y salsa especial',
        'unit_price': '14.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/3z7g7E5Njy8kqJDA3-300-x.webp',
    },
    {
        'sku': 'ENT-004', 'name': 'Nigiri de Langostino',
        'description': 'Bolita de arroz de sushi y corte fino de langostino cocido',
        'unit_price': '7.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/wyhsyphRGJWBB6qfR-300-x.webp',
    },
    {
        'sku': 'ENT-005', 'name': 'Nigiri de Salmón',
        'description': 'Bolita de arroz de sushi y corte fino de salmón',
        'unit_price': '9.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Pjxm6JmLnar5Mambk-300-x.webp',
    },
    {
        'sku': 'ENT-006', 'name': 'Nigiri de Trucha',
        'description': 'Bolita de arroz de sushi y corte fino de trucha asalmonada',
        'unit_price': '7.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/hC2FF253RSqhqagXf-300-x.webp',
    },
    {
        'sku': 'ENT-007', 'name': 'Sashimi de Langostino',
        'description': '4 cortes de langostino fresco con salsa shoyu, gari y wasabi',
        'unit_price': '16.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/3t3PBvAArhzDpXSbm-300-x.webp',
    },
    {
        'sku': 'ENT-008', 'name': 'Sashimi de Salmón',
        'description': '4 cortes de salmón con salsa shoyu, gari y wasabi',
        'unit_price': '20.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/zQCdD5uucfSJqA9LJ-300-x.webp',
    },
    {
        'sku': 'ENT-009', 'name': 'Sashimi de Trucha',
        'description': '4 cortes de trucha asalmonada con salsa shoyu, gari y wasabi',
        'unit_price': '15.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/xwLmy5avoNrdCndrN-300-x.webp',
    },

    # ── ENTRADAS CALIENTES ─────────────────────────────────────────────────
    {
        'sku': 'CAL-001', 'name': 'Ebi Furai',
        'description': 'Langostinos empanizados al panko, crujientes y dorados, acompañados de salsa especial',
        'unit_price': '18.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/ptRvKkswp3tH3wJ2Z-300-x.webp',
    },
    {
        'sku': 'CAL-002', 'name': 'Gyozas de Pescado',
        'description': 'Empanaditas rellenas de pescado fresco y verduras, servidas con salsa oriental',
        'unit_price': '14.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/x79Gyr9BZacaWpqr7-300-x.webp',
    },

    # ── TEMAKIS ────────────────────────────────────────────────────────────
    {
        'sku': 'TEM-001', 'name': 'Temaki Acevichado',
        'description': 'Cono relleno de ebi furai crujiente, palta y láminas de pescado',
        'unit_price': '16.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/xnMvpsnGJuBKMuQCE-300-x.webp',
    },
    {
        'sku': 'TEM-002', 'name': 'Temaki California',
        'description': 'Cono relleno de queso crema, palta y langostino blanqueado',
        'unit_price': '16.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/rrgmg6W2Z33scAEoM-300-x.webp',
    },

    # ── MESHI ──────────────────────────────────────────────────────────────
    {
        'sku': 'MES-001', 'name': 'Yakimeshi Mixto',
        'description': 'Arroz frito con verduras, pecanas, pollo, langostino y cerdo',
        'unit_price': '20.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/S4ngmpfhLHcmpRNDE-300-x.webp',
    },
    {
        'sku': 'MES-002', 'name': 'Nekimeshi de Pollo',
        'description': 'Arroz dulce de sushi salteado con verduras, pecanas y pollo',
        'unit_price': '18.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/uQnRCFm9cx3rv7SYN-300-x.webp',
    },

    # ── SOPAS ──────────────────────────────────────────────────────────────
    {
        'sku': 'SOP-001', 'name': 'Chicken Ramen',
        'description': 'Caldo umami, fideo ramen, pollo, huevo ajitsuke, cebollines y ajonjolí',
        'unit_price': '20.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/DmrFdykrKLkLrAnuw-300-x.webp',
    },
    {
        'sku': 'SOP-002', 'name': 'Ebi Ramen',
        'description': 'Caldo de langostinos con miso y ostión, fideos firmes, ebi furai crocante',
        'unit_price': '20.00', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/Gofw75d9q7BgB87JD-300-x.webp',
    },

    # ── SÁNDWICH SUSHI ─────────────────────────────────────────────────────
    {
        'sku': 'SAN-001', 'name': 'Sándwich Sushi Acevichado',
        'description': 'Sándwich frito relleno de tartar de pescado y langostinos en salsa acevichada',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/MaQmKdgQApLa4vXSG-300-x.webp',
    },
    {
        'sku': 'SAN-002', 'name': 'Sándwich Sushi Tradicional',
        'description': 'Sándwich relleno con queso crema, trucha, palta, gari y col morada',
        'unit_price': '25.90', 'image_url': 'https://tofuu.getjusto.com/orioneat-local/resized2/TkkBRnzAc3q5EHahG-300-x.webp',
    },
]


class Command(BaseCommand):
    help = 'Carga productos del menú en la base de datos'

    def handle(self, *args, **kwargs):
        # limpia SKUs obsoletos del primer seed
        deleted, _ = Product.objects.filter(sku__in=['ENT-001', 'ENT-002', 'ENT-003']).delete()
        if deleted:
            self.stdout.write(f'  Eliminados {deleted} productos con SKUs obsoletos')

        created = 0
        skipped = 0
        for data in PRODUCTS:
            obj, was_created = Product.objects.get_or_create(
                sku=data['sku'],
                defaults={
                    'name': data['name'],
                    'description': data.get('description', ''),
                    'unit_price': data['unit_price'],
                    'image_url': data.get('image_url'),
                    'stock': 50,
                    'is_featured': data.get('is_featured', False),
                    'ingredients': [],
                },
            )
            if was_created:
                created += 1
                self.stdout.write(f'  + {obj.name}')
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nListo: {created} creados, {skipped} ya existían.'
        ))
