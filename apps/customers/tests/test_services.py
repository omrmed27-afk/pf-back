from django.test import TestCase
from apps.customers.models import Customer
from apps.customers import services

MOCK_CUSTOMER = {
    "name": "Cliente Sur",
    "email": "sur@cliente.com",
    "customer_type": "individual",
}


class CustomerServicesTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(**MOCK_CUSTOMER)

    def test_get_all_customers_returns_queryset(self):
        result = services.get_all_customers()
        self.assertIn(self.customer, result)

    def test_get_all_customers_ordered_by_name(self):
        Customer.objects.create(name="AAA Primero", email="aaa@test.com")
        Customer.objects.create(name="ZZZ Ultimo", email="zzz@test.com")
        result = list(services.get_all_customers())
        names = [c.name for c in result]
        self.assertEqual(names, sorted(names))

    def test_get_customer_by_id_returns_correct_instance(self):
        result = services.get_customer_by_id(self.customer.pk)
        self.assertEqual(result, self.customer)

    def test_get_customer_by_id_raises_on_missing(self):
        with self.assertRaises(Customer.DoesNotExist):
            services.get_customer_by_id(99999)

    def test_create_customer(self):
        data = {"name": "Nuevo Cliente", "email": "nuevo@cliente.com"}
        customer = services.create_customer(data)
        self.assertEqual(customer.name, "Nuevo Cliente")
        self.assertTrue(Customer.objects.filter(pk=customer.pk).exists())

    def test_update_customer(self):
        updated = services.update_customer(self.customer, {"name": "Nombre Actualizado"})
        self.assertEqual(updated.name, "Nombre Actualizado")
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Nombre Actualizado")

    def test_delete_customer(self):
        pk = self.customer.pk
        services.delete_customer(self.customer)
        self.assertFalse(Customer.objects.filter(pk=pk).exists())
