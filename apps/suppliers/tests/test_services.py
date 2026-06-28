from django.test import TestCase
from apps.suppliers.models import Supplier
from apps.suppliers import services

MOCK_SUPPLIER = {
    "name": "Proveedor Sur",
    "email": "sur@proveedor.com",
    "phone": "1234567890",
    "address": "Ruta Sur 88",
    "contact_name": "Carlos Ruiz",
}


class SupplierServicesTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(**MOCK_SUPPLIER)

    def test_get_all_suppliers_returns_queryset(self):
        result = services.get_all_suppliers()
        self.assertIn(self.supplier, result)

    def test_get_all_suppliers_ordered_by_name(self):
        Supplier.objects.create(name="AAA Primero")
        Supplier.objects.create(name="ZZZ Ultimo")
        result = list(services.get_all_suppliers())
        names = [s.name for s in result]
        self.assertEqual(names, sorted(names))

    def test_get_supplier_by_id_returns_correct_instance(self):
        result = services.get_supplier_by_id(self.supplier.pk)
        self.assertEqual(result, self.supplier)

    def test_get_supplier_by_id_raises_on_missing(self):
        with self.assertRaises(Supplier.DoesNotExist):
            services.get_supplier_by_id(99999)

    def test_create_supplier(self):
        data = {"name": "Nuevo Proveedor", "email": "nuevo@test.com"}
        supplier = services.create_supplier(data)
        self.assertEqual(supplier.name, "Nuevo Proveedor")
        self.assertTrue(Supplier.objects.filter(pk=supplier.pk).exists())

    def test_update_supplier(self):
        updated = services.update_supplier(self.supplier, {"name": "Nombre Actualizado"})
        self.assertEqual(updated.name, "Nombre Actualizado")
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, "Nombre Actualizado")

    def test_delete_supplier(self):
        pk = self.supplier.pk
        services.delete_supplier(self.supplier)
        self.assertFalse(Supplier.objects.filter(pk=pk).exists())
